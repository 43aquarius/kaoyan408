import type { Question } from "../types";
import { mc2017Part1 } from "./mc1";
import { mc2017Part2 } from "./mc2";
import { comp2017 } from "./comp";

/** 2017 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）*/
export const questions: Question[] = [...mc2017Part1, ...mc2017Part2, ...comp2017].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
