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
  addAssistantMessage: (id: string, msg: ChatMessage) => void;
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
  addAssistantMessage: (id, chunk) =>
    set((state) => {
      const idx = state.messageHistory.findIndex((m) => m.id === id);
      if (idx !== -1) {
        const newHistory = state.messageHistory.map((m, i) =>
          i === idx ? { ...m, msgBody: m.msgBody + chunk.msg_body } : m
        );
        return { messageHistory: newHistory };
      } else {
        return {
          messageHistory: [
            ...state.messageHistory,
            { id, role: "assistant", msgBody: chunk.msg_body },
          ],
        };
      }
    }),
}));



