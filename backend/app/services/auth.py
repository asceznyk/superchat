from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Cookie

from app.core.config import Settings

settings = Settings()

def create_token(data:dict, expire_delta:int|None=None) -> str:
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(
    minutes = (expire_delta or settings.JWT_EXPIRE_MINS)
  )
  to_encode.update({"exp": expire})
  return jwt.encode(
    to_encode, settings.JWT_SERVER_SECRET, algorithm=settings.JWT_ALGORITHM
  )

def verify_token(token:str) -> dict:
  try:
    payload = jwt.decode(
      token,
      settings.JWT_SERVER_SECRET,
      algorithms=[settings.JWT_ALGORITHM],
    )
    return payload
  except JWTError:
    return {}

def get_current_user(session_id:str|None=Cookie(default=None)):
  if not session_id:
    return {
      "authenticated": False
    }
  try:
    info = verify_token(session_id)
    info["authenticated"] = True
    return info
  except ValueError:
    raise HTTPException(status_code=401, detail="Invalid token")



