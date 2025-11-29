import uuid

from typing import Optional, Dict, Union

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import Settings
from app.core.utils import get_limit_response
from app.models.states import ChatRequest
from app.services.dummy_client import get_chat_response
from app.services.redis_client import add_message, get_history

settings = Settings()

router = APIRouter()

def get_user_from_token(auth:Optional[str]=Header(None)) -> Dict[str,str]:
  if not auth:
    return {
      "authenticated": False
    }

@router.post("/", response_model=None)
async def chat(
  chat_req:ChatRequest, user=Depends(get_user_from_token)
) -> StreamingResponse:
  if not chat_req.chat_id:
    chat_req.chat_id = str(uuid.uuid4())
  chat_id = chat_req.chat_id
  is_auth = user["authenticated"]
  if not is_auth:
    await add_message(chat_id, chat_req)
    chat_history = await get_history(chat_id)
    if len(chat_history) >= settings.MAX_CHAT_MSGS:
      return StreamingResponse(
        get_limit_response(chat_id, is_auth),
        media_type="text/event-stream"
      )
  return StreamingResponse(
    get_chat_response(chat_id, is_auth, chat_history),
    media_type="text/event-stream"
  )


