import { useState } from "react";
import { Button } from "@/components/ui/button";
import { ArrowUp } from "lucide-react";

interface PromptAreaProps {
  placeholder: string;
}

interface TypographyH3LinkProps {
  text: string;
}

interface ChatHeaderProps {
  isLoggedIn: boolean;
}

function TypographyH3Link({ text }: TypographyH3LinkProps) {
  return (
    <h3 className="scroll-m-20 text-2xl font-semibold">
      <a href="/">{text}</a>
    </h3>
  );
}

function PromptArea({ placeholder }: PromptAreaProps) {
  const [inputValue, setInputValue] = useState("");
  function handleInput(event: React.FormEvent<HTMLSpanElement>) {
    setInputValue(event.currentTarget.innerText);
  }
  const classSpan = `
    whitespace-pre-wrap outline-none
    cursor-text after:text-gray-500
    pointer-events-auto w-full
  `;
  return (
    <div
      id="user-prompt-textarea"
      className="flex-1 min-h-10 whitespace-pre-wrap
      break-words overflow-y-auto outline-none
      px-2 py-2"
    >
      <span
        className={
          inputValue.length <= 0
            ? `${classSpan} placeholder`
            : classSpan
        }
        contentEditable
        onInput={handleInput}
        data-placeholder={placeholder}
        tabIndex={0}
      />
    </div>
  );
}

function SendButtonArea() {
  return (
    <div className="flex items-end">
      <Button className="rounded-full cursor-pointer h-10 w-10 p-0 ml-2">
        <ArrowUp />
      </Button>
    </div>
  );
}

export function ChatHeader({ isLoggedIn }: ChatHeaderProps) {
  const headerClass = `
    flex w-full items-center justify-between
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

export function ChatWindow() {
  const classChatArea = `
    flex items-center justify-between
    border border-solid border-gray-300 rounded-full
    w-full max-w-[700px] mx-auto gap-2
    py-2 px-2 sm:px-4
  `;
  return (
    <div className="flex flex-col w-full px-2 sm:px-4">
      <div className="flex justify-center min-h-[120px] sm:min-h-[150px]">
        <div className="flex mb-8 mt-8 sm:mb-16 sm:mt-16">
          <p className="text-xl sm:text-2xl text-center">
            How can I help you today?
          </p>
        </div>
      </div>
      <div className={classChatArea}>
        <PromptArea placeholder="Ask anything..." />
        <SendButtonArea />
      </div>
    </div>
  );
}


