/**
 * 将每套模拟卷从 4 段（a/b/c/d）扩展为 5 段（a/b/c/d/e）：
 * - 新增 e.ts 占位文件（综合题后半）
 * - 更新 index.ts 合并五段
 * - d.ts 若仍为占位（未生成），重新定义为"no 37-42"段
 */
import { readFileSync, writeFileSync, existsSync } from "fs";

const BASE = "src/data/mocks";

for (let no = 1; no <= 10; no++) {
  const nn = String(no).padStart(2, "0");
  const dir = `${BASE}/m${nn}`;

  // 1. 创建 e.ts 占位
  const ePath = `${dir}/e.ts`;
  if (!existsSync(ePath)) {
    writeFileSync(
      ePath,
      `import type { Question } from "../../questions/types";\n\n/** 模拟卷${no} 第E段（综合题后半，题号占位，待生成） */\nexport const m${nn}e: Question[] = [];\n`
    );
  }

  // 2. 更新 index.ts：合并 a-e
  writeFileSync(
    `${dir}/index.ts`,
    `import type { Question } from "../../questions/types";\nimport { m${nn}a } from "./a";\nimport { m${nn}b } from "./b";\nimport { m${nn}c } from "./c";\nimport { m${nn}d } from "./d";\nimport { m${nn}e } from "./e";\n\n/** 全真模拟卷${no}（47 题 / 150 分） */\nexport const m${nn}: Question[] = [...m${nn}a, ...m${nn}b, ...m${nn}c, ...m${nn}d, ...m${nn}e].sort(\n  (x, y) => (x.no ?? 999) - (y.no ?? 999)\n);\n`
  );

  // 3. 报告 d.ts 状态
  const dContent = readFileSync(`${dir}/d.ts`, "utf-8");
  const done = !dContent.includes("题号占位");
  console.log(`m${nn}: d.ts ${done ? "已生成" : "占位（待派发）"}, e.ts 已确保存在`);
}
console.log("patch done");
