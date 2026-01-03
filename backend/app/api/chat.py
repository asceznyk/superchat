import uuid
import json

from typing import Optional, Dict, Union

from fastapi import Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import settings
from app.core.utils import get_limit_response
from app.models.states import UserMessageRequest, ChatIdResponse, AIResponse

from app.services.cache import redis_client
from app.services.auth import get_current_user
from app.services.stream import MessageStreamer

from app.db.connection import get_db
from app.db.message import insert_message

#import app.services.google_client as google_client
import app.services.dummy_client as dummy_client

router = APIRouter()

@router.post("/", response_model=ChatIdResponse)
async def assign_thread_id(
  user_msg_req:UserMessageRequest,
  response:JSONResponse,
  user:Dict=Depends(get_current_user),
) -> ChatIdResponse:
  resp = ChatIdResponse(thread_id=str(uuid.uuid4()))
  if user['authenticated']:
    return resp
  response.set_cookie(
    key="guest_id",
    value=str(uuid.uuid4()),
    httponly=True,
    samesite="lax",
    max_age=settings.COOKIE_MAX_AGE_ANON_SECS,
  )
  return resp

@router.get("/{thread_id}", response_model=None)
async def get_converstaion_thread(
  thread_id:str,
  user:Dict=Depends(get_current_user),
  guest_id:str=Cookie(default=None)
) -> JSONResponse:
  actor_type, actor_id = "guest", guest_id
  is_auth = user['authenticated']
  if is_auth:
    actor_type = "auth"
    actor_id = user['actor']
  thread_key = f"thread:{actor_type}:{actor_id}:{thread_id}"
  history = await redis_client.get_chat_history(thread_key)
  return JSONResponse(content = jsonable_encoder(
    [json.loads(s) for s in history]
  ))

@router.post("/{thread_id}", response_model=None)
async def gen_ai_response(
  thread_id:str,
  user_msg_req:UserMessageRequest,
  user:Dict=Depends(get_current_user),
  guest_id:str=Cookie(default=None),
  conn=Depends(get_db)
) -> StreamingResponse:
  actor_type, actor_id = "guest", guest_id
  is_auth = user["authenticated"]
  if (not is_auth) and (not guest_id):
    raise HTTPException(401, detail="no valid cookies!")
  if is_auth:
    actor_type, actor_id = "auth", user['actor']
  thread_key = f"thread:{actor_type}:{actor_id}:{thread_id}"
  await redis_client.add_chat_message(
    thread_key, user_msg_req.model_dump_json()
  )
  if is_auth:
    await insert_message(
      conn,
      actor_id,
      thread_id,
      user_msg_req.msg_type,
      user_msg_req.msg_content
    )
  history = await redis_client.get_chat_history(thread_key)
  msg_streamer = MessageStreamer(
    response_stream = dummy_client.get_chat_response,
    chat_history = history,
    payload = {
      "actor_id": user_msg_req.ai_model_id,
      "thread_key": thread_key
    }
  )
  resp = StreamingResponse(
    msg_streamer.stream_and_persist(is_auth),
    media_type="text/event-stream"
  )
  return resp


