import { v4 as uuidv4 } from "uuid";
import { create } from "zustand";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  msgContent: string;
}

const initialState = {
  chatId: "",
  userInput: "",
  messageHistory: [] as ChatMessage[],
  isStreaming: false,
  abortController: null as AbortController | null,
  hasResponded: true,
  error: null as { message: string } | null,
};

type ChatState = typeof initialState & {
  chatId: string;
  setChatId: (text: string) => void;
  userInput: string;
  setUserInput: (text: string) => void;
  messageHistory: ChatMessage[];
  setMessageHistory: (history: ChatMessage[]) => void;
  addUserMessage: (msg: ChatMessage) => void;
  addAssistantMessage: (msg: ChatMessage) => void;
  addAssistantMsgChunk: (msg: ChatMessage) => void;
  isStreaming: boolean;
  setIsStreaming: (v: boolean) => void;
  abortController: AbortController | null;
  hasResponded: boolean;
  setHasResponded: (v: boolean) => void;
  error: { message:string } | null;
  setError: (v: { message:string  } | null) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  ...initialState,
  setUserInput: (text) => set({ userInput: text }),
  setChatId: (text) => set({ chatId: text }),
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


