"use client";

import {
  ArrowRight,
  BookMarked,
  CalendarDays,
  ChartPie,
  Clock3,
  Database,
  Flame,
  GraduationCap,
  Layers,
  NotebookPen,
  PenTool,
  RotateCcw,
  Sparkles,
  Target,
} from "lucide-react";
import { Typewriter } from "@/components/site/typewriter";
import { GitHubCounter } from "@/components/site/github-counter";
import { SubjectBadge } from "@/components/site/badges";
import { useApp } from "@/lib/store";
import { useProgress } from "@/lib/client";
import { ALL_QUESTIONS, YEARS, getQuestionsBy } from "@/data/questions";
import { SUBJECTS, SUBJECT_LIST } from "@/data/questions/types";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

const HERO_PHRASES = [
  "Hello, 考研人 👋".replace(" 👋", ""),
  "把近二十年 408 真题，一题一题刷穿。",
  "数据结构 · 计组 · 操统 · 计网",
  "今天也要稳住，能上岸。",
];

export function HomeView() {
  const { go, startPractice } = useApp();
  const { data } = useProgress();
  const years = [...YEARS].sort((a, b) => a - b);
  const latestYear = years[years.length - 1];
  const attemptedPct = ALL_QUESTIONS.length > 0 ? Math.round((data.attempted / ALL_QUESTIONS.length) * 100) : 0;
  const accuracy = data.attempted > 0 ? Math.round((data.correct / data.attempted) * 100) : 0;

  const startQuickPractice = () => {
    const wrongLeft = data.wrongIds.length > 0;
    const queue = wrongLeft
      ? data.wrongIds
      : getQuestionsBy({ subject: "all", year: "all", type: "single" }).map((q) => q.id);
    startPractice(queue, wrongLeft ? "错题重刷" : "单选快刷", wrongLeft ? "wrong" : "practice");
  };

  return (
    <div className="fade-in-up">
      {/* ============ Hero ============ */}
      <section className="border-b bg-gradient-to-b from-accent/40 to-transparent">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:py-24">
          <div className="flex flex-col items-start gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-2xl space-y-5">
              <div className="inline-flex items-center gap-1.5 rounded-full border bg-card px-3 py-1 text-xs font-medium text-muted-foreground">
                <Sparkles className="h-3.5 w-3.5 text-primary" />
                {YEARS.length} 年真题 · {ALL_QUESTIONS.length} 道原题 · 全科目覆盖
              </div>
              <h1 className="text-4xl font-bold leading-tight tracking-tight sm:text-5xl">
                <span className="text-primary">#</span> Hi, 考研人
                <br />
                <Typewriter
                  phrases={HERO_PHRASES}
                  className="text-foreground"
                />
              </h1>
              <p className="max-w-xl text-sm leading-relaxed text-muted-foreground sm:text-base">
                这里收录了 {years[0]}–{latestYear} 年考研 408 统考的真题原题与详解。
                刷题、模考、错题回顾、数据统计——用一个程序员的专注，把 150 分的每一步都踩实。
              </p>
              <div className="flex flex-wrap gap-3 pt-1">
                <Button size="lg" onClick={() => go("library")} className="gap-1.5">
                  <Layers className="h-4 w-4" />
                  进入题库
                  <ArrowRight className="h-4 w-4" />
                </Button>
                <Button size="lg" variant="outline" onClick={startQuickPractice} className="gap-1.5">
                  <PenTool className="h-4 w-4" />
                  {data.wrongIds.length > 0 ? `重刷 ${data.wrongIds.length} 道错题` : "快速刷题"}
                </Button>
                <Button size="lg" variant="ghost" onClick={() => go("mock")} className="gap-1.5">
                  <GraduationCap className="h-4 w-4" />
                  全真模考
                </Button>
              </div>
            </div>

            {/* 实时 GitHub 计数卡片 */}
            <div className="w-full max-w-xs space-y-3">
              <div className="text-xs font-medium text-muted-foreground">
                <span className="mr-1 inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-primary" />
                LIVE · 实时数据
              </div>
              <GitHubCounter />
              <div className="rounded-xl border border-dashed p-4 text-xs leading-relaxed text-muted-foreground">
                题库规模 <strong className="text-foreground">{ALL_QUESTIONS.length}</strong> 题 ·
                覆盖 <strong className="text-foreground">{YEARS.length}</strong> 个年份 ·
                你的正确率 <strong className="text-primary">{accuracy}%</strong>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ============ 我的学习进度 + 四科速览 ============ */}
      <section className="mx-auto max-w-6xl px-4 py-12">
        <div className="mb-6 flex items-end justify-between">
          <div>
            <h2 className="text-xl font-bold tracking-tight">我的进度</h2>
            <p className="mt-1 text-xs text-muted-foreground">本地保存，随刷随记</p>
          </div>
          <Button variant="ghost" size="sm" onClick={() => go("stats")} className="gap-1 text-muted-foreground">
            <ChartPie className="h-4 w-4" />
            详细数据
          </Button>
        </div>

        <div className="grid gap-4 md:grid-cols-4">
          <Card className="card-raise">
            <CardContent className="p-5">
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>已刷题数</span>
                <PenTool className="h-4 w-4 text-primary" />
              </div>
              <div className="mt-2 text-3xl font-bold tabular-nums">
                {data.attempted}
                <span className="text-base font-normal text-muted-foreground"> / {ALL_QUESTIONS.length}</span>
              </div>
              <Progress value={attemptedPct} className="mt-3 h-1.5" />
              <div className="mt-1.5 text-[11px] text-muted-foreground">题库进度 {attemptedPct}%</div>
            </CardContent>
          </Card>
          <Card className="card-raise">
            <CardContent className="p-5">
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>当前正确率</span>
                <Target className="h-4 w-4 text-primary" />
              </div>
              <div className="mt-2 text-3xl font-bold tabular-nums">{accuracy}%</div>
              <div className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
                累计作答 {data.totalRecords} 次 · 做对 {data.correct} 题
              </div>
            </CardContent>
          </Card>
          <Card className="card-raise cursor-pointer" onClick={() => useApp.getState().go("wrong")}>
            <CardContent className="p-5">
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>待消灭错题</span>
                <RotateCcw className="h-4 w-4 text-rose-500" />
              </div>
              <div className="mt-2 text-3xl font-bold tabular-nums text-rose-600 dark:text-rose-400">
                {data.wrongIds.length}
              </div>
              <div className="mt-3 text-[11px] text-muted-foreground">点击进入错题本重刷 →</div>
            </CardContent>
          </Card>
          <Card className="card-raise">
            <CardContent className="p-5">
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>收藏夹</span>
                <BookMarked className="h-4 w-4 text-amber-500" />
              </div>
              <div className="mt-2 text-3xl font-bold tabular-nums">{data.favoriteIds.length}</div>
              <div className="mt-3 text-[11px] text-muted-foreground">值得反复回看的题</div>
            </CardContent>
          </Card>
        </div>

        <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {SUBJECT_LIST.map((key) => {
            const s = SUBJECTS[key];
            const total = getQuestionsBy({ subject: key }).length;
            const done = data.records.filter((r) => r.questionId.includes(`-${key}-`)).length;
            return (
              <button
                key={key}
                onClick={() => {
                  useApp.getState().setLibFilters({ subject: key });
                  useApp.getState().go("library");
                }}
                className="card-raise group rounded-xl border bg-card p-5 text-left"
              >
                <div className="flex items-center justify-between">
                  <span
                    className="flex h-9 w-9 items-center justify-center rounded-lg text-sm font-bold"
                    style={{ backgroundColor: `${s.color}1a`, color: s.color }}
                  >
                    {s.short}
                  </span>
                  <span className="font-mono text-xs text-muted-foreground">{total} 题</span>
                </div>
                <div className="mt-3 text-sm font-semibold group-hover:text-primary">{s.name}</div>
                <div className="mt-1 text-[11px] leading-relaxed text-muted-foreground">{s.desc}</div>
                <div className="mt-3 flex items-center justify-between text-[11px] text-muted-foreground">
                  <span>满分 {s.score} 分</span>
                  <span className="font-mono">{done} 次作答</span>
                </div>
              </button>
            );
          })}
        </div>
      </section>

      {/* ============ 文章卡片（博客风） ============ */}
      <section className="mx-auto max-w-6xl px-4 pb-16">
        <div className="mb-6 flex items-end justify-between">
          <div>
            <h2 className="text-xl font-bold tracking-tight">刷题指南</h2>
            <p className="mt-1 text-xs text-muted-foreground">来自往年上岸人的实战经验</p>
          </div>
          <button
            onClick={() => go("notes")}
            className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline"
          >
            全部经验笔记 <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {[
            {
              title: "真题至少刷两遍，错题刷到不错为止",
              desc: "第一遍按科目推进，第二遍按年份成套模考。近 10 年真题里藏着 80% 的高频考点，错题本里藏着你的 20% 提分空间。",
              tag: "方法论",
              icon: BookMarked,
              onClick: () => go("library"),
            },
            {
              title: "综合应用题：先手写，再对答案",
              desc: "算法设计题先在纸上写出思路与代码框架，再对照参考答案。直接看答案等于把 13 分的大题变成 2 分的阅读理解。",
              tag: "大题攻略",
              icon: PenTool,
              onClick: () => {
                useApp.getState().setLibFilters({ type: "application" });
                go("library");
              },
            },
            {
              title: "考前一个月：每天一套全真模考",
              desc: "用 3 小时完整模拟 47 题节奏（本站为单科/组卷模式）。训练在时间压力下的取舍策略：单选 2 分钟没思路就先跳过。",
              tag: "冲刺计划",
              icon: Clock3,
              onClick: () => go("mock"),
            },
            {
              title: "全年备考全景：规划 · 分科 · 考场",
              desc: "从试卷基本盘到三阶段时间线，从四科攻略到真题三遍法与考场取舍策略——13 章经验笔记帮你建立完整方法论。",
              tag: "经验笔记",
              icon: NotebookPen,
              onClick: () => go("notes"),
            },
          ].map((post) => (
            <button
              key={post.title}
              onClick={post.onClick}
              className="card-raise group flex flex-col rounded-xl border bg-card p-5 text-left"
            >
              <div className="flex items-center justify-between">
                <span className="rounded-md bg-accent px-2 py-0.5 text-[11px] font-semibold text-primary">
                  {post.tag}
                </span>
                <post.icon className="h-4 w-4 text-muted-foreground/50 transition-colors group-hover:text-primary" />
              </div>
              <h3 className="mt-3 text-sm font-bold leading-snug group-hover:text-primary">{post.title}</h3>
              <p className="mt-2 flex-1 text-xs leading-relaxed text-muted-foreground">{post.desc}</p>
              <span className="mt-4 inline-flex items-center gap-1 text-xs font-medium text-primary opacity-80 transition-opacity group-hover:opacity-100">
                阅读全文 <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
              </span>
            </button>
          ))}
        </div>

        <div className="mt-8 flex flex-wrap items-center gap-3 rounded-xl border bg-card p-5">
          <Flame className="h-5 w-5 text-amber-500" />
          <div className="flex-1 text-sm">
            <span className="font-semibold">坚持就是胜利。</span>
            <span className="ml-2 text-xs text-muted-foreground">
              每天一个科目 10 题，{ALL_QUESTIONS.length} 题题库 ≈ {Math.ceil(ALL_QUESTIONS.length / 40)} 天刷完一轮。
            </span>
          </div>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <CalendarDays className="h-4 w-4" />
            <Database className="h-4 w-4" />
            数据保存在本地浏览器服务中
          </div>
        </div>
      </section>
    </div>
  );
}
