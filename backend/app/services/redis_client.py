from typing import Union, Optional

import redis.asyncio as redis

from app.core.config import settings
from app.models.states import ChatRequest, AIResponse

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

async def get_history(key:str):
  json_list = await client.ltrim(key, 0, 4)
  return json_list

async def add_key_value(key:str, value:str, ttl:int|None=None):
  if not ttl:
    await client.set(key, value)
  else:
    async with client.pipeline() as pipe:
      pipe.set(key, value)
      pipe.expire(key, ttl)
      await pipe.execute()

async def get_key_value(key:str) -> Optional[str]:
  res = await client.get(key)
  return res

async def delete_key_value(key:str):
  await client.delete(key)

async def does_key_exist(key:str) -> bool:
  res = await client.exists(key)
  return res


#async def incr_count(key:str):
#  await client.incr(key) ## FUTURE!

