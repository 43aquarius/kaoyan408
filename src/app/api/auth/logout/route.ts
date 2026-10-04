import { ok, fail, SESSION_COOKIE } from "@/lib/server";

export const dynamic = "force-dynamic";

/** POST /api/auth/logout — 登出：清除会话 cookie（账号数据保留在服务端） */
export async function POST() {
  try {
    const res = ok({ loggedOut: true });
    res.cookies.set(SESSION_COOKIE, "", {
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      maxAge: 0,
    });
    return res;
  } catch (e) {
    return fail((e as Error).message, 500);
  }
}
