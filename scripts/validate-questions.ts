/** 校验题库数据完整性
 *  全库校验: bun /home/z/my-project/scripts/validate-questions.ts
 *  单年校验: bun /home/z/my-project/scripts/validate-questions.ts --year 2009
 */
import type { Question } from "../src/data/questions/types";

const args = process.argv.slice(2);
const yearIdx = args.indexOf("--year");
const yearArg = yearIdx !== -1 ? Number(args[yearIdx + 1]) : null;

/** 单选科目标准卷面区间（仅告警，不判失败；个别年份 ±1 题以种子题 no 为准） */
const SUBJECT_RANGE: Record<string, [number, number]> = {
  ds: [1, 11],
  co: [12, 22],
  os: [23, 32],
  cn: [33, 40],
};

function checkQuestion(q: Question, ids: Set<string>, errors: string[]) {
  const p = (msg: string) => errors.push(`${q.id}: ${msg}`);
  if (ids.has(q.id)) p("重复 ID");
  ids.add(q.id);
  if (!/^(19|20)\d{2}-(ds|co|os|cn)-\d{2}$/.test(q.id)) p("ID 格式错误");
  if (!Number.isInteger(q.year) || q.year < 2009 || q.year > 2026) p(`年份异常 ${q.year}`);
  if (!["ds", "co", "os", "cn"].includes(q.subject)) p(`科目异常 ${q.subject}`);
  if (!["single", "application"].includes(q.type)) p(`题型异常 ${q.type}`);
  if (typeof q.score !== "number" || q.score <= 0 || q.score > 25) p(`分值异常 ${q.score}`);
  if (![1, 2, 3].includes(q.difficulty)) p(`难度异常 ${q.difficulty}（只能 1|2|3）`);
  if (!q.content || q.content.length < 10) p("题干过短");
  if (q.type === "single") {
    if (!Array.isArray(q.options) || q.options.length !== 4) p(`单选选项数 ${q.options.length} ≠ 4`);
    if (!["A", "B", "C", "D"].includes(q.answer)) p(`单选答案异常 ${q.answer}`);
  } else {
    if (Array.isArray(q.options) && q.options.length !== 0) p("应用题 options 应为空");
    if (!q.answer || q.answer.length < 20) p("应用题答案过短");
  }
  if (!q.analysis || q.analysis.length < 20) p("解析过短");
  if (!Array.isArray(q.tags) || q.tags.length === 0) p("无标签");
  for (const field of [q.content, q.answer, q.analysis, ...(q.options ?? [])]) {
    if (typeof field === "string") {
      if (field.includes("${")) p("存在未转义的 ${");
      if (/\$[^$]*\$/.test(field)) p("疑似 LaTeX");
      if (/<(img|div|span|table|b|i)\b/i.test(field)) p("疑似 HTML 标签");
    }
  }
}

