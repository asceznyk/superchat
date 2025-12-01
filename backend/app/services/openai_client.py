from typing import List, Union

import json
import asyncio

from openai import OpenAI

from app.models.states import ChatRequest, AIChunkResponse, AIResponse
from app.services.redis_client import add_message

from app.core.config import Settings
from app.core.utils import convert_to_openai_msgs

settings = Settings()

openai_client = OpenAI(
  api_key = settings.OPENAI_API_KEY
)

async def get_chat_response(chat_id:str, is_auth:bool, chat_history:List[str]):
  messages = convert_to_openai_msgs(chat_history)
  stream = openai_client.responses.create(
    model = "gpt-4o",
    input = messages,
    stream = True,
    temperature = 0
  )
  full_text, text = "", ""
  for event in stream:
    if event.type == "response.output_text.delta":
      text = event.delta
    data = AIChunkResponse(
      role = "assistant",
      chat_id = chat_id,
      msg_body = text,
      authenticated = is_auth
    )
    full_text += text
    yield f"{data.model_dump_json()}\n\n"
  ai_resp = AIResponse(
    role = "assistant",
    chat_id = chat_id,
    msg_body = full_text,
    authenticated = is_auth
  )
  await add_message(chat_id, ai_resp)





