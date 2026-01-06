import json

from typing import Optional, List

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

async def insert_message(
  conn:AsyncConnectionPool,
  actor_id:str,
  thread_id:str,
  msg_type:str,
  msg_content:str,
  branched_from_id:str|None = None,
) -> Optional[tuple[str,str]]:
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
      VALUES (%s, %s, %s, %s, %s)
      RETURNING id, created_at;
      """,
      (
        actor_id,
        thread_id,
        branched_from_id,
        msg_type,
        msg_content,
      ),
    )
    message_id, created_at = await cur.fetchone()
    return message_id, created_at



