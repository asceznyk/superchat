import './app.css'
import { useState } from 'react';
import { ChatHeader, ChatWindow } from '@/components/container'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/sidebar'

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  return (
    <div className="relative flex h-full w-full flex-row">
      {isLoggedIn && (
        <div class="flex">
          <SidebarProvider defaultOpen={false}>
            <AppSidebar/>
            <main>
              <SidebarTrigger/>
            </main>
          </SidebarProvider>
        </div>
      )}
      <div className="flex-grow flex-col">
        <ChatHeader isLoggedIn={isLoggedIn}/>
        <ChatWindow/>
      </div>
    </div>
  )
}

