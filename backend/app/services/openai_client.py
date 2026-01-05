from typing import List, Union

from openai import OpenAI

from app.models.states import MessageRequest, AIChunkResponse, AIResponse
from app.services.cache import redis_client

from app.core.config import settings
from app.core.utils import convert_to_openai_msgs

client = OpenAI(
  api_key = settings.OPENAI_API_KEY
)

async def get_chat_response(chat_history:List[str]):
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
      msg_content = text,
    )
    full_text += text
    yield f"{data.model_dump_json()}\n\n"
  ai_resp = AIResponse(
    role = "assistant",
    msg_content = full_text,
  )
  await redis_client.add_chat_message(ai_resp)





