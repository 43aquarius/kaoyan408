import type { Question } from "../../questions/types";
import { m07a } from "./a";
import { m07b } from "./b";
import { m07c } from "./c";
import { m07d } from "./d";
import { m07e } from "./e";
import { m07f } from "./f";

/** 全真模拟卷7（47 题 / 150 分） */
export const m07: Question[] = [...m07a, ...m07b, ...m07c, ...m07d, ...m07e, ...m07f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
