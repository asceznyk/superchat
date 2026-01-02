from typing import List, Union

from google import genai

from app.models.states import UserMessageRequest, AIChunkResponse, AIResponse
from app.services.cache import redis_client

from app.core.config import settings
from app.core.utils import convert_to_gemini_msgs

client = genai.Client(api_key = settings.GEMINI_API_KEY)

async def get_chat_response(
  history:List[str],
  model:str="gemini-2.5-flash"
):
  messages = convert_to_gemini_msgs(history)
  stream = client.models.generate_content_stream(
    model = model,
    config = genai.types.GenerateContentConfig(
      system_instruction=settings.GEMINI_SYSTEM_PROMPT
    ),
    contents = messages,
  )
  text = ""
  for chunk in stream:
    text = chunk.text
    if not text: continue
    data = AIChunkResponse(
      role = "assistant",
      msg_content = text
    )
    yield f"{data.model_dump_json()}\n\n"







