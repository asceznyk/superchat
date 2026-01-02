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
from app.services.auth import issue_jwt_pair, secure_cookie
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

@router.get("/")
async def get_auth_uri() -> str:
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
  await redis_client.add_key_value(state, 1)
  return auth_uri

@router.get("/callback")
async def set_session_cookies(req:Request, state:str, code:str, conn=Depends(get_db)):
  issued = await redis_client.get_key_value(state)
  if not issued:
    raise HTTPException(
      status_code=401, detail="state hasn't been issued"
    )
  await redis_client.delete_key_value(state)
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
  jwt_payload = {
    "sub": str(user_id),
    "actor": str(actor_id),
    "email": info["email"],
    "name": info.get("name", ""),
  }
  access_token, refresh_token = await issue_jwt_pair(jwt_payload)
  resp = RedirectResponse(url="http://localhost/") # change hardcoded URL
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
  if req.cookies.get('guest_id'):
    resp.delete_cookie('guest_id')
  return resp



