"use client";

import { create } from "zustand";

export type View = "home" | "library" | "practice" | "mock" | "wrong" | "stats" | "notes";

export interface LibFilters {
  year: string; // "all" | "2023" ...
  subject: string; // "all" | "ds" ...
  type: string; // "all" | "single" | "application"
  difficulty: string; // "all" | "1" | "2" | "3"
  tag: string; // "" | tag
  q: string; // 关键字
}

export const DEFAULT_LIB_FILTERS: LibFilters = {
  year: "all",
  subject: "all",
  type: "all",
  difficulty: "all",
  tag: "",
  q: "",
};

export interface PracticeSession {
  queue: string[];
  index: number;
  title: string;
  /** practice | wrong | favorite */
  mode: "practice" | "wrong" | "favorite";
}

interface AppState {
  view: View;
  libFilters: LibFilters;
  practice: PracticeSession | null;
  /** 进度数据版本号，答题后 +1 触发各视图刷新 */
  progressVersion: number;
  go: (view: View) => void;
  setLibFilters: (f: Partial<LibFilters>) => void;
  resetLibFilters: () => void;
  startPractice: (queue: string[], title: string, mode?: PracticeSession["mode"]) => void;
  moveQuestion: (delta: number) => void;
  jumpQuestion: (index: number) => void;
  endPractice: () => void;
  bumpProgress: () => void;
}

export const useApp = create<AppState>((set) => ({
  view: "home",
  libFilters: DEFAULT_LIB_FILTERS,
  practice: null,
  progressVersion: 0,
  go: (view) => {
    set({ view });
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0 });
      window.history.replaceState(null, "", view === "home" ? "/" : `/?v=${view}`);
    }
  },
  setLibFilters: (f) => set((s) => ({ libFilters: { ...s.libFilters, ...f } })),
  resetLibFilters: () => set({ libFilters: DEFAULT_LIB_FILTERS }),
  startPractice: (queue, title, mode = "practice") =>
    set({ view: "practice", practice: { queue, index: 0, title, mode } }),
  moveQuestion: (delta) =>
    set((s) => {
      if (!s.practice) return s;
      const index = Math.max(0, Math.min(s.practice.queue.length - 1, s.practice.index + delta));
      return { practice: { ...s.practice, index } };
    }),
  jumpQuestion: (index) =>
    set((s) => {
      if (!s.practice) return s;
      const i = Math.max(0, Math.min(s.practice.queue.length - 1, index));
      return { practice: { ...s.practice, index: i } };
    }),
  endPractice: () => set({ view: "library", practice: null }),
  bumpProgress: () => set((s) => ({ progressVersion: s.progressVersion + 1 })),
}));
