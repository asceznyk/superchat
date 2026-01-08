from typing import Optional
from pydantic import BaseModel

class UserProfile(BaseModel):
  name:str
  email:str

class MessageRequest(BaseModel):
  role:str
  msg_type:str
  msg_content:str
  ai_model_id:str

class ChatIdResponse(BaseModel):
  thread_id:str

class AIChunkResponse(BaseModel):
  role:str
  msg_content:str

class AIResponse(BaseModel):
  role:str
  msg_content:Optional[str]
  actor_id:str


