import { NextRequest } from "next/server";
import { db } from "@/lib/db";
import { getVisitorId, ok, fail } from "@/lib/server";

export const dynamic = "force-dynamic";

/** GET /api/progress — 汇总：做过题数/正确数/各科统计/错题ID/最近记录 */
export async function GET() {
  try {
    const userId = await getVisitorId();
    const [records, favorites, mocks] = await Promise.all([
      db.record.findMany({
        where: { userId },
        orderBy: { createdAt: "desc" },
      }),
      db.favorite.findMany({ where: { userId } }),
      db.mockExam.findMany({
        where: { userId, finished: true },
        orderBy: { createdAt: "desc" },
        take: 20,
      }),
    ]);

    const seen = new Map<string, { isCorrect: boolean; count: number; lastAt: string }>();
    for (const r of records) {
      const prev = seen.get(r.questionId);
      seen.set(r.questionId, {
        isCorrect: r.isCorrect,
        count: (prev?.count ?? 0) + 1,
        lastAt: r.createdAt.toISOString(),
      });
    }
    const wrongIds = [...seen.entries()].filter(([, v]) => !v.isCorrect).map(([k]) => k);
    const masteredIds = [...seen.entries()].filter(([, v]) => v.isCorrect).map(([k]) => k);

    // 按天统计刷题量（近30天）
    const byDay = new Map<string, { total: number; correct: number }>();
    for (const r of records) {
      const day = r.createdAt.toISOString().slice(0, 10);
      const cur = byDay.get(day) ?? { total: 0, correct: 0 };
      cur.total++;
      if (r.isCorrect) cur.correct++;
      byDay.set(day, cur);
    }

    return ok({
      totalRecords: records.length,
      attempted: seen.size,
      correct: masteredIds.length,
      wrongIds,
      masteredIds,
      favoriteIds: favorites.map((f) => f.questionId),
      byDay: Object.fromEntries(byDay),
      records: records.slice(0, 500).map((r) => ({
        id: r.id,
        questionId: r.questionId,
        isCorrect: r.isCorrect,
        userAnswer: r.userAnswer,
        mode: r.mode,
        createdAt: r.createdAt.toISOString(),
      })),
      mocks: mocks.map((m) => ({
        id: m.id,
        title: m.title,
        score: m.score,
        totalScore: m.totalScore,
        correctCnt: m.correctCnt,
        totalCnt: m.totalCnt,
        durationMs: m.durationMs,
        createdAt: m.createdAt.toISOString(),
      })),
    });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}

/** POST /api/progress — 提交一条作答记录 */
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { questionId, userAnswer, isCorrect, mode, mockId, timeMs } = body as {
      questionId: string;
      userAnswer: string;
      isCorrect: boolean;
      mode?: string;
      mockId?: string;
      timeMs?: number;
    };
    if (!questionId || typeof isCorrect !== "boolean" || !userAnswer) {
      return fail("参数不完整");
    }
    const userId = await getVisitorId();
    const rec = await db.record.create({
      data: {
        userId,
        questionId,
        userAnswer: String(userAnswer).slice(0, 2000),
        isCorrect,
        mode: mode ?? "practice",
        mockId,
        timeMs: Math.max(0, Math.min(3_600_000, Number(timeMs) || 0)),
      },
    });
    return ok({ id: rec.id });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}

/** DELETE /api/progress — 清空所有记录（重置） */
export async function DELETE() {
  try {
    const userId = await getVisitorId();
    await db.record.deleteMany({ where: { userId } });
    return ok({ cleared: true });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}
