import { useState } from 'react';

import { ChatHeader } from '@/components/chat-header'
import { ChatWindow } from '@/components/chat-window'
import { ChatFooter } from '@/components/chat-footer'

export default function ChatLayout({ isLoggedIn }) {
  const headerHeight = 80;
  const [footerHeight, setFooterHeight] = useState(headerHeight);
  return (
    <div className="flex flex-col flex-grow w-full">
      <ChatHeader isLoggedIn={isLoggedIn} />
      <ChatWindow headerHeight={headerHeight} footerHeight={footerHeight}/>
      <ChatFooter onHeightChange={setFooterHeight}/>
    </div>
  )
}


