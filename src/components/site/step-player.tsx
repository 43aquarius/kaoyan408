"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { ChevronLeft, ChevronRight, Pause, PlayCircle } from "lucide-react";
import type { AnimStep, AnimTreeNode, ExamAnimation } from "@/data/questions/types";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

/* ---------------- 二叉树布局（中序定 x，深度定 y） ---------------- */

interface TreePos {
  node: AnimTreeNode;
  x: number;
  y: number;
  parent?: TreePos;
}

function layoutTree(root: AnimTreeNode): { nodes: TreePos[]; width: number; height: number } {
  const nodes: TreePos[] = [];
  let seq = 0;
  let maxDepth = 0;
  const walk = (n: AnimTreeNode, depth: number, parent?: TreePos): TreePos => {
    maxDepth = Math.max(maxDepth, depth);
    const pos: TreePos = { node: n, x: 0, y: depth, parent };
    if (n.left) walk(n.left, depth + 1, pos);
    pos.x = seq++;
    nodes.push(pos);
    if (n.right) walk(n.right, depth + 1, pos);
    return pos;
  };
  walk(root, 0);
  return {
    nodes,
    width: seq * 56 + 12,
    height: (maxDepth + 1) * 62 + 12,
  };
}

function TreeView({ root, highlights }: { root: AnimTreeNode; highlights: (string | number)[] }) {
  const { nodes, width, height } = useMemo(() => layoutTree(root), [root]);
  const GX = 56;
  const GY = 62;
  return (
    <div className="overflow-x-auto">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        style={{ minWidth: Math.min(width, 520) }}
        className="mx-auto h-auto w-full max-w-xl"
        role="img"
        aria-label="二叉树结构图"
      >
        {nodes.map(({ node, x, y, parent }, i) =>
          parent ? (
            <line
              key={`l${i}`}
              x1={parent.x * GX + 28 + 6}
              y1={parent.y * GY + 30}
              x2={x * GX + 28 + 6}
              y2={y * GY + 2}
              className="stroke-muted-foreground/50"
              strokeWidth={1.5}
            />
          ) : null
        )}
        {nodes.map(({ node, x, y }, i) => {
          const hi = highlights.includes(node.value);
          return (
            <g key={`n${i}`}>
              <rect
                x={x * GX + 8}
                y={y * GY + 2}
                width={40}
                height={28}
                rx={7}
                className={cn(
                  hi ? "fill-emerald-500 stroke-emerald-600" : "fill-background stroke-border",
                  "transition-all duration-300"
                )}
                strokeWidth={1.5}
              />
              <text
                x={x * GX + 28}
                y={y * GY + 21}
                textAnchor="middle"
                className={cn("font-mono text-[13px] font-bold", hi ? "fill-white" : "fill-foreground")}
              >
                {String(node.value)}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

/* ---------------- 单步视图 ---------------- */

function StepView({ step }: { step: AnimStep }) {
  const stack = step.stack;
  return (
    <div className="space-y-3">
      {step.tree && <TreeView root={step.tree} highlights={step.treeHighlights ?? []} />}

      {step.table && (
        <div className="overflow-x-auto">
          <table className="mx-auto w-full max-w-lg border-collapse text-sm">
            <thead>
              <tr>
                {step.table.headers.map((h, i) => (
                  <th key={i} className="border bg-muted/60 px-3 py-1.5 text-left font-mono text-xs font-semibold">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {step.table.rows.map((row, ri) => {
                const hi = (step.rowHighlights ?? []).includes(ri);
                return (
                  <tr key={ri} className={cn("transition-colors", hi && "bg-emerald-500/15")}>
                    {row.map((cell, ci) => (
                      <td key={ci} className={cn("border px-3 py-1.5 font-mono text-xs", hi && "font-semibold")}>
                        {String(cell)}
                      </td>
                    ))}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {stack && (
        <div className="flex min-h-[88px] flex-col-reverse items-center justify-start gap-1 rounded-lg border bg-muted/20 p-3">
          {stack.length === 0 && <span className="font-mono text-xs text-muted-foreground">（空栈）</span>}
          {stack.map((v, i) => {
            const isTop = !!step.stackTop && i === stack.length - 1;
            return (
              <div
                key={i}
                className={cn(
                  "flex h-9 w-28 items-center justify-center rounded-md border font-mono text-sm transition-all duration-300",
                  isTop
                    ? "border-emerald-500 bg-emerald-500 text-white shadow-sm"
                    : "border-border bg-background"
                )}
              >
                {String(v)}
              </div>
            );
          })}
          <span className="mt-1 font-mono text-[10px] text-muted-foreground">栈底 ↑</span>
        </div>
      )}

      {step.array && (
        <div className="overflow-x-auto pb-1">
          <div className="flex min-w-max items-end gap-1.5">
            {step.array.map((v, i) => {
              const hi = (step.highlights ?? []).includes(i);
              const ptrs = (step.pointers ?? []).filter((p) => p.index === i);
              return (
                <div key={i} className="flex flex-col items-center gap-1">
                  <div
                    className={cn(
                      "flex h-11 min-w-11 items-center justify-center rounded-md border px-1.5 font-mono text-sm transition-all duration-300",
                      hi
                        ? "border-emerald-500 bg-emerald-500/15 font-bold text-emerald-700 dark:text-emerald-300"
                        : "border-border bg-background text-foreground"
                    )}
                  >
                    {v === null ? "∅" : String(v)}
                  </div>
                  <div className="flex h-4 flex-wrap justify-center gap-x-1 font-mono text-[10px] font-bold text-primary">
                    {ptrs.map((p) => (
                      <span key={p.name}>{p.name}</span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------------- 播放器 ---------------- */

export function StepPlayer({ animation }: { animation: ExamAnimation }) {
  const [idx, setIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);
  const total = animation.steps.length;

  useEffect(() => {
    if (!playing) return;
    timer.current = setInterval(() => {
      setIdx((i) => {
        if (i >= total - 1) {
          setPlaying(false);
          return i;
        }
        return i + 1;
      });
    }, 1700);
    return () => {
      if (timer.current) clearInterval(timer.current);
    };
  }, [playing, total]);

  const step = animation.steps[idx];

  return (
    <div className="rounded-xl border-2 border-primary/20 bg-card p-4">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <span className="flex items-center gap-1.5 text-sm font-bold">
          <PlayCircle className="h-4 w-4 text-primary" />
          动画讲解
          <span className="font-mono text-xs font-normal text-muted-foreground">{animation.title}</span>
        </span>
        <div className="ml-auto flex items-center gap-1">
          <Button
            variant="outline"
            size="icon"
            className="h-8 w-8"
            disabled={idx === 0}
            onClick={() => {
              setPlaying(false);
              setIdx((i) => Math.max(0, i - 1));
            }}
            aria-label="上一步"
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant={playing ? "secondary" : "default"}
            size="sm"
            className="h-8 gap-1 px-3"
            onClick={() => {
              if (idx >= total - 1) setIdx(0);
              setPlaying((p) => !p);
            }}
            aria-label={playing ? "暂停" : "自动播放"}
          >
            {playing ? <Pause className="h-3.5 w-3.5" /> : <PlayCircle className="h-3.5 w-3.5" />}
            {playing ? "暂停" : "播放"}
          </Button>
          <Button
            variant="outline"
            size="icon"
            className="h-8 w-8"
            disabled={idx >= total - 1}
            onClick={() => {
              setPlaying(false);
              setIdx((i) => Math.min(total - 1, i + 1));
            }}
            aria-label="下一步"
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <StepView step={step} />

      <div className="mt-3 rounded-lg bg-muted/30 px-3 py-2 text-sm leading-relaxed">
        <span className="mr-2 font-mono text-xs font-bold text-primary">
          [{idx + 1}/{total}]
        </span>
        {step.text}
      </div>

      {/* 步骤进度点 */}
      <div className="mt-2 flex flex-wrap gap-1">
        {animation.steps.map((_, i) => (
          <button
            key={i}
            onClick={() => {
              setPlaying(false);
              setIdx(i);
            }}
            aria-label={`跳到第 ${i + 1} 步`}
            className={cn(
              "h-1.5 rounded-full transition-all",
              i === idx ? "w-6 bg-primary" : i < idx ? "w-3 bg-primary/40" : "w-3 bg-border"
            )}
          />
        ))}
      </div>
    </div>
  );
}
