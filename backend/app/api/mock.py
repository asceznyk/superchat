import uuid
import asyncio

from fastapi.responses import StreamingResponse
from fastapi import APIRouter

from app.models.states import ChatRequest, AIChunkResponse

router = APIRouter()

async def dummy_call(dummy_req:ChatRequest):
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
async def dummy(dummy_req:ChatRequest):
  chat_id = dummy_req.chat_id
  if not dummy_req.chat_id:
    dummy_req.chat_id = str(uuid.uuid4())
  return StreamingResponse(
    dummy_call(dummy_req),
    media_type="text/event-stream"
  )


