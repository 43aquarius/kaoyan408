"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Bookmark,
  Check,
  CheckCircle2,
  ChevronRight,
  Home,
  ListChecks,
  Target,
  Trophy,
  X,
  XCircle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Markdown } from "@/components/site/markdown";
import { SubjectBadge, TypeBadge, DifficultyBadge, YearBadge } from "@/components/site/badges";
import { useApp } from "@/lib/store";
import { useProgress, submitRecord, toggleFavorite } from "@/lib/client";
import { QUESTION_MAP } from "@/data/questions";
import type { Question } from "@/data/questions/types";
import { cn } from "@/lib/utils";

export function PracticeView() {
  const { practice, moveQuestion, jumpQuestion, endPractice, bumpProgress } = useApp();
  const { data } = useProgress();
  const [answers, setAnswers] = useState<Record<string, { picked: string; correct: boolean }>>({});
  const [revealed, setRevealed] = useState<Record<string, boolean>>({});
  const [favSet, setFavSet] = useState<Set<string>>(new Set(data.favoriteIds));
  const startedAt = useRef<number>(Date.now());
  const [finished, setFinished] = useState(false);

  const queue = practice?.queue ?? [];
  const index = practice?.index ?? 0;
  const qid = queue[index];
  const q = qid ? QUESTION_MAP.get(qid) : undefined;

  useEffect(() => {
    setFavSet(new Set(data.favoriteIds));
  }, [data.favoriteIds]);

  // 重置会话
  useEffect(() => {
    if (practice) {
      setAnswers({});
      setRevealed({});
      setFinished(false);
      startedAt.current = Date.now();
    }
  }, [practice?.title, practice?.queue.length]);

  const answerSingle = useCallback(
    (letter: string) => {
      if (!q || q.type !== "single" || answers[q.id]) return;
      const correct = letter === q.answer;
      setAnswers((a) => ({ ...a, [q.id]: { picked: letter, correct } }));
      submitRecord({
        questionId: q.id,
        userAnswer: letter,
        isCorrect: correct,
        mode: practice?.mode ?? "practice",
        timeMs: Date.now() - startedAt.current,
      });
      bumpProgress();
      startedAt.current = Date.now();
    },
    [q, answers, practice?.mode, bumpProgress]
  );

  const selfGrade = useCallback(
    (correct: boolean) => {
      if (!q || q.type !== "application" || revealed[q.id]) return;
      setRevealed((r) => ({ ...r, [q.id]: true }));
      setAnswers((a) => ({ ...a, [q.id]: { picked: correct ? "SELF" : "SELF-WRONG", correct } }));
      submitRecord({
        questionId: q.id,
        userAnswer: correct ? "自评：正确" : "自评：有误",
        isCorrect: correct,
        mode: practice?.mode ?? "practice",
        timeMs: Date.now() - startedAt.current,
      });
      bumpProgress();
      startedAt.current = Date.now();
    },
    [q, revealed, practice?.mode, bumpProgress]
  );

  const revealApplication = useCallback(() => {
    if (!q || q.type !== "application") return;
    setRevealed((r) => ({ ...r, [q.id]: true }));
  }, [q]);

  const onToggleFav = useCallback(async () => {
    if (!q) return;
    const fav = await toggleFavorite(q.id);
    setFavSet((s) => {
      const n = new Set(s);
      if (fav) n.add(q.id);
      else n.delete(q.id);
      return n;
    });
  }, [q]);

  // 键盘快捷键
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (finished || !q) return;
      const tag = (e.target as HTMLElement)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA") return;
      const k = e.key.toUpperCase();
      if (q.type === "single" && "ABCD".includes(k) && !answers[q.id]) {
        answerSingle(k);
      } else if (k === "ARROWRIGHT" || (e.key === "Enter" && answers[q.id])) {
        if (index < queue.length - 1) moveQuestion(1);
        else setFinished(true);
      } else if (e.key === "ArrowLeft") {
        moveQuestion(-1);
      } else if (k === "F") {
        onToggleFav();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [q, answers, index, queue.length, finished, answerSingle, moveQuestion, onToggleFav]);

  const answeredCount = Object.keys(answers).length;
  const correctCount = Object.values(answers).filter((a) => a.correct).length;
  const progressPct = queue.length > 0 ? Math.round((answeredCount / queue.length) * 100) : 0;

  if (!practice || !q) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-20 text-center">
        <p className="text-sm text-muted-foreground">还没有进行中的刷题会话</p>
        <Button className="mt-4" onClick={() => useApp.getState().go("library")}>
          去题库选题
        </Button>
      </div>
    );
  }

  if (finished) {
    return (
      <FinishedScreen
        total={queue.length}
        answered={answeredCount}
        correct={correctCount}
        onRestart={() => {
          setAnswers({});
          setRevealed({});
          setFinished(false);
          jumpQuestion(0);
        }}
      />
    );
  }

  return (
    <div className="fade-in-up mx-auto max-w-4xl px-4 py-8">
      {/* 会话头 */}
      <div className="mb-6 space-y-3">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={endPractice} className="gap-1 text-muted-foreground">
            <X className="h-4 w-4" /> 结束
          </Button>
          <div className="min-w-0 flex-1">
            <div className="truncate text-sm font-semibold">{practice.title}</div>
            <div className="text-[11px] text-muted-foreground">
              第 {index + 1} / {queue.length} 题 · 已答 {answeredCount} · 答对 {correctCount}
            </div>
          </div>
          <button
            onClick={onToggleFav}
            aria-label={favSet.has(q.id) ? "取消收藏" : "收藏本题（F）"}
            className={cn(
              "inline-flex h-8 w-8 items-center justify-center rounded-md transition-all hover:scale-110",
              favSet.has(q.id) ? "text-amber-500" : "text-muted-foreground/60 hover:text-amber-500"
            )}
          >
            <Bookmark className="h-4 w-4" fill={favSet.has(q.id) ? "currentColor" : "none"} />
          </button>
        </div>
        <Progress value={progressPct} className="h-1.5" />
      </div>

      {/* 题目卡 */}
      <div className="mb-6 space-y-4">
        <div className="rounded-xl border bg-card p-5 sm:p-6">
          <div className="mb-3 flex flex-wrap items-center gap-1.5">
            <SubjectBadge subject={q.subject} />
            <YearBadge year={q.year} />
            <TypeBadge type={q.type} />
            <DifficultyBadge level={q.difficulty} />
            <span className="font-mono text-[11px] text-muted-foreground">{q.score} 分 · {q.id}</span>
          </div>
          <Markdown content={q.content} className="text-[15px]" />
        </div>

        {/* 作答区 */}
        {q.type === "single" ? (
          <div className="space-y-2.5">
            {q.options.map((opt, i) => {
              const letter = "ABCD"[i];
              const answered = !!answers[q.id];
              const isRight = answered && letter === q.answer;
              const isWrongPick = answered && answers[q.id].picked === letter && letter !== q.answer;
              return (
                <button
                  key={letter}
                  disabled={answered}
                  onClick={() => answerSingle(letter)}
                  className={cn(
                    "flex w-full items-start gap-3 rounded-xl border bg-card p-4 text-left text-sm transition-all",
                    !answered && "hover:-translate-y-0.5 hover:border-primary/50 hover:bg-accent/30 hover:shadow-md",
                    isRight && "border-emerald-500 bg-emerald-50 dark:bg-emerald-950/60",
                    isWrongPick && "border-rose-500 bg-rose-50 dark:bg-rose-950/60",
                    answered && !isRight && !isWrongPick && "opacity-55"
                  )}
                >
                  <span
                    className={cn(
                      "flex h-6 w-6 shrink-0 items-center justify-center rounded-lg border font-mono text-xs font-bold",
                      isRight && "border-emerald-500 bg-emerald-500 text-white",
                      isWrongPick && "border-rose-500 bg-rose-500 text-white",
                      !isRight && !isWrongPick && "text-muted-foreground"
                    )}
                  >
                    {letter}
                  </span>
                  <span className="flex-1 leading-relaxed">
                    <Markdown content={opt} className="[&>p]:!my-0" />
                  </span>
                  {isRight && <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-500" />}
                  {isWrongPick && <XCircle className="mt-0.5 h-4 w-4 shrink-0 text-rose-500" />}
                </button>
              );
            })}
          </div>
        ) : (
          <ApplicationPanel
            q={q}
            revealed={!!revealed[q.id]}
            graded={!!answers[q.id]}
            onReveal={revealApplication}
            onGrade={selfGrade}
          />
        )}

        {/* 解析 */}
        {answers[q.id] && (
          <div className="fade-in-up space-y-4 rounded-xl border-2 border-primary/20 bg-card p-5">
            <div className="flex items-center gap-2 text-sm font-bold">
              <Target className="h-4 w-4 text-primary" />
              {answers[q.id].correct ? (
                <span className="text-emerald-600 dark:text-emerald-400">回答正确</span>
              ) : (
                <span className="text-rose-600 dark:text-rose-400">回答错误，再消化一下</span>
              )}
              {q.type === "single" && (
                <span className="ml-auto font-mono text-xs font-normal text-muted-foreground">
                  正确答案 {q.answer}
                </span>
              )}
            </div>
            {q.type === "application" && (
              <div>
                <div className="mb-1.5 text-sm font-semibold">参考答案</div>
                <div className="rounded-lg border bg-muted/20 p-4">
                  <Markdown content={q.answer} />
                </div>
              </div>
            )}
            <div>
              <div className="mb-1.5 text-sm font-semibold">解析</div>
              <Markdown content={q.analysis} />
            </div>
          </div>
        )}
      </div>

      {/* 底部导航 */}
      <div className="sticky bottom-4 z-10 flex items-center gap-3 rounded-xl border bg-background/90 p-2.5 shadow-lg backdrop-blur-md">
        <Button variant="outline" size="sm" disabled={index === 0} onClick={() => moveQuestion(-1)} className="gap-1">
          <ArrowLeft className="h-4 w-4" /> 上一题
        </Button>
        <div className="mx-1 hidden flex-1 items-center gap-1 overflow-x-auto sm:flex" role="navigation" aria-label="题目跳转">
          {queue.map((id, i) => {
            const a = answers[id];
            return (
              <button
                key={id}
                onClick={() => jumpQuestion(i)}
                aria-label={`跳到第 ${i + 1} 题`}
                className={cn(
                  "h-6 w-6 shrink-0 rounded-md border font-mono text-[10px] font-bold transition-all hover:scale-110",
                  i === index && "ring-2 ring-primary ring-offset-1 ring-offset-background",
                  a?.correct && "border-emerald-500 bg-emerald-500 text-white",
                  a && !a.correct && "border-rose-500 bg-rose-500 text-white",
                  !a && "text-muted-foreground hover:border-primary/50"
                )}
              >
                {i + 1}
              </button>
            );
          })}
        </div>
        <span className="ml-auto font-mono text-xs text-muted-foreground sm:ml-0">
          {index + 1}/{queue.length}
        </span>
        {index < queue.length - 1 ? (
          <Button size="sm" onClick={() => moveQuestion(1)} className="gap-1">
            下一题 <ArrowRight className="h-4 w-4" />
          </Button>
        ) : (
          <Button size="sm" variant="default" onClick={() => setFinished(true)} className="gap-1">
            <ListChecks className="h-4 w-4" /> 完成
          </Button>
        )}
      </div>
      <p className="mt-3 hidden text-center text-[11px] text-muted-foreground/70 sm:block">
        快捷键：<kbd className="rounded border px-1">A</kbd>–<kbd className="rounded border px-1">D</kbd> 选择答案 ·
        <kbd className="mx-1 rounded border px-1">←</kbd>/<kbd className="rounded border px-1">→</kbd> 切题 ·
        <kbd className="mx-1 rounded border px-1">F</kbd> 收藏
      </p>
    </div>
  );
}

