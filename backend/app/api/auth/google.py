import secrets
import httpx

from urllib.parse import urlencode

from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from google.oauth2 import id_token
from google.auth.transport import requests

from app.core.config import settings
from app.db.connection import get_db
from app.db.user import upsert_user
from app.services.auth import (
  issue_jwt_pair, secure_cookie, get_current_guest, promote_guest_thread
)
from app.services.cache import redis_client

router = APIRouter()

def verify_google_id_token(token:str) -> dict:
  try:
    idinfo = id_token.verify_oauth2_token(
      token,
      requests.Request(),
      audience = settings.GOOGLE_OAUTH_CLIENT_ID,
    )
    return idinfo
  except ValueError:
    return {}

def validate_chat_path(path:str) -> str:
  if path == "":
    return path
  if not path.startswith("/chat"):
    raise HTTPException(400, detail="invalid path")
  if "://" in path or path.startswith("//"):
    raise HTTPException(400, detail="invalid path")
  return path

@router.get("/")
async def get_auth_uri(cpath:str) -> str:
  state = secrets.token_urlsafe(32)
  params = {
    "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
    "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI,
    "response_type": "code",
    "scope": "openid profile email",
    "access_type": "offline",
    "state": state
  }
  auth_uri = f"{settings.GOOGLE_OAUTH_AUTH_URI}?{urlencode(params)}"
  await redis_client.add_key_value(
    f"{settings.CACHE_PREFIX_OAUTH_STATE}:{state}", validate_chat_path(cpath),
    ttl = settings.CACHE_OAUTH_STATE_TTL_SECS
  )
  return auth_uri

@router.get("/callback")
async def set_session_cookies(
  state:str, code:str, req:Request,
  guest=Depends(get_current_guest), conn=Depends(get_db)
):
  chat_path = await redis_client.get_key_value(f"{settings.CACHE_PREFIX_OAUTH_STATE}:{state}")
  if chat_path is None or not len(chat_path):
    raise HTTPException(
      status_code=401, detail="state hasn't been issued"
    )
  await redis_client.delete_key_value(f"{settings.CACHE_PREFIX_OAUTH_STATE}:{state}")
  resp = None
  async with httpx.AsyncClient() as http_client:
    resp = await http_client.post(
      settings.GOOGLE_OAUTH_TOKEN_URI,
      data = {
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI
      }
    )
    if not resp or resp.status_code != 200:
      raise HTTPException(
        status_code=400, detail="didn't recive auth response"
      )
    resp = resp.json()
  info = verify_google_id_token(resp['id_token'])
  if not info:
    raise HTTPException(
      status_code=400, detail="id_token is not verifed!"
    )
  user_id, actor_id = await upsert_user(
    conn=conn,
    email=info['email'],
    name=info['name'],
    auth_type='oauth',
    auth_provider='google'
  )
  payload = {
    "sub": str(user_id),
    "aid": str(actor_id),
    "email": info["email"],
    "name": info.get("name", ""),
  }
  access_token, refresh_token = await issue_jwt_pair(payload)
  resp = await promote_guest_thread(
    conn, str(actor_id), guest.get('gid'),
    chat_path.split('/')[-1]
  )
  if req.cookies.get('guest_id'):
    resp.delete_cookie('guest_id')
  resp.set_cookie(**secure_cookie(
    "session_id",
    access_token,
    max_age=(settings.JWT_ACCESS_TTL_MINS*60)
  ))
  resp.set_cookie(**secure_cookie(
    "session_refresh",
    refresh_token,
    max_age=(settings.JWT_REFRESH_TTL_MINS*60)
  ))
  return resp



