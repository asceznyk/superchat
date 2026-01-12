import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useUserStore } from '@/store/user-store'
import { useThreadStore } from '@/store/thread-store'

import { getMessageHistory } from '@/api/messages'

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
  const threadId = useThreadStore(s => s.threadId)
  const setThreadId = useThreadStore(s => s.setThreadId)
  const setMessageHistory = useThreadStore(s => s.setMessageHistory)
  useEffect(() => {
    if (cid === threadId) return;
    (async () => {
      setThreadId(cid)
      if (!cid) {
        setMessageHistory([]);
        return;
      };
      setMessageHistory(await getMessageHistory(cid))
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


