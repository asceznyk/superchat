import os
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.models import states
from app.api import chat, mock

app = FastAPI(root_path="/api")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(mock.router, prefix="/mock", tags=["mock"])

@app.get("/", response_model=states.AIResponse)
async def root() -> JSONResponse:
  return JSONResponse(content=jsonable_encoder({"message":"Hello world!"}))


