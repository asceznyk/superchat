import uuid
import asyncio

from fastapi.responses import StreamingResponse
from fastapi import APIRouter

from app.models.states import DummyRequest, AIChunkResponse

router = APIRouter()

async def dummy_response():
  stream = "This is some content for you!"
  for chunk in stream.split(' '):
    data = AIChunkResponse(
      role = "assistant",
      chat_id = str(uuid.uuid4()),
      msg_body = chunk,
      authenticated = False
    )
    await asyncio.sleep(0.3)
    yield f"data: {data.model_dump_json()}\n\n"

@router.post("/")
async def dummy(dummy_req:DummyRequest):
  return StreamingResponse(
    dummy_response(),
    media_type="text/event-stream"
  )


