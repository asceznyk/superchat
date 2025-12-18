import { create } from "zustand";

interface ChatLabel {
  label: string;
}

interface UserState {
  isLoggedIn: boolean;
  setIsLoggedIn: (v: boolean) => void;
  chatHistory: ChatLabel[];
}

export const useUserStore = create<UserState>((set) => ({
  isLoggedIn: false,
  setIsLoggedIn: (v) => set({ isLoggedIn: v }),
}));

