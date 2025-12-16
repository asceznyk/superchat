import os
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.config import Settings
from app.models import states
from app.api import chat

settings = Settings()
app = FastAPI(root_path="/api")

settings = Settings()

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.ALLOW_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/", response_model=None)
async def root() -> JSONResponse:
  return JSONResponse(content=jsonable_encoder({"message":"Hello world!"}))


