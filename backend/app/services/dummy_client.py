from typing import List

import asyncio
import random

from app.models.states import AIChunkResponse, AIResponse
from app.core.utils import md_text_samples
from app.services.cache import redis_client

async def get_chat_response(thread_id:str, chat_history:List[str]):
  full_text = ""
  for text in md_text_samples[random.randint(0, len(md_text_samples)-1)]:
    data = AIChunkResponse(
      role = "assistant",
      msg_body = text,
    )
    full_text += text
    await asyncio.sleep(0.02)
    yield f"{data.model_dump_json()}\n\n"
  ai_resp = AIResponse(
    role = "assistant",
    msg_body = full_text,
  )
  await redis_client.add_chat_message(thread_id, ai_resp)



