import './app.css'
import { ChatHeader, ChatWindow } from '@/components/container'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '@/components/sidebar'
import { ThemeProvider } from '@/components/theme-provider'

function App() {
  return (
    <ThemeProvider>
      <div class="relative flex h-full w-full flex-row">
        <div class="flex">
          <SidebarProvider defaultOpen={false}>
            <AppSidebar/>
            <main>
              <SidebarTrigger/>
            </main>
          </SidebarProvider>
        </div>
        <div class="flex-grow flex-col">
          <ChatHeader/>
          <ChatWindow/>
        </div>
      </div>
    </ThemeProvider>
  )
}

export default App
