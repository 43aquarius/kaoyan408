import type { Question } from "../../questions/types";
import { m09a } from "./a";
import { m09b } from "./b";
import { m09c } from "./c";
import { m09d } from "./d";
import { m09e } from "./e";
import { m09f } from "./f";

/** 全真模拟卷9（47 题 / 150 分） */
export const m09: Question[] = [...m09a, ...m09b, ...m09c, ...m09d, ...m09e, ...m09f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
