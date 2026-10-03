import { NextRequest } from "next/server";
import { db } from "@/lib/db";
import { getVisitorId, ok, fail } from "@/lib/server";

export const dynamic = "force-dynamic";

/** POST /api/favorite — 切换收藏 */
export async function POST(req: NextRequest) {
  try {
    const { questionId } = (await req.json()) as { questionId: string };
    if (!questionId) return fail("缺少 questionId");
    const userId = await getVisitorId();
    const existing = await db.favorite.findUnique({
      where: { userId_questionId: { userId, questionId } },
    });
    if (existing) {
      await db.favorite.delete({ where: { id: existing.id } });
      return ok({ favorited: false });
    }
    await db.favorite.create({ data: { userId, questionId } });
    return ok({ favorited: true });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}

/** DELETE /api/favorite?questionId=xx — 取消收藏 */
export async function DELETE(req: NextRequest) {
  try {
    const questionId = req.nextUrl.searchParams.get("questionId");
    if (!questionId) return fail("缺少 questionId");
    const userId = await getVisitorId();
    await db.favorite.deleteMany({ where: { userId, questionId } });
    return ok({ favorited: false });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}
