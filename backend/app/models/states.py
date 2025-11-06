from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
  mock_id:Optional[str]
  chat_id:Optional[str]
  msg_text:str

class AIResponse(BaseModel):
  mock_id:Optional[str]
  chat_id:str
  msg_body:Optional[str]
  authenticated:bool

