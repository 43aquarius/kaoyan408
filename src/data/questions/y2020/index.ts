import type { Question } from "../types";
import { mc2020Part1 } from "./mc1";
import { mc2020Part2 } from "./mc2";
import { comp2020 } from "./comp";

/** 2020 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）*/
export const questions: Question[] = [...mc2020Part1, ...mc2020Part2, ...comp2020].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
