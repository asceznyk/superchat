from typing import Dict

import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse

from psycopg_pool import AsyncConnectionPool

from app.core.config import settings
from app.core.service import default_client
from app.models.states import MessageRequest

from app.services.cache import redis_client
from app.services.auth import (
  get_current_user, get_current_guest
)
from app.services.stream import MessageStreamer

from app.db.connection import get_db
from app.db.message import insert_messages_single, get_latest_messages
from app.db.thread import owns_thread, touch_thread

router = APIRouter()

@router.get("/{thread_id}", response_model=None)
async def get_user_messages(
  thread_id:str,
  user:Dict=Depends(get_current_user),
  guest:Dict=Depends(get_current_guest),
  conn:AsyncConnectionPool=Depends(get_db)
) -> JSONResponse:
  actor_type, actor_id = "guest", guest.get('gid')
  is_auth = user['authenticated']
  if (not is_auth) and (not guest['verified']):
    raise HTTPException(401, detail="no valid cookies!")
  if is_auth:
    actor_type, actor_id = "auth", user['aid']
  view_thread_key = f"{settings.CACHE_PREFIX_VIEW_THREAD}:{actor_type}:{actor_id}:{thread_id}"
  ctx_thread_key = f"{settings.CACHE_PREFIX_CTX_THREAD}:{actor_type}:{actor_id}:{thread_id}"
  history = await redis_client.get_chat_history(view_thread_key)
  if is_auth and len(history) <= 0:
    history = await get_latest_messages(conn, thread_id)
    await redis_client.add_chat_message(view_thread_key, history)
    await redis_client.add_chat_message(ctx_thread_key, history)
  return JSONResponse(content = jsonable_encoder(
    [json.loads(s) for s in history]
  ))

@router.post("/{thread_id}", response_model=None)
async def gen_ai_response(
  thread_id:str,
  msg_req:MessageRequest,
  user:Dict=Depends(get_current_user),
  guest:Dict=Depends(get_current_guest),
  conn:AsyncConnectionPool=Depends(get_db)
) -> StreamingResponse:
  is_auth = user['authenticated']
  if (not is_auth) and (not guest['verified']):
    raise HTTPException(401, detail="no valid cookies!")
  actor_type, actor_id = "guest", guest.get('gid')
  if is_auth:
    actor_type, actor_id = "auth", user['aid']
    owner_key = f"{settings.CACHE_PREFIX_THREAD_OWNER}:{actor_type}:{actor_id}"
    if not (await owns_thread(conn, owner_key, thread_id)):
      raise HTTPException(403, detail="no thread for current user")
  view_thread_key = f"{settings.CACHE_PREFIX_VIEW_THREAD}:{actor_type}:{actor_id}:{thread_id}"
  ctx_thread_key = f"{settings.CACHE_PREFIX_CTX_THREAD}:{actor_type}:{actor_id}:{thread_id}"
  await redis_client.add_chat_message(
    view_thread_key, msg_req.model_dump_json()
  )
  if is_auth:
    await redis_client.add_chat_message(
      ctx_thread_key, msg_req.model_dump_json()
    )
    await insert_messages_single(
      conn,
      actor_id,
      thread_id,
      None,
      msg_req.msg_type,
      msg_req.msg_content
    )
    await touch_thread(conn, actor_id, thread_id)
  history = await redis_client.get_chat_history(
    ctx_thread_key if is_auth else view_thread_key
  )
  msg_streamer = MessageStreamer(
    response_stream = default_client.get_chat_response,
    chat_history = history,
    payload = {
      "actor_id": msg_req.ai_model_id,
      "view_thread_key": view_thread_key,
      "ctx_thread_key": ctx_thread_key
    }
  )
  resp = StreamingResponse(
    msg_streamer.stream_and_persist(is_auth),
    media_type="text/event-stream"
  )
  return resp


