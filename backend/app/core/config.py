from typing import List

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(
  os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
  )
)
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

class Settings(BaseSettings):
  APP_NAME:str = "superchat"
  OPENAI_API_KEY:str = os.getenv("OPENAI_API_KEY")
  GEMINI_API_KEY:str = os.getenv("GEMINI_API_KEY")
  GEMINI_SYSTEM_PROMPT:str = """
  You are a chat assistant.
  Be witty, sarcastic stoic and pragmatic.
  Keep your answers concise.
  """
  MAX_ANON_CHAT_MSGS:int = 10
  CHAT_AUTH_TTL:int = 30 * 24 * 60 * 60
  CHAT_GUEST_TTL:int = 60 * 60
  MAX_AGE_ANON_ID:int = 24 * 60 * 60
  ALLOW_ORIGINS:List[str] = ["http://localhost", "http://localhost:3000"]
  TRUSTED_PROXIES:List[str] = ["172.18.0.0/12"]
  GOOGLE_OAUTH_AUTH_URI:str = "https://accounts.google.com/o/oauth2/auth"
  GOOGLE_OAUTH_TOKEN_URI:str = "https://oauth2.googleapis.com/token"
  GOOGLE_OAUTH_REDIRECT_URI:str = "http://localhost/api/auth/google/callback"
  GOOGLE_OAUTH_CLIENT_ID:str = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
  GOOGLE_OAUTH_CLIENT_SECRET:str = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
  JWT_SERVER_SECRET:str = os.getenv("JWT_SERVER_SECRET")
  JWT_ALGORITHM:str = "HS256"
  JWT_EXPIRE_MINS:int = 15


