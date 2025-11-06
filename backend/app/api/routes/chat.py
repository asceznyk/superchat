import uuid

from typing import Optional, Dict

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from app.models import states
#from app.services.openai_client import get_chat_response

router = APIRouter()

def get_user_from_token(auth:Optional[str]=Header(None)) -> Dict[str,str]:
  if not auth:
    return {
      "mock_id": str(uuid.uuid4()),
      "chat_id": str(uuid.uuid4()),
      "authenticated": False
    }

@router.post("/", response_model=states.AIResponse)
async def chat(chat_req:states.ChatRequest, user=Depends(get_user_from_token)):
  ai_resp = {}
  #if user["authenticated"]: ##TODO
  msg = chat_req.msg_text
  if not chat_req.mock_id:
    ai_resp["mock_id"] = user["mock_id"]
    ai_resp["chat_id"] = user["chat_id"]
  else:
    ai_resp["mock_id"] = chat_req.mock_id
    ai_resp["chat_id"] = chat_req.chat_id
  ai_resp["msg_body"] = "Hello from the dark side :D"
  ai_resp["authenticated"] = user["authenticated"]
  return ai_resp


