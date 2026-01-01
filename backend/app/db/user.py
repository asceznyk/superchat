from typing import Optional

from app.db.connection import get_db

async def upsert_user(
  conn,
  email: str,
  name: str,
  auth_type: str = "password",
  auth_provider: str = "self",
) -> str:
  parts = name.split() if name else []
  first_name = parts[0] if parts else ""
  last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
  username = email.split("@")[0]
  async with conn.cursor() as cur:
    await cur.execute(
      """
      WITH existing_user AS (
        SELECT actor_id
        FROM users
        WHERE email = %s
      ),
      new_actor AS (
        INSERT INTO actors (role)
        SELECT 'user'
        WHERE NOT EXISTS (SELECT 1 FROM existing_user)
        RETURNING id
      ),
      resolved_actor AS (
        SELECT actor_id AS id FROM existing_user
        UNION ALL
        SELECT id FROM new_actor
      )
      INSERT INTO users (
        username,
        email,
        first_name,
        last_name,
        auth_type,
        auth_provider,
        actor_id,
        last_login_at
      )
      SELECT
        %s, %s, %s, %s, %s, %s,
        resolved_actor.id,
        now()
      FROM resolved_actor
      ON CONFLICT (email)
      DO UPDATE SET
        last_login_at = EXCLUDED.last_login_at
      RETURNING user_id;
      """,
      (
        email,
        username,
        email,
        first_name,
        last_name,
        auth_type,
        auth_provider,
      ),
    )
    return (await cur.fetchone())[0]



