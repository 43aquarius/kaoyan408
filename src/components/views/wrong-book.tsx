"use client";

import { useMemo, useState } from "react";
import { Bookmark, PenTool, RotateCcw, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Markdown } from "@/components/site/markdown";
import { SubjectBadge, TypeBadge, YearBadge, DifficultyBadge, FavoriteButton } from "@/components/site/badges";
import { useApp } from "@/lib/store";
import { useProgress, toggleFavorite } from "@/lib/client";
import { QUESTION_MAP } from "@/data/questions";
import { cn } from "@/lib/utils";

type Tab = "wrong" | "favorite";

export function WrongBookView() {
  const { startPractice } = useApp();
  const { data, loading } = useProgress();
  const [tab, setTab] = useState<Tab>("wrong");
  const [favVersion, setFavVersion] = useState(0);

  const favSet = useMemo(() => {
    void favVersion;
    return new Set(data.favoriteIds);
  }, [data.favoriteIds, favVersion]);

  const questions = useMemo(
    () =>
      (tab === "wrong" ? data.wrongIds : data.favoriteIds)
        .map((id) => QUESTION_MAP.get(id))
        .filter(Boolean),
    [tab, data.wrongIds, data.favoriteIds]
  );

  const onToggleFav = async (qid: string) => {
    await toggleFavorite(qid);
    setFavVersion((v) => v + 1);
  };

  const start = (mode: "wrong" | "favorite") => {
    const ids = mode === "wrong" ? data.wrongIds : data.favoriteIds;
    if (ids.length === 0) return;
    startPractice(ids, mode === "wrong" ? "错题重刷" : "收藏夹刷题", mode);
  };

  return (
    <div className="fade-in-up mx-auto max-w-4xl px-4 py-8">
      <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">
            错题本 <span className="font-mono text-base font-normal text-muted-foreground">/ review</span>
          </h1>
          <p className="mt-1 text-xs text-muted-foreground">错题会一直留在这里，直到你把它做对</p>
        </div>
        <div className="flex gap-2">
          <Button
            variant={tab === "wrong" ? "default" : "outline"}
            size="sm"
            onClick={() => setTab("wrong")}
            className="gap-1.5"
          >
            <RotateCcw className="h-4 w-4" /> 错题 {data.wrongIds.length}
          </Button>
          <Button
            variant={tab === "favorite" ? "default" : "outline"}
            size="sm"
            onClick={() => setTab("favorite")}
            className="gap-1.5"
          >
            <Bookmark className="h-4 w-4" /> 收藏 {data.favoriteIds.length}
          </Button>
        </div>
      </div>

      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-24 animate-pulse rounded-xl border bg-card" />
          ))}
        </div>
      ) : questions.length === 0 ? (
        <div className="rounded-xl border border-dashed py-16 text-center">
          <Sparkles className="mx-auto h-8 w-8 text-primary/50" />
          <p className="mt-3 text-sm text-muted-foreground">
            {tab === "wrong"
              ? "错题本是空的——要么你很强，要么你还没开始刷 😏"
              : "还没有收藏任何题目，刷题时点击书签图标即可收藏"}
          </p>
          <Button
            className="mt-4"
            variant="outline"
            size="sm"
            onClick={() => useApp.getState().go("library")}
          >
            去题库逛逛
          </Button>
        </div>
      ) : (
        <>
          <Button
            onClick={() => start(tab)}
            className="mb-4 gap-1.5"
            disabled={questions.length === 0}
          >
            <PenTool className="h-4 w-4" />
            {tab === "wrong" ? "重刷全部错题" : "刷一遍收藏夹"}（{questions.length}）
          </Button>
          <div className="space-y-3">
            {questions.map((q) => (
              <article key={q!.id} className="card-raise rounded-xl border bg-card p-4">
                <div className="flex items-start gap-3">
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-1.5">
                      <SubjectBadge subject={q!.subject} />
                      <YearBadge year={q!.year} mockNo={q!.mockNo} />
                      <TypeBadge type={q!.type} />
                      <DifficultyBadge level={q!.difficulty} />
                      <span className="font-mono text-[11px] text-muted-foreground">{q!.id}</span>
                    </div>
                    <div className="mt-2 text-sm leading-relaxed">
                      <Markdown content={q!.content} className="line-clamp-3 [&>p]:!my-0" />
                    </div>
                  </div>
                  <FavoriteButton favorited={favSet.has(q!.id)} onToggle={() => onToggleFav(q!.id)} />
                </div>
                <details className="group mt-2">
                  <summary className="cursor-pointer select-none text-xs font-medium text-primary">
                    查看答案与解析
                  </summary>
                  <div className="mt-2 space-y-3 rounded-lg border bg-muted/20 p-4">
                    <div className="text-sm">
                      <span className="font-semibold">答案：</span>
                      <span className="font-mono font-bold text-primary">
                        {q!.type === "single" ? q!.answer : "见下方参考答案"}
                      </span>
                    </div>
                    {q!.type === "application" && <Markdown content={q!.answer} />}
                    <div>
                      <div className="mb-1 text-sm font-semibold">解析</div>
                      <Markdown content={q!.analysis} />
                    </div>
                  </div>
                </details>
                <button
                  onClick={() => startPractice([q!.id], "单题重刷", "wrong")}
                  className={cn(
                    "mt-2 inline-flex items-center gap-1 text-xs font-medium text-muted-foreground transition-colors hover:text-primary"
                  )}
                >
                  <PenTool className="h-3.5 w-3.5" /> 单独重刷此题
                </button>
              </article>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
