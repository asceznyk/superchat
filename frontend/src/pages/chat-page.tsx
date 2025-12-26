import { useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { getChatHistory } from '@/api/chat-service'
import { getUserProfile } from '@/api/auth'
import { useUserStore } from '@/store/user-store'
import { useChatStore } from '@/store/chat-store'

import ChatLayout from '@/components/chat-layout'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/sidebar'

export default function ChatPage() {
  const { cid } = useParams();
  const isLoggedIn = useUserStore(s => s.isLoggedIn)
  const chatId = useChatStore(s => s.chatId)
  const setChatId = useChatStore(s => s.setChatId)
  const setMessageHistory = useChatStore(s => s.setMessageHistory)
  useEffect(() => {
    if (!cid || cid === chatId) return;
    (async () => {
      setChatId(cid);
      const history = await getChatHistory(cid);
      setMessageHistory(history);
    })();
  }, [cid]);
  return (
    <div className="relative flex flex-col md:flex-row h-full w-full overflow-hidden">
      {/*isLoggedIn && (
        <div className="flex md:w-auto w-full">
          <SidebarProvider defaultOpen={false}>
            <AppSidebar />
            <main>
              <SidebarTrigger />
            </main>
          </SidebarProvider>
        </div>
      )*/}
      <ChatLayout />
    </div>
  );
}

