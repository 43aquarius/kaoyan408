export type Subject = "ds" | "co" | "os" | "cn";

export type QuestionType = "single" | "application";

/* ==================== 动画讲解（模拟卷） ==================== */

/** 指针标注（如 i、j、front、rear、top） */
export interface AnimPointer {
  name: string;
  /** 指向 array 的下标 */
  index: number;
}

/** 二叉树节点（递归嵌套） */
export interface AnimTreeNode {
  value: string | number;
  left?: AnimTreeNode | null;
  right?: AnimTreeNode | null;
}

/** 动画的单步状态 */
export interface AnimStep {
  /** 本步骤讲解文本 */
  text: string;
  /** 线性结构（数组 / 队列 / 帧序列 / 哈希表展开等） */
  array?: (string | number | null)[];
  /** array 中高亮的下标 */
  highlights?: number[];
  /** 指针集合 */
  pointers?: AnimPointer[];
  /** 栈（自底向上排列） */
  stack?: (string | number)[];
  /** 栈顶高亮（push/pop 的元素） */
  stackTop?: boolean;
  /** 二叉树 */
  tree?: AnimTreeNode | null;
  /** 高亮的树节点值 */
  treeHighlights?: (string | number)[];
  /** 表格（页表 / Cache 行 / 段表 / 设备表等） */
  table?: { headers: string[]; rows: (string | number)[][] };
  /** 高亮的表格行号（0 起） */
  rowHighlights?: number[];
}

/** 逐步动画讲解 */
export interface ExamAnimation {
  title: string;
  steps: AnimStep[];
}

export interface Question {
  /** 唯一 ID，真题格式: {year}-{subject}-{两位序号}，如 "2009-ds-01"；模拟卷格式: m{卷号}-{subject}-{两位序号}，如 "m01-ds-01" */
  id: string;
  /** 考研年份（2009-2026 真题；2027 = 模拟卷） */
  year: number;
  /** 原卷题号（1-47），不确定可省略 */
  no?: number;
  /** 模拟卷编号（1-10）；真题无此字段 */
  mockNo?: number;
  /** 科目: ds=数据结构 co=计算机组成原理 os=操作系统 cn=计算机网络 */
  subject: Subject;
  /** 题型: single=单项选择题 application=综合应用题 */
  type: QuestionType;
  /** 分值 */
  score: number;
  /** 难度: 1=简单 2=中等 3=较难 */
  difficulty: 1 | 2 | 3;
  /** 题干，Markdown 格式 */
  content: string;
  /** 选项（不含 "A." 前缀）；综合应用题为空数组 */
  options: string[];
  /** 单选: "A"|"B"|"C"|"D"；综合应用题: 完整参考答案（Markdown） */
  answer: string;
  /** 解析，Markdown 格式 */
  analysis: string;
  /** 知识点标签 */
  tags: string[];
  /** 逐项解析（模拟卷）：四个选项各自为什么对 / 为什么错 */
  optionAnalysis?: { A: string; B: string; C: string; D: string };
  /** 讲解配图（public 下路径，如 "/mocks/m01/q13.png"） */
  image?: string;
  /** 逐步动画讲解 */
  animation?: ExamAnimation;
}

export const SUBJECTS: Record<
  Subject,
  { name: string; short: string; en: string; score: number; color: string; desc: string }
> = {
  ds: {
    name: "数据结构",
    short: "数构",
    en: "Data Structures",
    score: 45,
    color: "#10b981",
    desc: "线性表、树与二叉树、图、查找与排序",
  },
  co: {
    name: "计算机组成原理",
    short: "计组",
    en: "Computer Organization",
    score: 45,
    color: "#f59e0b",
    desc: "数据的表示与运算、存储系统、指令系统、CPU 与总线",
  },
  os: {
    name: "操作系统",
    short: "操统",
    en: "Operating Systems",
    score: 35,
    color: "#ef4444",
    desc: "进程管理、内存管理、文件管理、I/O 管理",
  },
  cn: {
    name: "计算机网络",
    short: "计网",
    en: "Computer Networks",
    score: 25,
    color: "#8b5cf6",
    desc: "物理层、数据链路层、网络层、传输层与应用层",
  },
};

export const SUBJECT_LIST: Subject[] = ["ds", "co", "os", "cn"];

export const TYPE_LABEL: Record<QuestionType, string> = {
  single: "单项选择题",
  application: "综合应用题",
};

export const DIFFICULTY_LABEL: Record<number, string> = {
  1: "简单",
  2: "中等",
  3: "较难",
};
