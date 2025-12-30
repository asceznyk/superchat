from typing import List, Union

from google import genai

from app.models.states import ChatRequest, AIChunkResponse, AIResponse
from app.services.cache import redis_client

from app.core.config import settings
from app.core.utils import convert_to_gemini_msgs

client = genai.Client(
  api_key = settings.GEMINI_API_KEY
)

async def get_chat_response(
  thread_id:str,
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
  full_text, text = "", ""
  for chunk in stream:
    text = chunk.text
    print(f"text from google -> {text}")
    if not text: continue
    data = AIChunkResponse(
      role = "assistant",
      msg_body = text
    )
    full_text += text
    yield f"{data.model_dump_json()}\n\n"
  ai_resp = AIResponse(
    role = "assistant",
    msg_body = full_text
  )
  await redis_client.add_chat_message(thread_id, ai_resp)






