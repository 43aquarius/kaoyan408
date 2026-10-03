"use client";

import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, BookMarked, Info, Lightbulb } from "lucide-react";
import { NOTE_SECTIONS, NOTE_GROUPS, type NoteBlock, type NoteSection } from "@/data/notes";
import { Markdown } from "@/components/site/markdown";
import { cn } from "@/lib/utils";

/* ---------- 内容块渲染 ---------- */

const CALLOUT_STYLE = {
  tip: { icon: Lightbulb, cls: "border-emerald-500/40 bg-emerald-500/5", iconCls: "text-emerald-500" },
  warn: { icon: AlertTriangle, cls: "border-amber-500/40 bg-amber-500/5", iconCls: "text-amber-500" },
  info: { icon: Info, cls: "border-sky-500/40 bg-sky-500/5", iconCls: "text-sky-500" },
} as const;

function Block({ block }: { block: NoteBlock }) {
  switch (block.type) {
    case "para":
      return (
        <Markdown
          content={block.text}
          className="text-[15px] leading-7 text-foreground/90 [&_p]:!my-0"
        />
      );

    case "list":
      return block.ordered ? (
        <ol className="ml-1 space-y-2.5">
          {block.items.map((item, i) => (
            <li key={i} className="flex gap-3 text-[15px] leading-7 text-foreground/90">
              <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-md bg-primary/10 font-mono text-xs font-bold text-primary">
                {i + 1}
              </span>
              <Markdown content={item} className="[&_p]:!my-0" />
            </li>
          ))}
        </ol>
      ) : (
        <ul className="ml-1 space-y-2.5">
          {block.items.map((item, i) => (
            <li key={i} className="flex gap-3 text-[15px] leading-7 text-foreground/90">
              <span className="mt-[13px] h-1.5 w-1.5 shrink-0 rounded-full bg-primary/60" />
              <Markdown content={item} className="[&_p]:!my-0" />
            </li>
          ))}
        </ul>
      );

    case "table":
      return (
        <div className="overflow-x-auto rounded-xl border">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-muted/60">
                {block.headers.map((h, i) => (
                  <th key={i} className="whitespace-nowrap px-4 py-2.5 text-left font-semibold">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {block.rows.map((row, i) => (
                <tr key={i} className="border-b last:border-0 hover:bg-muted/30">
                  {row.map((cell, j) => (
                    <td
                      key={j}
                      className={cn("px-4 py-2.5", j === 0 && "whitespace-nowrap font-medium")}
                    >
                      <Markdown content={cell} className="[&_p]:!my-0" />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );

    case "callout": {
      const s = CALLOUT_STYLE[block.variant];
      return (
        <div className={cn("flex gap-3 rounded-xl border p-4", s.cls)}>
          <s.icon className={cn("mt-0.5 h-4.5 w-4.5 shrink-0", s.iconCls)} />
          <div className="min-w-0">
            <p className="mb-1 text-sm font-semibold">{block.title}</p>
            <Markdown content={block.text} className="text-sm leading-6 text-foreground/80 [&_p]:!my-0" />
          </div>
        </div>
      );
    }

    case "card-grid":
      return (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {block.cards.map((card, i) => (
            <div
              key={i}
              className="group rounded-xl border bg-card p-4 transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-md"
            >
              <div className="mb-2 flex items-center justify-between gap-2">
                <p className="text-sm font-semibold">{card.title}</p>
                {card.badge && (
                  <span className="shrink-0 rounded-full bg-primary/10 px-2 py-0.5 font-mono text-[11px] font-medium text-primary">
                    {card.badge}
                  </span>
                )}
              </div>
              <Markdown
                content={card.text}
                className="text-sm leading-6 text-muted-foreground [&_p]:!my-0"
              />
            </div>
          ))}
        </div>
      );

    case "stat-grid":
      return (
        <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
          {block.stats.map((stat, i) => (
            <div key={i} className="rounded-xl border bg-card p-4 text-center">
              <p className="font-mono text-xl font-bold text-primary">{stat.value}</p>
              <p className="mt-1 text-xs leading-5 text-muted-foreground">{stat.label}</p>
            </div>
          ))}
        </div>
      );
  }
}

function Section({ section }: { section: NoteSection }) {
  return (
    <section id={`note-${section.id}`} className="scroll-mt-20 space-y-5">
      <div>
        <h2 className="text-xl font-bold tracking-tight sm:text-2xl">{section.title}</h2>
        <p className="mt-1 text-sm text-muted-foreground">{section.summary}</p>
      </div>
      {section.blocks.map((block, i) => (
        <Block key={i} block={block} />
      ))}
    </section>
  );
}

/* ---------- 视图主体 ---------- */

export function NotesView() {
  const [active, setActive] = useState(NOTE_SECTIONS[0]?.id ?? "");

  const grouped = useMemo(
    () =>
      NOTE_GROUPS.map((g) => ({
        ...g,
        sections: NOTE_SECTIONS.filter((s) => s.group === g.key),
      })).filter((g) => g.sections.length > 0),
    [],
  );

  // 滚动监听：高亮当前阅读的章节
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            const id = e.target.id.replace("note-", "");
            setActive(id);
          }
        }
      },
      { rootMargin: "-15% 0px -70% 0px" },
    );
    for (const s of NOTE_SECTIONS) {
      const el = document.getElementById(`note-${s.id}`);
      if (el) observer.observe(el);
    }
    return () => observer.disconnect();
  }, []);

  const jump = (id: string) => {
    document.getElementById(`note-${id}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      {/* 页头 */}
      <header className="mb-10">
        <p className="mb-2 font-mono text-xs text-primary">{"// experience-notes"}</p>
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
          408 经验笔记
          <span className="ml-3 align-middle font-mono text-sm font-normal text-muted-foreground">
            {NOTE_SECTIONS.length} 章 · 考研408备考全景指南
          </span>
        </h1>
        <p className="mt-3 max-w-2xl text-[15px] leading-7 text-muted-foreground">
          整理自知乎、CSDN、B站、博客园及多所高校官网上岸经验贴的共识性观点——从试卷结构、全年规划、四科攻略到考场策略，
          帮你在刷 846 道真题之前先建立完整的备考方法论。
        </p>
      </header>

      <div className="flex gap-8">
        {/* 侧边栏目录（桌面端） */}
        <aside className="sticky top-20 hidden h-fit w-56 shrink-0 lg:block">
          <nav aria-label="笔记目录" className="space-y-4">
            {grouped.map((g) => (
              <div key={g.key}>
                <p className="mb-1.5 px-3 font-mono text-[11px] uppercase tracking-wider text-muted-foreground/70">
                  {g.label}
                </p>
                <ul className="space-y-0.5 border-l">
                  {g.sections.map((s) => (
                    <li key={s.id}>
                      <button
                        onClick={() => jump(s.id)}
                        title={s.summary}
                        className={cn(
                          "-ml-px w-full border-l-2 px-3 py-1.5 text-left text-[13px] transition-colors",
                          active === s.id
                            ? "border-primary font-medium text-primary"
                            : "border-transparent text-muted-foreground hover:border-primary/40 hover:text-foreground",
                        )}
                      >
                        {s.title}
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </nav>
        </aside>

        {/* 移动端横向章节导航 */}
        <div className="min-w-0 flex-1">
          <div className="mb-8 -mx-4 overflow-x-auto px-4 pb-2 lg:hidden">
            <div className="flex w-max gap-2">
              {NOTE_SECTIONS.map((s) => (
                <button
                  key={s.id}
                  onClick={() => jump(s.id)}
                  className={cn(
                    "whitespace-nowrap rounded-full border px-3 py-1.5 text-xs font-medium transition-colors",
                    active === s.id
                      ? "border-primary bg-primary/10 text-primary"
                      : "border-border text-muted-foreground hover:text-foreground",
                  )}
                >
                  {s.title}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-14">
            {NOTE_SECTIONS.map((section) => (
              <Section key={section.id} section={section} />
            ))}
          </div>

          {/* 页脚 */}
          <footer className="mt-16 flex items-center gap-2 rounded-xl border border-dashed p-4 text-sm text-muted-foreground">
            <BookMarked className="h-4 w-4 shrink-0" />
            <p>
              以上内容为经验帖共识整理，供参考不作保证；个体差异客观存在，请结合自身情况调整。分值结构以当年官方考试大纲为准。
            </p>
          </footer>
        </div>
      </div>
    </div>
  );
}
