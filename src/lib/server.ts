import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createHmac, randomBytes, scryptSync, timingSafeEqual } from "crypto";
import { db } from "@/lib/db";

/** 共享访客用户名（未登录时的做题数据归属） */
const VISITOR = "visitor";

/** 会话 Cookie 名与有效期（30 天） */
export const SESSION_COOKIE = "408_session";
export const SESSION_TTL = 30 * 24 * 3600;

/* ---------------- 密码（scrypt，无外部依赖） ---------------- */

export function hashPassword(password: string): string {
  const salt = randomBytes(16).toString("hex");
  const hash = scryptSync(password, salt, 64).toString("hex");
  return `${salt}:${hash}`;
}

export function verifyPassword(password: string, stored: string): boolean {
  const [salt, hash] = stored.split(":");
  if (!salt || !hash) return false;
  const candidate = scryptSync(password, salt, 64);
  const target = Buffer.from(hash, "hex");
  return candidate.length === target.length && timingSafeEqual(candidate, target);
}

/* ---------------- 会话令牌（HMAC 签名，httpOnly cookie） ---------------- */

function secret(): string {
  return process.env.AUTH_SECRET || "kaoyan408-dev-secret";
}

function sign(payload: string): string {
  return createHmac("sha256", secret()).update(payload).digest("base64url");
}

export function createSessionToken(userId: string): string {
  const exp = Math.floor(Date.now() / 1000) + SESSION_TTL;
  const payload = `${userId}.${exp}`;
  return `${payload}.${sign(payload)}`;
}

export function verifySessionToken(token: string | undefined): string | null {
  if (!token) return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  const [userId, exp, sig] = parts;
  const expected = sign(`${userId}.${exp}`);
  const a = Buffer.from(sig);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !timingSafeEqual(a, b)) return null;
  if (Number(exp) * 1000 < Date.now()) return null;
  return userId;
}

/** 仅读取登录会话（不回退访客），用于 /api/auth/me */
export async function getSessionUser() {
  const store = await cookies();
  const userId = verifySessionToken(store.get(SESSION_COOKIE)?.value);
  if (!userId) return null;
  const user = await db.user.findUnique({ where: { id: userId } });
  if (!user?.password) return null; // 会话必须对应真实账号
  return user;
}

/**
 * 获取当前数据归属的 userId：
 * 1. 已登录 → 账号 id（做题记录持久化到账号，跨设备可同步）
 * 2. 未登录 → 共享访客 id（保持匿名可用，历史数据不丢）
 *
 * 函数名保留 getVisitorId 以兼容既有 API 调用。
 */
export async function getVisitorId(): Promise<string> {
  const user = await getSessionUser();
  if (user) return user.id;

  let guest = await db.user.findUnique({ where: { name: VISITOR } });
  if (!guest) {
    guest = await db.user.create({ data: { name: VISITOR } });
  }
  return guest.id;
}

/** 登录/注册成功后，把当前访客的做题数据并入账号（可迁移） */
export async function mergeGuestData(guestId: string, userId: string): Promise<void> {
  if (guestId === userId) return;
  await db.record.updateMany({ where: { userId: guestId }, data: { userId } });
  await db.favorite.updateMany({ where: { userId: guestId }, data: { userId } });
  await db.mockExam.updateMany({ where: { userId: guestId }, data: { userId } });
}

/** 校验用户名：2-20 位，字母/数字/下划线/连字符/中文 */
export function validUsername(name: unknown): name is string {
  return (
    typeof name === "string" &&
    name.length >= 2 &&
    name.length <= 20 &&
    /^[a-zA-Z0-9_\-\u4e00-\u9fa5]+$/.test(name) &&
    name.toLowerCase() !== VISITOR
  );
}

/* ---------------- 响应工具 ---------------- */

export function ok<T>(data: T) {
  return NextResponse.json({ ok: true, data });
}

export function fail(message: string, status = 400) {
  return NextResponse.json({ ok: false, error: message }, { status });
}

export function parseJson<T>(raw: string, fallback: T): T {
  try {
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}
