import { NextRequest } from "next/server";
import { db } from "@/lib/db";
import {
  ok,
  fail,
  hashPassword,
  validUsername,
  getVisitorId,
  mergeGuestData,
  createSessionToken,
  SESSION_COOKIE,
  SESSION_TTL,
} from "@/lib/server";

export const dynamic = "force-dynamic";

/** POST /api/auth/register — 注册：用户名 + 密码，成功后自动登录并合并访客数据 */
export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const { name, password } = body as { name?: string; password?: string };

    if (!validUsername(name)) {
      return fail("用户名需 2-20 位，仅限字母、数字、下划线、连字符或中文");
    }
    if (typeof password !== "string" || password.length < 6 || password.length > 64) {
      return fail("密码长度需 6-64 位");
    }

    const exists = await db.user.findUnique({ where: { name } });
    if (exists) {
      return fail("该用户名已被注册");
    }

    const user = await db.user.create({
      data: { name, password: hashPassword(password) },
    });

    // 把当前访客的做题/收藏/模考数据并入新账号
    const guestId = await getVisitorId();
    await mergeGuestData(guestId, user.id);

    const res = ok({ name: user.name, createdAt: user.createdAt.toISOString() });
    res.cookies.set(SESSION_COOKIE, createSessionToken(user.id), {
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      maxAge: SESSION_TTL,
      // 沙箱为 http 预览，不设 secure 以保证 cookie 生效
    });
    return res;
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}
