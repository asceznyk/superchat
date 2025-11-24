import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownMessageProps {
  text: string
}

export function MarkdownMessage({ text }: MarkdownMessageProps) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        table: ({node, ...props}) => (
          <table className="w-full border-collapse my-4" {...props} />
        ),
        th: ({node, ...props}) => (
          <th className="border border-gray-300 px-2 py-1 bg-gray-600 font-semibold" {...props} />
        ),
        td: ({node, ...props}) => (
          <td className="border border-gray-300 px-2 py-1" {...props} />
        ),
      }}
    >
      {text}
    </ReactMarkdown>
  );
}

