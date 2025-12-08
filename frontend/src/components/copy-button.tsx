import { useState } from "react"

import { Check, Copy } from "lucide-react"

interface CopyButtonProps {
  text: string
  isCode: boolean
}

export default function CopyButton({ text, isCode, pos }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1200);
  };
  const defaultClass = `
    cursor-pointer
    opacity-0 group-hover:opacity-100
    transition-opacity
  `;
  const codeClass = `
    absolute top-2
    bg-gray-800 hover:bg-gray-700 text-gray-300
    p-1 rounded
  `;
  const bubbleClass = "";
  return (
    <button
      onClick={handleCopy}
      className={defaultClass + (isCode ? codeClass : bubbleClass)}
    >
      {copied ? <Check size={16} /> : <Copy size={16} />}
    </button>
  );
}
