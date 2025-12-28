from typing import Optional

from app.db.connection import get_db

async def upsert_user(
  conn,
  email:str,
  name:str,
  auth_type:Optional[str]='password',
  auth_provider:Optional[str]='self'
) -> int:
  parts = name.split() if name else []
  first_name = parts[0] if parts else ""
  last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
  username = email.split('@')[0]
  async with conn.cursor() as cur:
    await cur.execute(
      """
      INSERT INTO users (
        username,
        email,
        first_name,
        last_name,
        auth_type,
        auth_provider,
        last_login_at
      )
      VALUES (%s, %s, %s, %s, %s, %s, now())
      ON CONFLICT (email)
      DO UPDATE SET
        last_login_at = EXCLUDED.last_login_at
      RETURNING user_id
      """,
      (
        username,
        email,
        first_name,
        last_name,
        auth_type,
        auth_provider
      ),
    )
    return (await cur.fetchone())[0]





