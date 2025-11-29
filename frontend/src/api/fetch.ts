import axios from "axios";

const api = axios.create({
  baseURL: "/api"
});

export async function getRoot() {
  const res = await api.get('/');
  return res.data;
}

export async function streamChatResponse(msgBody:string, chatId:string="") {
  const res = await fetch("/api/chat/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(
      {
        role: "user",
        chat_id: chatId,
        msg_body: msgBody,
      }
    ),
  });
  if (!res.ok) throw new Error("Request failed");
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  return { reader, decoder };
}



