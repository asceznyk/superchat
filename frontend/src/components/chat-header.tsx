import { Button } from "@/components/ui/button"
import { AuthDialog } from "@/components/auth-dialog"

function TypographyH3Link({ text }: { text: string }) {
  return (
    <h3 className="text-2xl font-semibold">
      <a href="/">{text}</a>
    </h3>
  );
}

export function ChatHeader({ isLoggedIn }: { isLoggedIn: boolean }) {
  const headerClass = `
  flex fixed top-0 w-full items-center justify-between
  py-3 px-4 bg-background border-b border-border
  `;
  const buttonClass = `
  rounded-full cursor-pointer px-4 py-2 text-sm sm:text-base
  `;
  return (
    <div className={headerClass}>
      <TypographyH3Link text="Superchat" />
      {!isLoggedIn && (
        <div className="flex gap-2">
          <AuthDialog text="Login or Register"/>
        </div>
      )}
    </div>
  );
}

