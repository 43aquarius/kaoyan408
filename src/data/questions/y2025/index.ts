import type { Question } from "../types";
import { mc2025Part1 } from "./mc1";
import { mc2025Part2 } from "./mc2";
import { comp2025 } from "./comp";

/** 2025 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）*/
export const questions: Question[] = [...mc2025Part1, ...mc2025Part2, ...comp2025].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