async function main() {
  // ---------- 单年模式：校验全量 47 题结构 ----------
  if (yearArg) {
    if (!Number.isInteger(yearArg) || yearArg < 2009 || yearArg > 2026) {
      console.error("用法: bun scripts/validate-questions.ts --year 2009（2009-2026）");
      process.exit(1);
    }
    let mod: { questions: Question[] };
    try {
      mod = (await import(`../src/data/questions/y${yearArg}/index.ts`)) as { questions: Question[] };
    } catch (e) {
      console.error(`无法加载 src/data/questions/y${yearArg}/index.ts：`, (e as Error).message);
      process.exit(1);
    }
    const qs = mod.questions;
    const errors: string[] = [];
    const ids = new Set<string>();
    for (const q of qs) checkQuestion(q, ids, errors);

    const singles = qs.filter((q) => q.type === "single");
    const apps = qs.filter((q) => q.type === "application");
    if (qs.length !== 47) errors.push(`总题数 ${qs.length} ≠ 47`);
    if (singles.length !== 40) errors.push(`单选数量 ${singles.length} ≠ 40`);
    if (apps.length !== 7) errors.push(`综合题数量 ${apps.length} ≠ 7`);

    // 卷面题号 1-47 不重不漏
    const noCount = new Map<number, number>();
    for (const q of qs) {
      if (q.no === undefined) {
        errors.push(`${q.id}: 缺少卷面题号 no`);
        continue;
      }
      noCount.set(q.no, (noCount.get(q.no) ?? 0) + 1);
    }
    for (let i = 1; i <= 47; i++) {
      const c = noCount.get(i) ?? 0;
      if (c === 0) errors.push(`缺少卷面题号 ${i}`);
      else if (c > 1) errors.push(`卷面题号 ${i} 重复出现 ${c} 次`);
    }
    for (const q of singles) {
      if (q.no === undefined || q.no < 1 || q.no > 40) errors.push(`${q.id}: 单选题号应在 1-40`);
      else if (q.score !== 2) errors.push(`${q.id}: 单选分值应为 2`);
    }
    for (const q of apps) {
      if (q.no === undefined || q.no < 41 || q.no > 47) errors.push(`${q.id}: 综合题号应在 41-47`);
    }
    const appScore = apps.reduce((s, q) => s + q.score, 0);
    if (appScore !== 70) errors.push(`综合题分值合计 ${appScore} ≠ 70`);

    // 科目区间告警（不判失败）
    const warns: string[] = [];
    for (const q of singles) {
      if (q.no === undefined) continue;
      const [lo, hi] = SUBJECT_RANGE[q.subject];
      if (q.no < lo || q.no > hi) warns.push(`${q.id}(no=${q.no})`);
    }

    // 种子题保留检查（旧抽样版文件仍存在时执行）
    try {
      const old = (await import(`../src/data/questions/y${yearArg}.ts`)) as { questions: Question[] };
      const newIds = new Set(qs.map((q) => q.id));
      const missing = old.questions.filter((q) => !newIds.has(q.id)).map((q) => q.id);
      if (missing.length) errors.push(`种子题丢失或被改 id: ${missing.join(", ")}`);
      else console.log(`种子题保留: ${old.questions.length}/${old.questions.length}`);
    } catch {
      console.log("（旧抽样版文件已移除，跳过种子检查）");
    }

    const bySub = qs.reduce<Record<string, number>>((m, q) => ((m[q.subject] = (m[q.subject] ?? 0) + 1), m), {});
    console.log(`\n===== ${yearArg} 年 · ${qs.length} 题（单选 ${singles.length} / 综合 ${apps.length}）=====`);
    console.log("科目分布:", Object.entries(bySub).map(([k, v]) => `${k}=${v}`).join(" "));
    console.log("综合分值:", apps.map((q) => `${q.no}题=${q.score}分`).join(" "), `| 合计 ${appScore}`);
    if (warns.length) console.log("⚠️ 科目区间告警:", warns.join("; "));
    if (errors.length) {
      console.error(`\n❌ 发现 ${errors.length} 个问题:`);
      for (const e of errors) console.error(" -", e);
      process.exit(1);
    }
    console.log(`✅ ${yearArg} 年校验通过\n`);
    return;
  }

  // ---------- 全库模式 ----------
  const { ALL_QUESTIONS, YEARS } = await import("../src/data/questions");
  const ids = new Set<string>();
  const errors: string[] = [];
  let single = 0;
  let app = 0;
  const perYear = new Map<number, number>();
  const perSubject = new Map<string, number>();
  for (const q of ALL_QUESTIONS as Question[]) {
    checkQuestion(q, ids, errors);
    if (q.type === "single") single++;
    else app++;
    perYear.set(q.year, (perYear.get(q.year) ?? 0) + 1);
    perSubject.set(q.subject, (perSubject.get(q.subject) ?? 0) + 1);
  }
  for (const [y, c] of perYear) {
    if (c !== 16 && c !== 47) errors.push(`${y} 年题数 ${c} 异常（应为 16 抽样版或 47 全量版）`);
  }
  const expanded = [...perYear.values()].filter((c) => c === 47).length;
  console.log(`总题数: ${ALL_QUESTIONS.length}（单选 ${single}，应用 ${app}）`);
  console.log(`全量扩充进度: ${expanded}/${perYear.size} 年`);
  console.log(`覆盖年份: ${YEARS.join(", ")}`);
  console.log("各科分布:", [...perSubject.entries()].map(([k, v]) => `${k}=${v}`).join(" "));
  const years = [...perYear.entries()].sort((a, b) => a[0] - b[0]);
  console.log(
    "各年分布:",
    years.map(([y, c]) => `${y}:${c}${c === 47 ? "✓" : "…"}`).join(" ")
  );
  console.log(`知识点标签数: ${new Set(ALL_QUESTIONS.flatMap((q) => q.tags)).size}`);
  if (errors.length) {
    console.error(`\n发现 ${errors.length} 个问题:`);
    for (const e of errors) console.error(" -", e);
    process.exit(1);
  }
  console.log("\n✅ 校验通过，无问题");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
