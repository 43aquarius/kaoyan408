import type { Question } from "../types";
import { mc2023Part1 } from "./mc1";
import { mc2023Part2 } from "./mc2";
import { comp2023 } from "./comp";

/** 2023 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）*/
export const questions: Question[] = [...mc2023Part1, ...mc2023Part2, ...comp2023].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
