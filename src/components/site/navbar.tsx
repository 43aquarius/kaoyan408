"use client";

import { useState } from "react";
import { BookOpen, GraduationCap, LayoutGrid, Menu, NotebookPen, PenTool, ChartPie, RotateCcw, X } from "lucide-react";
import { useApp, type View } from "@/lib/store";
import { ThemeToggle } from "./theme-toggle";
import { GitHubCounter } from "./github-counter";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const NAV_ITEMS: { key: View; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
  { key: "home", label: "首页", icon: GraduationCap },
  { key: "library", label: "题库", icon: LayoutGrid },
  { key: "practice", label: "刷题", icon: PenTool },
  { key: "mock", label: "模考", icon: BookOpen },
  { key: "wrong", label: "错题本", icon: RotateCcw },
  { key: "stats", label: "数据", icon: ChartPie },
  { key: "notes", label: "经验", icon: NotebookPen },
];

export function Navbar() {
  const { view, go, practice } = useApp();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleNav = (v: View) => {
    if (v === "practice" && !practice) {
      // 没有进行中的刷题会话 → 去题库选题
      go("library");
      return;
    }
    go(v);
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-6xl items-center gap-4 px-4">
        <button
          onClick={() => go("home")}
          className="flex items-center gap-2 font-bold tracking-tight"
          aria-label="回到首页"
        >
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary font-mono text-xs font-bold text-primary-foreground">
            408
          </span>
          <span className="text-[15px]">
            刷题志<span className="ml-1.5 hidden font-mono text-xs font-normal text-muted-foreground sm:inline">kaoyan408.dev</span>
          </span>
        </button>

        <nav className="hidden items-center gap-0.5 md:flex" aria-label="主导航">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.key}
              onClick={() => handleNav(item.key)}
              className={cn(
                "relative rounded-md px-3 py-1.5 text-sm font-medium transition-colors",
                view === item.key
                  ? "text-primary"
                  : "text-muted-foreground hover:bg-accent/60 hover:text-foreground"
              )}
              aria-current={view === item.key ? "page" : undefined}
            >
              <span className="flex items-center gap-1.5">
                <item.icon className="h-3.5 w-3.5" />
                {item.label}
              </span>
              {view === item.key && (
                <span className="absolute inset-x-3 -bottom-[13px] h-0.5 rounded-full bg-primary" />
              )}
            </button>
          ))}
        </nav>

        <div className="ml-auto flex items-center gap-2">
          <div className="hidden sm:block">
            <GitHubCounter compact />
          </div>
          <ThemeToggle />
          <Button
            variant="ghost"
            size="icon"
            className="h-9 w-9 md:hidden"
            onClick={() => setMobileOpen((v) => !v)}
            aria-label={mobileOpen ? "关闭菜单" : "打开菜单"}
            aria-expanded={mobileOpen}
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
        </div>
      </div>

      {mobileOpen && (
        <nav className="border-t bg-background px-4 py-2 md:hidden" aria-label="移动端导航">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.key}
              onClick={() => {
                handleNav(item.key);
                setMobileOpen(false);
              }}
              className={cn(
                "flex w-full items-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium",
                view === item.key ? "bg-accent text-primary" : "text-muted-foreground"
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </button>
          ))}
        </nav>
      )}
    </header>
  );
}
