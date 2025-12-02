from typing import List

import asyncio
import random

from app.models.states import AIChunkResponse, AIResponse
from app.core.utils import md_text_samples
from app.services.redis_client import add_message

async def get_chat_response(chat_id:str, is_auth:bool, chat_history:List[str]):
  full_text = ""
  for text in md_text_samples[0]: #md_text_samples[random.randint(0, len(md_text_samples)-1)]:
    data = AIChunkResponse(
      role = "assistant",
      chat_id = chat_id,
      msg_body = text,
      authenticated = is_auth
    )
    full_text += text
    await asyncio.sleep(0.02)
    yield f"{data.model_dump_json()}\n\n"
  ai_resp = AIResponse(
    role = "assistant",
    chat_id = chat_id,
    msg_body = full_text,
    authenticated = is_auth
  )
  await add_message(chat_id, ai_resp)



