import { create } from "zustand";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  msg_body: string;
}

interface ChatState {
  userInput: string;
  messageHistory: ChatMessage[];
  setUserInput: (text: string) => void;
  addMessage: (msg: ChatMessage) => void;
  clearInput: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  userInput: "",
  messageHistory: [],
  setUserInput: (text) => set({ userInput: text }),
  addMessage: (msg) =>
    set((state) => ({
      messageHistory: [...state.messageHistory, msg],
    })),
  clearInput: () => set({ userInput: "" }),
}));



