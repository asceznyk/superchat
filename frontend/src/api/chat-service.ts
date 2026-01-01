import api, { fetchWithAuth } from '@/api/setup'

export async function createChatId() {
  const res = await api.post('/chat/', {
    role: "user",
    msg_body: "ping"
  });
  return res.data.chat_id;
}

export async function getChatHistory(chatId:string) {
  const res = await api.get(`/chat/${chatId}`);
  return res.data;
}

export async function streamChatResponse(
  userInput:string, chatId:string, signal:AbortController=null
) {
  const res = await fetchWithAuth(`/api/chat/${chatId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(
      {
        role: "user",
        msg_body: userInput,
      }
    ),
    signal
  });
  if (!res.ok) throw new Error("Request failed");
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  return { reader, decoder };
}



