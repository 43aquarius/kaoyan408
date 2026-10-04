# 408刷题志 · kaoyan408.dev

> 近 20 年考研 408 真题 + 10 套全真模拟卷 —— 1316 道题全量收录，每题逐项精讲，程序员博客风的刷题体验。

[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-blue)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-38bdf8)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 项目简介

**408刷题志** 是一个考研计算机学科专业基础综合（科目代码 408）的刷题网站，收录 **2009–2026 共 18 年、每年 47 题、合计 846 道**真题（40 单选 + 7 综合应用的完整卷面结构），以及 **10 套本站自研全真模拟卷（470 题）**——每道单选题的每一个选项都有对错原因讲解，重点题目配 matplotlib 图示与逐步动画推演。

风格参考程序员博客（CyC2018/CS-Notes 一脉）：打字机 Hero、hover 浮起卡片、代码复制闪光、顶部阅读进度条、实时 GitHub Star/Fork 计数、亮/暗/系统三态主题平滑切换。

## 题库规模

| 项目 | 数值 |
|---|---|
| 真题年份 | 2009–2026（18 年，每年 47 题） |
| 模拟卷 | 10 套（每套 47 题，卷面结构与官方一致） |
| 总题量 | **1316 题**（真题 846 + 模拟 470；单选 1120 + 综合 196） |
| 科目分布 | 数据结构 363 · 计组 363 · 操统 328 · 计网 262 |
| 知识点标签 | 1378 个 |
| 模拟卷讲解 | 400 条逐项解析 · 33 张图示 · 26 个逐步动画（311 步） |

各科卷面结构（每年固定）：

| 科目 | 分值 | 单选题号 | 综合题号 |
|---|---|---|---|
| 数据结构 | 45 分 | 1–11 | 41–42 |
| 计算机组成原理 | 45 分 | 12–22 | 43–44 |
| 操作系统 | 35 分 | 23–32 | 45–46 |
| 计算机网络 | 25 分 | 33–40 | 47 |

> 2026 年为回忆版（考试太新，网上尚无完整真题资料，UI 已标注）；其余年份均以真题原题/忠实还原为准，附图题已文字化处理。
>
> 10 套模拟卷分别定位：全考点基准 / 高频计算 / 概念辨析 / 算法深化 / 系统交叉 / 协议全景 / 难点攻坚 / 基础自查 / 场景冲刺 / 终极押题。每套科目分值严格对齐官方（数据结构 45 + 计组 45 + 操统 35 + 计网 25 = 150）。

## 功能特性

- **账号系统**：用户名密码注册/登录（scrypt 密码哈希 + HMAC 签名 httpOnly 会话 Cookie），做题记录/收藏/模考成绩持久化到账号；未登录可访客刷题，登录时自动并入账号
- **题库**：按年份/套卷/科目/题型/难度/知识点多维筛选 + 关键字搜索 + 分页；题目卡片展开即答，即时判分落库
- **刷题模式**：键盘快捷键答题（A-D 选答案、←→ 切题）、答题卡导航、进度记忆
- **模考**：真题整卷 / 模拟卷 / 智能组卷三种模式，全量卷自动建议 180 分钟考场时长、倒计时、交卷判分、成绩单与试卷回顾
- **逐项精讲（模拟卷）**：每道单选四个选项各自的对错原因、推导依据；综合题分小问完整推导 + C 代码
- **图示讲解**：matplotlib 生成的结构图/流程图（Cache 映射、哈夫曼树、流水线时空图、目录树等）
- **动画讲解**：内置 StepPlayer 播放器，数组/指针/栈/二叉树/表格五种可视化，逐步演示排序、页面置换、Dijkstra、BST 判定、TCP 拥塞控制等过程，支持自动播放与步进
- **错题本**：错题/收藏双 Tab，自动归集，支持整本重刷
- **数据统计**：作答/正确率/科目掌握度/年份完成度等多维图表
- **经验笔记**：13 章备考全景指南（试卷基本盘、全年时间线、四科攻略、真题三遍法、误区避坑、考场策略、共识数字速查卡）

