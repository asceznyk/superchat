import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import { getChatHistory } from '@/api/chat-service'
import { useChatStore } from '@/store/chat-store'

import { ChatHeader, ChatWindow, ChatFooter } from '@/components/chat-layout'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/sidebar'

export default function ChatPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const headerHeight = 80;
  const [footerHeight, setFooterHeight] = useState(headerHeight);
  const { cid } = useParams();
  const chatId = useChatStore(s => s.chatId);
  const setChatId = useChatStore(s => s.setChatId);
  const setMessageHistory = useChatStore(s => s.setMessageHistory);
  useEffect(() => {
    if (cid == chatId) return;
    const run = async () => {
      setChatId(cid);
      let history = await getChatHistory(cid);
      console.log(history);
      setMessageHistory(history);
    }
    run();
  }, [cid]);
  return (
    <div className="relative flex flex-col md:flex-row h-full w-full overflow-hidden">
      {isLoggedIn && (
        <div className="flex md:w-auto w-full">
          <SidebarProvider defaultOpen={false}>
            <AppSidebar />
            <main>
              <SidebarTrigger />
            </main>
          </SidebarProvider>
        </div>
      )}
      <div className="flex flex-col flex-grow w-full">
        <ChatHeader isLoggedIn={isLoggedIn} />
        <ChatWindow headerHeight={headerHeight} footerHeight={footerHeight}/>
        <ChatFooter onHeightChange={setFooterHeight}/>
      </div>
    </div>
  );
}

