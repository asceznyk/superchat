from typing import Union

import redis.asyncio as redis

from app.models.states import ChatRequest, AIResponse

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def add_message(key:str, message:Union[ChatRequest,AIResponse]):
  await redis_client.rpush(key, message.model_dump_json())

async def get_history(key:str):
  json_list = await redis_client.lrange(key, 0, -1)
  return json_list

