import uuid
import json

from typing import Optional, Dict, Union

from fastapi import Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import settings
from app.core.utils import get_limit_response
from app.models.states import ChatRequest, ChatIdResponse
from app.services.cache import redis_client
from app.services.auth import get_current_user

import app.services.google_client as google_client

router = APIRouter()

@router.post("/", response_model=ChatIdResponse)
async def assign_chat_id(
  chat_req:ChatRequest,
  response:JSONResponse,
  session_id:str|None=Cookie(default=None)
) -> ChatIdResponse:
  resp = ChatIdResponse(chat_id = str(uuid.uuid4()))
  if session_id:
    return resp
  response.set_cookie(
    key="session_id",
    value=str(uuid.uuid4()),
    httponly=True,
    samesite="lax",
    max_age=settings.MAX_AGE_ANON_ID,
  )
  return resp

@router.get("/{chat_id}", response_model=None)
async def converstaion_thread(
  chat_id:str,
  user:Dict=Depends(get_current_user),
  session_id:str|None=Cookie(default=None)
) -> JSONResponse:
  is_auth = user["authenticated"]
  thread_id = f"thread:{"auth" if is_auth else "guest"}:{session_id}:{chat_id}"
  history = await redis_client.get_history(thread_id)
  return JSONResponse(content = jsonable_encoder(
    [json.loads(s) for s in history]
  ))

@router.post("/{chat_id}", response_model=None)
async def ai_response(
  chat_id:str,
  chat_req:ChatRequest,
  user:Dict=Depends(get_current_user),
  session_id:str|None=Cookie(default=None)
) -> StreamingResponse:
  is_auth = user["authenticated"]
  logged = "auth" if is_auth else "guest"
  thread_id = f"thread:{logged}:{session_id}:{chat_id}"
  if not is_auth:
    await redis_client.add_chat_message(thread_id, chat_req)
    history = await redis_client.get_history(thread_id)
  return StreamingResponse(
    google_client.get_chat_response(thread_id, history),
    media_type="text/event-stream"
  )


