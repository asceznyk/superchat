import pytest
from httpx import AsyncClient, ASGITransport

from unittest.mock import AsyncMock, patch
from asgi_lifespan import LifespanManager

from app.main import app

@pytest.fixture
async def client():
  with patch("app.main.db_pool.open", new=AsyncMock()), \
    patch("app.main.db_pool.close", new=AsyncMock()):
    async with LifespanManager(app):
      transport = ASGITransport(app=app)
      async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
      ) as client:
        yield client

