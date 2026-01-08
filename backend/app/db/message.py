import json

from typing import Optional, List, Tuple

from psycopg_pool import AsyncConnectionPool

from app.core.config import settings

async def get_latest_messages(
  conn:AsyncConnectionPool,
  thread_id:str,
  limit:int=settings.CACHE_MSGS_CTX_LIMIT
) -> List[str]:
  async with conn.cursor() as cur:
    await cur.execute(
      """
      SELECT *
      FROM (
        SELECT
          a.actor_role,
          m.msg_type,
          m.msg_content,
          m.created_at
        FROM messages AS m
        JOIN actors AS a
          ON m.actor_id = a.id
        WHERE m.thread_id = %s
        ORDER BY m.created_at DESC
        LIMIT %s
      ) t
      ORDER BY created_at ASC;
      """,
      (thread_id, limit),
    )
    rows = await cur.fetchall()
  return [
    json.dumps({
      "role": r[0],
      "msg_type": r[1],
      "msg_content": r[2],
    })
    for r in rows
  ]

async def insert_messages(
  conn:AsyncConnectionPool,
  actor_ids:List[str],
  thread_ids:List[str],
  branched_from_ids:List[Optional[str]],
  msg_types:List[str],
  msg_contents:List[str],
) -> List[Tuple[str,str]]:
  async with conn.cursor() as cur:
    await cur.execute(
      """
      INSERT INTO messages (
        actor_id,
        thread_id,
        branched_from_id,
        msg_type,
        msg_content
      )
      SELECT *
      FROM
      UNNEST(
        %s::uuid[],
        %s::uuid[],
        %s::uuid[],
        %s::text[],
        %s::text[]
      )
      RETURNING id, created_at;
      """,
      (
        actor_ids,
        thread_ids,
        branched_from_ids,
        msg_types,
        msg_contents,
      ),
    )
    return await cur.fetchall()

async def insert_messages_single(
  conn:AsyncConnectionPool,
  actor_id:str,
  thread_id:str,
  branched_from_id:str|None,
  msg_type:str,
  msg_content:str,
) -> List[Tuple[str,str]]:
  return await insert_messages(
    conn,
    [actor_id],
    [thread_id],
    [branched_from_id],
    [msg_type],
    [msg_content],
  )



