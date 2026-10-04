import type { Question } from "./types";
export type { Question, Subject, QuestionType } from "./types";
export { SUBJECTS, SUBJECT_LIST, TYPE_LABEL, DIFFICULTY_LABEL } from "./types";
import { questions as y2009 } from "./y2009";
import { questions as y2010 } from "./y2010";
import { questions as y2011 } from "./y2011";
import { questions as y2012 } from "./y2012";
import { questions as y2013 } from "./y2013";
import { questions as y2014 } from "./y2014";
import { questions as y2015 } from "./y2015";
import { questions as y2016 } from "./y2016";
import { questions as y2017 } from "./y2017";
import { questions as y2018 } from "./y2018";
import { questions as y2019 } from "./y2019";
import { questions as y2020 } from "./y2020";
import { questions as y2021 } from "./y2021";
import { questions as y2022 } from "./y2022";
import { questions as y2023 } from "./y2023";
import { questions as y2024 } from "./y2024";
import { questions as y2025 } from "./y2025";
import { questions as y2026 } from "./y2026";
import { ALL_MOCK_QUESTIONS, MOCK_YEAR } from "../mocks";

/** 回忆版年份：考试太新、网上尚无完整真题资料，由回忆+改编题构成 */
export const RECALL_YEARS: number[] = [2026];

export const ALL_QUESTIONS: Question[] = [
  ...y2009,
  ...y2010,
  ...y2011,
  ...y2012,
  ...y2013,
  ...y2014,
  ...y2015,
  ...y2016,
  ...y2017,
  ...y2018,
  ...y2019,
  ...y2020,
  ...y2021,
  ...y2022,
  ...y2023,
  ...y2024,
  ...y2025,
  ...y2026,
  ...ALL_MOCK_QUESTIONS,
].sort((a, b) => a.year - b.year || a.subject.localeCompare(b.subject) || a.id.localeCompare(b.id));

export const QUESTION_MAP = new Map(ALL_QUESTIONS.map((q) => [q.id, q]));

export const YEARS = [...new Set(ALL_QUESTIONS.map((q) => q.year))].sort((a, b) => b - a);

/** 真题年份（不含模拟卷 2027） */
export const REAL_YEARS = YEARS.filter((y) => y !== MOCK_YEAR);

export const ALL_TAGS = [
  ...new Set(ALL_QUESTIONS.flatMap((q) => q.tags)),
].sort((a, b) => a.localeCompare(b, "zh"));

export function getQuestionsBy(filter: Partial<Record<"year" | "subject" | "type", unknown>>): Question[] {
  // year 用字符串比较：Select 传 "2023"、数据为数字 2023，避免类型不同导致漏匹配
  // "m1"~"m10" 表示按模拟卷单套筛选；"2027"（MOCK_YEAR）为全部模拟卷
  const yearMatch = (q: Question, v: unknown): boolean => {
    if (v === undefined || v === null || v === "all") return true;
    const s = String(v);
    if (/^m([1-9]|10)$/.test(s)) return q.mockNo === Number(s.slice(1));
    return String(q.year) === s;
  };
  return ALL_QUESTIONS.filter(
    (q) =>
      yearMatch(q, filter.year) &&
      (filter.subject === undefined || filter.subject === null || filter.subject === "all" || q.subject === filter.subject) &&
      (filter.type === undefined || filter.type === null || filter.type === "all" || q.type === filter.type)
  );
}

/** 随机打乱数组（Fisher-Yates），返回新数组 */
export function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
