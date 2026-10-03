"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  AlarmClock,
  BadgeCheck,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  Flag,
  History,
  Layers,
  Play,
  RotateCcw,
  Settings2,
  Shuffle,
  Trash2,
  Trophy,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Markdown } from "@/components/site/markdown";
import { SubjectBadge, TypeBadge, DifficultyBadge } from "@/components/site/badges";
import { useApp } from "@/lib/store";
import { useProgress } from "@/lib/client";
import {
  YEARS,
  QUESTION_MAP,
  getQuestionsBy,
  shuffle,
  type Question,
} from "@/data/questions";
import { SUBJECTS, SUBJECT_LIST } from "@/data/questions/types";
import { cn } from "@/lib/utils";

type Phase = "setup" | "running" | "result";

interface RunningState {
  mockId: string;
  questionIds: string[];
  title: string;
  durationMs: number;
  startedAt: number;
}

interface ResultState {
  score: number;
  totalScore: number;
  correctCnt: number;
  totalCnt: number;
  answers: Record<string, string>;
  results: Record<string, boolean>;
  questionIds: string[];
  elapsedMs: number;
  mockId: string;
}

export function MockView() {
  const bumpProgress = useApp((s) => s.bumpProgress);
  const { data } = useProgress();
  const [phase, setPhase] = useState<Phase>("setup");
  const [running, setRunning] = useState<RunningState | null>(null);
  const [result, setResult] = useState<ResultState | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [index, setIndex] = useState(0);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [now, setNow] = useState(Date.now());
  const submittedRef = useRef(false);

  // 倒计时
  useEffect(() => {
    if (phase !== "running") return;
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, [phase]);

  const remainingMs = running ? Math.max(0, running.durationMs - (now - running.startedAt)) : 0;
  const remainingStr = useMemo(() => {
    const s = Math.floor(remainingMs / 1000);
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    const sec = s % 60;
    return h > 0
      ? `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`
      : `${m}:${String(sec).padStart(2, "0")}`;
  }, [remainingMs]);

  const submit = useCallback(
    async (auto = false) => {
      if (!running || submittedRef.current) return;
      submittedRef.current = true;
      const elapsedMs = Date.now() - running.startedAt;
      try {
        const r = await fetch("/api/mock", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: running.mockId, answers, elapsedMs }),
        });
        const j = await r.json();
        if (j?.ok) {
          setResult({
            score: j.data.score,
            totalScore: j.data.totalScore,
            correctCnt: j.data.correctCnt,
            totalCnt: j.data.totalCnt,
            answers,
            results: j.data.results,
            questionIds: running.questionIds,
            elapsedMs,
            mockId: running.mockId,
          });
          setPhase("result");
          bumpProgress();
        } else {
          submittedRef.current = false;
        }
      } catch {
        submittedRef.current = false;
      }
      void auto;
    },
    [running, answers, bumpProgress]
  );

  // 时间到自动交卷
  useEffect(() => {
    if (phase === "running" && running && remainingMs <= 0) {
      submit(true);
    }
  }, [phase, running, remainingMs, submit]);

  const startMock = async (questionIds: string[], title: string, minutes: number) => {
    try {
      const r = await fetch("/api/mock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, questionIds, minutes }),
      });
      const j = await r.json();
      if (!j?.ok) return;
      submittedRef.current = false;
      setAnswers({});
      setIndex(0);
      setResult(null);
      setRunning({
        mockId: j.data.id,
        questionIds,
        title,
        durationMs: minutes * 60_000,
        startedAt: Date.now(),
      });
      setPhase("running");
      window.scrollTo({ top: 0 });
    } catch {
      /* 网络异常时静默 */
    }
  };

  const deleteMock = async (id: string) => {
    await fetch(`/api/mock?id=${id}`, { method: "DELETE" });
    bumpProgress();
  };

  if (phase === "setup" || !running) {
    return (
      <MockSetup
        onStart={startMock}
        history={data.mocks}
        onDelete={deleteMock}
      />
    );
  }

  if (phase === "result" && result) {
    return (
      <MockResult
        result={result}
        onSelfGrade={async (qid, correct) => {
          const next = { ...result.answers, [qid]: correct ? "__SELF_CORRECT__" : "__SELF_WRONG__" };
          setAnswers(next);
          try {
            const r = await fetch("/api/mock", {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                id: result.mockId,
                answers: next,
                elapsedMs: result.elapsedMs,
              }),
            });
            const j = await r.json();
            if (j?.ok) {
              setResult({
                ...result,
                answers: next,
                results: j.data.results,
                score: j.data.score,
                correctCnt: j.data.correctCnt,
              });
              bumpProgress();
            }
          } catch {
            /* ignore */
          }
        }}
        onBack={() => setPhase("setup")}
      />
    );
  }

  const qid = running.questionIds[index];
  const q = QUESTION_MAP.get(qid);
  const answeredCount = running.questionIds.filter((id) => answers[id]).length;
  const timeLow = remainingMs < 60_000;

  return (
    <div className="fade-in-up mx-auto max-w-4xl px-4 py-6">
      {/* 计时器 + 进度 */}
      <div className="sticky top-[56px] z-20 -mx-4 mb-5 border-b bg-background/90 px-4 py-3 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <ClipboardCheck className="h-4 w-4" />
            <span className="max-w-[180px] truncate font-medium text-foreground">{running.title}</span>
          </div>
          <div
            className={cn(
              "ml-auto flex items-center gap-1.5 rounded-lg border px-3 py-1 font-mono text-sm font-bold tabular-nums",
              timeLow
                ? "animate-pulse border-rose-500 bg-rose-50 text-rose-600 dark:bg-rose-950"
                : "border-primary/40 bg-accent/40 text-primary"
            )}
            aria-live="polite"
          >
            <AlarmClock className="h-4 w-4" />
            {remainingStr}
          </div>
          <Button size="sm" variant="destructive" onClick={() => setConfirmOpen(true)} className="gap-1">
            <Flag className="h-3.5 w-3.5" /> 交卷
          </Button>
        </div>
        <div className="mt-2 flex items-center gap-3">
          <Progress
            value={(answeredCount / running.questionIds.length) * 100}
            className="h-1 flex-1"
          />
          <span className="font-mono text-[11px] text-muted-foreground">
            {answeredCount}/{running.questionIds.length}
          </span>
        </div>
      </div>

      {q && (
        <>
          <div className="rounded-xl border bg-card p-5 sm:p-6">
            <div className="mb-3 flex flex-wrap items-center gap-1.5">
              <span className="rounded-md bg-primary px-2 py-0.5 font-mono text-[11px] font-bold text-primary-foreground">
                第 {index + 1} 题
              </span>
              <SubjectBadge subject={q.subject} />
              <TypeBadge type={q.type} />
              <DifficultyBadge level={q.difficulty} />
              <span className="font-mono text-[11px] text-muted-foreground">{q.score} 分</span>
            </div>
            <Markdown content={q.content} className="text-[15px]" />
          </div>

          <div className="mt-4">
            {q.type === "single" ? (
              <div className="space-y-2.5">
                {q.options.map((opt, i) => {
                  const letter = "ABCD"[i];
                  const picked = answers[q.id] === letter;
                  return (
                    <button
                      key={letter}
                      onClick={() => setAnswers((a) => ({ ...a, [q.id]: letter }))}
                      className={cn(
                        "flex w-full items-start gap-3 rounded-xl border bg-card p-4 text-left text-sm transition-all hover:-translate-y-0.5 hover:border-primary/50 hover:shadow-md",
                        picked && "border-primary bg-accent/50 shadow-sm"
                      )}
                    >
                      <span
                        className={cn(
                          "flex h-6 w-6 shrink-0 items-center justify-center rounded-lg border font-mono text-xs font-bold",
                          picked ? "border-primary bg-primary text-primary-foreground" : "text-muted-foreground"
                        )}
                      >
                        {letter}
                      </span>
                      <span className="flex-1 leading-relaxed">
                        <Markdown content={opt} className="[&>p]:!my-0" />
                      </span>
                    </button>
                  );
                })}
              </div>
            ) : (
              <div className="rounded-xl border-2 border-dashed bg-card p-5 text-sm">
                <div className="font-semibold">综合应用题 · {q.score} 分</div>
                <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
                  请在答题纸上完整作答（本站模式下可先在纸上写清步骤）。交卷后可对照参考答案自评得分。
                </p>
                <div className="mt-3 flex gap-2">
                  <Button
                    size="sm"
                    variant={answers[q.id] === "__DONE__" ? "default" : "outline"}
                    onClick={() => setAnswers((a) => ({ ...a, [q.id]: "__DONE__" }))}
                    className="gap-1"
                  >
                    <BadgeCheck className="h-3.5 w-3.5" /> 标记为已作答
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* 底部导航 */}
          <div className="sticky bottom-4 z-10 mt-6 rounded-xl border bg-background/90 p-2.5 shadow-lg backdrop-blur-md">
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" disabled={index === 0} onClick={() => setIndex((i) => i - 1)}>
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <div className="flex flex-1 flex-wrap gap-1" role="navigation" aria-label="答题卡">
                {running.questionIds.map((id, i) => {
                  const answered = !!answers[id];
                  return (
                    <button
                      key={id}
                      onClick={() => setIndex(i)}
                      aria-label={`第 ${i + 1} 题${answered ? "（已作答）" : ""}`}
                      className={cn(
                        "h-6 w-6 rounded-md border font-mono text-[10px] font-bold transition-all hover:scale-110",
                        i === index && "ring-2 ring-primary ring-offset-1 ring-offset-background",
                        answered
                          ? "border-primary bg-primary text-primary-foreground"
                          : "text-muted-foreground hover:border-primary/50"
                      )}
                    >
                      {i + 1}
                    </button>
                  );
                })}
              </div>
              <Button
                variant="outline"
                size="sm"
                disabled={index >= running.questionIds.length - 1}
                onClick={() => setIndex((i) => i + 1)}
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </>
      )}

      <Dialog open={confirmOpen} onOpenChange={setConfirmOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>确认交卷？</DialogTitle>
            <DialogDescription>
              已作答 {answeredCount} / {running.questionIds.length} 题
              {answeredCount < running.questionIds.length && "，未答题目将计为零分"}。交卷后立即判分。
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setConfirmOpen(false)}>
              继续答题
            </Button>
            <Button variant="destructive" onClick={() => submit(false)}>
              交卷
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

/* ============ 组卷设置 ============ */
function MockSetup({
  onStart,
  history,
  onDelete,
}: {
  onStart: (ids: string[], title: string, minutes: number) => void;
  history: { id: string; title: string; score: number; totalScore: number; correctCnt: number; totalCnt: number; durationMs: number; createdAt: string }[];
  onDelete: (id: string) => void;
}) {
  const [mode, setMode] = useState<"year" | "smart">("year");
  const [year, setYear] = useState<number>(YEARS[0]);
  const [subjects, setSubjects] = useState<string[]>(SUBJECT_LIST);
  const [count, setCount] = useState(20);
  const [customMinutes, setCustomMinutes] = useState<number | null>(null);

  const yearQuestions = useMemo(() => getQuestionsBy({ year }), [year]);
  // 全量真题卷（47题/150分）自动建议考场时长 180 分钟；用户改过后尊重自定义值
  const isFullPaper = mode === "year" && yearQuestions.length >= 40;
  const yearScore = yearQuestions.reduce((a, b) => a + b.score, 0);
  const minutes = customMinutes ?? (isFullPaper ? 180 : 45);

  const toggleSubject = (s: string) => {
    setSubjects((cur) => (cur.includes(s) ? cur.filter((x) => x !== s) : [...cur, s]));
  };

  const start = () => {
    if (mode === "year") {
      const ids = yearQuestions.map((q) => q.id);
      const score = yearQuestions.reduce((a, b) => a + b.score, 0);
      onStart(ids, `${year} 年真题模考（${ids.length}题/${score}分）`, minutes);
    } else {
      const pool = getQuestionsBy({ type: "single" }).filter((q) => subjects.includes(q.subject));
      const picked = shuffle(pool).slice(0, Math.min(count, pool.length));
      onStart(
        picked.map((q) => q.id),
        `智能组卷 · ${picked.length} 道单选`,
        minutes
      );
    }
  };

  return (
    <div className="fade-in-up mx-auto max-w-3xl px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight">
          模考 <span className="font-mono text-base font-normal text-muted-foreground">/ mock</span>
        </h1>
        <p className="mt-1 text-xs text-muted-foreground">成套限时训练，还原考场节奏</p>
      </div>

      <div className="rounded-xl border bg-card p-5">
        {/* 模式选择 */}
        <div className="grid grid-cols-2 gap-2">
          {[
            { key: "year" as const, label: "真题模考", desc: "整年原题 · 含应用题", icon: Layers },
            { key: "smart" as const, label: "智能组卷", desc: "随机单选 · 自由配置", icon: Shuffle },
          ].map((m) => (
            <button
              key={m.key}
              onClick={() => setMode(m.key)}
              className={cn(
                "flex items-start gap-2.5 rounded-lg border p-3.5 text-left transition-all",
                mode === m.key ? "border-primary bg-accent/40 shadow-sm" : "hover:border-primary/40"
              )}
            >
              <m.icon className={cn("mt-0.5 h-4.5 w-4.5", mode === m.key ? "text-primary" : "text-muted-foreground")} />
              <span>
                <span className="block text-sm font-semibold">{m.label}</span>
                <span className="mt-0.5 block text-[11px] text-muted-foreground">{m.desc}</span>
              </span>
            </button>
          ))}
        </div>

        {mode === "year" ? (
          <div className="mt-5 space-y-4">
            <div>
              <Label className="text-xs">选择年份</Label>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {YEARS.map((y) => (
                  <button
                    key={y}
                    onClick={() => setYear(y)}
                    className={cn(
                      "rounded-lg border px-2.5 py-1 font-mono text-xs font-semibold transition-all hover:-translate-y-0.5",
                      year === y ? "border-primary bg-primary text-primary-foreground" : "text-muted-foreground hover:border-primary/50"
                    )}
                  >
                    {y}
                  </button>
                ))}
              </div>
            </div>
            <p className="rounded-lg bg-muted/40 px-3 py-2 text-xs text-muted-foreground">
              {year} 年卷共 {yearQuestions.length} 题（
              {SUBJECT_LIST.map((s) => `${SUBJECTS[s].short} ${yearQuestions.filter((q) => q.subject === s).length}`).join(" · ")}
              ），合计 {yearQuestions.reduce((a, b) => a + b.score, 0)} 分
            </p>
          </div>
        ) : (
          <div className="mt-5 space-y-4">
            <div>
              <Label className="text-xs">科目范围</Label>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {SUBJECT_LIST.map((s) => (
                  <button
                    key={s}
                    onClick={() => toggleSubject(s)}
                    className={cn(
                      "rounded-lg border px-2.5 py-1 text-xs font-semibold transition-all hover:-translate-y-0.5",
                      subjects.includes(s) ? "text-white" : "text-muted-foreground hover:border-primary/50"
                    )}
                    style={
                      subjects.includes(s)
                        ? { backgroundColor: SUBJECTS[s].color, borderColor: SUBJECTS[s].color }
                        : undefined
                    }
                  >
                    {SUBJECTS[s].name}
                  </button>
                ))}
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex-1">
                <Label className="text-xs" htmlFor="mock-count">题目数量</Label>
                <Input
                  id="mock-count"
                  type="number"
                  min={5}
                  max={60}
                  value={count}
                  onChange={(e) => setCount(Math.max(5, Math.min(60, Number(e.target.value) || 20)))}
                  className="mt-1.5 h-9"
                />
              </div>
            </div>
          </div>
        )}

        <div className="mt-4 flex items-center gap-4">
          <div className="w-32">
            <Label className="text-xs" htmlFor="mock-minutes">限时（分钟）</Label>
            <Input
              id="mock-minutes"
              type="number"
              min={5}
              max={180}
              value={minutes}
              onChange={(e) => {
                if (e.target.value === "") {
                  setCustomMinutes(null);
                  return;
                }
                const v = Number(e.target.value);
                setCustomMinutes(Number.isFinite(v) ? Math.max(5, Math.min(180, v)) : null);
              }}
              className="mt-1.5 h-9"
            />
            {isFullPaper && (
              <p className="mt-1 text-[11px] leading-tight text-muted-foreground">
                全量真题卷（{yearQuestions.length}题/{yearScore}分）· 考场时长 180 分钟
              </p>
            )}
          </div>
          <Button
            size="lg"
            className="ml-auto mt-5 gap-1.5"
            onClick={start}
            disabled={mode === "smart" && subjects.length === 0}
          >
            <Play className="h-4 w-4" /> 开始模考
          </Button>
        </div>
      </div>

      {/* 历史成绩 */}
      <div className="mt-8">
        <h2 className="flex items-center gap-1.5 text-sm font-bold">
          <History className="h-4 w-4 text-muted-foreground" /> 模考历史
        </h2>
        {history.length === 0 ? (
          <p className="mt-3 rounded-xl border border-dashed py-8 text-center text-xs text-muted-foreground">
            还没有模考记录，来一场吧
          </p>
        ) : (
          <div className="mt-3 space-y-2">
            {history.map((m) => (
              <div key={m.id} className="card-raise flex items-center gap-3 rounded-lg border bg-card px-4 py-3">
                <Trophy className={cn("h-4 w-4", m.score / Math.max(1, m.totalScore) >= 0.6 ? "text-amber-500" : "text-muted-foreground")} />
                <div className="min-w-0 flex-1">
                  <div className="truncate text-sm font-medium">{m.title}</div>
                  <div className="text-[11px] text-muted-foreground">
                    {new Date(m.createdAt).toLocaleString("zh-CN", { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" })} ·
                    用时 {Math.round(m.durationMs / 60000)} 分钟
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-mono text-sm font-bold tabular-nums">
                    {m.score}
                    <span className="text-muted-foreground">/{m.totalScore}</span>
                  </div>
                  <div className="text-[11px] text-muted-foreground">
                    答对 {m.correctCnt}/{m.totalCnt}
                  </div>
                </div>
                <button
                  onClick={() => onDelete(m.id)}
                  className="rounded-md p-1.5 text-muted-foreground/50 transition-colors hover:bg-rose-50 hover:text-rose-500 dark:hover:bg-rose-950"
                  aria-label="删除该记录"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

/* ============ 成绩单 ============ */
function MockResult({
  result,
  onSelfGrade,
  onBack,
}: {
  result: ResultState;
  onSelfGrade: (qid: string, correct: boolean) => void;
  onBack: () => void;
}) {
  const [filter, setFilter] = useState<"all" | "wrong">("all");
  const scorePct = Math.round((result.score / Math.max(1, result.totalScore)) * 100);
  const questions = result.questionIds
    .map((id) => QUESTION_MAP.get(id))
    .filter(Boolean) as Question[];
  const shown = filter === "all" ? questions : questions.filter((q) => !result.results[q.id]);

  return (
    <div className="fade-in-up mx-auto max-w-4xl px-4 py-8">
      {/* 成绩卡 */}
      <div className="rounded-2xl border bg-card p-6 text-center">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
          <Trophy className="h-7 w-7 text-primary" />
        </div>
        <div className="mt-3 text-3xl font-bold tabular-nums">
          {result.score}
          <span className="text-lg font-normal text-muted-foreground"> / {result.totalScore} 分</span>
        </div>
        <div className="mt-1 text-sm text-muted-foreground">
          答对 {result.correctCnt}/{result.totalCnt} 题 · 用时 {Math.round(result.elapsedMs / 60000)} 分钟 · 得分率 {scorePct}%
        </div>
        <Progress value={scorePct} className="mx-auto mt-4 h-2 max-w-sm" />
        <div className="mt-4 flex justify-center gap-3">
          <Button variant="outline" onClick={onBack} className="gap-1.5">
            <RotateCcw className="h-4 w-4" /> 再来一场
          </Button>
          <Button onClick={() => useApp.getState().go("stats")} className="gap-1.5">
            <Settings2 className="h-4 w-4" /> 看数据趋势
          </Button>
        </div>
      </div>

      {/* 试卷回顾 */}
      <div className="mt-8 flex items-center justify-between">
        <h2 className="text-lg font-bold">试卷回顾</h2>
        <div className="flex gap-1 rounded-lg border p-0.5 text-xs">
          {(["all", "wrong"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={cn(
                "rounded-md px-2.5 py-1 font-medium transition-colors",
                filter === f ? "bg-primary text-primary-foreground" : "text-muted-foreground"
              )}
            >
              {f === "all" ? "全部" : "只看错题"}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-4 space-y-3">
        {shown.map((q, i) => {
          const correct = result.results[q.id];
          const ua = result.answers[q.id];
          return (
            <div
              key={q.id}
              className={cn(
                "rounded-xl border bg-card p-5",
                correct ? "border-emerald-500/30" : "border-rose-500/40"
              )}
            >
              <div className="mb-2 flex flex-wrap items-center gap-1.5">
                <span className="font-mono text-xs font-bold text-muted-foreground">#{i + 1}</span>
                <SubjectBadge subject={q.subject} />
                <TypeBadge type={q.type} />
                <span
                  className={cn(
                    "ml-auto rounded-md px-2 py-0.5 text-[11px] font-bold",
                    correct
                      ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-400"
                      : "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-400"
                  )}
                >
                  {correct ? `+${q.score} 分` : "0 分"}
                </span>
              </div>
              <Markdown content={q.content} className="text-sm" />
              <div className="mt-3 rounded-lg bg-muted/30 p-3.5 text-sm">
                <div className="flex flex-wrap gap-x-6 gap-y-1">
                  <span>
                    <span className="text-muted-foreground">你的答案：</span>
                    <span className={cn("font-mono font-bold", correct ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600 dark:text-rose-400")}>
                      {q.type === "single"
                        ? ua && ua !== "__DONE__"
                          ? ua
                          : "未作答"
                        : ua === "__SELF_CORRECT__"
                          ? "自评正确"
                          : ua === "__SELF_WRONG__"
                            ? "自评有误"
                            : "未自评"}
                    </span>
                  </span>
                  {q.type === "single" && (
                    <span>
                      <span className="text-muted-foreground">正确答案：</span>
                      <span className="font-mono font-bold text-primary">{q.answer}</span>
                    </span>
                  )}
                </div>
              </div>

              {/* 应用题自评 */}
              {q.type === "application" && ua !== "__SELF_CORRECT__" && ua !== "__SELF_WRONG__" && (
                <div className="mt-3 rounded-lg border-2 border-dashed p-4">
                  <div className="mb-2 text-sm font-semibold">参考答案（自评本题）</div>
                  <Markdown content={q.answer} className="text-sm" />
                  <div className="mt-3 flex gap-2">
                    <Button size="sm" variant="outline" onClick={() => onSelfGrade(q.id, true)} className="border-emerald-500/50 text-emerald-600 dark:text-emerald-400">
                      自评：做对了（+{q.score} 分）
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => onSelfGrade(q.id, false)} className="border-rose-500/50 text-rose-600 dark:text-rose-400">
                      自评：有误
                    </Button>
                  </div>
                </div>
              )}

              <details className="group mt-3">
                <summary className="cursor-pointer select-none text-xs font-medium text-primary">
                  查看解析
                </summary>
                <div className="mt-2 rounded-lg border bg-muted/20 p-4">
                  {q.type === "application" && (
                    <div className="mb-3">
                      <div className="mb-1 text-sm font-semibold">参考答案</div>
                      <Markdown content={q.answer} />
                    </div>
                  )}
                  <div className="text-sm font-semibold">解析</div>
                  <Markdown content={q.analysis} />
                </div>
              </details>
            </div>
          );
        })}
        {shown.length === 0 && (
          <div className="rounded-xl border border-dashed py-12 text-center text-sm text-muted-foreground">
            全部正确，漂亮！
          </div>
        )}
      </div>
    </div>
  );
}
