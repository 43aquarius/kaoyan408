import type { Question } from "../types";
import { mc2026Part1 } from "./mc1";
import { mc2026Part2 } from "./mc2";
import { comp2026 } from "./comp";

/** 2026 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用，回忆版）*/
export const questions: Question[] = [...mc2026Part1, ...mc2026Part2, ...comp2026].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
