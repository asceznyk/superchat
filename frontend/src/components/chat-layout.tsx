import { useState, useRef, useEffect } from "react";
import { ArrowUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useChatStore } from "@/store/chat-store";

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
  const messageHistory = useChatStore((s) => s.messageHistory);
  return (
    <div
      className="flex-1 overflow-y-auto px-4"
      style={{
        marginTop: headerHeight,
        marginBottom: footerHeight + 20
      }}
    >
      <div className="max-w-[800px] mx-auto">
      {messageHistory.map((m) => (
        <div
          key={m.id}
          className="max-w-min bg-blue-600 text-white p-3 rounded-xl ml-auto mb-4"
        >
          {m.msg_body}
        </div>
      ))}
      </div>
    </div>
  );
}

interface PromptAreaProps {
  placeholder: string;
  onHeightChange?: (h: number) => void;
}

function PromptArea({ placeholder, onHeightChange }: PromptAreaProps) {
  const userInput = useChatStore((s) => s.userInput);
  const setUserInput = useChatStore((s) => s.setUserInput);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  useEffect(() => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = `${el.scrollHeight}px`;
      onHeightChange?.(el.scrollHeight);
    }
  }, [userInput]);
  const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = event.target.value;
    setUserInput(val);
  };
  const classSpan = `
    absolute top-2 text-gray-500 pointer-events-none select-none
  `;
  return (
    <div className="relative flex-grow min-h-10 px-2 py-2">
      {userInput.length === 0 && (
        <span
          className={classSpan}
          data-placeholder={placeholder}
        >
          {placeholder}
        </span>
      )}
      <textarea
        ref={textareaRef}
        value={userInput}
        onChange={handleInput}
        className="
          block w-full resize-none
          bg-transparent outline-none
          text-base text-foreground
          placeholder-transparent
          max-h-[200px] overflow-y-auto
        "
        rows={1}
        tabIndex={0}
      />
    </div>
  );
}

function SendButton() {
  const addMessage = useChatStore((s) => s.addMessage);
  const setUserInput = useChatStore((s) => s.setUserInput);
  const userInput = useChatStore((s) => s.userInput);
  const handleSend = () => {
    console.log("userInput - before: ", userInput);
    if (!userInput.trim()) return;
    addMessage({
      id: "some-random-id",
      role: "user",
      msg_body: userInput,
    });
    setUserInput("");
    console.log("userInput - after: ", userInput);
  };
  return (
    <div className="flex items-end">
      <Button
        className="rounded-full cursor-pointer h-10 w-10 p-0 ml-2"
        onClick={handleSend}
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
    w-full max-w-[800px] mx-auto gap-2
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
      <div className="flex mb-[4px]">
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
      <div className="flex justify-center mb-[4px]">
        <span className="text-sm">
          Superchat is a ChatGPT wrapper - it can make mistakes
        </span>
      </div>
    </div>
  );
}


