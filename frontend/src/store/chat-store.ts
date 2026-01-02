import { v4 as uuidv4 } from "uuid";
import { create } from "zustand";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  msgContent: string;
}

interface ChatState {
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
  userInput: "",
  setUserInput: (text) => set({ userInput: text }),
  chatId: "",
  setChatId: (text) => set({ chatId: text }),
  messageHistory: [],
  setMessageHistory: (history) =>
    set({
      messageHistory: history.map((msg) => ({
        id: uuidv4(),
        role: msg.role,
        msgContent: msg.msg_content,
      })),
    }),
  addUserMessage: (msg) =>
    set((state) => ({
      messageHistory: [...state.messageHistory, msg],
    })),
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
      const lastIndex = state.messageHistory.length-1;
      const updatedHistory = state.messageHistory.map((msg, idx) =>
        idx === lastIndex
        ? { ...msg, msgContent: msg.msgContent + chunk.msg_content }
        : msg
      );
      return { messageHistory: updatedHistory }
    }),
  isStreaming: false,
  setIsStreaming: (v) => set({ isStreaming: v }),
  abortController: null,
  setAbortController: (c) => set({ abortController: c }),
  hasResponded: true,
  setHasResponded: (v) => set({ hasResponded: v }),
  error: null,
  setError: (o) => set({ error: o })
}));



