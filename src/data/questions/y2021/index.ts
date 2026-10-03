import type { Question } from "../types";
import { mc2021Part1 } from "./mc1";
import { mc2021Part2 } from "./mc2";
import { comp2021 } from "./comp";

/** 2021 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）*/
export const questions: Question[] = [...mc2021Part1, ...mc2021Part2, ...comp2021].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
