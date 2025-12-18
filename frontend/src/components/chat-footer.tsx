import { useState, useRef, useEffect } from "react"
import { useSendChat } from "@/hooks/use-send-chat"
import { useChatStore } from "@/store/chat-store"

import { ArrowUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ErrorAlert } from "@/components/error-alert"

interface PromptAreaProps {
  placeholder: string;
  onHeightChange?: (h: number) => void;
  onEnter? : () => void;
}

function PromptArea(
  { placeholder, onHeightChange, onSend }: PromptAreaProps
) {
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
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (userInput.trim().length === 0) return;
      onSend();
    }
  };
  const classSpan = `
    absolute top-2 text-gray-500 pointer-events-none select-none
  `;
  return (
    <div className="relative flex-grow min-h-10 px-2 py-2 w-full">
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
        onKeyDown={handleKeyDown}
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

interface SendButtonProps {
  onSend?: () => void;
  onStop?: () => void;
}

function SendButton({ onSend, onStop }: SendButtonProps) {
  const isStreaming = useChatStore((s) => s.isStreaming);
  return (
    <div className="flex items-end">
      {
        isStreaming ? (
          <Button
            className="rounded-full cursor-pointer h-10 w-10 p-0 ml-2"
            onClick={onStop}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 10 10"
              fill="currentColor"
            >
              <rect x="0" y="0" width="10" rx="3" height="10"></rect>
            </svg>
          </Button>
        ) : (
          <Button
            className="rounded-full cursor-pointer h-10 w-10 p-0 ml-2"
            onClick={onSend}
          >
            <ArrowUp />
          </Button>
        )
      }
    </div>
  );
}

interface ChatFooterProps {
  onHeightChange?: (h: number) => void;
}

export function ChatFooter({onHeightChange}: ChatFooterProps) {
  const [inputHeight, setInputHeight] = useState(40);
  const footerRef = useRef<HTMLDivElement>(null);
  const error = useChatStore((s) => s.error);
  const setError = useChatStore((s) => s.setError);
  const classTextarea = `
    flex justify-between items-end border border-solid border-gray-300
    gap-2
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
  const { streamMsg, stopMsg } = useSendChat();
  const handleSend = streamMsg;
  const handleStop = stopMsg;
  return (
    <div
      ref={footerRef}
      className="flex flex-col w-full fixed bottom-0 bg-background"
    >
      <div className="w-full max-w-[700px] mx-auto">
        {
          error && (
            <ErrorAlert
              message={error.message}
              onClose={() => setError(null)}
            />
          )
        }
        <div className="flex flex-col mb-[4px] px-4 w-full">
          <div
            className={
              `${classTextarea} ${inputHeight > 40 ? "rounded-md" : "rounded-full"}`
            }
          >
            <PromptArea
              placeholder="Ask anything..."
              onHeightChange={setInputHeight}
              onSend={handleSend}
            />
            <SendButton onSend={handleSend} onStop={handleStop} />
          </div>
        </div>
        <div className="flex justify-center mb-[4px]">
          <span className="text-xs">
            Superchat is a LLM wrapper - it can make mistakes
          </span>
        </div>
      </div>
    </div>
  );
}

