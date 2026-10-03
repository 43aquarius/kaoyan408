export type Subject = "ds" | "co" | "os" | "cn";

export type QuestionType = "single" | "application";

export interface Question {
  /** 唯一 ID，格式: {year}-{subject}-{两位序号}，如 "2009-ds-01" */
  id: string;
  /** 考研年份（2009-2026），即该年 12 月/次年 1 月举行的初试 */
  year: number;
  /** 原卷题号（1-47），不确定可省略 */
  no?: number;
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
