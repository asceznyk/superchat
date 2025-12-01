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
  MAX_CHAT_MSGS:int = 10
  CHAT_AUTH_TTL:int = 30 * 24 * 60 * 60
  CHAT_GUEST_TTL:int = 60 * 60


