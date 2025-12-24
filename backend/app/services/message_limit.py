from fastapi import Cookie

from app.services.redis_client import get_msg_count

async def limit_user_message(session_id:str|None=Cookie(default=None)) -> bool:
  msg_count = await get_msg_count(session_id)
  if msg_count >= settings.MAX_ANON_CHAT_MSGS:
    await set_msg_limit(session_id)
    return True
  return False

