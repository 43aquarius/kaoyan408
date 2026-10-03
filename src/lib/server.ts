import { NextResponse } from "next/server";
import { db } from "@/lib/db";

/** 默认访客用户名（无登录系统，单机自用） */
const VISITOR = "visitor";

/** 获取或创建默认访客用户，返回 userId */
export async function getVisitorId(): Promise<string> {
  let user = await db.user.findUnique({ where: { name: VISITOR } });
  if (!user) {
    user = await db.user.create({ data: { name: VISITOR } });
  }
  return user.id;
}

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
