import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownMessageProps {
  text: string;
}

export function MarkdownMessage({ text }: MarkdownMessageProps) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ node, ...props }) => (
          <h1 className="text-3xl font-bold mt-3 mb-4" {...props} />
        ),
        h2: ({ node, ...props }) => (
          <h2 className="text-2xl font-semibold mt-3 mb-4" {...props} />
        ),
        h3: ({ node, ...props }) => (
          <h3 className="text-xl font-semibold mt-3 mb-4" {...props} />
        ),
        blockquote: ({ node, ...props }) => (
          <blockquote
            className="border-l-4 border-gray-600 pl-4 mt-0 mx-2 mb-4 italic text-gray-300"
            {...props}
          />
        ),
        p: ({ node, ...props }) => (
          <p className="mt-0 mx-2 mb-4 leading-relaxed" {...props} />
        ),
        ul: ({ node, ...props }) => (
          <ul className="list-disc ml-6 mt-0 mb-4" {...props} />
        ),
        ol: ({ node, ...props }) => (
          <ol className="list-decimal ml-6 mt-0 mb-4" {...props} />
        ),
        li: ({ node, ...props }) => (
          <li className="my-0" {...props} />
        ),
        table: ({ node, ...props }) => (
          <table className="w-full border-collapse my-2 text-left" {...props} />
        ),
        th: ({ node, ...props }) => (
          <th
            className="border border-gray-500 px-2 py-1 bg-gray-800 font-semibold"
            {...props}
          />
        ),
        td: ({ node, ...props }) => (
          <td className="border border-gray-700 px-2 py-1" {...props} />
        ),
        pre: ({node, ...props}) => (
          <pre className="mx-2 my-4" {...props}/>
        )
      }}
    >
      {text}
    </ReactMarkdown>
  );
}

