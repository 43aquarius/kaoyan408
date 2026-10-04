"use client";

import { useCallback, useEffect, useState, useSyncExternalStore } from "react";
import { useApp } from "@/lib/store";

const emptySubscribe = () => () => {};

/** hydration 安全的 mounted 标记（不触发 set-state-in-effect） */
export function useMounted() {
  return useSyncExternalStore(
    emptySubscribe,
    () => true,
    () => false
  );
}

export interface ProgressData {
  totalRecords: number;
  attempted: number;
  correct: number;
  wrongIds: string[];
  masteredIds: string[];
  favoriteIds: string[];
  byDay: Record<string, { total: number; correct: number }>;
  records: {
    id: string;
    questionId: string;
    isCorrect: boolean;
    userAnswer: string;
    mode: string;
    createdAt: string;
  }[];
  mocks: {
    id: string;
    title: string;
    score: number;
    totalScore: number;
    correctCnt: number;
    totalCnt: number;
    durationMs: number;
    createdAt: string;
  }[];
}

const EMPTY: ProgressData = {
  totalRecords: 0,
  attempted: 0,
  correct: 0,
  wrongIds: [],
  masteredIds: [],
  favoriteIds: [],
  byDay: {},
  records: [],
  mocks: [],
};

/** 全局进度数据 Hook：progressVersion 变化时自动刷新 */
export function useProgress() {
  const version = useApp((s) => s.progressVersion);
  // 用 appliedVersion 派生 loading，避免在 effect 体内同步 setState
  const [snapshot, setSnapshot] = useState<{ applied: number; data: ProgressData }>({
    applied: -1,
    data: EMPTY,
  });
  const loading = snapshot.applied !== version;

  useEffect(() => {
    let alive = true;
    fetch("/api/progress")
      .then((r) => r.json())
      .then((j) => {
        if (alive) {
          setSnapshot({
            applied: version,
            data: j?.ok ? (j.data as ProgressData) : EMPTY,
          });
        }
      })
      .catch(() => {
        // 失败时也解除 loading（保持/重置为空数据）
        if (alive) setSnapshot((s) => ({ applied: version, data: s.data }));
      });
    return () => {
      alive = false;
    };
  }, [version]);

  return { data: snapshot.data, loading };
}

/** 提交一条作答记录 */
export async function submitRecord(body: {
  questionId: string;
  userAnswer: string;
  isCorrect: boolean;
  mode?: string;
  mockId?: string;
  timeMs?: number;
}) {
  try {
    await fetch("/api/progress", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } catch {
    /* 本地记录失败不阻断交互 */
  }
}

/** 切换收藏 */
export async function toggleFavorite(questionId: string): Promise<boolean> {
  try {
    const r = await fetch("/api/favorite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ questionId }),
    });
    const j = await r.json();
    return !!j?.data?.favorited;
  } catch {
    return false;
  }
}

export interface GitHubInfo {
  stars: number;
  forks: number;
  fullName: string;
  htmlUrl: string;
  description: string;
}

/** GitHub 实时数据（5 分钟自动刷新） */
export function useGitHub() {
  const [info, setInfo] = useState<GitHubInfo | null>(null);
  const [failed, setFailed] = useState(false);

  const load = useCallback(() => {
    fetch("/api/github")
      .then((r) => r.json())
      .then((j) => {
        if (j?.ok && j.data) setInfo(j.data as GitHubInfo);
        else setFailed(true);
      })
      .catch(() => setFailed(true));
  }, []);

  useEffect(() => {
    load();
    const t = setInterval(load, 5 * 60 * 1000);
    return () => clearInterval(t);
  }, [load]);

  return { info, failed };
}

/** 数字滚动动画（GitHub 计数用） */
export function useCountUp(target: number, duration = 1200) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (target <= 0) return;
    let raf = 0;
    const start = performance.now();
    const from = 0;
    const tick = (now: number) => {
      const p = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setValue(Math.round(from + (target - from) * eased));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, duration]);
  return value;
}

export function formatNumber(n: number): string {
  if (n >= 10000) return `${(n / 1000).toFixed(1)}k`;
  return n.toLocaleString("en-US");
}

/* ==================== 注册 / 登录 ==================== */

export interface AuthUser {
  name: string;
  createdAt: string;
}

interface AuthResult {
  ok: boolean;
  error?: string;
  user?: AuthUser;
}

async function authPost(path: string, body: Record<string, unknown>): Promise<AuthResult> {
  try {
    const r = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return (await r.json()) as AuthResult;
  } catch {
    return { ok: false, error: "网络异常，请稍后重试" };
  }
}

export function loginRequest(name: string, password: string) {
  return authPost("/api/auth/login", { name, password });
}

export function registerRequest(name: string, password: string) {
  return authPost("/api/auth/register", { name, password });
}

export async function logoutRequest(): Promise<void> {
  try {
    await fetch("/api/auth/logout", { method: "POST" });
  } catch {
    /* ignore */
  }
}

/** 当前登录用户（null = 访客模式） */
export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    fetch("/api/auth/me")
      .then((r) => r.json())
      .then((j) => {
        if (!alive) return;
        setUser(j?.ok ? (j.data?.user ?? null) : null);
        setLoading(false);
      })
      .catch(() => {
        if (alive) setLoading(false);
      });
    return () => {
      alive = false;
    };
  }, []);

  /** 事件处理器中手动刷新（登录/登出后调用） */
  const refresh = useCallback(async () => {
    try {
      const r = await fetch("/api/auth/me");
      const j = await r.json();
      setUser(j?.ok ? (j.data?.user ?? null) : null);
    } catch {
      /* ignore */
    }
  }, []);

  return { user, loading, refresh };
}
