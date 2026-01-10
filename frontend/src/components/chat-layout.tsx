import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useUserStore } from '@/store/user-store'
import { useChatStore } from '@/store/chat-store'

import { getChatHistory } from '@/api/chat'

import { ChatHeader } from '@/components/chat-header'
import { ChatWindow } from '@/components/chat-window'
import { ChatFooter } from '@/components/chat-footer'

import { AppSidebar } from '@/components/app-sidebar'
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar'

export default function ChatLayout() {
  const headerHeight = 80;
  const [footerHeight, setFooterHeight] = useState(headerHeight);
  const { cid } = useParams()
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
      const history = await getChatHistory(cid)
      console.log(history)
      setMessageHistory(history)
    })();
  }, [cid]);
  return (
    <div className="flex flex-grow">
      {isLoggedIn ? (
        <SidebarProvider defaultOpen={false}>
          <AppSidebar />
          <SidebarInset>
            <ChatHeader />
            <ChatWindow />
            <ChatFooter onHeightChange={setFooterHeight}/>
          </SidebarInset>
        </SidebarProvider>
      ) : (
        <main className="flex flex-col flex-1">
          <ChatHeader />
          <ChatWindow />
          <ChatFooter onHeightChange={setFooterHeight} />
        </main>
      )}
    </div>
  )
}


