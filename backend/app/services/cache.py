from typing import Optional, Union, Dict, List

import redis.asyncio as redis

from app.core.config import settings

class RedisClient:

  def __init__(self, client:Optional[redis.Redis]=None):
    self.client = client or redis.Redis(
      host="redis",
      port=6379,
      decode_responses=True,
    )

  async def q_put(self, q_key:str, payload:str):
    await self.client.lpush(q_key, payload)

  async def q_get(self, q_key:str) -> str:
    return (await self.client.brpop(q_key))

  async def add_to_set(self, key:str, item:str, ttl:Optional[int]=None):
    async with self.client.pipeline() as pipe:
      pipe.sadd(key, item)
      if ttl is not None:
        pipe.expire(key, ttl)
      await pipe.execute()

  async def is_set_member(self, key:str, item:str) -> bool:
    return (await self.client.sismember(key, item))

  async def remove_from_set(self, key:str, value:str):
    await self.client.srem(key, value)

  async def add_chat_message(
    self,
    key:str,
    payload:Union[List[str],str],
    limit:int=settings.CACHE_MSGS_CTX_LIMIT
  ):
    ttl = settings.CACHE_CHAT_GUEST_TTL_SECS if key.startswith("thread:guest:") \
      else settings.CACHE_CHAT_AUTH_TTL_SECS
    async with self.client.pipeline() as pipe:
      pipe.rpush(key, *(payload if type(payload) == list else [payload]))
      pipe.ltrim(key, -limit, -1)
      pipe.expire(key, ttl)
      await pipe.execute()

  async def get_chat_history(
    self, key:str
  ) -> List[str]:
    return (await self.client.lrange(key, 0, -1))

  async def add_key_value(self, key:str, value:str, ttl:Optional[int]=None):
    async with self.client.pipeline() as pipe:
      pipe.set(key, value)
      if ttl is not None:
        pipe.expire(key, ttl)
      await pipe.execute()

  async def get_key_value(self, key:str) -> Optional[str]:
    return await self.client.get(key)

  async def delete_key_value(self, key:str):
    if not (await self.client.exists(key)): return
    await self.client.delete(key)

  async def does_key_exist(self, key:str) -> bool:
    return bool(await self.client.exists(key))

redis_client = RedisClient()


