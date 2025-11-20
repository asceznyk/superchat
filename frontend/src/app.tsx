import './app.css'
import { useState } from 'react';
import { ChatHeader, ChatWindow, ChatFooter } from '@/components/chat-layout'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/sidebar'

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [footerHeight, setFooterHeight] = useState(80);
  const headerHeight = 80;
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


