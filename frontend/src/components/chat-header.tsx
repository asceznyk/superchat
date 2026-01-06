import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

import { useUserStore } from '@/store/user-store'
import { useChatStore } from '@/store/chat-store'

import { performLogout } from '@/services/auth'
import { getUserProfile, logoutUser } from '@/api/auth'

import { Button } from "@/components/ui/button"
import { AuthDialog } from "@/components/auth-dialog"

function TypographyH3Link({ text }: { text: string }) {
  return (
    <h3 className="text-2xl font-semibold">
      <a href="/">{text}</a>
    </h3>
  );
}

type UserProfileProps = {
  name: string
}

export function UserProfile({ name }: UserProfileProps) {
  return (
    <h4 className="font-medium">
      {name}
    </h4>
  )
}

export function ChatHeader() {
  const baseHeader = `
  flex fixed top-0 w-full items-center justify-between
  py-3 px-4 bg-background border-b border-border
  `;
  const baseBtn = `rounded-full cursor-pointer`;
  const isLoggedIn = useUserStore(s => s.isLoggedIn)
  const setIsLoggedIn = useUserStore(s => s.setIsLoggedIn)
  const navigate = useNavigate()
  const handleClickLogout = async () => {
    performLogout()
    navigate('/')
  }
  useEffect(() => {
    (async () => {
      const profile = await getUserProfile()
      if (!profile) return;
      setIsLoggedIn(true)
    })();
  }, []);
  return (
    <div className={baseHeader}>
      <TypographyH3Link text="Superchat" />
        <div className="flex gap-2">
        {isLoggedIn ?
          (
            <Button
              className={baseBtn}
              variant="outline"
              onClick={handleClickLogout}
            >
              Logout
            </Button>
          )
        : (
            <AuthDialog text="Login or Register" />
        )}
        </div>
    </div>
  );
}

