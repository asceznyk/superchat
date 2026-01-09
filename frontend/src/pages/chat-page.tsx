import { useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { getChatHistory } from '@/api/chat'
import { getUserProfile } from '@/api/auth'
import { useUserStore } from '@/store/user-store'
import { useChatStore } from '@/store/chat-store'

import ChatLayout from '@/components/chat-layout'
import { Button } from '@/components/ui/button'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/app-sidebar'

export default function ChatPage() {
  let { cid } = useParams();
  const isLoggedIn = useUserStore(s => s.isLoggedIn)
  const chatId = useChatStore(s => s.chatId)
  const setChatId = useChatStore(s => s.setChatId)
  const setMessageHistory = useChatStore(s => s.setMessageHistory)
  useEffect(() => {
    if (cid === chatId) return;
    (async () => {
      setChatId(cid)
      if (!cid) {
        setMessageHistory([]);
        return;
      };
      setMessageHistory(await getChatHistory(cid))
    })();
  }, [cid]);
  return (
    <div className="relative flex flex-row h-screen w-screen overflow-hidden">
      {isLoggedIn && (
        <div className="flex shrink-0 h-full border-r">
          <SidebarProvider defaultOpen={false}>
            <AppSidebar />
              <div className="bg-sidebar">
                <div className="py-3 px-1">
                  <SidebarTrigger className="text-2xl font-semibold" />
                </div>
              </div>
          </SidebarProvider>
        </div>
      )}
      <ChatLayout />
    </div>
  );
}

