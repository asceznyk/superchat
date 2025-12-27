import uuid

from typing import Dict

from fastapi import APIRouter, HTTPException, Cookie, Depends
from fastapi.responses import JSONResponse

from app.models.states import UserProfile
from app.core.config import Settings
from app.services.redis_client import does_key_exist, delete_key_value
from app.services.auth import (
  issue_jwt_pair, verify_token, get_current_user, secure_cookie
)

settings = Settings()

router = APIRouter()

@router.get("/me", response_model=UserProfile)
def user_profile_info(user:Dict=Depends(get_current_user)):
  if not user['authenticated']:
    raise HTTPException(status_code=400, detail="token is not verified")
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
  except:
    raise HTTPException(status_code=401, detail="Invalid refresh token")
  refresh_jti = info['jti']
  is_token_valid = await does_key_exist(refresh_jti)
  if not is_token_valid:
    raise HTTPException(status_code=401, detail="Refresh token revoked")
  success = {"set": True}
  await delete_key_value(refresh_jti)
  access_token, refresh_token = await issue_jwt_pair(info)
  resp = JSONResponse(content=success)
  resp.set_cookie(**secure_cookie(
    "session_id",
    access_token,
    max_age=(settings.JWT_ACCESS_TTL*60)
  ))
  resp.set_cookie(**secure_cookie(
    "session_refresh",
    refresh_token,
    max_age=(settings.JWT_REFRESH_TTL*60)
  ))
  return resp


