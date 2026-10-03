import { NextRequest } from "next/server";
import { db } from "@/lib/db";
import { getVisitorId, ok, fail, parseJson } from "@/lib/server";

export const dynamic = "force-dynamic";

/** GET /api/mock — 模考历史列表 */
export async function GET() {
  try {
    const userId = await getVisitorId();
    const mocks = await db.mockExam.findMany({
      where: { userId },
      orderBy: { createdAt: "desc" },
      take: 50,
    });
    return ok(
      mocks.map((m) => ({
        id: m.id,
        title: m.title,
        questionIds: parseJson<string[]>(m.questionIds, []),
        answers: parseJson<Record<string, string>>(m.answers, {}),
        results: parseJson<Record<string, boolean>>(m.results, {}),
        score: m.score,
        totalScore: m.totalScore,
        correctCnt: m.correctCnt,
        totalCnt: m.totalCnt,
        durationMs: m.durationMs,
        finished: m.finished,
        createdAt: m.createdAt.toISOString(),
      }))
    );
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}

/** POST /api/mock — 创建模考（服务端组卷，防止客户端作弊看答案） */
export async function POST(req: NextRequest) {
  try {
    const body = (await req.json()) as {
      title?: string;
      questionIds?: string[];
      minutes?: number;
    };
    const questionIds = body.questionIds ?? [];
    if (!Array.isArray(questionIds) || questionIds.length === 0) {
      return fail("题目列表为空");
    }
    const userId = await getVisitorId();
    const mock = await db.mockExam.create({
      data: {
        userId,
        title: (body.title ?? "智能模考").slice(0, 100),
        questionIds: JSON.stringify(questionIds),
        answers: "{}",
        results: "{}",
        totalCnt: questionIds.length,
        durationMs: (body.minutes ?? 90) * 60_000,
      },
    });
    return ok({ id: mock.id, createdAt: mock.createdAt.toISOString() });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}

/** PUT /api/mock — 交卷：判分并落库 */
export async function PUT(req: NextRequest) {
  try {
    const body = (await req.json()) as {
      id: string;
      answers: Record<string, string>;
      elapsedMs: number;
    };
    if (!body?.id) return fail("缺少模考 ID");
    const userId = await getVisitorId();
    const mock = await db.mockExam.findFirst({ where: { id: body.id, userId } });
    if (!mock) return fail("模考不存在", 404);

    const { ALL_QUESTIONS } = await import("@/data/questions");
    const qids = parseJson<string[]>(mock.questionIds, []);
    const answers = body.answers ?? {};

    let score = 0;
    let totalScore = 0;
    let correctCnt = 0;
    const results: Record<string, boolean> = {};
    for (const qid of qids) {
      const q = ALL_QUESTIONS.find((x) => x.id === qid);
      if (!q) continue;
      totalScore += q.score;
      const ua = answers[qid];
      // 单选：与标准答案比对；应用题：交卷后自评（__SELF_CORRECT__ / __SELF_WRONG__）
      const correct =
        !!ua &&
        (q.type === "single"
          ? ua === q.answer
          : ua === "__SELF_CORRECT__");
      results[qid] = correct;
      if (correct) {
        score += q.score;
        correctCnt++;
      }
    }

    await db.mockExam.update({
      where: { id: mock.id },
      data: {
        answers: JSON.stringify(answers),
        results: JSON.stringify(results),
        score,
        totalScore,
        correctCnt,
        finished: true,
        durationMs: Math.max(0, Math.min(24 * 3600_000, body.elapsedMs ?? 0)),
      },
    });

    // 写入作答记录（mode=mock）：先清掉旧记录，支持交卷后自评重新判分
    await db.record.deleteMany({ where: { userId, mockId: mock.id } });
    const rs = qids
      .filter((qid) => answers[qid])
      .map((qid) => {
        const q = ALL_QUESTIONS.find((x) => x.id === qid);
        return {
          userId,
          questionId: qid,
          userAnswer: String(answers[qid]).slice(0, 2000),
          isCorrect: results[qid] ?? false,
          mode: "mock",
          mockId: mock.id,
        };
      });
    if (rs.length) await db.record.createMany({ data: rs });

    return ok({ score, totalScore, correctCnt, totalCnt: qids.length, results });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}

/** DELETE /api/mock?id=xx — 删除模考记录 */
export async function DELETE(req: NextRequest) {
  try {
    const id = req.nextUrl.searchParams.get("id");
    if (!id) return fail("缺少 id");
    const userId = await getVisitorId();
    await db.record.deleteMany({ where: { userId, mockId: id } });
    await db.mockExam.deleteMany({ where: { id, userId } });
    return ok({ deleted: true });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}
