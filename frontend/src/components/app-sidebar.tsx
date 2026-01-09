import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import { useUserStore } from '@/store/user-store'

import { getUserThreads } from '@/api/auth'

import {
  MessageCirclePlus, Menu
} from 'lucide-react'

import {
  Sidebar,
  SidebarTrigger,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader
} from '@/components/ui/sidebar'

export function AppSidebar() {
  const threadHistory = useUserStore(s => s.threadHistory)
  const setThreadHistory = useUserStore(s => s.setThreadHistory)
  const navigate = useNavigate()
  const handleClick = async (threadId:string) => {
    if (!threadId) {
      navigate('/chat')
      return
    }
    navigate(`/chat/${threadId}`)
  }
  useEffect(() => {
    (async () => {
      setThreadHistory(await getUserThreads())
    })()
  }, [])
  return (
    <Sidebar className="border-none">
      <SidebarHeader className="py-3">
        <SidebarGroup className="p-0">
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton
                  className="cursor-pointer h-9"
                  asChild
                  onClick={() => handleClick()}
                >
                  <a>
                    <MessageCirclePlus />
                    <span>Start Chat</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>History</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {threadHistory.map(item => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton
                    className="cursor-pointer"
                    asChild
                    onClick={() => handleClick(item.id)}
                  >
                    <a><span>{item.title}</span></a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}



