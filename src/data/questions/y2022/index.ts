import type { Question } from "../types";
import { mc2022Part1 } from "./mc1";
import { mc2022Part2 } from "./mc2";
import { comp2022 } from "./comp";

/** 2022 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）*/
export const questions: Question[] = [...mc2022Part1, ...mc2022Part2, ...comp2022].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
