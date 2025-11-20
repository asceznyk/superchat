import { useState, useRef, useEffect } from "react";
import { ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";

interface TypographyH3LinkProps {
  text: string;
}

function TypographyH3Link({ text }: TypographyH3LinkProps) {
  return (
    <h3 className="text-2xl font-semibold">
      <a href="/" className="text-blue-600">{text}</a>
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

interface ChatWindowProps {
  headerHeight: number;
  footerHeight: number;
}

export function ChatWindow(
  {headerHeight, footerHeight}: ChatWindowProps
) {
  const messages = ['Hi', 'Hello', 'Yes', 'No', 'Maybe!', 'This', 'is', 'good', 'stuff'];
  return (
    <div
      className="flex-1 overflow-y-auto px-4"
      style={{
        marginTop: headerHeight,
        marginBottom: footerHeight + 20
      }}
    >
      {messages.map((m, i) => (
        <div
          key={i}
          className="max-w-min bg-blue-600 text-white p-3 rounded-xl ml-auto mb-4"
        >
          {m}
        </div>
      ))}
    </div>
  );
}

interface PromptAreaProps {
  placeholder: string;
  onHeightChange?: (h: number) => void;
}

function PromptArea({ placeholder, onHeightChange }: PromptAreaProps) {
  const [inputValue, setInputValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  useEffect(() => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = `${el.scrollHeight}px`;
      onHeightChange?.(el.scrollHeight);
    }
  }, [inputValue]);
  const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(event.target.value);
  };
  const classSpan = `
    absolute top-2 text-gray-500 pointer-events-none select-none
  `;
  return (
    <div className="relative flex-grow min-h-10 px-2 py-2">
      {inputValue.length === 0 && (
        <span
          className={classSpan}
          data-placeholder={placeholder}
        >
          {placeholder}
        </span>
      )}
      <textarea
        ref={textareaRef}
        value={inputValue}
        onChange={handleInput}
        className="
          block w-full resize-none
          bg-transparent outline-none
          text-base text-foreground
          placeholder-transparent
          max-h-[200px] overflow-y-auto
          hide-scrollbar
        "
        rows={1}
        tabIndex={0}
      />
    </div>
  );
}

function SendButton() {
  return (
    <div className="flex items-end">
      <Button
        className="rounded-full cursor-pointer h-10 w-10 p-0 ml-2"
      >
        <ArrowUp />
      </Button>
    </div>
  );
}

interface ChatFooterProps {
  onHeightChange?: (h: number) => void;
}

export function ChatFooter({onHeightChange}: ChatFooterProps) {
  const [inputHeight, setInputHeight] = useState(40);
  const footerRef = useRef<HTMLDivElement>(null);
  const classTextarea = `
    flex justify-between items-end border border-solid border-gray-300
    w-full max-w-[700px] mx-auto gap-2
    py-2 px-2
  `;
  useEffect(() => {
    const el = footerRef.current;
    if (!el) return;
    const observer = new ResizeObserver(() => {
      onHeightChange?.(el.offsetHeight);
    });
    observer.observe(el);
    return () => observer.disconnect();
  }, []);
  return (
    <div
      ref={footerRef}
      className="flex fixed bottom-0 bg-background flex-col w-full px-4"
    >
      <div className="flex">
        <div
          className={
            `${classTextarea} ${inputHeight > 40 ? "rounded-md" : "rounded-full"}`
          }
        >
          <PromptArea
            placeholder="Ask anything..."
            onHeightChange={setInputHeight}
          />
          <SendButton />
        </div>
      </div>
      <div className="flex justify-center">
        <span className="text-sm sm:text-base">
          Superchat is a ChatGPT wrapper - it can make mistakes
        </span>
      </div>
    </div>
  );
}


