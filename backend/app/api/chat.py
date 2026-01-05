import uuid
import json

from typing import Optional, Dict, Union

from fastapi import Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, Depends, Header, HTTPException

from app.core.config import settings
from app.core.utils import get_limit_response
from app.models.states import MessageRequest, ChatIdResponse, AIResponse

from app.services.cache import redis_client
from app.services.auth import (
  secure_cookie, create_token, get_current_user, get_current_guest
)
from app.services.stream import MessageStreamer

from app.db.connection import get_db
from app.db.message import insert_message

#import app.services.google_client as google_client
import app.services.dummy_client as dummy_client

router = APIRouter()

@router.post("/", response_model=ChatIdResponse)
async def assign_thread_id(
  msg_reg:MessageRequest,
  response:JSONResponse,
  user:Dict=Depends(get_current_user)
) -> ChatIdResponse:
  resp = ChatIdResponse(thread_id=str(uuid.uuid4()))
  if user['authenticated']:
    return resp
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
async def get_converstaion_thread(
  thread_id:str,
  user:Dict=Depends(get_current_user),
  guest:Dict=Depends(get_current_guest)
) -> JSONResponse:
  actor_type, actor_id = "guest", guest
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
  msg_reg:MessageRequest,
  user:Dict=Depends(get_current_user),
  guest:Dict=Depends(get_current_guest),
  conn=Depends(get_db)
) -> StreamingResponse:
  is_auth = user["authenticated"]
  if (not is_auth) and (not guest["verified"]):
    raise HTTPException(401, detail="no valid cookies!")
  actor_type, actor_id = "guest", guest.get("gid")
  if is_auth:
    actor_type, actor_id = "auth", user['actor']
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
    response_stream = dummy_client.get_chat_response,
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


