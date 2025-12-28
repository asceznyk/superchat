from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/

class settings(BaseSettings):

  APP_NAME:str = "superchat"
  APP_ENV:str

  OPENAI_API_KEY:str
  GEMINI_API_KEY:str
  GEMINI_SYSTEM_PROMPT:str = (
    "You are a chat assistant. "
    "Be witty, sarcastic, stoic and pragmatic. "
    "Keep your answers concise."
  )

  MAX_ANON_CHAT_MSGS:int = 10
  CHAT_AUTH_TTL:int = 30 * 24 * 60 * 60
  CHAT_GUEST_TTL:int = 60 * 60
  MAX_AGE_ANON_ID:int = 24 * 60 * 60

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
  JWT_ACCESS_TTL:int = 15
  JWT_REFRESH_TTL:int = 24 * 60

  PG_USER:str
  PG_PSWD:str
  PG_DB:str
  PG_HOST:str = "postgres"
  PG_PORT:int = 5432

  @property
  def DB_URL(self) -> str:
    return (
      f"postgresql://{self.PG_USER}:"
        f"{self.PG_PSWD}@{self.PG_HOST}:"
        f"{self.PG_PORT}/{self.PG_DB}"
    )

  class Config:
    env_file = BASE_DIR / ".env"
    case_sensitive = True

settings = settings()

