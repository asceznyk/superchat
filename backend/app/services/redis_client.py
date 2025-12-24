from typing import Union, Optional

import redis.asyncio as redis

from app.core.config import Settings
from app.models.states import ChatRequest, AIResponse

settings = Settings()

client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def add_message(key:str, message:Union[ChatRequest,AIResponse]):
  ttl = (
    settings.CHAT_GUEST_TTL
    if key.startswith("thread:guest:")
    else settings.CHAT_AUTH_TTL
  )
  async with client.pipeline() as pipe:
    pipe.rpush(key, message.model_dump_json())
    pipe.expire(key, ttl)
    await pipe.execute()

async def set_state_key(key:str, value:str, ttl=int|None):
  await client.set(key, value)
  if ttl:
    client.expire(key, ttl)

async def get_state_key(key:str) -> Optional[str]:
  res = await client.get(key)
  return res

async def delete_state_key(key:str):
  await client.delete(key)

#async def incr_count(key:str):
#  await client.incr(key) ## FUTURE!

async def get_history(key:str):
  json_list = await client.lrange(key, 0, -1)
  return json_list

