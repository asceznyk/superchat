import api, { unwrap, fetchWithAuth } from '@/api/setup'
import { CHAT_CONFIG } from '@/config/chat'

export async function getMessageHistory(threadId:string) {
  const res = await api.get(`/messages/${threadId}`);
  return res.data;
}

export async function streamChatResponse(
  userInput:string,
  threadId:string,
  signal:AbortController=null,
  msgType:string="text"
) {
  const res = await fetchWithAuth(`/api/messages/${threadId}`, {
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