function ApplicationPanel({
  q,
  revealed,
  graded,
  onReveal,
  onGrade,
}: {
  q: Question;
  revealed: boolean;
  graded: boolean;
  onReveal: () => void;
  onGrade: (correct: boolean) => void;
}) {
  return (
    <div className="rounded-xl border-2 border-dashed bg-card p-5">
      <div className="text-sm font-semibold">综合应用题</div>
      <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
        建议先在纸上独立完成，再对照参考答案自评。诚实自评，错题本才会长出翅膀。
      </p>
      {!revealed ? (
        <Button variant="outline" size="sm" className="mt-3" onClick={onReveal}>
          完成，对照答案
        </Button>
      ) : (
        !graded && (
          <div className="fade-in-up mt-4 space-y-3">
            <div className="rounded-lg border bg-muted/20 p-4">
              <div className="mb-1.5 text-sm font-semibold">参考答案</div>
              <Markdown content={q.answer} />
            </div>
            <div className="flex flex-wrap gap-2">
              <Button size="sm" variant="outline" onClick={() => onGrade(true)} className="gap-1.5 border-emerald-500/50 text-emerald-600 hover:bg-emerald-50 hover:text-emerald-600 dark:text-emerald-400 dark:hover:bg-emerald-950">
                <Check className="h-4 w-4" /> 我做对了
              </Button>
              <Button size="sm" variant="outline" onClick={() => onGrade(false)} className="gap-1.5 border-rose-500/50 text-rose-600 hover:bg-rose-50 hover:text-rose-600 dark:text-rose-400 dark:hover:bg-rose-950">
                <X className="h-4 w-4" /> 我做错了
              </Button>
            </div>
          </div>
        )
      )}
    </div>
  );
}

