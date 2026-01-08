from typing import Dict

import json
import uuid

from typing import Tuple, Literal

from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Cookie
from fastapi.responses import JSONResponse, RedirectResponse

from psycopg_pool import AsyncConnectionPool

from app.core.config import settings
from app.services.cache import redis_client
from app.db.thread import create_thread_with_retry
from app.db.message import insert_messages

def secure_cookie(
  key:str, value:str, max_age:int|None=None
) -> Dict[str,str]:
  return {
    'key': key,
    'value': value,
    'httponly': True,
    'samesite': "lax",
    'secure': (settings.APP_ENV != "development"),
    'path': "/",
    'max_age': max_age
  }

def create_token(
  data:dict, *, token_type:Literal['access','refresh','guest']
) -> str:
  to_encode = data.copy()
  expire = datetime.now(timezone.utc)
  if token_type == 'access':
    expire += timedelta(
      minutes = settings.JWT_ACCESS_TTL_MINS
    )
    secret = settings.JWT_ACCESS_SECRET
  elif token_type == 'refresh':
    expire += timedelta(
      minutes = settings.JWT_REFRESH_TTL_MINS
    )
    secret = settings.JWT_REFRESH_SECRET
  else:
    expire += timedelta(
      minutes = settings.JWT_GUEST_TTL_MINS
    )
    secret = settings.JWT_GUEST_SECRET
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)

async def issue_jwt_pair(token_claims:dict) -> Tuple[str,str]:
  access_token = create_token({
    **token_claims,
    'jti':str(uuid.uuid4())
  }, token_type='access')
  refresh_jti = str(uuid.uuid4())
  refresh_token = create_token({
    **token_claims,
    'jti': refresh_jti
  }, token_type='refresh')
  await redis_client.add_key_value(
    f"{settings.CACHE_PREFIX_REFRESH_JTI}:{refresh_jti}", 1
  )
  return access_token, refresh_token

def verify_token(
  token:str, *, token_type:Literal['access','refresh','guest']
) -> Dict[str,str]:
  payload = {}
  try:
    if token_type == 'access':
      secret = settings.JWT_ACCESS_SECRET
    elif token_type == 'refresh':
      secret = settings.JWT_REFRESH_SECRET
    else:
      secret = settings.JWT_GUEST_SECRET
    payload = jwt.decode(
      token, secret,
      algorithms = [settings.JWT_ALGORITHM],
      audience = (
        settings.GOOGLE_OAUTH_CLIENT_ID if token_type in ['access','refresh'] \
        else None
      )
    )
  except ExpiredSignatureError:
    pass
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid token")
  return payload

def get_current_user(session_id:str|None=Cookie(default=None)) -> Dict[str,str]:
  if not session_id:
    return {
      "authenticated": False
    }
  try:
    info = verify_token(session_id, token_type='access')
    info["authenticated"] = (True if info else False)
    return info
  except ValueError:
    raise HTTPException(status_code=401, detail="Invalid token")

def get_current_guest(guest_id:str|None=Cookie(default=None)) -> Dict[str,str]:
  if not guest_id:
    return {
      "verified": False
    }
  try:
    info = verify_token(guest_id, token_type='guest')
    info["verified"] = (True if info else False)
    return info
  except ValueError:
    raise HTTPException(status_code=401, detail="Invalid token")

async def promote_guest_thread(
  conn:AsyncConnectionPool,
  actor_id:str,
  guest_id:str,
  thread_id:str
) -> RedirectResponse:
  url = settings.APP_FRONTEND_URL
  resp = RedirectResponse(url=url)
  if not guest_id:
    return resp
  history = await redis_client.get_chat_history(
    f"{settings.CACHE_PREFIX_VIEW_THREAD}:guest:{guest_id}:{thread_id}"
  )
  if history is None or not len(history):
    return resp
  created_thread_id = await create_thread_with_retry(
    conn, actor_id, "Chat"
  )
  num_msgs = len(history)
  actor_ids, msg_types, msg_contents = [], [], []
  for msg in history:
    msg = json.loads(msg)
    actor_ids.append(actor_id if msg['role'] == "user" else msg['actor_id'])
    msg_types.append(msg.get('msg_type', 'text'))
    msg_contents.append(msg['msg_content'])
  await insert_messages(
    conn,
    actor_ids,
    [created_thread_id]*num_msgs,
    [None]*num_msgs,
    msg_types,
    msg_contents
  )
  url += f"/chat/{str(created_thread_id)}"
  return RedirectResponse(url=url)

