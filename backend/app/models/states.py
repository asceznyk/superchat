from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
  role:str
  msg_body:str

class ChatIdResponse(BaseModel):
  chat_id:str

class AIChunkResponse(BaseModel):
  role:str
  msg_body:str

class AIResponse(BaseModel):
  role:str
  msg_body:Optional[str]

class AILimitResponse(BaseModel):
  msg_body:str
  msg_type:str


