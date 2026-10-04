"use client";

import { useMemo } from "react";
import {
  Activity,
  BarChart3,
  CalendarCheck,
  CheckCircle2,
  Percent,
  PenTool,
  Target,
  TrendingUp,
} from "lucide-react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useApp } from "@/lib/store";
import { useProgress } from "@/lib/client";
import {
  ALL_QUESTIONS,
  YEARS,
  getQuestionsBy,
  QUESTION_MAP,
} from "@/data/questions";
import { SUBJECTS, SUBJECT_LIST } from "@/data/questions/types";

const CHART_COLORS = ["#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

export function StatsView() {
  const { data, loading } = useProgress();
  const go = useApp((s) => s.go);

  const stats = useMemo(() => {
    const recordMap = new Map<string, { correct: boolean; count: number }>();
    for (const r of data.records) {
      recordMap.set(r.questionId, {
        correct: r.isCorrect,
        count: (recordMap.get(r.questionId)?.count ?? 0) + 1,
      });
    }

    // 各科统计
    const bySubject = SUBJECT_LIST.map((s, i) => {
      const all = getQuestionsBy({ subject: s });
      const attempted = all.filter((q) => recordMap.has(q.id));
      const correct = attempted.filter((q) => recordMap.get(q.id)?.correct);
      return {
        key: s,
        name: SUBJECTS[s].name,
        color: CHART_COLORS[i],
        total: all.length,
        attempted: attempted.length,
        correct: correct.length,
        accuracy: attempted.length > 0 ? Math.round((correct.length / attempted.length) * 100) : 0,
      };
    });

    // 近 30 天（补零）
    const days: { day: string; label: string; count: number; correct: number }[] = [];
    const now = new Date();
    for (let i = 29; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(now.getDate() - i);
      const key = d.toISOString().slice(0, 10);
      const v = data.byDay[key];
      days.push({
        day: key,
        label: `${d.getMonth() + 1}/${d.getDate()}`,
        count: v?.total ?? 0,
        correct: v?.correct ?? 0,
      });
    }

    // 各年份完成度（2027 = 模拟卷合集）
    const byYear = [...YEARS]
      .sort((a, b) => a - b)
      .map((y) => {
        const all = getQuestionsBy({ year: y });
        const done = all.filter((q) => recordMap.has(q.id)).length;
        const correct = all.filter((q) => recordMap.get(q.id)?.correct).length;
        return {
          year: y,
          label: y === 2027 ? "模拟卷" : String(y),
          total: all.length,
          done,
          correct,
          pct: Math.round((done / all.length) * 100),
        };
      });

    // 难度分布（已做）
    const byDifficulty = [1, 2, 3].map((d) => {
      const attempted = ALL_QUESTIONS.filter(
        (q) => q.difficulty === d && recordMap.has(q.id)
      );
      const correct = attempted.filter((q) => recordMap.get(q.id)?.correct);
      return {
        name: d === 1 ? "简单" : d === 2 ? "中等" : "较难",
        答对: correct.length,
        答错: attempted.length - correct.length,
      };
    });

    const totalAccuracy =
      data.attempted > 0 ? Math.round((data.correct / data.attempted) * 100) : 0;

    return { bySubject, days, byYear, byDifficulty, totalAccuracy };
  }, [data]);

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-8">
        <div className="grid gap-4 md:grid-cols-2">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-56 animate-pulse rounded-xl border bg-card" />
          ))}
        </div>
      </div>
    );
  }

  const isEmpty = data.attempted === 0;

  return (
    <div className="fade-in-up mx-auto max-w-5xl px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold tracking-tight">
          数据 <span className="font-mono text-base font-normal text-muted-foreground">/ stats</span>
        </h1>
        <p className="mt-1 text-xs text-muted-foreground">用数据看见自己的成长曲线</p>
      </div>

      {/* 概览 */}
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {[
          { label: "累计作答", value: `${data.totalRecords}`, unit: "次", icon: PenTool },
          { label: "已刷题目", value: `${data.attempted}`, unit: `/ ${ALL_QUESTIONS.length} 题`, icon: CheckCircle2 },
          { label: "总体正确率", value: `${stats.totalAccuracy}`, unit: "%", icon: Percent },
          { label: "模考场次", value: `${data.mocks.length}`, unit: "场", icon: Target },
        ].map((s) => (
          <Card key={s.label} className="card-raise">
            <CardContent className="p-4">
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>{s.label}</span>
                <s.icon className="h-4 w-4 text-primary" />
              </div>
              <div className="mt-1.5 text-2xl font-bold tabular-nums">
                {s.value}
                <span className="ml-1 text-xs font-normal text-muted-foreground">{s.unit}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {isEmpty ? (
        <div className="mt-6 rounded-xl border border-dashed py-16 text-center">
          <BarChart3 className="mx-auto h-10 w-10 text-primary/40" />
          <p className="mt-3 text-sm text-muted-foreground">还没有刷题数据，先去刷几题再来吧</p>
          <button
            onClick={() => go("library")}
            className="mt-4 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-85"
          >
            进入题库
          </button>
        </div>
      ) : (
        <div className="mt-6 grid gap-4 lg:grid-cols-2">
          {/* 近30天趋势 */}
          <Card>
            <CardContent className="p-5">
              <div className="mb-4 flex items-center gap-2 text-sm font-bold">
                <Activity className="h-4 w-4 text-primary" /> 近 30 天刷题量
              </div>
              <ResponsiveContainer width="100%" height={220}>
                <AreaChart data={stats.days} margin={{ top: 4, right: 8, left: -22, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#10b981" stopOpacity={0.35} />
                      <stop offset="100%" stopColor="#10b981" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.1} />
                  <XAxis
                    dataKey="label"
                    tick={{ fontSize: 10 }}
                    interval={4}
                    stroke="currentColor"
                    opacity={0.5}
                  />
                  <YAxis tick={{ fontSize: 10 }} stroke="currentColor" opacity={0.5} allowDecimals={false} />
                  <Tooltip
                    contentStyle={{
                      borderRadius: 10,
                      border: "1px solid rgba(128,128,128,0.2)",
                      fontSize: 12,
                    }}
                    labelFormatter={(l) => `${l}`}
                  />
                  <Area
                    type="monotone"
                    dataKey="count"
                    name="作答次数"
                    stroke="#10b981"
                    strokeWidth={2}
                    fill="url(#colorCount)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* 各科正确率 */}
          <Card>
            <CardContent className="p-5">
              <div className="mb-4 flex items-center gap-2 text-sm font-bold">
                <Target className="h-4 w-4 text-primary" /> 各科正确率与完成度
              </div>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={stats.bySubject} margin={{ top: 4, right: 8, left: -22, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.1} />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} stroke="currentColor" opacity={0.5} />
                  <YAxis tick={{ fontSize: 10 }} stroke="currentColor" opacity={0.5} domain={[0, 100]} unit="%" />
                  <Tooltip
                    contentStyle={{
                      borderRadius: 10,
                      border: "1px solid rgba(128,128,128,0.2)",
                      fontSize: 12,
                    }}
                    formatter={(v: number) => [`${v}%`, "正确率"]}
                  />
                  <Bar dataKey="accuracy" name="正确率" radius={[6, 6, 0, 0]} maxBarSize={48}>
                    {stats.bySubject.map((s) => (
                      <Cell key={s.key} fill={s.color} fillOpacity={0.85} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="mt-3 grid grid-cols-4 gap-2 text-center">
                {stats.bySubject.map((s) => (
                  <div key={s.key} className="text-[11px] text-muted-foreground">
                    <span className="font-mono font-bold text-foreground">
                      {s.attempted}/{s.total}
                    </span>
                    <br />
                    {s.name}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* 难度分布 */}
          <Card>
            <CardContent className="p-5">
              <div className="mb-4 flex items-center gap-2 text-sm font-bold">
                <TrendingUp className="h-4 w-4 text-primary" /> 难度掌握分布
              </div>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={stats.byDifficulty} margin={{ top: 4, right: 8, left: -22, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.1} />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} stroke="currentColor" opacity={0.5} />
                  <YAxis tick={{ fontSize: 10 }} stroke="currentColor" opacity={0.5} allowDecimals={false} />
                  <Tooltip
                    contentStyle={{
                      borderRadius: 10,
                      border: "1px solid rgba(128,128,128,0.2)",
                      fontSize: 12,
                    }}
                  />
                  <Bar dataKey="答对" stackId="a" fill="#10b981" radius={[0, 0, 0, 0]} maxBarSize={48} />
                  <Bar dataKey="答错" stackId="a" fill="#f87171" radius={[6, 6, 0, 0]} maxBarSize={48} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* 年份完成度 */}
          <Card>
            <CardContent className="p-5">
              <div className="mb-4 flex items-center gap-2 text-sm font-bold">
                <CalendarCheck className="h-4 w-4 text-primary" /> 各年份完成度
              </div>
              <div className="max-h-[220px] space-y-2.5 overflow-y-auto pr-1">
                {stats.byYear.map((y) => (
                  <div key={y.year} className="flex items-center gap-3">
                    <span className="w-10 shrink-0 font-mono text-xs font-semibold text-muted-foreground">
                      {y.label}
                    </span>
                    <Progress value={y.pct} className="h-2 flex-1" />
                    <span className="w-20 shrink-0 text-right font-mono text-[11px] text-muted-foreground">
                      {y.done}/{y.total} 题
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* 模考趋势 */}
      {data.mocks.length > 0 && (
        <Card className="mt-4">
          <CardContent className="p-5">
            <div className="mb-4 flex items-center gap-2 text-sm font-bold">
              <Target className="h-4 w-4 text-primary" /> 模考成绩记录
            </div>
            <div className="space-y-2">
              {[...data.mocks].reverse().map((m, i) => {
                const pct = Math.round((m.score / Math.max(1, m.totalScore)) * 100);
                return (
                  <div key={m.id} className="flex items-center gap-3">
                    <span className="w-6 text-center font-mono text-[11px] text-muted-foreground">
                      #{i + 1}
                    </span>
                    <span className="w-40 shrink-0 truncate text-xs">{m.title}</span>
                    <Progress value={pct} className="h-2 flex-1" />
                    <span className="w-24 shrink-0 text-right font-mono text-[11px] font-bold tabular-nums">
                      {m.score}/{m.totalScore}
                    </span>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* 最近作答记录 */}
      {data.records.length > 0 && (
        <Card className="mt-4">
          <CardContent className="p-5">
            <div className="mb-4 text-sm font-bold">最近作答</div>
            <div className="max-h-72 space-y-1.5 overflow-y-auto pr-1">
              {data.records.slice(0, 30).map((r) => {
                const q = QUESTION_MAP.get(r.questionId);
                return (
                  <div
                    key={r.id}
                    className="flex items-center gap-2.5 rounded-lg border bg-muted/20 px-3 py-2 text-xs"
                  >
                    <span
                      className={
                        r.isCorrect
                          ? "font-bold text-emerald-600 dark:text-emerald-400"
                          : "font-bold text-rose-600 dark:text-rose-400"
                      }
                    >
                      {r.isCorrect ? "✓" : "✗"}
                    </span>
                    <span className="font-mono text-muted-foreground">{r.questionId}</span>
                    <span className="truncate text-muted-foreground">
                      {q ? q.tags.join(" / ") : ""}
                    </span>
                    <span className="ml-auto shrink-0 text-muted-foreground/70">
                      {new Date(r.createdAt).toLocaleString("zh-CN", {
                        month: "numeric",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </span>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
