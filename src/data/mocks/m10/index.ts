import type { Question } from "../../questions/types";
import { m10a } from "./a";
import { m10b } from "./b";
import { m10c } from "./c";
import { m10d } from "./d";
import { m10e } from "./e";
import { m10f } from "./f";

/** 全真模拟卷10（47 题 / 150 分） */
export const m10: Question[] = [...m10a, ...m10b, ...m10c, ...m10d, ...m10e, ...m10f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
