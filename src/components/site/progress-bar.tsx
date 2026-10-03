"use client";

import { useEffect, useState } from "react";

/** 顶部阅读进度条：随窗口滚动增长 */
export function ReadingProgress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const el = document.documentElement;
        const total = el.scrollHeight - el.clientHeight;
        setProgress(total > 0 ? Math.min(100, (el.scrollTop / total) * 100) : 0);
      });
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div
      className="reading-progress-bar fixed left-0 top-0 z-[60] h-[3px] rounded-r-full"
      style={{ width: `${progress}%`, opacity: progress > 0.5 ? 1 : 0 }}
      role="progressbar"
      aria-label="阅读进度"
      aria-valuenow={Math.round(progress)}
      aria-valuemin={0}
      aria-valuemax={100}
    />
  );
}
