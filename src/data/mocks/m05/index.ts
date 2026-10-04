import type { Question } from "../../questions/types";
import { m05a } from "./a";
import { m05b } from "./b";
import { m05c } from "./c";
import { m05d } from "./d";
import { m05e } from "./e";
import { m05f } from "./f";

/** 全真模拟卷5（47 题 / 150 分） */
export const m05: Question[] = [...m05a, ...m05b, ...m05c, ...m05d, ...m05e, ...m05f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
