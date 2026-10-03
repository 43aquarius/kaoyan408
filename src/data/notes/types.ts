/** 408 经验笔记 · 数据类型定义 */

export type NoteBlock =
  /** 普通段落（Markdown 内联语法） */
  | { type: "para"; text: string }
  /** 要点列表 */
  | { type: "list"; items: string[]; ordered?: boolean }
  /** 表格 */
  | { type: "table"; headers: string[]; rows: string[][] }
  /** 提示块：tip=绿灯建议 / warn=黄灯警示 / info=蓝灯背景 */
  | { type: "callout"; variant: "tip" | "warn" | "info"; title: string; text: string }
  /** 卡片栅格（阶段卡、科目卡等） */
  | { type: "card-grid"; cards: { title: string; badge?: string; text: string }[] }
  /** 数字速查卡 */
  | { type: "stat-grid"; stats: { value: string; label: string }[] };

export interface NoteSection {
  /** URL 锚点 id */
  id: string;
  /** 侧边栏标题 */
  title: string;
  /** 分组：plan=规划 / subject=分科 / method=方法 / exam=冲刺 */
  group: "plan" | "subject" | "method" | "exam";
  /** 一句话摘要（侧边栏悬浮提示 & SEO） */
  summary: string;
  /** 内容块 */
  blocks: NoteBlock[];
}

export const NOTE_GROUPS: { key: NoteSection["group"]; label: string }[] = [
  { key: "plan", label: "备考规划" },
  { key: "subject", label: "分科攻略" },
  { key: "method", label: "方法论" },
  { key: "exam", label: "冲刺与考场" },
];
