import api, { fetchWithAuth } from '@/api/setup'
import { CHAT_CONFIG } from '@/config/chat'

export async function createChatId() {
  const res = await api.post('/chat/', {
    role: "user",
    msg_type: "text",
    msg_content: "ping",
    ai_model_id: CHAT_CONFIG.DEFAULT_MODEL_ID
  });
  return res.data.thread_id;
}

export async function getChatHistory(chatId:string) {
  const res = await api.get(`/chat/${chatId}`);
  return res.data;
}

export async function streamChatResponse(
  userInput:string,
  chatId:string,
  signal:AbortController=null,
  msgType:string="text"
) {
  const res = await fetchWithAuth(`/api/chat/${chatId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(
      {
        role: "user",
        msg_type: msgType,
        msg_content: userInput,
        ai_model_id: CHAT_CONFIG.DEFAULT_MODEL_ID
      }
    ),
    signal
  });
  if (!res.ok) throw new Error("Request failed");
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  return { reader, decoder };
}



