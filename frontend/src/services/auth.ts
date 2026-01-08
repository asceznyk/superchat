import { getUserProfile, logoutUser } from '@/api/auth'
import { useUserStore } from '@/store/user-store'
import { useChatStore } from '@/store/chat-store'

export async function performLogout() {
  try {
    await logoutUser()
  } finally {
    useUserStore.getState().reset()
    useChatStore.getState().reset()
  }
}

