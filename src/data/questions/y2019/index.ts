import type { Question } from "../types";
import { mc2019Part1 } from "./mc1";
import { mc2019Part2 } from "./mc2";
import { comp2019 } from "./comp";

/** 2019 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）*/
export const questions: Question[] = [...mc2019Part1, ...mc2019Part2, ...comp2019].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
