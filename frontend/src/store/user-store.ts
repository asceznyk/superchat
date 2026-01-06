import { create } from "zustand";

interface ChatLabel {
  label: string;
}

const initialState = {
  isLoggedIn: false,
  name: "",
  email: "",
  chatHistory: [] as ChatLabel[],
}

type UserState = typeof initialState & {
  isLoggedIn: boolean;
  setIsLoggedIn: (v: boolean) => void;
  name: string;
  setName: (v: string) => void;
  email: string;
  setEmail: (v: string) => void;
  chatHistory: ChatLabel[];
  reset: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  ...initialState,
  setIsLoggedIn: (v) => set({ isLoggedIn: v }),
  setName: (v) => set({ name: v }),
  setEmail: (v) => set({ email: v }),
  reset: () => set(() => initialState),
}));

