import type { Question } from "../../questions/types";
import { m06a } from "./a";
import { m06b } from "./b";
import { m06c } from "./c";
import { m06d } from "./d";
import { m06e } from "./e";
import { m06f } from "./f";

/** 全真模拟卷6（47 题 / 150 分） */
export const m06: Question[] = [...m06a, ...m06b, ...m06c, ...m06d, ...m06e, ...m06f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
