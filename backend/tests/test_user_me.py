from unittest.mock import patch

def fake_user(authenticated=True):
  return {
    "authenticated": authenticated,
    "name": "Aris",
    "email": "aris@test.com"
  }

async def test_user_me_anon(client):
  with patch("app.services.auth.get_current_user", return_value=fake_user(False)):
    resp = await client.get("/api/auth/user/me")
    assert resp.status_code == 401

async def test_user_me_auth_despite(client):
  with patch("app.services.auth.get_current_user", return_value=fake_user()):
    resp = await client.get("/api/auth/user/me")
    assert resp.status_code == 401
    data = resp.json()



