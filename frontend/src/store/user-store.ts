import { create } from "zustand";

interface ChatLabel {
  label: string;
}

interface UserState {
  isLoggedIn: boolean;
  setIsLoggedIn: (v: boolean) => void;
  name: string;
  setName: (v: string) => void;
  email: string;
  setEmail: (v: string) => void;
  chatHistory: ChatLabel[];
}

export const useUserStore = create<UserState>((set) => ({
  isLoggedIn: false,
  setIsLoggedIn: (v) => set({ isLoggedIn: v }),
  name: "",
  setName: (v) => set({ name: v }),
  email: "",
  setEmail: (v) => set({ email: v })
}));

