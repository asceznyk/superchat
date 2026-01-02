from typing import Callable, List

import json
import asyncio

from app.models.states import AIResponse

from app.services.cache import redis_client
from app.db.message import insert_message

async def stream_and_persist(
  chat_stream:Callable,
  history:List[str],
  thread_key:str,
  actor_id:str,
  conn:object|None=None
):
  try:
    full_text = ""
    async for chunk in chat_stream(history):
      yield chunk
      resp = json.loads(chunk)
      full_text += resp['msg_content']
  except asyncio.CancelledError:
    print("WTF?")
    raise
  except Exception as e:
    print("error:", e)
    raise
  finally:
    ai_resp = AIResponse(
      role = "assistant",
      msg_content = full_text
    )
    await redis_client.add_chat_message(thread_key, ai_resp)
    if conn is not None:
      await insert_message(
        conn,
        actor_id,
        thread_key.split(":")[-1],
        'text',
        full_text
      )




