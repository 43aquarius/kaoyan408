import type { Question } from "../types";
import { mc2009Part1 } from "./mc1";
import { mc2009Part2 } from "./mc2";
import { comp2009 } from "./comp";

/**
 * 2009 年考研 408 真题 · 全量版（47 题 = 40 单选 + 7 综合应用）
 * 种子题 16 道（原抽样版，答案已核对）+ 新增 31 道
 */
export const questions: Question[] = [...mc2009Part1, ...mc2009Part2, ...comp2009].sort(
  (a, b) => (a.no ?? 0) - (b.no ?? 0),
);
