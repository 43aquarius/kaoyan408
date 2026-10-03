"use client";

import { useCallback, useRef, useState } from "react";
import { Check, Copy, Terminal } from "lucide-react";
import { useTheme } from "next-themes";
import { useMounted } from "@/lib/client";
import PrismAsyncLight from "react-syntax-highlighter/dist/esm/prism-async-light";
import c from "react-syntax-highlighter/dist/esm/languages/prism/c";
import cpp from "react-syntax-highlighter/dist/esm/languages/prism/cpp";
import java from "react-syntax-highlighter/dist/esm/languages/prism/java";
import python from "react-syntax-highlighter/dist/esm/languages/prism/python";
import javascript from "react-syntax-highlighter/dist/esm/languages/prism/javascript";
import oneDark from "react-syntax-highlighter/dist/esm/styles/prism/one-dark";
import oneLight from "react-syntax-highlighter/dist/esm/styles/prism/one-light";

PrismAsyncLight.registerLanguage("c", c);
PrismAsyncLight.registerLanguage("cpp", cpp);
PrismAsyncLight.registerLanguage("c++", cpp);
PrismAsyncLight.registerLanguage("java", java);
PrismAsyncLight.registerLanguage("python", python);
PrismAsyncLight.registerLanguage("javascript", javascript);
PrismAsyncLight.registerLanguage("js", javascript);

const LANG_LABEL: Record<string, string> = {
  c: "C",
  cpp: "C++",
  "c++": "C++",
  java: "Java",
  python: "Python",
  javascript: "JavaScript",
  js: "JavaScript",
  text: "Text",
  txt: "Text",
};

interface CodeBlockProps {
  code: string;
  language?: string;
}

/** copy-flash 代码块：复制时按钮缩放闪烁 + 外圈绿色光环扩散 */
export function CodeBlock({ code, language = "text" }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);
  const [flashing, setFlashing] = useState(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const { resolvedTheme } = useTheme();
  const mounted = useMounted();

  const onCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = code;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
      } catch {
        /* ignore */
      }
      document.body.removeChild(ta);
    }
    setCopied(true);
    setFlashing(true);
    if (timer.current) clearTimeout(timer.current);
    timer.current = setTimeout(() => {
      setCopied(false);
      setFlashing(false);
    }, 1400);
  }, [code]);

  const lang = LANG_LABEL[language?.toLowerCase()] ?? language?.toUpperCase() ?? "TEXT";
  const isKnown =
    ["c", "cpp", "c++", "java", "python", "javascript", "js"].includes(
      language?.toLowerCase()
    );
  const style = mounted && resolvedTheme === "dark" ? oneDark : oneLight;

  return (
    <div
      className={`code-block group relative my-1 overflow-hidden rounded-lg border bg-card ${
        flashing ? "code-flash" : ""
      }`}
    >
      <div className="flex items-center justify-between border-b bg-muted/40 py-1 pl-3 pr-1.5">
        <span className="flex items-center gap-1.5 text-[11px] font-medium tracking-wide text-muted-foreground">
          <Terminal className="h-3 w-3" />
          {lang}
        </span>
        <button
          onClick={onCopy}
          aria-label={copied ? "已复制" : "复制代码"}
          className={`copy-btn-flash inline-flex h-6 items-center gap-1 rounded-md border bg-background/80 px-2 text-[11px] font-medium transition-colors hover:border-primary/40 hover:text-primary ${
            copied ? "text-primary" : "text-muted-foreground"
          }`}
        >
          {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
          {copied ? "已复制" : "复制"}
        </button>
      </div>
      {isKnown ? (
        <PrismAsyncLight
          language={language}
          style={style}
          customStyle={{
            margin: 0,
            padding: "0.85rem 1rem",
            background: "transparent",
            fontSize: "0.8rem",
            lineHeight: 1.7,
          }}
          codeTagProps={{ style: { fontFamily: "var(--font-mono)" } }}
        >
          {code}
        </PrismAsyncLight>
      ) : (
        <pre className="overflow-x-auto p-3.5 text-[0.8rem] leading-relaxed">
          <code className="font-mono">{code}</code>
        </pre>
      )}
    </div>
  );
}
