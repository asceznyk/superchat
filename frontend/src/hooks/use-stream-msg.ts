import { v4 as uuidv4 } from "uuid"

import { useNavigate } from "react-router-dom"
import { useChatStore } from "@/store/chat-store"
import { streamChatResponse, createChatId } from "@/api/chat-service"

import { CHAT_CONFIG } from "@/config/chat"

function throwServerError(err:Object, errorFunc: (err:Object) => void) {
  /*if(err.response?.status === 500) {
    errorFunc({ message: CHAT_CONFIG.ERROR_MSG_500 })
  }*/
  errorFunc({ message: CHAT_CONFIG.ERROR_MSG_500 });
  return;
}

export function useStreamMessage() {
  const userInput = useChatStore((s) => s.userInput);
  const chatId = useChatStore((s) => s.chatId);
  const abortController = useChatStore((s) => s.abortController);
  const setUserInput = useChatStore((s) => s.setUserInput);
  const setChatId = useChatStore((s) => s.setChatId);
  const addUserMessage = useChatStore((s) => s.addUserMessage);
  const addAssistantMessage = useChatStore((s) => s.addAssistantMessage);
  const addAssistantMsgChunk = useChatStore((s) => s.addAssistantMsgChunk);
  const setIsStreaming = useChatStore((s) => s.setIsStreaming);
  const setAbortController = useChatStore((s) => s.setAbortController);
  const setHasResponded = useChatStore((s) => s.setHasResponded);
  const setError = useChatStore((s) => s.setError);
  const navigate = useNavigate();
  const gracefulError = (err:Object) => {
    throwServerError(err, setError)
    setHasResponded(true)
  }
  const streamMsg = async () => {
    if (!userInput.trim())
      return;
    let cid = chatId;
    if (!cid) {
      cid = await createChatId();
      setChatId(cid);
      navigate(`/chat/${cid}`);
    }
    setHasResponded(false);
    const ac = new AbortController();
    setAbortController(ac);
    addUserMessage({
      id: uuidv4(),
      role: "user",
      msgBody: userInput,
    });
    setUserInput("");
    addAssistantMessage({
      id: uuidv4(),
      role: "assistant",
      msg_body: "",
    });
    let reader, decoder;
    try {
      const res = await streamChatResponse(userInput, cid, ac.signal);
      reader = res.reader;
      decoder = res.decoder;
    } catch (err) {
      gracefulError(err)
      return;
    }
    try {
      setIsStreaming(true);
      let buffer = "";
      while (true) {
        const { value, done } = await reader.read();
        const chunk = decoder.decode(value, {stream: true});
        if (chunk) setHasResponded(true);
        if (done) break;
        buffer += chunk;
        let lines = buffer.split(/\r?\n/);
        buffer = lines.pop()!
        for (let line of lines) {
          try {
            const obj = JSON.parse(line);
            addAssistantMsgChunk(obj);
          } catch(err) {
            console.warn("Couldn't parse line from backend", err);
            console.warn("line", line);
            gracefulError(err)
          }
        }
      }
      setIsStreaming(false)
    } catch(err) {
      gracefulError(err)
      setIsStreaming(false)
    }
  };
  const stopMsg = () => {
    abortController?.abort();
    setIsStreaming(false);
    setAbortController(null);
  }
  return { streamMsg, stopMsg };
}

