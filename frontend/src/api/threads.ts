import api, { unwrap } from '@/api/setup'
import { CHAT_CONFIG } from '@/config/chat'

export async function createThreadId() {
  const res = await api.post('/threads/', null, { withCredentials: true });
  return res.data.thread_id;
}

export const getUserThreads = () => unwrap(
  api.get('/threads/', null, { withCredentials: true })
)

