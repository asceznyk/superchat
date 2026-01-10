import { useEffect } from 'react'

import ChatLayout from '@/components/chat-layout'

export default function ChatPage() {
  return (
    <div className="relative flex flex-row h-screen w-screen overflow-hidden">
      <ChatLayout />
    </div>
  );
}

