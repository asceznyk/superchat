from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
  chat_id:Optional[str]
  msg_text:str

class AIResponse(BaseModel):
  chat_id:str
  msg_body:Optional[str]
  authenticated:bool

