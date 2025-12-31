from app.main import app
from app.api.auth.user import get_current_user

def fake_user(authenticated=True):
  return {
    "authenticated": authenticated,
    "name": "Aris",
    "email": "aris@test.com",
  }

def override_current_user(auth:bool=True):
  def _override():
    return fake_user(auth)
  return _override

async def test_user_me_anon(client):
  app.dependency_overrides[get_current_user] = override_current_user(False)
  resp = await client.get("/api/auth/user/me")
  assert resp.status_code == 401
  app.dependency_overrides.clear()

async def test_user_me_auth(client):
  app.dependency_overrides[get_current_user] = override_current_user()
  resp = await client.get("/api/auth/user/me")
  assert resp.status_code == 200
  data = resp.json()
  assert data["email"] == "aris@test.com"
  app.dependency_overrides.clear()

async def test_refresh_success(client, patch_redis):
  jti = "refresh-jti"
  redis_key = f"user:jti:{jti}"
  patch_redis.store[redis_key] = 1
  client.cookies.set("session_refresh", "valid-refresh-token")
  resp = await client.post("/api/auth/user/refresh")
  assert resp.status_code == 200
  assert resp.json() == {"set": True}
  assert "session_id" in resp.cookies
  assert "session_refresh" in resp.cookies
  assert redis_key not in patch_redis.store

async def test_refresh_missing_cookie(client):
  resp = await client.post("/api/auth/user/refresh")
  assert resp.status_code == 401
  assert resp.json()["detail"] == "Missing refresh token"

async def test_refresh_revoked_token(client):
  client.cookies.set("session_refresh", "valid-refresh-token")
  resp = await client.post("/api/auth/user/refresh")
  assert resp.status_code == 401
  assert resp.json()["detail"] == "Refresh token revoked"



