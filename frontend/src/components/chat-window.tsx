import { useRef, useEffect } from "react"
import { useChatStore } from "@/store/chat-store"

import MarkdownMessage from "@/components/markdown-message"
import TypingIndicator from "@/components/typing-indicator"
import CopyButton from "@/components/copy-button"

export function ChatWindow() {
  const messageHistory = useChatStore((s) => s.messageHistory);
  const hasResponded = useChatStore((s) => s.hasResponded);
  const containerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    el.scrollTo({
      top: el.scrollHeight,
      behavior: "smooth",
    });
  }, [messageHistory]);
  const defaultClass = "group mb-4 ";
  const userDivClass = "ml-auto w-fit max-w-[85%]";
  const userBubbleClass = `
    break-words whitespace-pre-wrap bg-gray-600
    text-white p-3 rounded-xl mb-[10px]
  `;
  const assistantBubbleClass = `
    w-fit break-words whitespace-normal max-w-[100%]
    text-white mr-auto mb-[10px]
  `;
  const lastChildPTagClass = "[&>p:last-child]:mb-0";
  return (
    <div
      ref={containerRef}
      className="overflow-y-auto px-4 w-full h-full max-w-[750px] mx-auto my-4"
    >
      <div>
      {messageHistory.map((m, i) => (
        <div
          key={m.id}
          className={defaultClass + (m.role === "user" ? userDivClass:"")}
        >
          <div
            className={
              lastChildPTagClass +
              (m.role === "user" ? userBubbleClass : assistantBubbleClass)
            }
          >
            {
              !hasResponded
                && m.role === "assistant"
                && i === (messageHistory.length-1) ?
              (
                <TypingIndicator />
              ) : (
                <MarkdownMessage text={m.msgContent} />
              )
            }
          </div>
            {
              (hasResponded || m.role === "user") && (
                <CopyButton text={m.msgContent} />
              )
            }
        </div>
      ))}
      </div>
    </div>
  );
}

