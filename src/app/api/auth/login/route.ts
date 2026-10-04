import { NextRequest } from "next/server";
import { db } from "@/lib/db";
import {
  ok,
  fail,
  verifyPassword,
  getVisitorId,
  mergeGuestData,
  createSessionToken,
  SESSION_COOKIE,
  SESSION_TTL,
} from "@/lib/server";

export const dynamic = "force-dynamic";

/** POST /api/auth/login — 登录：校验密码，合并访客数据，写会话 cookie */
export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const { name, password } = body as { name?: string; password?: string };

    if (typeof name !== "string" || typeof password !== "string" || !name || !password) {
      return fail("请输入用户名和密码");
    }

    const user = await db.user.findUnique({ where: { name } });
    if (!user?.password || !verifyPassword(password, user.password)) {
      return fail("用户名或密码错误");
    }

    // 把当前访客的做题/收藏/模考数据并入账号
    const guestId = await getVisitorId();
    await mergeGuestData(guestId, user.id);

    const res = ok({ name: user.name, createdAt: user.createdAt.toISOString() });
    res.cookies.set(SESSION_COOKIE, createSessionToken(user.id), {
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      maxAge: SESSION_TTL,
    });
    return res;
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}
