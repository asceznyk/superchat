import pytest
from httpx import AsyncClient, ASGITransport

from unittest.mock import AsyncMock, patch
from asgi_lifespan import LifespanManager

from tests.api.mocks import FakeRedis

from app.main import app
from app.api.auth.user import get_current_user

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

@pytest.fixture(autouse=True)
def patch_redis():
  fake = FakeRedis()
  with (
    patch("app.services.cache.redis_client", fake),
    patch("app.api.auth.user.redis_client", fake),
    patch("app.api.auth.google.redis_client", fake),
  ):
    yield fake

@pytest.fixture(autouse=True)
def mock_verify_token():
  with patch("app.api.auth.user.verify_token") as mock:
    mock.return_value = {
      "sub": "user-1",
      "email": "aris@test.com",
      "name": "Aris Sceznyk",
      "jti": "refresh-jti",
    }
    yield mock

@pytest.fixture(autouse=True)
def mock_issue_jwt_pair():
  with patch("app.api.auth.user.issue_jwt_pair") as mock:
    mock.return_value = ("access-token", "refresh-token")
    yield mock



