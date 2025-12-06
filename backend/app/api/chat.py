import uuid
import json

from typing import Optional, Dict, Union

from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import Settings
from app.core.utils import get_limit_response

from app.models.states import ChatRequest, ChatIdResponse

from app.services.redis_client import add_message, get_history

#from app.services.dummy_client import get_chat_response
#from app.services.openai_client import get_chat_response
import app.services.google_client as google_client

settings = Settings()

router = APIRouter()

def get_user_from_token(auth:Optional[str]=Header(None)) -> Dict[str,str]:
  if not auth:
    return {
      "authenticated": False
    }

@router.post("/", response_model=ChatIdResponse)
async def assign_chat_id(chat_req:ChatRequest) -> ChatIdResponse:
  return ChatIdResponse(chat_id = str(uuid.uuid4()))

@router.get("/{chat_id}", response_model=None)
async def converstaion_thread(
  chat_id:str, user=Depends(get_user_from_token)
) -> JSONResponse:
  is_auth = user["authenticated"]
  thread_id = f"thread:{"auth" if is_auth else "guest"}:{chat_id}"
  history = await get_history(thread_id)
  return JSONResponse(content = jsonable_encoder(
    [json.loads(s) for s in history]
  ))

@router.post("/{chat_id}", response_model=None)
async def ai_response(
  chat_id:str,
  chat_req:ChatRequest,
  user=Depends(get_user_from_token)
) -> StreamingResponse:
  is_auth = user["authenticated"]
  logged = "auth" if is_auth else "guest"
  thread_id = f"thread:{logged}:{chat_id}"
  if not is_auth:
    await add_message(thread_id, chat_req)
    history = await get_history(thread_id)
    if len(history) >= settings.MAX_CHAT_MSGS:
      return StreamingResponse(
        get_limit_response(is_auth),
        media_type="text/event-stream"
      )
  return StreamingResponse(
    google_client.get_chat_response(thread_id, history),
    media_type="text/event-stream"
  )