function FinishedScreen({
  total,
  answered,
  correct,
  onRestart,
}: {
  total: number;
  answered: number;
  correct: number;
  onRestart: () => void;
}) {
  const acc = answered > 0 ? Math.round((correct / answered) * 100) : 0;
  return (
    <div className="fade-in-up mx-auto max-w-md px-4 py-20 text-center">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
        <Trophy className="h-8 w-8 text-primary" />
      </div>
      <h2 className="mt-4 text-2xl font-bold">本轮刷题完成</h2>
      <p className="mt-1 text-sm text-muted-foreground">题目已自动记入错题本与数据统计</p>
      <div className="mt-6 grid grid-cols-3 gap-3">
        {[
          { label: "答题数", value: `${answered}/${total}` },
          { label: "答对", value: `${correct}` },
          { label: "正确率", value: `${acc}%` },
        ].map((s) => (
          <div key={s.label} className="rounded-xl border bg-card p-4">
            <div className="text-xl font-bold tabular-nums">{s.value}</div>
            <div className="mt-1 text-[11px] text-muted-foreground">{s.label}</div>
          </div>
        ))}
      </div>
      <div className="mt-6 flex justify-center gap-3">
        <Button onClick={onRestart} variant="outline" className="gap-1.5">
          <ChevronRight className="h-4 w-4" /> 再刷一轮
        </Button>
        <Button onClick={() => useApp.getState().go("wrong")} variant="outline" className="gap-1.5">
          <Home className="h-4 w-4" /> 查看错题本
        </Button>
        <Button onClick={() => useApp.getState().go("stats")} className="gap-1.5">
          查看数据
        </Button>
      </div>
    </div>
  );
}
