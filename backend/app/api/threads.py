from typing import Dict

import uuid

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse

from psycopg_pool import AsyncConnectionPool

from app.core.config import settings
from app.models.states import MessageRequest, ChatIdResponse, AIResponse
from app.services.auth import (get_current_user, cookie_attrs, create_token)

from app.db.connection import get_db
from app.db.thread import (
  create_thread_with_retry, get_user_threads, delete_thread
)

router = APIRouter()

@router.get("/")
async def list_user_threads(
  user:Dict=Depends(get_current_user),
  conn:AsyncConnectionPool=Depends(get_db)
):
  is_auth = user['authenticated']
  if not is_auth:
    raise HTTPException(401, detail='action unauthorized!')
  actor_id = user['aid']
  return (await get_user_threads(conn, actor_id))

@router.post("/", response_model=ChatIdResponse)
async def assign_thread_id(
  msg_req:MessageRequest,
  resp:JSONResponse,
  user:Dict=Depends(get_current_user),
  conn:AsyncConnectionPool=Depends(get_db)
) -> ChatIdResponse:
  gen_thread_id = str(uuid.uuid4())
  if user['authenticated']:
    actor_id = user['aid']
    created_thread_id = str(await create_thread_with_retry(
      conn,
      actor_id,
      "Chat",
      gen_thread_id
    ))
    await redis_client.add_to_set(
      f"{settings.CACHE_PREFIX_THREAD_OWNER}:auth:{actor_id}",
      created_thread_id
    )
    return ChatIdResponse(thread_id=created_thread_id)
  cid_resp = ChatIdResponse(thread_id=gen_thread_id)
  payload = {
    "gid": str(uuid.uuid4()),
    "type": "guest"
  }
  guest_token = create_token(payload, token_type='guest')
  resp.set_cookie(**cookie_attrs(
    "guest_id",
    guest_token,
    max_age=(settings.JWT_GUEST_TTL_MINS*60)
  ))
  return cid_resp

@router.post("/delete/{thread_id}")
async def delete_user_thread(
  thread_id:str,
  user:Dict=Depends(get_current_user),
  conn:AsyncConnectionPool=Depends(get_db)
):
  is_auth = user['authenticated']
  if not is_auth:
    raise HTTPException(401, detail='action unauthorized!')
  actor_id = user['aid']
  return (await delete_thread(conn, actor_id, thread_id))

