import pytest
import copy
import uuid
import rich
import json

from typing import Optional, Dict
from fastapi.testclient import TestClient
from langchain_core.messages import (
  AIMessage,
  BaseMessage,
  HumanMessage,
  SystemMessage,
)

from main import app, users_chat_history, system_template

client = TestClient(app)

def make_user_state(
  user_id:str="us123",
  msg_type:str="start",
  msg_body:Optional[str]=None,
  chat_id:Optional[str]=None,
) -> Dict[str,Optional[str]]:
  return {
    "user_id":user_id,
    "msg_type":msg_type,
    "msg_body":msg_body,
    "chat_id":chat_id,
    "testing":True,
  }

def populate_chat_history(user_chat_key:str):
  users_chat_history.clear() ##clears everything!
  users_chat_history[user_chat_key] = [
    SystemMessage(system_template + "I have a headache"),
    AIMessage("How long have you had it for?"),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst.")
  ]
  return users_chat_history[user_chat_key]

def test_chat_start():
  payload = make_user_state(msg_type="start", msg_body="I have a stomach ache")
  response = client.post("/triage", json=payload)
  assert response.status_code == 200
  data = response.json()
  rich.print(json.dumps)
  assert "chat_id" in data and isinstance(data["chat_id"], str)
  assert "msg_body" in data and len(data["msg_body"]["content"]) > 0
  users_chat_history.clear()

def test_chat_ongoing():
  chat_id = str(uuid.uuid4())
  payload = make_user_state(
    msg_type="ongoing",
    msg_body="I'd say about a 6, 6.5",
    chat_id=chat_id
  )
  user_chat_key = payload["user_id"]+"--"+chat_id
  history = copy.deepcopy(populate_chat_history(user_chat_key))
  print(f"users_chat_history: before = {users_chat_history}")
  response = client.post("/triage", json=payload)
  assert response.status_code == 200
  conversation = users_chat_history[user_chat_key]
  rich.print(f"users_chat_history: after = {users_chat_history}")
  rich.print(f"conversation = {conversation}")
  rich.print(f"history = {history}")
  assert len(conversation) == len(history)+2
  assert isinstance(conversation[-1], AIMessage)
  users_chat_history.clear()

def test_chat_rewind():
  chat_id = str(uuid.uuid4())
  payload = make_user_state(
    msg_type="rewind",
    chat_id=chat_id
  )
  user_chat_key = payload["user_id"]+"--"+chat_id
  history = copy.deepcopy(populate_chat_history(user_chat_key))
  response = client.post("/triage", json=payload)
  conversation = users_chat_history[user_chat_key]
  rich.print(f"conversation = {conversation}")
  rich.print(f"history = {history}")
  assert response.status_code == 200
  assert len(conversation) == len(history)-2
  assert conversation[-1].content == "How long have you had it for?"
  users_chat_history.clear()

def test_max_limit():
  chat_id = str(uuid.uuid4())
  payload = make_user_state(
    msg_type="ongoing",
    msg_body="Can you do something else for me?",
    chat_id=chat_id
  )
  user_chat_key = payload["user_id"]+"--"+chat_id
  users_chat_history.clear()
  users_chat_history[user_chat_key] = [
    SystemMessage(system_template + "I have a headache"),
    AIMessage("How long have you had it for?"),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
    HumanMessage("For about 2 days now"),
    AIMessage("How bad is it on a scale of 1 to 10? 10 being worst."),
  ]
  response = client.post("/triage", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["msg_body"]["content"].startswith("Max limit!")
  users_chat_history.clear()

