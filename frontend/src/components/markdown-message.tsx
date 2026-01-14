import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism"

import CopyButton from "@/components/copy-button"

interface CodeBlockProps {
  language: string
  code: string
}

function CodeBlock({ language, code }: CodeBlockProps) {
  return (
    <div
      className="
      relative my-4 group w-full
      break-all overflow-x-auto whitespace-pre-wrap
      "
    >
      <CopyButton text={code} isCode={true} />
      <SyntaxHighlighter
        language={language}
        style={oneDark}
        wrapLongLines
        customStyle={{
          borderRadius: "8px",
          padding: "12px",
          fontSize: "14px",
          maxWidth: "100%",
          overflowX: "auto",
          whiteSpace: "pre-wrap",
        }}
        codeTagProps={{
          style: {
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          },
        }}
      >
        {code.replace(/\n$/, "")}
      </SyntaxHighlighter>
    </div>
  );
}

interface MarkdownMessageProps {
  text: string
}

export default function MarkdownMessage({ text }: MarkdownMessageProps) {
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
            className="border-l-4 border-gray-600 pl-4 mt-0 mb-4 italic text-gray-300"
            {...props}
          />
        ),
        p: ({ node, ...props }) => (
          <p className="mt-0 mb-4 leading-relaxed" {...props} />
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
          <div className="overflow-x-auto min-w-0">
            <table
              className="w-full table-fixed border-collapse my-2 text-left"
              {...props}
            />
          </div>
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
        code({ inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || "");
          const text = String(children);
          const isMultiline = text.includes("\n");
          if (inline || !match) {
            return (
              <code className={
                isMultiline
                ? `
                  block w-full max-w-full
                  bg-gray-800 text-gray-100
                  px-2 py-2 rounded
                  overflow-x-auto
                  whitespace-pre-wrap
                  break-all
                `
                : `
                  inline
                  bg-gray-800 text-gray-100
                  px-1 py-0 rounded
                  break-all
                `
              }>
                {children}
              </code>
            );
          }
          return <CodeBlock language={match[1]} code={String(children)} />;
        },
        pre: ({node, ...props}) => (
          <pre className="my-4 w-full max-w-full overflow-x-auto" {...props}/>
        )
      }}
    >
      {text}
    </ReactMarkdown>
  );
}



