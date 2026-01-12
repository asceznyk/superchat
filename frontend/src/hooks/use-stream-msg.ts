import { v4 as uuidv4 } from "uuid"

import { useNavigate } from "react-router-dom"
import { useThreadStore } from "@/store/thread-store"
import { useUserStore } from "@/store/user-store"
import { createThreadId, getUserThreads } from "@/api/threads"
import { streamChatResponse } from "@/api/messages"

import { CHAT_CONFIG } from "@/config/chat"

function throwServerError(err:Object, errorFunc: (err:Object) => void) {
  /*if(err.response?.status === 500) {
    errorFunc({ message: CHAT_CONFIG.ERROR_MSG_500 })
  }*/
  errorFunc({ message: CHAT_CONFIG.ERROR_MSG_500 });
  return;
}

export function useStreamMessage() {
  const userInput = useThreadStore((s) => s.userInput);
  const startThread = useThreadStore((s) => s.startThread);
  const threadId = useThreadStore((s) => s.threadId);
  const abortController = useThreadStore((s) => s.abortController);
  const setUserInput = useThreadStore((s) => s.setUserInput);
  const setStartThread = useThreadStore((s) => s.setStartThread);
  const setThreadId = useThreadStore((s) => s.setThreadId);
  const addUserMessage = useThreadStore((s) => s.addUserMessage);
  const addAssistantMessage = useThreadStore((s) => s.addAssistantMessage);
  const addAssistantMsgChunk = useThreadStore((s) => s.addAssistantMsgChunk);
  const setIsStreaming = useThreadStore((s) => s.setIsStreaming);
  const setAbortController = useThreadStore((s) => s.setAbortController);
  const setHasResponded = useThreadStore((s) => s.setHasResponded);
  const setError = useThreadStore((s) => s.setError);
  const isLoggedIn = useUserStore(s => s.isLoggedIn);
  const setThreadHistory = useUserStore(s => s.setThreadHistory);
  const navigate = useNavigate();
  const gracefulError = (err:Object) => {
    throwServerError(err, setError)
    setHasResponded(true)
  }
  const streamMsg = async () => {
    if (!userInput.trim())
      return;
    let cid = threadId;
    if (!cid) {
      cid = await createThreadId()
      setThreadId(cid)
      navigate(`/chat/${cid}`)
    }
    setHasResponded(false);
    const ac = new AbortController();
    setAbortController(ac);
    addUserMessage({
      id: uuidv4(),
      role: "user",
      msgContent: userInput,
    });
    setUserInput("");
    addAssistantMessage({
      id: uuidv4(),
      role: "assistant",
      msg_content: "",
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
      if (isLoggedIn && !startThread) {
        setStartThread(true)
        setThreadHistory(await getUserThreads())
      }
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

