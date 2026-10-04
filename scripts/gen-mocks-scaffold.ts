/**
 * 生成 10 套模拟卷数据骨架：
 * - src/data/mocks/m{NN}/{a,b,c,d}.ts  占位文件（子代理覆写为完整题目）
 * - src/data/mocks/m{NN}/index.ts      合并四部分
 * - public/mocks/m{NN}/                配图目录
 */
import { mkdirSync, writeFileSync } from "fs";

const MOCK_META: { no: number; title: string; subtitle: string; focus: string; difficulty: 1 | 2 | 3 }[] = [
  { no: 1, title: "全真模拟卷（一）", subtitle: "全考点均衡基准卷", focus: "对标 2023-2025 真题考点分布与难度曲线，四科主干考点全覆盖，作为模考基线", difficulty: 2 },
  { no: 2, title: "全真模拟卷（二）", subtitle: "高频计算专项卷", focus: "浮点运算、Cache 命中率、页表地址转换、子网划分、TCP 拥塞窗口等计算重灾区集中训练", difficulty: 3 },
  { no: 3, title: "全真模拟卷（三）", subtitle: "概念辨析强化卷", focus: "易混概念正反对比：存储层次 vs 存取方式、TCP vs UDP、组合 vs 时序、进程 vs 线程", difficulty: 2 },
  { no: 4, title: "全真模拟卷（四）", subtitle: "算法设计深化卷", focus: "数据结构大题为主攻方向：二叉树遍历变形、图算法、排序查找综合、算法设计题完整推演", difficulty: 3 },
  { no: 5, title: "全真模拟卷（五）", subtitle: "系统交叉综合卷", focus: "计组 × 操作系统交叉命题：中断与异常、指令流水线、调度与并发的全链路理解", difficulty: 3 },
  { no: 6, title: "全真模拟卷（六）", subtitle: "网络协议全景卷", focus: "自物理层至应用层逐层深挖，含滑动窗口、路由协议、HTTP/DNS 协议交互过程分析", difficulty: 2 },
  { no: 7, title: "全真模拟卷（七）", subtitle: "难点攻坚卷", focus: "难度上探：AVL 旋转、B 树分裂合并、死锁银行家算法、浮点边界值、路由聚合与 NAT", difficulty: 3 },
  { no: 8, title: "全真模拟卷（八）", subtitle: "基础巩固自查卷", focus: "难度 1-2 为主，适合二轮复习后快速自查基础漏洞，错一题都值得回归教材", difficulty: 1 },
  { no: 9, title: "全真模拟卷（九）", subtitle: "场景应用冲刺卷", focus: "仿真 2024-2026 新题风格：真实场景建模（校园网、存储系统设计、并发程序分析）", difficulty: 2 },
  { no: 10, title: "全真模拟卷（十）", subtitle: "终极押题检验卷", focus: "浓缩十年最高频考点，考前一周终极检验，命中即分数", difficulty: 3 },
];

const BASE = "src/data/mocks";
mkdirSync(BASE, { recursive: true });

for (const m of MOCK_META) {
  const nn = String(m.no).padStart(2, "0");
  const dir = `${BASE}/m${nn}`;
  mkdirSync(dir, { recursive: true });
  mkdirSync(`public/mocks/m${nn}`, { recursive: true });

  // 四个分段占位文件（子代理覆写）
  for (const part of ["a", "b", "c", "d"]) {
    writeFileSync(
      `${dir}/${part}.ts`,
      `import type { Question } from "../../questions/types";\n\n/** 模拟卷${m.no} 第${part.toUpperCase()}段（题号占位，待生成） */\nexport const m${nn}${part}: Question[] = [];\n`
    );
  }

  // 合并索引
  writeFileSync(
    `${dir}/index.ts`,
    `import type { Question } from "../../questions/types";\nimport { m${nn}a } from "./a";\nimport { m${nn}b } from "./b";\nimport { m${nn}c } from "./c";\nimport { m${nn}d } from "./d";\n\n/** 全真模拟卷${m.no}（47 题 / 150 分） */\nexport const m${nn}: Question[] = [...m${nn}a, ...m${nn}b, ...m${nn}c, ...m${nn}d].sort(\n  (x, y) => (x.no ?? 999) - (y.no ?? 999)\n);\n`
  );
}

// 根索引 + 元数据
const imports = MOCK_META.map((m) => `import { m${String(m.no).padStart(2, "0")} } from "./m${String(m.no).padStart(2, "0")}";`).join("\n");
const metaRows = MOCK_META.map(
  (m) =>
    `  { no: ${m.no}, title: "${m.title}", subtitle: "${m.subtitle}", focus: "${m.focus}", difficulty: ${m.difficulty} },`
).join("\n");
const sets = MOCK_META.map((m) => `  m${String(m.no).padStart(2, "0")},`).join("\n");

writeFileSync(
  `${BASE}/index.ts`,
  `import type { Question } from "../questions/types";\n${imports}\n\n/** 模拟卷元数据 */\nexport interface MockMeta {\n  no: number;\n  title: string;\n  subtitle: string;\n  focus: string;\n  /** 整卷难度: 1=基础 2=标准 3=攻坚 */\n  difficulty: 1 | 2 | 3;\n  /** 建议时长（分钟） */\n  durationMin: number;\n}\n\nexport const MOCKS: MockMeta[] = [\n${metaRows}\n].map((m) => ({ ...m, durationMin: 180 }));\n\nconst SETS: Question[][] = [\n${sets}\n];\n\n/** 全部模拟卷题目（10 套 × 47 题） */\nexport const ALL_MOCK_QUESTIONS: Question[] = SETS.flat();\n\n/** 取某一套模拟卷的题目（按卷号 1-10） */\nexport function getMockQuestions(no: number): Question[] {\n  return SETS[no - 1] ?? [];\n}\n\n/** 模拟卷年份标识（与真题 year 区分） */\nexport const MOCK_YEAR = 2027;\n`
);

console.log("scaffold done:", MOCK_META.length, "mocks");
