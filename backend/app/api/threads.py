from typing import Dict

import uuid

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from psycopg_pool import AsyncConnectionPool

from app.core.config import settings
from app.models.states import ThreadRenameRequest, ThreadIDResponse
from app.services.auth import get_current_user, cookie_attrs, create_token
from app.services.cache import redis_client

from app.db.connection import get_db
from app.db.thread import (
  create_thread_with_retry, get_user_threads,
  delete_thread, rename_thread
)

router = APIRouter()

@router.get("/")
async def list_user_threads(
  user:Dict=Depends(get_current_user),
  conn:AsyncConnectionPool=Depends(get_db)
) -> JSONResponse:
  is_auth = user['authenticated']
  if not is_auth:
    raise HTTPException(401, detail='action unauthorized!')
  return JSONResponse(content=jsonable_encoder(
    await get_user_threads(conn, user['aid'])
  ))

@router.post("/", response_model=ThreadIDResponse)
async def assign_thread_id(
  resp:JSONResponse,
  user:Dict=Depends(get_current_user),
  conn:AsyncConnectionPool=Depends(get_db)
) -> ThreadIDResponse:
  gen_thread_id = str(uuid.uuid4())
  if user['authenticated']:
    actor_id = user['aid']
    created_thread_id = str(await create_thread_with_retry(
      conn,
      actor_id,
      "Old Chat",
      gen_thread_id
    ))
    await redis_client.add_to_set(
      f"{settings.CACHE_PREFIX_THREAD_OWNER}:auth:{actor_id}",
      created_thread_id
    )
    return ThreadIDResponse(thread_id=created_thread_id)
  cid_resp = ThreadIDResponse(thread_id=gen_thread_id)
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

@router.post("/rename/{thread_id}")
async def rename_user_thread(
  thread_id:str,
  rename_req:ThreadRenameRequest,
  user:Dict=Depends(get_current_user),
  conn:AsyncConnectionPool=Depends(get_db)
):
  is_auth = user['authenticated']
  if not is_auth:
    raise HTTPException(401, detail='action unauthorized!')
  return (await rename_thread(
    conn, user['aid'], thread_id, rename_req.thread_title
  ))

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
  await redis_client.delete_key_value(
    f"{settings.CACHE_PREFIX_VIEW_THREAD}:auth:{actor_id}:{thread_id}"
  )
  await redis_client.delete_key_value(
    f"{settings.CACHE_PREFIX_CTX_THREAD}:auth:{actor_id}:{thread_id}"
  )
  return (await delete_thread(conn, actor_id, thread_id))


