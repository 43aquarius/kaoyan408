"use client";

import { useCallback, useMemo, useState } from "react";
import { ChevronDown, ChevronLeft, ChevronRight, Filter, PenTool, Search, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Markdown } from "@/components/site/markdown";
import { QuestionExtras } from "@/components/site/question-extras";
import { SubjectBadge, TypeBadge, DifficultyBadge, YearBadge, FavoriteButton } from "@/components/site/badges";
import { useApp, type LibFilters } from "@/lib/store";
import { useProgress, toggleFavorite, submitRecord } from "@/lib/client";
import {
  ALL_QUESTIONS,
  REAL_YEARS,
  ALL_TAGS,
  getQuestionsBy,
  type Question,
} from "@/data/questions";
import { DIFFICULTY_LABEL } from "@/data/questions/types";
import { MOCKS } from "@/data/mocks";
import { cn } from "@/lib/utils";

const PAGE_SIZE = 20;

export function LibraryView() {
  const { libFilters, startPractice } = useApp();
  const { data, loading } = useProgress();
  const [expanded, setExpanded] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [favVersion, setFavVersion] = useState(0);

  // 更新筛选同时重置页码（事件驱动，避免 effect 内 setState）
  const updateFilters = useCallback((f: Partial<LibFilters>) => {
    useApp.getState().setLibFilters(f);
    setPage(1);
  }, []);

  const filtered = useMemo(() => {
    const q = libFilters.q.trim().toLowerCase();
    return getQuestionsBy({
      year: libFilters.year,
      subject: libFilters.subject,
      type: libFilters.type,
    }).filter((x) => {
      if (libFilters.difficulty !== "all" && String(x.difficulty) !== libFilters.difficulty) return false;
      if (libFilters.tag && !x.tags.includes(libFilters.tag)) return false;
      if (q) {
        const hay = `${x.content} ${x.tags.join(" ")} ${x.options.join(" ")}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
  }, [libFilters]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  // 外部筛选变化可能导致 page 超界，渲染时钳位
  const safePage = Math.min(page, totalPages);
  const pageQuestions = filtered.slice((safePage - 1) * PAGE_SIZE, safePage * PAGE_SIZE);

  const wrongSet = new Set(data.wrongIds);
  const doneSet = new Set(data.masteredIds);

  const startFilterPractice = () => {
    const ids = filtered.map((q) => q.id);
    if (ids.length === 0) return;
    startPractice(ids, `筛选刷题 · ${ids.length} 题`, "practice");
  };

  const onToggleFav = async (qid: string) => {
    await toggleFavorite(qid);
    setFavVersion((v) => v + 1);
  };

  const favSet = useMemo(() => {
    void favVersion;
    return new Set(data.favoriteIds);
  }, [data.favoriteIds, favVersion]);

  return (
    <div className="fade-in-up mx-auto max-w-5xl px-4 py-8">
      {/* 标题区 */}
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">
            题库 <span className="font-mono text-base font-normal text-muted-foreground">/ questions</span>
          </h1>
          <p className="mt-1 text-xs text-muted-foreground">
            {REAL_YEARS.length} 年真题 + {MOCKS.length} 套模拟卷 · 共 {ALL_QUESTIONS.length} 题 · 逐项解析
          </p>
        </div>
        <Button onClick={startFilterPractice} disabled={filtered.length === 0} className="gap-1.5">
          <PenTool className="h-4 w-4" />
          刷当前筛选（{filtered.length}）
        </Button>
      </div>

      {/* 筛选区 */}
      <div className="mb-4 rounded-xl border bg-card p-4">
        <div className="flex flex-wrap items-center gap-2">
          <Filter className="h-4 w-4 text-muted-foreground" />
          {/* 年份 */}
          <Select value={libFilters.year} onValueChange={(v) => updateFilters({ year: v })}>
            <SelectTrigger className="h-8 w-[118px] text-xs"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">全部年份</SelectItem>
              {[...REAL_YEARS].sort((a, b) => b - a).map((y) => (
                <SelectItem key={y} value={String(y)}>{y} 年</SelectItem>
              ))}
              <SelectItem value="2027" className="font-medium">模拟卷（全部）</SelectItem>
              {MOCKS.map((m) => (
                <SelectItem key={m.no} value={`m${m.no}`}>
                  {m.title}·{m.subtitle}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {/* 科目 */}
          <Select value={libFilters.subject} onValueChange={(v) => updateFilters({ subject: v })}>
            <SelectTrigger className="h-8 w-[130px] text-xs"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">全部科目</SelectItem>
              <SelectItem value="ds">数据结构</SelectItem>
              <SelectItem value="co">计算机组成</SelectItem>
              <SelectItem value="os">操作系统</SelectItem>
              <SelectItem value="cn">计算机网络</SelectItem>
            </SelectContent>
          </Select>
          {/* 题型 */}
          <Select value={libFilters.type} onValueChange={(v) => updateFilters({ type: v })}>
            <SelectTrigger className="h-8 w-[120px] text-xs"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">全部题型</SelectItem>
              <SelectItem value="single">单项选择题</SelectItem>
              <SelectItem value="application">综合应用题</SelectItem>
            </SelectContent>
          </Select>
          {/* 难度 */}
          <Select value={libFilters.difficulty} onValueChange={(v) => updateFilters({ difficulty: v })}>
            <SelectTrigger className="h-8 w-[104px] text-xs"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">全部难度</SelectItem>
              <SelectItem value="1">简单</SelectItem>
              <SelectItem value="2">中等</SelectItem>
              <SelectItem value="3">较难</SelectItem>
            </SelectContent>
          </Select>
          {/* 知识点 */}
          <Select value={libFilters.tag || "all"} onValueChange={(v) => updateFilters({ tag: v === "all" ? "" : v })}>
            <SelectTrigger className="h-8 w-[150px] text-xs"><SelectValue placeholder="知识点" /></SelectTrigger>
            <SelectContent className="max-h-72">
              <SelectItem value="all">全部知识点</SelectItem>
              {ALL_TAGS.map((t) => (
                <SelectItem key={t} value={t}>{t}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          {/* 搜索 */}
          <div className="relative ml-auto">
            <Search className="absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={libFilters.q}
              onChange={(e) => updateFilters({ q: e.target.value })}
              placeholder="搜题干 / 知识点…"
              className="h-8 w-52 pl-8 text-xs"
              aria-label="搜索题目"
            />
            {libFilters.q && (
              <button
                onClick={() => updateFilters({ q: "" })}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                aria-label="清空搜索"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            )}
          </div>
        </div>
        {(libFilters.year !== "all" || libFilters.subject !== "all" || libFilters.type !== "all" ||
          libFilters.difficulty !== "all" || libFilters.tag || libFilters.q) && (
          <button
            onClick={() => { useApp.getState().resetLibFilters(); setPage(1); }}
            className="mt-3 inline-flex items-center gap-1 text-xs text-muted-foreground transition-colors hover:text-primary"
          >
            <X className="h-3 w-3" /> 清除筛选
          </button>
        )}
      </div>

      {/* 题目列表 */}
      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-28 animate-pulse rounded-xl border bg-card" />
          ))}
        </div>
      ) : pageQuestions.length === 0 ? (
        <div className="rounded-xl border border-dashed py-16 text-center text-sm text-muted-foreground">
          没有符合条件的题目，试试放宽筛选条件
        </div>
      ) : (
        <div className="space-y-3">
          {pageQuestions.map((q) => (
            <QuestionRow
              key={q.id}
              q={q}
              expanded={expanded === q.id}
              onExpand={() => setExpanded(expanded === q.id ? null : q.id)}
              favorited={favSet.has(q.id)}
              onToggleFav={() => onToggleFav(q.id)}
              status={wrongSet.has(q.id) ? "wrong" : doneSet.has(q.id) ? "done" : "none"}
            />
          ))}
        </div>
      )}

      {/* 分页 */}
      {totalPages > 1 && (
        <div className="mt-6 flex items-center justify-center gap-2">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
            <ChevronLeft className="h-4 w-4" /> 上一页
          </Button>
          <span className="px-2 text-xs text-muted-foreground">
            第 <strong className="text-foreground">{page}</strong> / {totalPages} 页 · 共 {filtered.length} 题
          </span>
          <Button variant="outline" size="sm" disabled={page >= totalPages} onClick={() => setPage((p) => p + 1)}>
            下一页 <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  );
}

function QuestionRow({
  q,
  expanded,
  onExpand,
  favorited,
  onToggleFav,
  status,
}: {
  q: Question;
  expanded: boolean;
  onExpand: () => void;
  favorited: boolean;
  onToggleFav: () => void;
  status: "wrong" | "done" | "none";
}) {
  return (
    <article
      className={cn(
        "card-raise cursor-pointer rounded-xl border bg-card p-4 transition-colors",
        expanded && "border-primary/40"
      )}
      onClick={onExpand}
    >
      <div className="flex items-start gap-3">
        <div className="mt-0.5 flex flex-col items-center gap-1">
          <span
            className={cn(
              "flex h-6 w-6 items-center justify-center rounded-full border font-mono text-[10px] font-bold",
              status === "wrong" && "border-rose-400 bg-rose-50 text-rose-600 dark:bg-rose-950 dark:text-rose-400",
              status === "done" && "border-emerald-400 bg-emerald-50 text-emerald-600 dark:bg-emerald-950 dark:text-emerald-400",
              status === "none" && "text-muted-foreground"
            )}
            aria-label={status === "wrong" ? "错题" : status === "done" ? "已做对" : "未做过"}
          >
            {q.no ?? "·"}
          </span>
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-1.5">
            <SubjectBadge subject={q.subject} />
            <YearBadge year={q.year} mockNo={q.mockNo} />
            <TypeBadge type={q.type} />
            <DifficultyBadge level={q.difficulty} />
            <span className="font-mono text-[11px] text-muted-foreground">{q.score} 分</span>
            {q.tags.slice(0, 2).map((t) => (
              <Badge key={t} variant="secondary" className="text-[10px] font-normal text-muted-foreground">
                {t}
              </Badge>
            ))}
          </div>
          <div className="mt-2 line-clamp-2 text-sm leading-relaxed text-foreground/90">
            <Markdown content={q.content} className="line-clamp-2 [&>p]:!my-0" />
          </div>
          <div className="mt-2 flex items-center gap-2 text-[11px] text-muted-foreground">
            <span className="font-mono">{q.id}</span>
            <span className="ml-auto inline-flex items-center gap-1 transition-colors group-hover:text-primary">
              {expanded ? "收起" : "展开答题"}
              <ChevronDown className={cn("h-3.5 w-3.5 transition-transform", expanded && "rotate-180")} />
            </span>
          </div>
        </div>
        <FavoriteButton favorited={favorited} onToggle={onToggleFav} />
      </div>

      {expanded && (
        <div className="mt-4 border-t pt-4" onClick={(e) => e.stopPropagation()}>
          <InlineAnswer key={q.id} q={q} />
        </div>
      )}
    </article>
  );
}

/** 题库内展开的快速作答区（key={q.id} 保证切题重置） */
function InlineAnswer({ q }: { q: Question }) {
  const [picked, setPicked] = useState<string | null>(null);
  const [revealed, setRevealed] = useState(false);
  const [selfEvaluated, setSelfEvaluated] = useState(false);
  const bumpProgress = useApp((s) => s.bumpProgress);

  const submit = (userAnswer: string, isCorrect: boolean) => {
    submitRecord({ questionId: q.id, userAnswer, isCorrect, mode: "practice" });
    bumpProgress();
  };

  return (
    <div className="space-y-3">
      <Markdown content={q.content} />
      {q.type === "single" ? (
        <div className="space-y-2">
          {q.options.map((opt, i) => {
            const letter = "ABCD"[i];
            const isRight = revealed && letter === q.answer;
            const isWrongPick = revealed && picked === letter && letter !== q.answer;
            return (
              <button
                key={letter}
                disabled={revealed}
                onClick={() => {
                  if (revealed) return;
                  setPicked(letter);
                  setRevealed(true);
                  submit(letter, letter === q.answer);
                }}
                className={cn(
                  "flex w-full items-start gap-2.5 rounded-lg border p-3 text-left text-sm transition-all",
                  !revealed && "hover:border-primary/50 hover:bg-accent/40",
                  isRight && "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/60",
                  isWrongPick && "border-rose-500 bg-rose-50 dark:bg-rose-950/60",
                  !isRight && !isWrongPick && revealed && "opacity-60"
                )}
              >
                <span
                  className={cn(
                    "flex h-5 w-5 shrink-0 items-center justify-center rounded-full border font-mono text-[11px] font-bold",
                    isRight && "border-emerald-500 bg-emerald-500 text-white",
                    isWrongPick && "border-rose-500 bg-rose-500 text-white",
                    !isRight && !isWrongPick && "text-muted-foreground"
                  )}
                >
                  {letter}
                </span>
                <span className="flex-1">
                  <Markdown content={opt} className="[&>p]:!my-0" />
                </span>
              </button>
            );
          })}
        </div>
      ) : (
        !revealed && (
          <Button variant="outline" size="sm" onClick={() => setRevealed(true)}>
            显示参考答案
          </Button>
        )
      )}

      {q.type === "application" && revealed && !selfEvaluated && (
        <div className="flex flex-wrap items-center gap-2 text-sm">
          <span className="text-muted-foreground">对照后自评：</span>
          <Button
            size="sm"
            variant="outline"
            className="h-8 gap-1 border-emerald-500/50 text-emerald-600 hover:bg-emerald-50 dark:text-emerald-400 dark:hover:bg-emerald-950/50"
            onClick={() => {
              setSelfEvaluated(true);
              submit("correct", true);
            }}
          >
            ✓ 做出来了
          </Button>
          <Button
            size="sm"
            variant="outline"
            className="h-8 gap-1 border-rose-500/50 text-rose-600 hover:bg-rose-50 dark:text-rose-400 dark:hover:bg-rose-950/50"
            onClick={() => {
              setSelfEvaluated(true);
              submit("wrong", false);
            }}
          >
            ✗ 没做出来
          </Button>
        </div>
      )}

      {revealed && (
        <div className="space-y-3 rounded-lg border bg-muted/30 p-4 fade-in-up">
          {q.type === "single" ? (
            <div className="text-sm">
              <span className="font-semibold">答案：</span>
              <span className={cn("ml-1 font-mono text-base font-bold", picked === q.answer ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400")}>
                {q.answer}
              </span>
              {picked && (
                <span className="ml-2 text-xs text-muted-foreground">
                  （你的选择：{picked} {picked === q.answer ? "✓ 正确" : "✗ 错误"}）
                </span>
              )}
            </div>
          ) : (
            <div className="text-sm">
              <div className="mb-1 font-semibold">参考答案</div>
              <Markdown content={q.answer} />
            </div>
          )}
          <div className="border-t pt-3 text-sm">
            <div className="mb-1 font-semibold">解析</div>
            <Markdown content={q.analysis} />
          </div>
          <QuestionExtras q={q} />
        </div>
      )}
    </div>
  );
}
