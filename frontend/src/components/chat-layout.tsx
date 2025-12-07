import { v4 as uuidv4 } from "uuid";
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { ArrowUp, Square } from "lucide-react";

import { useChatStore } from "@/store/chat-store";
import { streamChatResponse, createChatId } from "@/api/chat-service";

import { CHAT_CONFIG } from "@/config/chat"
import { Button } from "@/components/ui/button";
import MarkdownMessage from "@/components/markdown-message"
import TypingIndicator from "@/components/typing-indicator"

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

interface ChatWindowProps {
  headerHeight: number;
  footerHeight: number;
}

export function ChatWindow(
  {headerHeight, footerHeight}: ChatWindowProps
) {
  const messageHistory = useChatStore((s) => s.messageHistory);
  const hasResponded = useChatStore((s) => s.hasResponded);
  const containerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = containerRef.current;
    if (el) {
      el.scrollTo({
        top: el.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messageHistory]);
  const userBubbleClass = `
    w-fit break-words whitespace-pre-wrap max-w-[85%] bg-gray-600
    text-white p-3 rounded-xl ml-auto mb-4
  `;
  const assistantBubbleClass = `
    w-fit break-words whitespace-normal max-w-[100%]
    text-white p-3 mr-auto mb-4
  `;
  const lastChildPTagClass = "[&>p:last-child]:mb-0";
  return (
    <div
      ref={containerRef}
      className="overflow-y-auto px-4"
      style={{
        marginTop: headerHeight,
        marginBottom: footerHeight + 20,
        height: `calc(100vh - ${headerHeight + footerHeight + 20}px)`
      }}
    >
      <div
        className="max-w-[800px] mx-auto"
      >
      {messageHistory.map((m, i) => (
        <div
          key={m.id}
          className={
            lastChildPTagClass +
            (m.role === "user" ? userBubbleClass : assistantBubbleClass)
          }
        >
          {
            !hasResponded && m.role === "assistant" && i === (messageHistory.length-1) ?
            (
              <TypingIndicator />
            ) : (
              <MarkdownMessage text={m.msgBody} />
            )
          }
        </div>
      ))}
      </div>
    </div>
  );
}

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
              viewBox="0 0 12 12"
              fill="currentColor"
            >
              <rect x="0" y="0" width="12" rx="3" height="12"></rect>
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
  const userInput = useChatStore((s) => s.userInput);
  const setUserInput = useChatStore((s) => s.setUserInput);
  const chatId = useChatStore((s) => s.chatId);
  const setChatId = useChatStore((s) => s.setChatId);
  const addUserMessage = useChatStore((s) => s.addUserMessage);
  const addAssistantMessage = useChatStore((s) => s.addAssistantMessage);
  const addAssistantMsgChunk = useChatStore((s) => s.addAssistantMsgChunk);
  const messageHistory = useChatStore((s) => s.messageHistory);
  const setIsStreaming = useChatStore((s) => s.setIsStreaming);
  const abortController = useChatStore((s) => s.abortController);
  const setAbortController = useChatStore((s) => s.setAbortController);
  const hasResponded = useChatStore((s) => s.hasResponded);
  const setHasResponded = useChatStore((s) => s.setHasResponded);
  const navigate = useNavigate();
  const handleSend = async () => {
    if (!userInput.trim() || messageHistory.length >= CHAT_CONFIG.MAX_MESSAGES)
      return;
    let cid = chatId;
    if (!cid) {
      cid = await createChatId();
      setChatId(cid);
      navigate(`/chat/${cid}`);
    }
    setHasResponded(false);
    const ac = new AbortController();
    setAbortController(ac);
    addUserMessage({
      id: uuidv4(),
      role: "user",
      msgBody: userInput,
    });
    setUserInput("");
    addAssistantMessage({
      id: uuidv4(),
      role: "assistant",
      msg_body: "",
    });
    let reader, decoder;
    try {
      const res = await streamChatResponse(userInput, cid, ac.signal);
      reader = res.reader;
      decoder = res.decoder;
    } catch (err) {
      console.warn("Request aborted or failed", err);
      return;
    }
    try {
      setIsStreaming(true);
      let buffer = "";
      while (true) {
        const { value, done } = await reader.read();
        const chunk = decoder.decode(value, {stream: true});
        console.log(`chunk = ${chunk}`);
        if (chunk) setHasResponded(true);
        if (done) break;
        buffer += chunk;
        let lines = buffer.split(/\r?\n/);
        buffer = lines.pop()!
        for (let line of lines) {
          try {
            const obj = JSON.parse(line);
            addAssistantMsgChunk(obj);
          } catch(err) {
            console.warn("Couldn't parse line from backend", err);
            console.warn("line", line);
          }
        }
      }
      setIsStreaming(false);
    } catch(err) {
      console.error('error from server?', err);
    }
  };
  const handleStop = () => {
    abortController?.abort();
    setIsStreaming(false);
    setAbortController(null);
    return;
  }
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
  );
}


