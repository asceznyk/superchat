import uuid

from typing import Optional, Dict

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from app.models.states import ChatRequest, AIResponse
from app.services.openai_client import get_chat_response
from app.services.redis_client import add_message, get_history

router = APIRouter()

def get_user_from_token(auth:Optional[str]=Header(None)) -> Dict[str,str]:
  if not auth:
    return {
      "authenticated": False
    }

@router.post("/", response_model=AIResponse)
async def chat(chat_req:ChatRequest, user=Depends(get_user_from_token)):
  #if user["authenticated"]: ##TODO
  msg = chat_req.msg_text
  if not chat_req.chat_id:
    chat_id = str(uuid.uuid4())
  else:
    chat_id = chat_req.chat_id
  await add_message(chat_id, chat_req)
  chat_history = await get_history(chat_id)
  ai_text = get_chat_response(chat_history)
  ai_resp = AIResponse(
    chat_id = chat_id,
    msg_body = ai_text,
    authenticated = user["authenticated"]
  )
  await add_message(chat_id, ai_resp)
  return ai_resp


