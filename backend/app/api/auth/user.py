import uuid

from typing import Dict

from jose import JWTError

from fastapi import APIRouter, HTTPException, Cookie, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.models.states import UserProfile
from app.core.config import settings
from app.services.cache import redis_client
from app.services.auth import (
  issue_jwt_pair, verify_token,
  get_current_user, get_current_guest, secure_cookie
)
from app.db.connection import get_db
from app.db.thread import create_thread_with_retry

router = APIRouter()

@router.get("/me", response_model=UserProfile)
def user_profile_info(
  req:Request, user:Dict=Depends(get_current_user)
) -> UserProfile:
  if not user['authenticated']:
    raise HTTPException(status_code=401, detail="token is not verified")
  return UserProfile(
    name = user['name'],
    email = user['email']
  )

@router.post("/refresh")
async def user_refresh_session(
  session_refresh:str=Cookie(default=None)
) -> JSONResponse:
  if not session_refresh:
    raise HTTPException(status_code=401, detail="Missing refresh token")
  try:
    info = verify_token(session_refresh, token_type='refresh')
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid refresh token")
  jti_key = f"{settings.CACHE_PREFIX_REFRESH_JTI}:{info['jti']}"
  is_token_valid = await redis_client.does_key_exist(jti_key)
  if not is_token_valid:
    raise HTTPException(status_code=401, detail="Refresh token revoked")
  await redis_client.delete_key_value(jti_key)
  access_token, refresh_token = await issue_jwt_pair(info)
  resp = JSONResponse(content={"set":True})
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

@router.post("/logout")
async def delete_session_cookies(req:Request) -> RedirectResponse:
  resp = RedirectResponse(
    url=settings.APP_FRONTEND_URL,
    status_code=303
  )
  if req.cookies.get('session_id'):
    resp.delete_cookie("session_id")
  if req.cookies.get('session_refresh'):
    resp.delete_cookie("session_refresh")
    info = verify_token(
      req.cookies.get('session_refresh'),
      token_type='refresh'
    )
    await redis_client.delete_key_value(
      f"{settings.CACHE_PREFIX_REFRESH_JTI}:{info['jti']}"
    )
  return resp


