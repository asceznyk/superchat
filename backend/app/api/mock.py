import uuid
import asyncio

from fastapi.responses import StreamingResponse
from fastapi import APIRouter

from app.models.states import DummyRequest, AIChunkResponse

router = APIRouter()

async def dummy_response(chat_id:str):
  md_text_sample = """
| Month    | Savings |  Fuck |
| -------- | ------- | ------|
| January  | $250    | Y     |
| February | $80     | N     |
| March    | $420    | Y     |

# Heading 1
## Heading 2
### Heading 3

This is a paragraph of **bold text** and *italic text*. You can also combine them like ***bold and italic***.
To strike through text, use ~~strikethrough~~.

- This is a list item.
- Another list item.
  - A nested list item.

1. Ordered list item one.
2. Ordered list item two.

> This is a blockquote. It's useful for quoting text or highlighting specific information.

Here's some `inline code`.

```python
# This is a code block in Python
def hello_world():
    print("Hello, Markdown!")
```
  """
  for chunk in md_text_sample:
    data = AIChunkResponse(
      role = "assistant",
      chat_id = chat_id,
      msg_body = chunk,
      authenticated = False
    )
    await asyncio.sleep(0.02)
    yield f"{data.model_dump_json()}\n".encode("utf-8")

@router.post("/")
async def dummy(dummy_req:DummyRequest):
  chat_id = dummy_req.chat_id
  if not dummy_req.chat_id:
    chat_id = str(uuid.uuid4())
  return StreamingResponse(
    dummy_response(chat_id),
    media_type="text/event-stream"
  )


