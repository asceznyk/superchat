import api, { unwrap } from '@/api/setup'
import { CHAT_CONFIG } from '@/config/chat'

export const createThreadId = async () => unwrap(
  api.post('/threads/', null, { withCredentials: true })
)

export const getUserThreads = async () => unwrap(
  api.get('/threads/', null, { withCredentials: true })
)

export const renameThread = async (threadId:string, title:string) => unwrap(
  api.post(
    `/threads/rename/${threadId}`,
    {
      thread_title: title
    },
    { withCredentials: true }
  )
)

export const deleteThread = async (threadId:string) => unwrap(
  api.post(`/threads/delete/${threadId}`, null, { withCredentials: true })
)

