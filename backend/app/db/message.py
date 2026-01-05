from typing import Optional

async def insert_message(
  conn,
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



