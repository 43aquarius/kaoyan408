import type { NoteSection } from "./types";
import { PLAN_SECTIONS } from "./basics";
import { SUBJECT_SECTIONS } from "./subjects";
import { METHOD_SECTIONS } from "./methods";
import { EXAM_SECTIONS } from "./strategy";

export type { NoteSection, NoteBlock } from "./types";
export { NOTE_GROUPS } from "./types";

/** 全部经验笔记章节（按展示顺序） */
export const NOTE_SECTIONS: NoteSection[] = [
  ...PLAN_SECTIONS,
  ...SUBJECT_SECTIONS,
  ...METHOD_SECTIONS,
  ...EXAM_SECTIONS,
];

export const NOTE_SECTION_MAP = new Map(NOTE_SECTIONS.map((s) => [s.id, s]));
