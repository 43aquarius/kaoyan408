import type { Question } from "../types";
import { mc2014Part1 } from "./mc1";
import { mc2014Part2 } from "./mc2";
import { comp2014 } from "./comp";

/**
 * 2014 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）
 * 种子题 16 道（原抽样版，答案已核对）+ 新增 31 道
 */
export const questions: Question[] = [...mc2014Part1, ...mc2014Part2, ...comp2014].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
