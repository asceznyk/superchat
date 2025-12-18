import { Button } from "@/components/ui/button"

interface TypographyH3LinkProps {
text: string;
}

function TypographyH3Link({ text }: TypographyH3LinkProps) {
return (
  <h3 className="text-2xl font-semibold">
    <a href="/">{text}</a>
  </h3>
);
}

interface ChatHeaderProps {
isLoggedIn: boolean;
}

export function ChatHeader({ isLoggedIn }: ChatHeaderProps) {
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
        <Button className={buttonClass}>Login</Button>
        <Button className={buttonClass}>Signup</Button>
      </div>
    )}
  </div>
);
}

