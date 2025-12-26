import { useEffect } from 'react';

import { getUserProfile } from '@/api/auth'
import { useUserStore } from '@/store/user-store'

import { Button } from "@/components/ui/button"
import { AuthDialog } from "@/components/auth-dialog"

//import { TypographyH4 } from "@/components/ui/typography"

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
  const headerClass = `
  flex fixed top-0 w-full items-center justify-between
  py-3 px-4 bg-background border-b border-border
  `;
  const buttonClass = `
  rounded-full cursor-pointer px-4 py-2 text-sm sm:text-base
  `;
  const isLoggedIn = useUserStore(s => s.isLoggedIn)
  const name = useUserStore(s => s.name)
  const setIsLoggedIn = useUserStore(s => s.setIsLoggedIn)
  const setName = useUserStore(s => s.setName)
  useEffect(() => {
    (async () => {
      const profile = await getUserProfile();
      if (!profile) return;
      setIsLoggedIn(true);
      setName(profile.name);
    })();
  }, []);
  return (
    <div className={headerClass}>
      <TypographyH3Link text="Superchat" />
        <div className="flex gap-2">
        {isLoggedIn ?
          (
            <UserProfile name={name} />
          )
        : (
            <AuthDialog text="Login or Register" />
        )}
        </div>
    </div>
  );
}

