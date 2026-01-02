from typing import List

import asyncio
import random

from app.models.states import AIChunkResponse, AIResponse
from app.core.utils import md_text_samples
from app.services.cache import redis_client

async def get_chat_response(history:List[str]):
  for text in md_text_samples[random.randint(0, len(md_text_samples)-1)]:
    data = AIChunkResponse(
      role = "assistant",
      msg_content = text,
    )
    await asyncio.sleep(0.02)
    yield f"{data.model_dump_json()}\n\n"



