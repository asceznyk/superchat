import { v4 as uuidv4 } from "uuid";
import { create } from "zustand";

interface ThreadMessage {
  id: string;
  role: "user" | "assistant";
  msgContent: string;
}

const initialState = {
  threadId: "",
  userInput: "",
  startThread: false,
  messageHistory: [] as ThreadMessage[],
  isStreaming: false,
  abortController: null as AbortController | null,
  hasResponded: true,
  error: null as { message: string } | null,
};

type ThreadState = typeof initialState & {
  threadId: string;
  setThreadId: (text: string) => void;
  userInput: string;
  setUserInput: (text: string) => void;
  startThread: boolean;
  setStartThread: (v: boolean) => void;
  messageHistory: ThreadMessage[];
  setMessageHistory: (history: ThreadMessage[]) => void;
  addUserMessage: (msg: ThreadMessage) => void;
  addAssistantMessage: (msg: ThreadMessage) => void;
  addAssistantMsgChunk: (msg: ThreadMessage) => void;
  isStreaming: boolean;
  setIsStreaming: (v: boolean) => void;
  abortController: AbortController | null;
  hasResponded: boolean;
  setHasResponded: (v: boolean) => void;
  error: { message:string } | null;
  setError: (v: { message:string  } | null) => void;
}

export const useThreadStore = create<ThreadState>((set) => ({
  ...initialState,
  setUserInput: (text) => set({ userInput: text }),
  setStartThread: (v) => set({ startThread: v }),
  setThreadId: (text) => set({ threadId: text }),
  setMessageHistory: (history) =>
    set({
      messageHistory: history.map((msg) => ({
        id: uuidv4(),
        role: msg.role,
        msgContent: msg.msg_content,
      })),
    }),
  addUserMessage: (msg) =>
    set((state) => ({ messageHistory: [...state.messageHistory, msg] })),
  addAssistantMessage: (chunk) =>
    set((state) => {
      return {
        messageHistory: [
          ...state.messageHistory,
          { id: chunk.id, role: chunk.role, msgContent: chunk.msg_content },
        ]
      }
    }),
  addAssistantMsgChunk: (chunk) =>
    set((state) => {
      if (state.messageHistory.length <= 0) return state;
      const last = state.messageHistory[state.messageHistory.length - 1];
      if (!last || last.role !== "assistant") return state;
      return {
        messageHistory: [
          ...state.messageHistory.slice(0, -1),
          { ...last, msgContent: last.msgContent + chunk.msg_content },
        ],
      };
    }),
  setIsStreaming: (v) => set({ isStreaming: v }),
  setAbortController: (c) => set({ abortController: c }),
  setHasResponded: (v) => set({ hasResponded: v }),
  setError: (o) => set({ error: o }),
  reset: () => set(() => initialState),
}));


