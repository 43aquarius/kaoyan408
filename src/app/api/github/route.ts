import { ok, fail } from "@/lib/server";

export const revalidate = 300; // 缓存 5 分钟，避免频繁调用限额

interface RepoInfo {
  stars: number;
  forks: number;
  fullName: string;
  htmlUrl: string;
  description: string;
}

const REPO = "CyC2018/CS-Notes";

async function parseShieldValue(v: string): Promise<number> {
  // shields.io 返回 "178k" / "178,000" 之类
  const s = v.replace(/,/g, "").trim();
  if (s.endsWith("k")) return Math.round(parseFloat(s) * 1000);
  if (s.endsWith("M")) return Math.round(parseFloat(s) * 1_000_000);
  return parseInt(s, 10) || 0;
}

/** GET /api/github — 实时获取 CS-Notes 仓库 star/fork 数（GitHub API 限流时走 shields.io 备用源） */
export async function GET() {
  try {
    // 主源：GitHub REST API
    let stars = 0;
    let forks = 0;
    let primaryOk = false;
    try {
      const res = await fetch(`https://api.github.com/repos/${REPO}`, {
        headers: {
          Accept: "application/vnd.github+json",
          "User-Agent": "kaoyan-408-site",
        },
        next: { revalidate: 300 },
      });
      if (res.ok) {
        const j = (await res.json()) as {
          stargazers_count?: number;
          forks_count?: number;
        };
        stars = j.stargazers_count ?? 0;
        forks = j.forks_count ?? 0;
        primaryOk = true;
      }
    } catch {
      primaryOk = false;
    }

    // 备用源：shields.io 徽章 JSON
    if (!primaryOk) {
      try {
        const [sRes, fRes] = await Promise.all([
          fetch(`https://img.shields.io/github/stars/${REPO}.json`, {
            next: { revalidate: 300 },
          }),
          fetch(`https://img.shields.io/github/forks/${REPO}.json`, {
            next: { revalidate: 300 },
          }),
        ]);
        if (sRes.ok && fRes.ok) {
          const sJson = (await sRes.json()) as { value?: string };
          const fJson = (await fRes.json()) as { value?: string };
          stars = await parseShieldValue(sJson.value ?? "0");
          forks = await parseShieldValue(fJson.value ?? "0");
          primaryOk = true;
        }
      } catch {
        primaryOk = false;
      }
    }

    if (!primaryOk) return ok<RepoInfo | null>(null);

    return ok<RepoInfo>({
      stars,
      forks,
      fullName: REPO,
      htmlUrl: `https://github.com/${REPO}`,
      description: "技术面试基础知识整理（备用数据源同步中）",
    });
  } catch {
    return fail("GitHub API 请求失败", 502);
  }
}
