import { useRef, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useUserStore } from '@/store/user-store'
import { useThreadStore } from '@/store/thread-store'

import { getUserThreads, renameThread, deleteThread } from '@/api/threads'

import {
  MessageCirclePlus, Menu
} from 'lucide-react'

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader
} from '@/components/ui/sidebar'

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu"

import { MoreHorizontal } from "lucide-react"

export function AppSidebar() {
  const threadHistory = useUserStore(s => s.threadHistory)
  const setThreadHistory = useUserStore(s => s.setThreadHistory)
  const setStartThread = useThreadStore(s => s.setStartThread)
  const navigate = useNavigate()
  const [renamingId, setRenamingId] = useState<string | null>(null)
  const [draftTitle, setDraftTitle] = useState("")
  const inputRef = useRef<HTMLInputElement>(null)
  //const catchThreads = useUserStore.getState().threadHistory;
  const handleClickThread = async (threadId:string) => {
    setStartThread(false)
    if (!threadId) {
      navigate('/chat')
      return
    }
    navigate(`/chat/${threadId}`)
  }
  const handleClickDelete = async (threadId:string) => {
    setStartThread(false)
    await deleteThread(threadId)
    navigate('/chat')
    setThreadHistory(await getUserThreads())
  }
  const handleClickRename = async (threadId:string, title:string) => {
    setRenamingId(threadId)
    setDraftTitle(title)
  }
  const commitRename = (id:string, title:string) => {
    const mapped = threadHistory.map(({ id, title, pinned }) => ({
      id,
      thread_title: title,
      is_pinned: pinned,
    }));
    setThreadHistory(
      mapped.map(t =>
        t.id === id
          ? { ...t, thread_title: title.trim() || t.thread_title }
          : t
      )
    );
    setRenamingId(null);
    renameThread(id, title).catch(() => {});
  };
  const cancelRename = () => {
    setRenamingId(null);
    setDraftTitle("");
  };
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
                  onClick={() => handleClickThread()}
                >
                  <a>
                    <MessageCirclePlus />
                    <span>New Chat</span>
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
          <SidebarGroupContent className="overflow-y-auto">
            <SidebarMenu>
              {threadHistory.map(item => (
                <SidebarMenuItem
                  key={item.id} className="
                  group rounded-md dark:hover:bg-sidebar-accent
                  cursor-pointer
                  "
                >
                  <div className="flex items-center justify-between w-full">
                    <SidebarMenuButton
                      asChild
                      onClick={() => handleClickThread(item.id)}
                      className="
                      flex-1 text-left
                      dark:hover:bg-transparent
                      "
                    >
                      <a>
                        {renamingId === item.id ? (
                          <input
                            ref={inputRef}
                            defaultValue={item.title}
                            className="
                              w-full bg-transparent outline-none
                              text-sm
                            "
                            autoFocus
                            onMouseDown={e => e.stopPropagation()}
                            onFocus={e => e.currentTarget.select()}
                            onClick={e => e.stopPropagation()}
                            onKeyDown={e => {
                              if (e.key === "Enter") {
                                commitRename(item.id, e.currentTarget.value)
                              }
                              if (e.key === "Escape") {
                                cancelRename()
                              }
                            }}
                          />
                          ) : (
                          <span className="truncate">{item.title}</span>
                        )}
                      </a>
                    </SidebarMenuButton>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <button
                          className="
                            ml-1 p-2 rounded
                            hover:bg-muted
                            dark:hover:bg-transparent
                            cursor-pointer
                          "
                          onClick={e => e.stopPropagation()}
                        >
                          <MoreHorizontal className="h-4 w-4" />
                        </button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          className="cursor-pointer"
                          onClick={() => handleClickRename(item.id, item.title)}
                        >
                          Rename
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          className="text-destructive cursor-pointer"
                          onClick={() => handleClickDelete(item.id)}
                        >
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}


