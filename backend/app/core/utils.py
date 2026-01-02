from typing import List, Dict

import asyncio
import json

from app.models.states import AIChunkResponse

TEMPTLATE_LIMIT_MSG = "You need to be logged-in to text more"

md_text_samples = [
  """
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

| Month    | Savings |  Fuck | Beer | Month    | Savings |  Fuck | Beer |
| -------- | ------- | ----- |----- | -------- | ------- | ----- |----- |
| January  | $250    | Y     | Y    | January  | $250    | Y     | Y    |
| February | $80     | N     | N    | February | $80     | N     | N    |
| March    | $420    | Y     | Y    | March    | $420    | Y     | Y    |
  """,
  """
  ```
  <HoldOnMyBrother />
  ```

  This is true peace
  """,
  """
  Do you want help with Math or Sex?
  """
]

def convert_to_openai_msgs(history:List[str]) -> List[Dict]:
  messages = []
  for msg_str in history:
    msg_json = json.loads(msg_str)
    role =  "user" if msg_json["role"] != "assistant" else "assistant"
    messages.append({
      "role": role,
      "content": msg_json["msg_content"]
    })
  return messages

def convert_to_gemini_msgs(history:List[str]) -> List[Dict]:
  messages = []
  for msg_str in history:
    msg_json = json.loads(msg_str)
    role = msg_json["role"]
    if role == "assistant": role = "model"
    messages.append({
      "role": role,
      "parts": [{"text": msg_json["msg_content"]}]
    })
  return messages

async def get_limit_response(is_auth:bool):
  for text in TEMPTLATE_LIMIT_MSG:
    data = AIChunkResponse(
      role = "assistant",
      msg_content = text,
      authenticated = is_auth
    )
    await asyncio.sleep(0.02)
    yield f"{data.model_dump_json()}\n\n"