## 技术栈

- **框架**：Next.js 16（App Router）+ React 19 + TypeScript
- **样式**：Tailwind CSS 4 + shadcn/ui 组件体系
- **状态**：Zustand（视图路由 / 刷题会话）
- **数据**：静态 TS 题库（`src/data/questions/`，按年份分目录）+ Prisma/SQLite（用户记录）
- **渲染**：react-markdown + remark-gfm（题干/解析/代码块，支持 GFM 表格与复制闪光代码块）

## 快速开始

```bash
# 安装依赖
bun install   # 或 npm install

# 初始化数据库
bunx prisma db push

# 启动开发服务器
bun dev       # 或 npm run dev
```

打开 [http://localhost:3000](http://localhost:3000) 即可使用。

## 目录结构

```
├── prisma/                  # Prisma schema（用户/作答/收藏/模考成绩）
├── scripts/
│   ├── validate-questions.ts        # 题库校验脚本（全库/单年/单套模拟卷模式）
│   ├── mock-agent-spec.md           # 模拟卷生成规范
│   └── mocks/                       # 配图 matplotlib 脚本
├── src/
│   ├── app/                  # Next.js App Router（页面 + API 路由，含 /api/auth/*）
│   ├── components/
│   │   ├── site/             # 导航/页脚/主题切换/Markdown/StepPlayer动画/逐项解析
│   │   ├── views/            # 首页/题库/刷题/模考/错题本/数据/经验笔记
│   │   └── ui/               # shadcn/ui 基础组件
│   ├── data/
│   │   ├── questions/        # 真题题库（y2009/ ~ y2026/）
│   │   ├── mocks/            # 模拟卷（m01/ ~ m10/，每套 a-f 六段）
│   │   └── notes/            # 经验笔记结构化数据
│   └── lib/                  # Zustand store / 认证 / 工具函数
└── public/mocks/             # 模拟卷配图 PNG
```

## 题库数据说明

- 真题：每年一个目录 `y{年份}/mc1.ts`（题号 1–20）、`mc2.ts`（21–40）、`comp.ts`（41–47）、`index.ts`（聚合导出）
- 模拟卷：每套一个目录 `m{卷号}/a~f.ts` 六段（a-c 单选各 12 题、d 含 2 综合、e/f 综合），`year=2027, mockNo=卷号`
- 模拟卷扩展字段：`optionAnalysis`（四选项逐项解析）、`image`（配图路径）、`animation`（逐步动画：array/pointers/stack/tree/table）
- 综合题答案为 Markdown（按小问分点，含完整解题步骤）
- 数据质量：`bun scripts/validate-questions.ts` 校验（真题单年 / 模拟卷单套 / 全库三种模式），含科目分值=官方、逐项解析覆盖、配图存在性、动画有效性等硬校验

## API 路由

| 路由 | 方法 | 说明 |
|---|---|---|
| `/api/auth/register` | POST | 注册（scrypt 哈希，成功自动登录并合并访客数据） |
| `/api/auth/login` | POST | 登录（HMAC 会话 Cookie，30 天） |
| `/api/auth/logout` | POST | 登出 |
| `/api/auth/me` | GET | 当前登录状态 |
| `/api/progress` | GET / POST / DELETE | 拉取与写入作答记录（登录后归账号，访客本地） |
| `/api/favorite` | GET / POST / DELETE | 收藏管理 |
| `/api/github` | GET | GitHub 实时 Star/Fork 计数（带缓存与 shields.io 备用源） |
| `/api/mock` | POST | 模考交卷判分与成绩存档 |

## 声明

- 本项目题库用于学习交流，真题版权归原命题方所有；2026 年为回忆版；10 套模拟卷为本站自研，与任何教辅机构无关
- 经验笔记内容整理自公开经验帖的共识性观点，仅供参考，个体差异客观存在

## License

MIT
