from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings
from pydantic import ConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class settings(BaseSettings):
  model_config = ConfigDict(
    env_file = BASE_DIR / ".env",
    case_sensitive = True
  )

  APP_NAME:str = "superchat"
  APP_ENV:str
  APP_FRONTEND_URL:str

  OPENAI_API_KEY:str
  GEMINI_API_KEY:str
  GEMINI_SYSTEM_PROMPT:str = (
    "You are a chat assistant. "
    "Be witty, sarcastic, stoic and pragmatic. "
    "Keep your answers concise."
  )

  CACHE_AI_RESP_KEY:str = "ai_resp:writeback"
  CACHE_CHAT_AUTH_TTL_SECS:int = 30 * 24 * 60 * 60
  CACHE_CHAT_GUEST_TTL_SECS:int = 60 * 60
  COOKIE_MAX_AGE_ANON_SECS:int = 24 * 60 * 60

  ALLOW_ORIGINS:List[str] = [
    "http://localhost",
    "http://localhost:3000",
  ]
  TRUSTED_PROXIES:List[str] = ["172.18.0.0/12"]

  GOOGLE_OAUTH_AUTH_URI:str = "https://accounts.google.com/o/oauth2/auth"
  GOOGLE_OAUTH_TOKEN_URI:str = "https://oauth2.googleapis.com/token"
  GOOGLE_OAUTH_REDIRECT_URI:str
  GOOGLE_OAUTH_CLIENT_ID:str
  GOOGLE_OAUTH_CLIENT_SECRET:str

  JWT_ACCESS_SECRET:str
  JWT_REFRESH_SECRET:str
  JWT_ALGORITHM:str = "HS256"
  JWT_ACCESS_TTL_MINS:int = 15
  JWT_REFRESH_TTL_MINS:int = 24 * 60

  PG_USER:str
  PG_PSWD:str
  PG_MAIN_DB:str
  PG_TEST_DB:str
  PG_HOST:str = "postgres"
  PG_PORT:int = 5432

  @property
  def DB_URL(self) -> str:
    selected_db = self.PG_MAIN_DB if self.APP_ENV != "testing" else self.PG_TEST_DB
    return (
      f"postgresql://{self.PG_USER}:"
        f"{self.PG_PSWD}@{self.PG_HOST}:"
        f"{self.PG_PORT}/{selected_db}"
    )

settings = settings()

