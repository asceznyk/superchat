import secrets
import httpx

from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from app.core.config import Settings
from app.services.redis_client import (
  set_state_key, get_state_key, delete_state_key
)

settings = Settings()

router = APIRouter()

@router.get("/")
async def get_auth_uri() -> str:
  state = secrets.token_urlsafe(32)
  params = {
    "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
    "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI,
    "response_type": "code",
    "scope": "openid profile",
    "access_type": "offline",
    "state": state
  }
  auth_uri = f"{settings.GOOGLE_OAUTH_AUTH_URI}?{urlencode(params)}"
  await set_state_key(state, 1)
  return auth_uri

@router.get("/callback")
async def get_access_token(
  state:str, code:str, scope:str, authuser:int, prompt:str
):
  issued = await get_state_key(state)
  if not issued:
    raise HTTPException(
      status_code=400, detail="state hasn't been issued"
    )
  await delete_state_key(state)
  async with httpx.AsyncClient() as client:
    resp = await client.post(
      settings.GOOGLE_OAUTH_TOKEN_URI,
      data = {
        "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_OAUTH_REDIRECT_URI
      }
    )
    if resp.status_code == 200:
      resp = resp.json()
    ## verify access_token with id_token

