from psycopg_pool import AsyncConnectionPool

from app.core.config import settings

db_pool = AsyncConnectionPool(
  settings.DB_URL,
  min_size = 1,
  max_size = 10,
)

async def get_db():
  async with db_pool.connection() as conn:
    yield conn




