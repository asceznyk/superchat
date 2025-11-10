from typing import List, Union

import json
import asyncio

from openai import OpenAI

from app.models.states import ChatRequest, AIChunkResponse, AIResponse
from app.services.redis_client import add_message, get_history

from app.core.config import Settings

settings = Settings()

openai_client = OpenAI(
  api_key = settings.OPENAI_API_KEY
)

async def get_chat_response(chat_req:ChatRequest, is_auth:bool):
  chat_id = chat_req.chat_id
  await add_message(chat_id, chat_req)
  chat_history = await get_history(chat_id)
  print(f"chat_history = {chat_history}")
  messages = []
  for msg_str in chat_history:
    msg_json = json.loads(msg_str)
    role =  "user" if msg_json["role"] != "assistant" else "assistant"
    messages.append({
      "role": role,
      "content": msg_json["msg_body"]
    })
  stream = openai_client.chat.completions.create(
    model = "gpt-4o",
    messages = messages,
    stream = True,
    temperature = 0
  )
  full_text = ""
  for chunk in stream:
    if not chunk.choices or not chunk.choices[0].delta.content:
      continue
    text = chunk.choices[0].delta.content
    print(f"text = {text}")
    data = AIChunkResponse(
      role = "assistant",
      chat_id = chat_id,
      msg_body = text,
      authenticated = is_auth
    )
    full_text += text
    yield f"data: {data.model_dump_json()}\n\n"
  data = AIChunkResponse(
    role = "assistant",
    chat_id = chat_id,
    msg_body = "[DONE]",
    authenticated = is_auth
  )
  yield f"data: {data.model_dump_json()}\n\n"
  ai_resp = AIResponse(
    role = "assistant",
    chat_id = chat_id,
    msg_body = full_text,
    authenticated = is_auth
  )
  await add_message(chat_id, ai_resp)





