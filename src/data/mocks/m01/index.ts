import type { Question } from "../../questions/types";
import { m01a } from "./a";
import { m01b } from "./b";
import { m01c } from "./c";
import { m01d } from "./d";
import { m01e } from "./e";
import { m01f } from "./f";

/** 全真模拟卷1（47 题 / 150 分） */
export const m01: Question[] = [...m01a, ...m01b, ...m01c, ...m01d, ...m01e, ...m01f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
