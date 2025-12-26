import uuid

from typing import Dict

from fastapi import APIRouter, HTTPException, Cookie, Depends
from fastapi.responses import JSONResponse

from app.models.states import UserProfile
from app.core.config import Settings
from app.services.auth import create_token, verify_token, get_current_user

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

@router.get("/refresh")
def refresh_session_token(
  user:Dict=Depends(get_current_user),
  session_refresh:str=Cookie(default=None)
) -> JSONResponse:
  if not session_refresh:
    raise HTTPException(status_code=401, detail="Missing refresh token")
  info = verify_token(session_refresh)
  success = {"set": True}
  if user['authenticated']:
    return JSONResponse(content=success)
  del info['iat']
  info['jti'] = str(uuid.uuid4())
  access_token = create_token(info)
  resp = JSONResponse(content=success)
  resp.set_cookie(
    key="session_id",
    value=access_token,
    httponly=True,
    samesite="lax"
  )
  return resp


