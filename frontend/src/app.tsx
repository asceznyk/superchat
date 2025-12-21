import './app.css'
import { useState } from 'react';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ChatPage from '@/pages/chat-page';
import { ThemeProvider } from '@/components/theme-provider';

export default function App() {
  return (
    <ThemeProvider defaultTheme="dark">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/chat/:cid" element={<ChatPage />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}


