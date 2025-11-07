from typing import List, Union

from app.models.states import ChatRequest, AIResponse

def get_chat_response(
  chat_history:List[Union[ChatRequest, AIResponse]]
) -> str:
  print(f"chat_history = {chat_history}")
  return "Basic message - success!"




