/**
 * 将每套模拟卷从 5 段（a-e）扩展为 6 段（a-f）：
 * - 新增 f.ts 占位
 * - index.ts 合并 a-f
 * 分段结构：a(1-12) b(13-24) c(25-36) d(37-42) e(43-45) f(46-47)
 */
import { writeFileSync, existsSync } from "fs";

const BASE = "src/data/mocks";

for (let no = 1; no <= 10; no++) {
  const nn = String(no).padStart(2, "0");
  const dir = `${BASE}/m${nn}`;

  const fPath = `${dir}/f.ts`;
  if (!existsSync(fPath)) {
    writeFileSync(
      fPath,
      `import type { Question } from "../../questions/types";\n\n/** 模拟卷${no} 第F段（综合题末段，题号占位，待生成） */\nexport const m${nn}f: Question[] = [];\n`
    );
  }

  writeFileSync(
    `${dir}/index.ts`,
    `import type { Question } from "../../questions/types";\nimport { m${nn}a } from "./a";\nimport { m${nn}b } from "./b";\nimport { m${nn}c } from "./c";\nimport { m${nn}d } from "./d";\nimport { m${nn}e } from "./e";\nimport { m${nn}f } from "./f";\n\n/** 全真模拟卷${no}（47 题 / 150 分） */\nexport const m${nn}: Question[] = [...m${nn}a, ...m${nn}b, ...m${nn}c, ...m${nn}d, ...m${nn}e, ...m${nn}f].sort(\n  (x, y) => (x.no ?? 999) - (y.no ?? 999)\n);\n`
  );
}
console.log("6-segment patch done for all 10 mocks");
