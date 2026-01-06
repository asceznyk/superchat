from sqlalchemy import text
from psycopg.errors import UniqueViolation

from psycopg_pool import AsyncConnectionPool

from app.services.cache import redis_client

async def create_thread(
  conn:AsyncConnectionPool,
  actor_id:str,
  thread_title:str,
  thread_id:str|None = None,
  is_pinned:bool = False,
) -> str|None:
  async with conn.cursor() as cur:
    try:
      if thread_id is None:
        await cur.execute(
          """
          INSERT INTO threads (
            actor_id,
            thread_title,
            is_pinned
          )
          VALUES (%s, %s, %s)
          RETURNING id;
          """,
          (
            actor_id,
            thread_title,
            is_pinned,
          ),
        )
      else:
        await cur.execute(
          """
          INSERT INTO threads (
            id,
            actor_id,
            thread_title,
            is_pinned
          )
          VALUES (%s, %s, %s, %s)
          RETURNING id;
          """,
          (
            thread_id,
            actor_id,
            thread_title,
            is_pinned,
          ),
        )
      (created_thread_id,) = await cur.fetchone()
      return created_thread_id
    except UniqueViolation:
      return None

async def create_thread_with_retry(
  conn:AsyncConnectionPool, actor_id:str, thread_title:str, thread_id:str|None
) -> str:
  created_thread_id = await create_thread(
    conn,
    actor_id,
    thread_title,
    thread_id
  )
  if created_thread_id is None:
    return (await create_thread_with_retry(
      conn, actor_id, thread_title, str(uuid.uuid4())
    ))
  return created_thread_id

async def db_check_thread_ownership(
  conn:AsyncConnectionPool,
  actor_id:str,
  thread_id:str,
) -> bool:
  async with conn.cursor() as cur:
    result = await cur.execute(
      """
      SELECT 1
      FROM threads
      WHERE id = %s AND actor_id = %s
      LIMIT 1
      """,
      (
        thread_id,
        actor_id
      ),
    )
    return (await result.fetchone()) is not None

async def owns_thread(
  conn:AsyncConnectionPool,
  owner_key:str,
  thread_id:str,
) -> bool:
  actor_id = owner_key.split(":")[-1]
  if (await redis_client.is_set_member(owner_key, thread_id)):
    return True
  owned = await db_check_thread_ownership(
    conn,
    actor_id=actor_id,
    thread_id=thread_id,
  )
  if not owned:
    return False
  await redis_client.add_to_set(owner_key, thread_id)
  return True


