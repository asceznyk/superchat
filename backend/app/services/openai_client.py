from typing import List, Union

from openai import OpenAI

from app.models.states import ChatRequest, AIChunkResponse, AIResponse
from app.services.redis_client import add_message

from app.core.config import Settings
from app.core.utils import convert_to_openai_msgs

settings = Settings()

client = OpenAI(
  api_key = settings.OPENAI_API_KEY
)

async def get_chat_response(thread_id:str, chat_history:List[str]):
  messages = convert_to_openai_msgs(chat_history)
  stream = client.responses.create(
    model = "gpt-4o-mini",
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
      msg_body = text,
    )
    full_text += text
    yield f"{data.model_dump_json()}\n\n"
  ai_resp = AIResponse(
    role = "assistant",
    msg_body = full_text,
  )
  await add_message(thread_id, ai_resp)





