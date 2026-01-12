import { getUserProfile, logoutUser } from '@/api/auth'
import { useUserStore } from '@/store/user-store'
import { useThreadStore } from '@/store/thread-store'

export async function performLogout() {
  try {
    await logoutUser()
  } finally {
    useUserStore.getState().reset()
    useThreadStore.getState().reset()
  }
}

