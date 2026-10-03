"use client";

import { Star, GitFork, ExternalLink, WifiOff } from "lucide-react";
import { useGitHub, useCountUp, formatNumber } from "@/lib/client";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

/** 实时 GitHub star / fork 计数（数字滚动动画，5 分钟自动刷新） */
export function GitHubCounter({ compact = false }: { compact?: boolean }) {
  const { info, failed } = useGitHub();
  const stars = useCountUp(info?.stars ?? 0);
  const forks = useCountUp(info?.forks ?? 0, 1000);

  if (failed) {
    return (
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <div className="inline-flex items-center gap-1.5 rounded-full border border-dashed border-border px-3 py-1 text-xs text-muted-foreground">
              <WifiOff className="h-3.5 w-3.5" />
              GitHub 实时数据暂不可用
            </div>
          </TooltipTrigger>
          <TooltipContent>网络受限时展示离线模式，不影响刷题功能</TooltipContent>
        </Tooltip>
      </TooltipProvider>
    );
  }

  if (compact) {
    return (
      <a
        href={info?.htmlUrl ?? "https://github.com/CyC2018/CS-Notes"}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-3 rounded-full border bg-card px-3.5 py-1.5 text-xs font-medium tabular-nums transition-colors hover:border-primary/40 hover:text-primary"
        aria-label="GitHub 仓库"
      >
        <span className="inline-flex items-center gap-1">
          <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
          {info ? formatNumber(stars) : "--"}
        </span>
        <span className="inline-flex items-center gap-1">
          <GitFork className="h-3.5 w-3.5 text-muted-foreground" />
          {info ? formatNumber(forks) : "--"}
        </span>
      </a>
    );
  }

  return (
    <div className="grid grid-cols-2 gap-3">
      <a
        href={info?.htmlUrl ?? "https://github.com/CyC2018/CS-Notes"}
        target="_blank"
        rel="noopener noreferrer"
        className="card-raise group flex flex-col gap-1 rounded-xl border bg-card p-4"
        aria-label={`该仓库获得 ${info?.stars ?? 0} 个 star`}
      >
        <span className="flex items-center justify-between text-xs text-muted-foreground">
          <span>Stars</span>
          <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400 transition-transform group-hover:scale-110" />
        </span>
        <span className="count-up-num text-2xl font-bold tracking-tight">
          {info ? formatNumber(stars) : "···"}
        </span>
        <span className="truncate text-[11px] text-muted-foreground">
          {info?.fullName ?? "CyC2018/CS-Notes"}
        </span>
      </a>
      <a
        href={info?.htmlUrl ?? "https://github.com/CyC2018/CS-Notes"}
        target="_blank"
        rel="noopener noreferrer"
        className="card-raise group flex flex-col gap-1 rounded-xl border bg-card p-4"
        aria-label={`该仓库有 ${info?.forks ?? 0} 个 fork`}
      >
        <span className="flex items-center justify-between text-xs text-muted-foreground">
          <span>Forks</span>
          <GitFork className="h-3.5 w-3.5 text-muted-foreground transition-transform group-hover:scale-110" />
        </span>
        <span className="count-up-num text-2xl font-bold tracking-tight">
          {info ? formatNumber(forks) : "···"}
        </span>
        <span className="inline-flex items-center gap-0.5 text-[11px] text-muted-foreground">
          实时同步 <ExternalLink className="h-3 w-3" />
        </span>
      </a>
    </div>
  );
}
