"use client";

import { Database, Github, Heart } from "lucide-react";
import { YEARS, ALL_QUESTIONS } from "@/data/questions";
import { useApp } from "@/lib/store";

export function Footer() {
  const go = useApp((s) => s.go);
  const years = [...YEARS].sort((a, b) => a - b);

  return (
    <footer className="mt-auto border-t bg-muted/30">
      <div className="mx-auto max-w-6xl px-4 py-8">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
          <div className="max-w-md space-y-2">
            <div className="flex items-center gap-2 font-bold">
              <span className="flex h-6 w-6 items-center justify-center rounded-md bg-primary font-mono text-[10px] font-bold text-primary-foreground">
                408
              </span>
              刷题志
            </div>
            <p className="text-xs leading-relaxed text-muted-foreground">
              考研408真题刷题平台。题目均为历年统考原题（文字化整理，图表类原题以文字精确描述或替换为同年无图真题），
              解析含参考答案与思路点拨，仅供个人学习使用。
            </p>
            <p className="flex items-center gap-1 text-xs text-muted-foreground">
              <Database className="h-3 w-3" />
              已收录 {YEARS.length - 1} 年真题 + 10 套模拟卷 · {ALL_QUESTIONS.length} 题
            </p>
          </div>

          <div className="flex flex-col gap-3 text-xs sm:items-end">
            <div className="flex flex-wrap gap-x-1 gap-y-1.5 sm:justify-end">
              <span className="w-full text-muted-foreground sm:text-right">真题年份</span>
              {years.map((y) => (
                <button
                  key={y}
                  onClick={() => go("library")}
                  className="rounded px-1.5 py-0.5 font-mono text-muted-foreground transition-colors hover:bg-accent hover:text-primary"
                >
                  {y}
                </button>
              ))}
            </div>
            <div className="flex items-center gap-3 text-muted-foreground">
              <a
                href="https://github.com/CyC2018/CS-Notes"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 transition-colors hover:text-primary"
              >
                <Github className="h-3.5 w-3.5" />
                CS-Notes
              </a>
              <span className="inline-flex items-center gap-1">
                用
                <Heart className="h-3 w-3 fill-rose-400 text-rose-400" />
                面向考研人构建
              </span>
            </div>
          </div>
        </div>
        <div className="mt-6 border-t pt-4 text-center text-[11px] text-muted-foreground/70">
          © 2026 刷题志 kaoyan408.dev · 数据来源于历年考研408统考真题 · 如有解析争议请以官方答案为准
        </div>
      </div>
    </footer>
  );
}
