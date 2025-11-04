import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
  APP_NAME:str = "diagene"
  OPENAI_API_KEY:str = os.getenv("OPENAI_API_KEY")
  MAX_CHAT_MSGS:int = 40


