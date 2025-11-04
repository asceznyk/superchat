import os
import uuid
import uvicorn
import json

from typing import Optional, List, Union
from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
  AIMessage,
  BaseMessage,
  HumanMessage,
  SystemMessage
)

from config import Settings

class UserState(BaseModel):
  user_id:str
  msg_type:str
  msg_body:Optional[str]
  chat_id:Optional[str]
  testing:Optional[bool]

class AIState(BaseModel):
  chat_id:str
  msg_body:str

settings = Settings()

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

system_template = f"""
You are a medical professional, and you are chatting with patient.
 - Conduct a medical diagnosis by asking symptomatic yes/no questions.
 - Ask one question at a time. DO NOT ask multiple questions.
 - Ask clarifying questions step-by-step (about 10-15 questions max).
 - Keep the language simple and clear.
 - Generate a report of top 3 possible medical diseases.

The patient has stated their symptom below:
"""

gen_llm = ChatOpenAI(
  model="gpt-4o",
  temperature=0,
  max_tokens=None,
  timeout=None,
  max_retries=2
)

users_chat_history = {}

origins = ["http://localhost:3000"]

app = FastAPI(root_path="/api")

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def get_conversation(
  user_chat_key:str
) -> List[Union[SystemMessage,HumanMessage,AIMessage]]:
  if users_chat_history.get(user_chat_key) is None:
    users_chat_history[user_chat_key] = []
    return users_chat_history[user_chat_key]
  return users_chat_history[user_chat_key]

@app.post("/triage", response_model=AIState)
async def get_symptpomatic_question(user_state:UserState) -> JSONResponse:
  ai_state = {}
  chat_id = user_state.chat_id
  if user_state.msg_type == "start":
    chat_id = str(uuid.uuid4())
  user_chat_key = f"{user_state.user_id}--{chat_id}"
  conversation = get_conversation(user_chat_key)
  ai_state["chat_id"] = chat_id
  if len(conversation) >= settings.MAX_CHAT_MSGS:
    ai_state["msg_body"] = {"content": "Max limit!, please start a new chat."}
    return JSONResponse(content=jsonable_encoder(ai_state))
  if user_state.msg_type == "ongoing":
    conversation.append(HumanMessage(user_state.msg_body))
  elif user_state.msg_type == "start":
    conversation.append(
      SystemMessage(system_template + user_state.msg_body)
    )
  else:
    conversation.pop()
    conversation.pop()
  if user_state.msg_type == "rewind":
    ai_state["msg_body"] = {"content": conversation[-1].content}
  else:
    if user_state.testing: ai_state["msg_body"] = {"content": "Test OK!"}
    else:
      ai_state["msg_body"] = json.loads(
        gen_llm.invoke(conversation).json()
      )
    conversation.append(AIMessage(ai_state["msg_body"]["content"]))
  users_chat_history[user_chat_key] = conversation
  return JSONResponse(content=jsonable_encoder(ai_state))

@app.get("/")
async def root():
  return {"message":"Hello world!"}


