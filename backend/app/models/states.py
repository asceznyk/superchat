from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
  role:Optional[str]
  chat_id:Optional[str]
  msg_body:str

class AIChunkResponse(BaseModel):
  role:str
  chat_id:str
  msg_body:str
  authenticated:bool

class AIResponse(BaseModel):
  role:str
  chat_id:str
  msg_body:Optional[str]
  authenticated:bool

class AILimitResponse(BaseModel):
  msg_body:str
  msg_type:str


