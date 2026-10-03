# 408刷题志 · kaoyan408.dev

> 近 20 年考研 408 真题原题刷题网站 —— 846 道真题全量收录，程序员博客风的刷题体验。

[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-blue)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-38bdf8)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 项目简介

**408刷题志** 是一个考研计算机学科专业基础综合（科目代码 408）的刷题网站，收录 **2009–2026 共 18 年、每年 47 题、合计 846 道**真题（40 单选 + 7 综合应用的完整卷面结构），并提供备考经验笔记。

风格参考程序员博客（CyC2018/CS-Notes 一脉）：打字机 Hero、hover 浮起卡片、代码复制闪光、顶部阅读进度条、实时 GitHub Star/Fork 计数、亮/暗/系统三态主题平滑切换。

## 题库规模

| 项目 | 数值 |
|---|---|
| 覆盖年份 | 2009–2026（18 年） |
| 每年题量 | 47 题（40 单选 × 2 分 + 7 综合应用共 70 分 = 150 分） |
| 总题量 | **846 题**（单选 720 + 综合 126） |
| 科目分布 | 数据结构 233 · 计组 233 · 操统 218 · 计网 162 |
| 知识点标签 | 892 个 |

各科卷面结构（每年固定）：

| 科目 | 分值 | 单选题号 | 综合题号 |
|---|---|---|---|
| 数据结构 | 45 分 | 1–11 | 41–42 |
| 计算机组成原理 | 45 分 | 12–22 | 43–44 |
| 操作系统 | 35 分 | 23–32 | 45–46 |
| 计算机网络 | 25 分 | 33–40 | 47 |

> 2026 年为回忆版（考试太新，网上尚无完整真题资料，UI 已标注）；其余年份均以真题原题/忠实还原为准，附图题已文字化处理。

## 功能特性

- **题库**：按年份/科目/题型/难度/知识点多维筛选 + 关键字搜索 + 分页；题目卡片展开即答，即时判分
- **刷题模式**：键盘快捷键答题（A-D 选答案、←→ 切题）、答题卡导航、进度记忆
- **模考**：整年原题全真模考（47 题自动建议 180 分钟考场时长）、倒计时、交卷判分、成绩单与试卷回顾
- **错题本**：错题/收藏双 Tab，自动归集，支持整本重刷
- **数据统计**：作答/正确率/科目掌握度等多维图表
- **经验笔记**：13 章备考全景指南（试卷基本盘、全年时间线、四科攻略、真题三遍法、误区避坑、考场策略、共识数字速查卡），整理自知乎/CSDN/B站/博客园及高校官网上岸经验贴
- **刷题记录持久化**：SQLite（Prisma ORM）存储作答记录、收藏、模考成绩

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
│   ├── validate-questions.ts        # 题库校验脚本（全库/单年模式）
│   └── question-agent-instructions.md  # 题库数据生成规范
├── src/
│   ├── app/                  # Next.js App Router（页面 + API 路由）
│   ├── components/
│   │   ├── site/             # 导航/页脚/进度条/主题切换/GitHub计数/Markdown
│   │   ├── views/            # 首页/题库/刷题/模考/错题本/数据/经验笔记
│   │   └── ui/               # shadcn/ui 基础组件
│   ├── data/
│   │   ├── questions/        # 题库（y2009/ ~ y2026/，每年 mc1/mc2/comp/index）
│   │   └── notes/            # 经验笔记结构化数据
│   └── lib/                  # Zustand store / 工具函数
```

## 题库数据说明

- 每年一个目录：`y{年份}/mc1.ts`（题号 1–20）、`mc2.ts`（题号 21–40）、`comp.ts`（题号 41–47）、`index.ts`（聚合导出）
- 题目字段：`id / year / no(卷面题号) / subject / type / score / difficulty / content / options / answer / analysis / tags`
- 综合题答案为 Markdown（按小问分点，含完整解题步骤），解析含「思路点拨 + 评分要点」
- 数据质量：`bun scripts/validate-questions.ts` 校验每年 47 题不重不漏、单选 40/综合 7、综合分值合计 70、ID/格式约束

## API 路由

| 路由 | 方法 | 说明 |
|---|---|---|
| `/api/progress` | GET / POST | 拉取与写入作答记录（匿名设备 ID） |
| `/api/favorite` | GET / POST / DELETE | 收藏管理 |
| `/api/github` | GET | GitHub 实时 Star/Fork 计数（带缓存与 shields.io 备用源） |
| `/api/mock` | POST | 模考交卷判分与成绩存档 |

## 声明

- 本项目题库用于学习交流，题目版权归原命题方所有；2026 年为回忆版
- 经验笔记内容整理自公开经验帖的共识性观点，仅供参考，个体差异客观存在

## License

MIT
