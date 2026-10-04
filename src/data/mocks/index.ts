import type { Question } from "../questions/types";
import { m01 } from "./m01";
import { m02 } from "./m02";
import { m03 } from "./m03";
import { m04 } from "./m04";
import { m05 } from "./m05";
import { m06 } from "./m06";
import { m07 } from "./m07";
import { m08 } from "./m08";
import { m09 } from "./m09";
import { m10 } from "./m10";

/** 模拟卷元数据 */
export interface MockMeta {
  no: number;
  title: string;
  subtitle: string;
  focus: string;
  /** 整卷难度: 1=基础 2=标准 3=攻坚 */
  difficulty: 1 | 2 | 3;
  /** 建议时长（分钟） */
  durationMin: number;
}

export const MOCKS: MockMeta[] = [
  { no: 1, title: "全真模拟卷（一）", subtitle: "全考点均衡基准卷", focus: "对标 2023-2025 真题考点分布与难度曲线，四科主干考点全覆盖，作为模考基线", difficulty: 2 as 1 | 2 | 3, durationMin: 180 },
  { no: 2, title: "全真模拟卷（二）", subtitle: "高频计算专项卷", focus: "浮点运算、Cache 命中率、页表地址转换、子网划分、TCP 拥塞窗口等计算重灾区集中训练", difficulty: 3 as 1 | 2 | 3, durationMin: 180 },
  { no: 3, title: "全真模拟卷（三）", subtitle: "概念辨析强化卷", focus: "易混概念正反对比：存储层次 vs 存取方式、TCP vs UDP、组合 vs 时序、进程 vs 线程", difficulty: 2 as 1 | 2 | 3, durationMin: 180 },
  { no: 4, title: "全真模拟卷（四）", subtitle: "算法设计深化卷", focus: "数据结构大题为主攻方向：二叉树遍历变形、图算法、排序查找综合、算法设计题完整推演", difficulty: 3 as 1 | 2 | 3, durationMin: 180 },
  { no: 5, title: "全真模拟卷（五）", subtitle: "系统交叉综合卷", focus: "计组 × 操作系统交叉命题：中断与异常、指令流水线、调度与并发的全链路理解", difficulty: 3 as 1 | 2 | 3, durationMin: 180 },
  { no: 6, title: "全真模拟卷（六）", subtitle: "网络协议全景卷", focus: "自物理层至应用层逐层深挖，含滑动窗口、路由协议、HTTP/DNS 协议交互过程分析", difficulty: 2 as 1 | 2 | 3, durationMin: 180 },
  { no: 7, title: "全真模拟卷（七）", subtitle: "难点攻坚卷", focus: "难度上探：AVL 旋转、B 树分裂合并、死锁银行家算法、浮点边界值、路由聚合与 NAT", difficulty: 3 as 1 | 2 | 3, durationMin: 180 },
  { no: 8, title: "全真模拟卷（八）", subtitle: "基础巩固自查卷", focus: "难度 1-2 为主，适合二轮复习后快速自查基础漏洞，错一题都值得回归教材", difficulty: 1 as 1 | 2 | 3, durationMin: 180 },
  { no: 9, title: "全真模拟卷（九）", subtitle: "场景应用冲刺卷", focus: "仿真 2024-2026 新题风格：真实场景建模（校园网、存储系统设计、并发程序分析）", difficulty: 2 as 1 | 2 | 3, durationMin: 180 },
  { no: 10, title: "全真模拟卷（十）", subtitle: "终极押题检验卷", focus: "浓缩十年最高频考点，考前一周终极检验，命中即分数", difficulty: 3 as 1 | 2 | 3, durationMin: 180 },
];

const SETS: Question[][] = [
  m01,
  m02,
  m03,
  m04,
  m05,
  m06,
  m07,
  m08,
  m09,
  m10,
];

/** 全部模拟卷题目（10 套 × 47 题） */
export const ALL_MOCK_QUESTIONS: Question[] = SETS.flat();

/** 取某一套模拟卷的题目（按卷号 1-10） */
export function getMockQuestions(no: number): Question[] {
  return SETS[no - 1] ?? [];
}

/** 模拟卷年份标识（与真题 year 区分） */
export const MOCK_YEAR = 2027;
