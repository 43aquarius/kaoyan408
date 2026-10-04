import type { Question } from "../../questions/types";
import { m04a } from "./a";
import { m04b } from "./b";
import { m04c } from "./c";
import { m04d } from "./d";
import { m04e } from "./e";
import { m04f } from "./f";

/** 全真模拟卷4（47 题 / 150 分） */
export const m04: Question[] = [...m04a, ...m04b, ...m04c, ...m04d, ...m04e, ...m04f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
