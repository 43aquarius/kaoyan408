import type { Question } from "../../questions/types";
import { m08a } from "./a";
import { m08b } from "./b";
import { m08c } from "./c";
import { m08d } from "./d";
import { m08e } from "./e";
import { m08f } from "./f";

/** 全真模拟卷8（47 题 / 150 分） */
export const m08: Question[] = [...m08a, ...m08b, ...m08c, ...m08d, ...m08e, ...m08f].sort(
  (x, y) => (x.no ?? 999) - (y.no ?? 999)
);
