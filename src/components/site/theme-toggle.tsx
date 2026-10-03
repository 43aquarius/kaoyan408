"use client";

import { useRef } from "react";
import { useTheme } from "next-themes";
import { Moon, Sun, Monitor } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useMounted } from "@/lib/client";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

/**
 * 三态主题切换（亮 / 暗 / 跟随系统）。
 * 切换时在 html 上临时加 .theme-transition 类，
 * 让全站色彩以 0.45s 平滑过渡（globals.css 中定义）。
 */
export function ThemeToggle() {
  const { setTheme, resolvedTheme, theme } = useTheme();
  const mounted = useMounted();
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const switchTo = (next: string) => {
    const root = document.documentElement;
    if (timer.current) clearTimeout(timer.current);
    root.classList.add("theme-transition");
    setTheme(next);
    // 等过渡结束后移除，避免影响日常 hover 过渡
    timer.current = setTimeout(() => root.classList.remove("theme-transition"), 500);
  };

  const current = mounted ? (theme === "system" ? "system" : resolvedTheme) : "system";

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="relative h-9 w-9" aria-label="切换主题">
          <Sun
            className={`h-[1.15rem] w-[1.15rem] transition-all duration-300 ${
              current === "light" ? "scale-100 rotate-0 opacity-100" : "scale-50 -rotate-90 opacity-0"
            } absolute`}
          />
          <Moon
            className={`h-[1.15rem] w-[1.15rem] transition-all duration-300 ${
              current === "dark" ? "scale-100 rotate-0 opacity-100" : "scale-50 rotate-90 opacity-0"
            } absolute`}
          />
          <Monitor
            className={`h-[1.15rem] w-[1.15rem] transition-all duration-300 ${
              current === "system" ? "scale-100 rotate-0 opacity-100" : "scale-50 rotate-90 opacity-0"
            } absolute`}
          />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="min-w-32">
        <DropdownMenuItem onClick={() => switchTo("light")} aria-label="浅色模式">
          <Sun className="mr-2 h-4 w-4" />
          浅色
          {current === "light" && <span className="ml-auto text-primary">·</span>}
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => switchTo("dark")} aria-label="深色模式">
          <Moon className="mr-2 h-4 w-4" />
          深色
          {current === "dark" && <span className="ml-auto text-primary">·</span>}
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => switchTo("system")} aria-label="跟随系统">
          <Monitor className="mr-2 h-4 w-4" />
          跟随系统
          {current === "system" && <span className="ml-auto text-primary">·</span>}
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
