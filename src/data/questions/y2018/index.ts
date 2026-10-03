import type { Question } from "../types";
import { mc2018Part1 } from "./mc1";
import { mc2018Part2 } from "./mc2";
import { comp2018 } from "./comp";

/** 2018 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）*/
export const questions: Question[] = [...mc2018Part1, ...mc2018Part2, ...comp2018].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
