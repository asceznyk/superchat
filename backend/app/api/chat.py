import uuid

from typing import Optional, Dict

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from app.models.states import ChatRequest, AIResponse
from app.services.openai_client import get_chat_response

router = APIRouter()

def get_user_from_token(auth:Optional[str]=Header(None)) -> Dict[str,str]:
  if not auth:
    return {
      "authenticated": False
    }

@router.post("/")
async def chat(chat_req:ChatRequest, user=Depends(get_user_from_token)):
  #if user["authenticated"]: ##TODO
  if not chat_req.chat_id:
    chat_req.chat_id = str(uuid.uuid4())
  return StreamingResponse(
    get_chat_response(chat_req, user["authenticated"]),
    media_type="text/event-stream"
  )


