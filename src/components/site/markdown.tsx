"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { CodeBlock } from "./code-block";

interface MarkdownProps {
  content: string;
  className?: string;
}

/** 题干/解析 Markdown 渲染器（GFM 表格 + copy-flash 代码块） */
export function Markdown({ content, className = "" }: MarkdownProps) {
  return (
    <div className={`md-body ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code(props) {
            const { children, className: cls, node, ...rest } = props;
            const match = /language-(\w+)/.exec(cls ?? "");
            const text = String(children ?? "").replace(/\n$/, "");
            const isBlock = match || text.includes("\n") || node?.position?.start.line !== node?.position?.end.line;
            if (isBlock) {
              return <CodeBlock code={text} language={match?.[1] ?? "text"} />;
            }
            return (
              <code className={cls} {...rest}>
                {children}
              </code>
            );
          },
          pre(props) {
            // pre 交由内部 CodeBlock 自己渲染，避免双重包裹
            return <>{props.children}</>;
          },
          a(props) {
            const { href, children } = props;
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary underline underline-offset-2 hover:opacity-80"
              >
                {children}
              </a>
            );
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
