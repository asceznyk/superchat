import { create } from "zustand";

interface ThreadLabel {
  id: string
  title: string
}

const initialState = {
  isLoggedIn: false,
  name: "",
  email: "",
  threadHistory: [] as ThreadLabel[],
}

type UserState = typeof initialState & {
  isLoggedIn: boolean;
  setIsLoggedIn: (v: boolean) => void;
  name: string;
  setName: (v: string) => void;
  email: string;
  setEmail: (v: string) => void;
  threadHistory: ThreadLabel[];
  setThreadHistory: (threads: ThreadLabel[]) => void;
  reset: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  ...initialState,
  setIsLoggedIn: (v) => set({ isLoggedIn: v }),
  setName: (v) => set({ name: v }),
  setEmail: (v) => set({ email: v }),
  setThreadHistory: (threads) =>
    set({
      threadHistory: threads.map((item) => ({
        id: item.id,
        title: item.thread_title,
        pinned: item.is_pinned
      })),
    }),
  reset: () => set(() => initialState),
}));

