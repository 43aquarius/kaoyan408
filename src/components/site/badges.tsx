"use client";

import { Bookmark, CheckCircle2, XCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { SUBJECTS, TYPE_LABEL, DIFFICULTY_LABEL, type Question } from "@/data/questions/types";
import { RECALL_YEARS } from "@/data/questions";
import { cn } from "@/lib/utils";

export function SubjectBadge({ subject, className }: { subject: Question["subject"]; className?: string }) {
  const s = SUBJECTS[subject];
  return (
    <span
      className={cn("inline-flex items-center rounded-md px-1.5 py-0.5 text-[11px] font-semibold", className)}
      style={{ backgroundColor: `${s.color}1f`, color: s.color }}
    >
      {s.name}
    </span>
  );
}

export function TypeBadge({ type }: { type: Question["type"] }) {
  return (
    <Badge variant="outline" className="text-[11px] font-medium text-muted-foreground">
      {TYPE_LABEL[type]}
    </Badge>
  );
}

export function DifficultyBadge({ level }: { level: number }) {
  const color = level === 1 ? "text-emerald-600 border-emerald-300 bg-emerald-50 dark:text-emerald-400 dark:border-emerald-800 dark:bg-emerald-950" 
    : level === 2 ? "text-amber-600 border-amber-300 bg-amber-50 dark:text-amber-400 dark:border-amber-800 dark:bg-amber-950"
    : "text-rose-600 border-rose-300 bg-rose-50 dark:text-rose-400 dark:border-rose-800 dark:bg-rose-950";
  return (
    <span className={cn("inline-flex items-center rounded-md border px-1.5 py-0.5 text-[11px] font-semibold", color)}>
      {DIFFICULTY_LABEL[level]}
    </span>
  );
}

export function YearBadge({ year }: { year: number }) {
  const recall = RECALL_YEARS.includes(year);
  return (
    <span
      className="inline-flex items-center rounded-md border font-mono text-[11px] font-semibold text-muted-foreground px-1.5 py-0.5"
      title={recall ? "考试较新，暂无完整真题资料，本卷为回忆版" : undefined}
    >
      {year} 真题{recall ? "·回忆版" : ""}
    </span>
  );
}

export function FavoriteButton({
  favorited,
  onToggle,
  size = "md",
}: {
  favorited: boolean;
  onToggle: () => void;
  size?: "sm" | "md";
}) {
  return (
    <button
      onClick={(e) => {
        e.stopPropagation();
        onToggle();
      }}
      aria-label={favorited ? "取消收藏" : "收藏本题"}
      aria-pressed={favorited}
      className={cn(
        "inline-flex items-center justify-center rounded-md transition-all hover:scale-110 active:scale-95",
        size === "md" ? "h-8 w-8" : "h-7 w-7",
        favorited ? "text-amber-500" : "text-muted-foreground/60 hover:text-amber-500"
      )}
    >
      <Bookmark className={size === "md" ? "h-4.5 w-4.5" : "h-4 w-4"} fill={favorited ? "currentColor" : "none"} />
    </button>
  );
}

export function JudgeIcon({ correct }: { correct: boolean }) {
  return correct ? (
    <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-500" />
  ) : (
    <XCircle className="h-4 w-4 shrink-0 text-rose-500" />
  );
}
