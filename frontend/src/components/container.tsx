import { useState } from "react";
import { Button } from "@/components/ui/button";

interface PromptAreaProps {
  placeholder: string;
}

interface TypographyH3LinkProps {
  text: string;
}

interface ChatHeaderProps {
  isLoggedIn: boolean;
}

function TypographyH3Link({text}: TypographyH3LinkProps) {
  return (
    <h3 className="scroll-m-20 text-2xl font-semibold">
      <a href='/'>{text}</a>
    </h3>
  );
}

function PromptArea({placeholder}: PromptAreaProps) {
  const [inputValue, setInputValue] = useState('');
  function handleInput(event) {
    setInputValue(event.target.innerText);
  }
  const classSpan:string = `whitespace-pre-wrap outline-none
                            cursor-text after:text-gray-500
                            pointer-events-auto`;
  return (
    <div
      id="prompt-text-area"
      className="w-90 min-h-10 whitespace-pre-wrap
      break-words resize-none overflow-y-auto outline-none
      border-1 border-solid rounded-sm px-2 py-2"
    >
      <span
        className={
          (inputValue.trim().length <= 0)
            ? `${classSpan} placeholder`
            : classSpan
        }
        contentEditable
        onInput={handleInput}
        data-placeholder={placeholder}
        tabIndex={0}
      >
      </span>
    </div>
  );
}


export function ChatHeader({isLoggedIn}: ChatHeaderProps) {
  return (
    <div className="flex w-full py-2 px-4 bg-background">
      <div className="flex min-w-30">
        <TypographyH3Link text="Superchat" />
      </div>
      <div className="flex flex-1" />
      {!isLoggedIn && (
        <div className="flex min-w-20 justify-end gap-2">
          <Button className="rounded-full">Login</Button>
          <Button className="rounded-full">Signup</Button>
        </div>
      )}
    </div>
  );
}

export function ChatWindow() {
  return (
    <div className="flex mx-auto px-4 flex-col">
      <div className="flex justify-center min-h-30">
        <div className="flex mb-16 mt-16">
          <p className="text-2xl text-center">
            How can I help you today?
          </p>
        </div>
      </div>
      <div className="flex justify-center min-w-70">
        <div className="flex">
          <PromptArea placeholder="Ask anything"/>
        </div>
      </div>
    </div>
  );
}

