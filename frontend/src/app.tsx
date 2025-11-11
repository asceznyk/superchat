import './app.css'
import { useState } from 'react';
import { ChatHeader, ChatWindow } from '@/components/container'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/sidebar'

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
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
        <ChatWindow />
      </div>
    </div>
  );
}


