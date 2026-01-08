import json

from app.core.config import settings
from app.services.cache import redis_client
from app.db.connection import db_pool
from app.db.message import insert_messages_single

async def writeback_consumer():
  while True:
    _, raw = await redis_client.q_get(settings.CACHE_AI_RESP_WB)
    payload = json.loads(raw)
    await redis_client.add_chat_message(
      payload['view_thread_key'],
      payload['ai_resp']
    )
    thread_id = payload['view_thread_key'].split(":")[-1]
    is_auth = payload['is_auth']
    ai_resp = json.loads(payload['ai_resp'])
    if not is_auth:
      continue
    await redis_client.add_chat_message(
      payload['ctx_thread_key'],
      payload['ai_resp']
    )
    async with db_pool.connection() as conn:
      await insert_messages_single(
        conn,
        payload['actor_id'],
        thread_id,
        None,
        'text',
        ai_resp['msg_content'],
      )

