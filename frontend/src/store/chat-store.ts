import { create } from "zustand";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  msgBody: string;
}

interface ChatState {
  chatId: string;
  setChatId: (text: string) => void;
  userInput: string;
  setUserInput: (text: string) => void;
  messageHistory: ChatMessage[];
  addUserMessage: (msg: ChatMessage) => void;
  addAssistantMessage: (msg: ChatMessage) => void;
  addAssistantMsgChunk: (msg: ChatMessage) => void;
  isStreaming: boolean;
  setIsStreaming: (v: boolean) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  userInput: "",
  setUserInput: (text) => set({ userInput: text }),
  chatId: "",
  setChatId: (text) => set({ chatId: text }),
  messageHistory: [],
  addUserMessage: (msg) =>
    set((state) => ({
      messageHistory: [...state.messageHistory, msg],
    })),
  addAssistantMessage: (chunk) =>
    set((state) => {
      return {
        messageHistory: [
          ...state.messageHistory,
          { id: chunk.id, role: chunk.role, msgBody: chunk.msg_body },
        ]
      }
    }),
  addAssistantMsgChunk: (chunk) =>
    set((state) => {
      const lastIndex = state.messageHistory.length-1;
      const updatedHistory = state.messageHistory.map((msg, idx) =>
        idx === lastIndex
        ? { ...msg, msgBody: msg.msgBody + chunk.msg_body }
        : msg
      );
      return { messageHistory: updatedHistory }
    }),
  isStreaming: false,
  setIsStreaming: (v) => set({ isStreaming: v })
}));



