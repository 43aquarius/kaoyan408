import type { Question } from "../../questions/types";
import { m02a } from "./a";
import { m02b } from "./b";
import { m02c } from "./c";
import { m02d } from "./d";
import { m02e } from "./e";
import { m02f } from "./f";

/** 全真模拟卷2（47 题 / 150 分） */
export const m02: Question[] = [...m02a, ...m02b, ...m02c, ...m02d, ...m02e, ...m02f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
