"use client";

import { CheckCircle2, ImageIcon, XCircle } from "lucide-react";
import type { Question } from "@/data/questions/types";
import { StepPlayer } from "./step-player";
import { cn } from "@/lib/utils";

/**
 * 模拟卷增强讲解区：逐项解析（每题每选项）+ 配图 + 动画。
 * 真题无这些字段时完全不渲染。
 */
export function QuestionExtras({ q }: { q: Question }) {
  if (!q.optionAnalysis && !q.image && !q.animation) return null;

  return (
    <div className="space-y-4">
      {/* 逐项解析 */}
      {q.optionAnalysis && (
        <div>
          <div className="mb-2 text-sm font-semibold">逐项解析</div>
          <div className="space-y-1.5">
            {(["A", "B", "C", "D"] as const).map((L) => {
              const text = q.optionAnalysis?.[L];
              if (!text) return null;
              const right = q.type === "single" && q.answer === L;
              return (
                <div
                  key={L}
                  className={cn(
                    "flex items-start gap-2.5 rounded-lg border p-2.5 text-sm leading-relaxed",
                    right
                      ? "border-emerald-500/60 bg-emerald-50/70 dark:bg-emerald-950/40"
                      : "border-border bg-muted/20"
                  )}
                >
                  <span
                    className={cn(
                      "mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border font-mono text-[11px] font-bold",
                      right
                        ? "border-emerald-500 bg-emerald-500 text-white"
                        : "border-border text-muted-foreground"
                    )}
                  >
                    {L}
                  </span>
                  <span className="flex-1">
                    {right && (
                      <span className="mr-1 inline-flex items-center gap-0.5 font-semibold text-emerald-600 dark:text-emerald-400">
                        <CheckCircle2 className="h-3.5 w-3.5" /> 正确项
                      </span>
                    )}
                    {!right && q.type === "single" && (
                      <XCircle className="mr-1 inline h-3.5 w-3.5 align-[-2px] text-muted-foreground/70" />
                    )}
                    {text}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 配图 */}
      {q.image && (
        <figure>
          <figcaption className="mb-2 flex items-center gap-1.5 text-sm font-semibold">
            <ImageIcon className="h-4 w-4 text-primary" />
            图示解析
          </figcaption>
          <a href={q.image} target="_blank" rel="noreferrer" title="点击查看大图">
            <img
              src={q.image}
              alt="题图解析"
              loading="lazy"
              className="w-full rounded-lg border bg-white p-2 dark:bg-white"
            />
          </a>
        </figure>
      )}

      {/* 动画 */}
      {q.animation && <StepPlayer animation={q.animation} />}
    </div>
  );
}
