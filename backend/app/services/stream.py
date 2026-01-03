from typing import Callable, List, Dict

import json
import asyncio

from app.core.config import settings
from app.services.cache import redis_client
from app.models.states import AIResponse

class MessageStreamer():

  def __init__(
    self,
    response_stream:Callable,
    chat_history:List[str],
    payload:Dict[str,str]
  ):
    self.response_stream = response_stream
    self.chat_history = chat_history
    self.payload = payload
    self.full_text = ""

  async def stream_and_persist(self, is_auth:bool=False):
    try:
      self.full_text = ""
      async for chunk in self.response_stream(self.chat_history):
        yield chunk
        resp = json.loads(chunk)
        self.full_text += resp['msg_content']
    except asyncio.CancelledError:
      raise
    except Exception as e:
      raise
    finally:
      self.payload['ai_resp'] = AIResponse(
        role = 'assistant',
        msg_content = self.full_text
      ).model_dump_json()
      self.payload['is_auth'] = is_auth
      await redis_client.q_put(
        settings.CACHE_AI_RESP_KEY, json.dumps(self.payload)
      )




