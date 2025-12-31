import json
import httpx
from httpx import Response, Request, MockTransport

from unittest.mock import patch, AsyncMock

from app.main import app
from app.api.auth.google import get_db

MockAsyncClient = httpx.AsyncClient

async def override_get_db():
  return object()

def google_token_handler(request: Request) -> Response:
  return Response(
    status_code=200,
    json={"id_token": "fake-id-token"},
  )

async def test_google_auth_uri(client, patch_redis):
  resp = await client.get("/api/auth/google/")
  assert resp.status_code == 200
  assert "accounts.google.com" in resp.text

async def test_google_callback_success(client, patch_redis):
  patch_redis.store["state123"] = 1
  transport = MockTransport(google_token_handler)
  with patch(
    "app.api.auth.google.httpx.AsyncClient",
    lambda **kwargs: MockAsyncClient(transport=transport, **kwargs),
  ), \
    patch("app.api.auth.google.verify_google_id_token") as mock_verify, \
    patch("app.api.auth.google.upsert_user", return_value=1):
    mock_verify.return_value = {
      "email": "aris@test.com",
      "name": "Aris"
    }
    app.dependency_overrides[get_db] = override_get_db
    resp = await client.get(
      "/api/auth/google/callback",
      params={"state": "state123", "code": "code123"}
    )
    assert resp.status_code == 307
    assert "session_id" in resp.cookies
    assert "session_refresh" in resp.cookies
    app.dependency_overrides.clear()


