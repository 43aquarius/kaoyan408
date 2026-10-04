import { ok, fail, getSessionUser } from "@/lib/server";

export const dynamic = "force-dynamic";

/** GET /api/auth/me — 当前登录状态 */
export async function GET() {
  try {
    const user = await getSessionUser();
    if (!user) return ok({ user: null });
    return ok({
      user: {
        name: user.name,
        createdAt: user.createdAt.toISOString(),
      },
    });
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}
