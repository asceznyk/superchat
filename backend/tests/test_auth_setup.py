import pytest
from unittest.mock import patch

from tests.mocks import FakeRedis

@pytest.fixture(autouse=True)
def patch_redis():
  fake_redis = FakeRedis()
  with patch("app.services.cache.redis_client", fake_redis):
    yield fake_redis

