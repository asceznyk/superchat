import uuid
import json

from typing import Optional, Dict, Union

from fastapi import Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from psycopg_pool import AsyncConnectionPool

from app.core.config import settings
from app.core.service import default_client
from app.core.utils import get_limit_response
from app.models.states import MessageRequest, ChatIdResponse, AIResponse

from app.services.cache import redis_client
from app.services.auth import (
  secure_cookie, create_token, get_current_user, get_current_guest
)
from app.services.stream import MessageStreamer

from app.db.connection import get_db
from app.db.message import insert_message, get_latest_messages
from app.db.thread import create_thread_with_retry, owns_thread

router = APIRouter()

@router.post("/", response_model=ChatIdResponse)
async def assign_thread_id(
  msg_reg:MessageRequest,
  response:JSONResponse,
  user:Dict=Depends(get_current_user),
  conn:AsyncConnectionPool=Depends(get_db)
) -> ChatIdResponse:
  gen_thread_id = str(uuid.uuid4())
  if user['authenticated']:
    actor_id = user['actor']
    created_thread_id = str(await create_thread_with_retry(
      conn,
      actor_id,
      "Chat",
      gen_thread_id
    ))
    await redis_client.add_to_set(
      f"owner:auth:{actor_id}", created_thread_id
    )
    return ChatIdResponse(thread_id=created_thread_id)
  resp = ChatIdResponse(thread_id=gen_thread_id)
  payload = {
    "gid": str(uuid.uuid4()),
    "typ": "guest"
  }
  guest_token = create_token(payload, token_type='guest')
  response.set_cookie(**secure_cookie(
    "guest_id",
    guest_token,
    max_age=(settings.JWT_GUEST_TTL_MINS*60)
  ))
  return resp

@router.get("/{thread_id}", response_model=None)
async def load_converstaion_thread(
  thread_id:str,
  user:Dict=Depends(get_current_user),
  guest:Dict=Depends(get_current_guest),
  conn:AsyncConnectionPool=Depends(get_db)
) -> JSONResponse:
  actor_type, actor_id = "guest", guest.get('gid')
  is_auth = user['authenticated']
  if is_auth:
    actor_type, actor_id = "auth", user['actor']
  thread_key = f"thread:{actor_type}:{actor_id}:{thread_id}"
  history = await redis_client.get_chat_history(thread_key)
  if is_auth and len(history) <= 0:
    history = await get_latest_messages(conn, thread_id)
    await redis_client.add_chat_message(thread_key, history)
  return JSONResponse(content = jsonable_encoder(
    [json.loads(s) for s in history]
  ))

@router.post("/{thread_id}", response_model=None)
async def gen_ai_response(
  thread_id:str,
  msg_reg:MessageRequest,
  user:Dict=Depends(get_current_user),
  guest:Dict=Depends(get_current_guest),
  conn:AsyncConnectionPool=Depends(get_db)
) -> StreamingResponse:
  is_auth = user["authenticated"]
  if (not is_auth) and (not guest["verified"]):
    raise HTTPException(401, detail="no valid cookies!")
  actor_type, actor_id = "guest", guest.get("gid")
  if is_auth:
    actor_type, actor_id = "auth", user['actor']
    owner_key = f"owner:{actor_type}:{actor_id}"
    if not (await owns_thread(conn, owner_key, thread_id)):
      raise HTTPException(403, detail="no thread for current user")
  thread_key = f"thread:{actor_type}:{actor_id}:{thread_id}"
  await redis_client.add_chat_message(
    thread_key, msg_reg.model_dump_json()
  )
  if is_auth:
    await insert_message(
      conn,
      actor_id,
      thread_id,
      msg_reg.msg_type,
      msg_reg.msg_content
    )
  history = await redis_client.get_chat_history(thread_key)
  msg_streamer = MessageStreamer(
    response_stream = default_client.get_chat_response,
    chat_history = history,
    payload = {
      "actor_id": msg_reg.ai_model_id,
      "thread_key": thread_key
    }
  )
  resp = StreamingResponse(
    msg_streamer.stream_and_persist(is_auth),
    media_type="text/event-stream"
  )
  return resp


