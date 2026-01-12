import os
import uuid
import asyncio

import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.models import states
from app.api import auth, messages, threads
from app.db.connection import db_pool
from app.services.response_writeback import writeback_consumer

@asynccontextmanager
async def lifespan(app: FastAPI):
  await db_pool.open()
  worker_task = asyncio.create_task(writeback_consumer())
  try:
    yield
  finally:
    worker_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
      await worker_task
    await db_pool.close()

app = FastAPI(root_path="/api", lifespan=lifespan)

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.ALLOW_ORIGINS,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(auth.user.router, prefix="/auth/user")
app.include_router(auth.google.router, prefix="/auth/google")
app.include_router(messages.router, prefix="/messages")
app.include_router(threads.router, prefix="/threads")


