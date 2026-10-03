"use client";

import { useEffect, useState } from "react";

interface TypewriterProps {
  phrases: string[];
  typeSpeed?: number;
  deleteSpeed?: number;
  holdTime?: number;
  className?: string;
}

/** 打字机问候语：逐字打印 → 停顿 → 逐字删除 → 下一句 */
export function Typewriter({
  phrases,
  typeSpeed = 110,
  deleteSpeed = 45,
  holdTime = 1800,
  className,
}: TypewriterProps) {
  const [text, setText] = useState("");
  const [idx, setIdx] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const current = phrases[idx % phrases.length];
    const delay = deleting
      ? deleteSpeed
      : text === current
        ? holdTime
        : typeSpeed;

    const t = setTimeout(() => {
      if (!deleting && text === current) {
        setDeleting(true);
      } else if (deleting && text === "") {
        setDeleting(false);
        setIdx((i) => (i + 1) % phrases.length);
      } else if (deleting) {
        setText(current.slice(0, text.length - 1));
      } else {
        setText(current.slice(0, text.length + 1));
      }
    }, delay);
    return () => clearTimeout(t);
  }, [text, deleting, idx, phrases, typeSpeed, deleteSpeed, holdTime]);

  return (
    <span className={className} aria-label={phrases[0]}>
      {text}
      <span className="typewriter-caret" aria-hidden="true" />
    </span>
  );
}
