import uuid

from typing import Tuple, Literal

from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Cookie

from app.core.config import Settings
from app.services.redis_client import add_key_value

settings = Settings()

def create_token(data:dict, *, token_type:Literal['access','refresh']) -> str:
  to_encode = data.copy()
  if token_type == 'access':
    expire = datetime.now(timezone.utc) + timedelta(
      minutes = settings.JWT_ACCESS_TTL
    )
    secret = settings.JWT_ACCESS_SECRET
  else:
    expire = datetime.now(timezone.utc) + timedelta(
      minutes = settings.JWT_REFRESH_TTL
    )
    secret = settings.JWT_REFRESH_SECRET
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)

async def issue_jwt_pair(info:dict) -> Tuple[str,str]:
  token_defaults = {
    'email': info['email'],
    'email_verified': info['email_verified'],
    'name': info['name'],
    'aud': info['aud']
  }
  access_token = create_token({
    **token_defaults,
    'jti':str(uuid.uuid4())
  }, token_type='access')
  refresh_jti = str(uuid.uuid4())
  refresh_token = create_token({
    **token_defaults,
    'jti': refresh_jti
  }, token_type='refresh')
  await add_key_value(refresh_jti, 1)
  return access_token, refresh_token

def verify_token(token:str, *, token_type:Literal['access','refresh']) -> dict:
  payload = {}
  try:
    if token_type == 'access':
      secret = settings.JWT_ACCESS_SECRET
    else:
      secret = settings.JWT_REFRESH_SECRET
    payload = jwt.decode(
      token, secret,
      algorithms=[settings.JWT_ALGORITHM],
      audience=settings.GOOGLE_OAUTH_CLIENT_ID
    )
  except ExpiredSignatureError:
    pass
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid token")
  return payload

def get_current_user(session_id:str|None=Cookie(default=None)):
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



