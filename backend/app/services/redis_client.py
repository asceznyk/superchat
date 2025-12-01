from typing import Union

import redis.asyncio as redis

from app.core.config import Settings
from app.models.states import ChatRequest, AIResponse

settings = Settings()

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def add_message(key:str, message:Union[ChatRequest,AIResponse]):
  ttl = (
    settings.CHAT_GUEST_TTL
    if key.startswith("chat:guest:")
    else settings.CHAT_AUTH_TTL
  )
  async with redis_client.pipeline() as pipe:
    pipe.rpush(key, message.model_dump_json())
    pipe.expire(key, ttl)
    await pipe.execute()

async def get_history(key:str):
  json_list = await redis_client.lrange(key, 0, -1)
  return json_list

