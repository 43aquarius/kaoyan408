import type { Question } from "../../questions/types";
import { m03a } from "./a";
import { m03b } from "./b";
import { m03c } from "./c";
import { m03d } from "./d";
import { m03e } from "./e";
import { m03f } from "./f";

/** 全真模拟卷3（47 题 / 150 分） */
export const m03: Question[] = [...m03a, ...m03b, ...m03c, ...m03d, ...m03e, ...m03f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
