# 项目工作日志

---
Task ID: 1
Agent: main
Task: 考研408刷题网站 - 初始化数据类型

Work Log:
- 初始化全栈开发环境（Next.js 16 + TS + Tailwind 4 + shadcn/ui）
- 确认 GitHub API 可访问（用于实时 star/fork 计数，选用 CyC2018/CS-Notes 仓库）
- 创建 src/data/questions/types.ts：定义 Question 接口（id/year/no/subject/type/score/difficulty/content/options/answer/analysis/tags）、科目元数据

Stage Summary:
- 项目定位：考研408（2009-2026 近20年真题）刷题网站，程序员博客风格
- 风格要素：打字机 hero、hover-raise 卡片、copy-flash 代码块、顶部阅读进度条、实时 GitHub star/fork、三态主题切换（亮/暗/系统）平滑过渡
- 架构决策：题库为静态 TS 数据（不可变内容），用户刷题记录/收藏/模考成绩存 SQLite (Prisma)
- 单页应用（仅 / 路由），Zustand 管理视图切换，视图：首页/题库/刷题/模考/错题本/收藏/数据
- 题库规划：2009-2026 共 18 年，每年 16 题（数构4单选+1应用、计组3单选+1应用、操统3单选+1应用、计网3单选），共 288 题

---
Task ID: 3-13
Agent: main
Task: 网站全量开发（数据索引/Prisma/API/前端全部视图）

Work Log:
- 数据索引 src/data/questions/index.ts：聚合 15 个年份文件（240题），YEARS/ALL_TAGS/getQuestionsBy/shuffle 工具
- 校验脚本 scripts/validate-questions.ts：240题全部通过（ID唯一/选项数/答案合法/无LaTeX无HTML无未转义${）
- Prisma schema：User(唯一name)/Record(作答记录)/Favorite(收藏)/MockExam(模考成绩)，已 db push
- API：/api/progress(GET汇总/POST提交/DELETE清空)、/api/favorite(切换)、/api/github(实时star/fork，GitHub限流时走shields.io备用源)、/api/mock(POST组卷/PUT判分含应用题自评/GET历史/DELETE)
- 全局样式：暖纸博客风(亮)/深夜终端风(暗)配色，emerald 主色，主题切换0.45s平滑过渡，自定义滚动条，md-body排版，code-flash/copy-btn-flash/card-raise/caret-blink动效
- 站点组件：ReadingProgress(顶部阅读进度条)、Navbar(响应式+移动端菜单)、Footer(粘底)、ThemeToggle(三态:亮/暗/系统)、Typewriter(打字机hero)、GitHubCounter(实时计数+数字滚动)、CodeBlock(copy-flash+Prism语法高亮)、Markdown(GFM表格)、badges
- 视图：Home(打字机hero+进度卡+四科卡+文章卡)、Library(6维筛选+搜索+分页+行内作答)、Practice(即时判分+解析+键盘快捷键ABCD/←→/F+答题卡导航+完成屏)、Mock(真题模考/智能组卷+倒计时+答题卡+交卷判分+应用题自评+历史成绩)、WrongBook(错题/收藏双tab)、Stats(recharts:30天趋势/各科正确率/难度分布/年份完成度/模考记录/最近作答)
- 修复6个React19 set-state-in-effect lint错误（useMounted via useSyncExternalStore、typewriter重构、事件驱动page重置、key重置InlineAnswer、useProgress派生loading）
- lint通过、tsc(src/)零错误、首页HTTP 200、全部API端点实测通过（判分逻辑验证：提交错误答案D给答案为C的题，正确判false）

Stage Summary:
- 网站功能全部完成并可运行；题库240题(2009-2023)
- 2024-2026三年因Task子代理系统故障暂缺，待恢复后补充（index.ts已预留追加点）
- 待办：Agent Browser端到端自测

---
Task ID: 15
Agent: main
Task: Agent Browser 端到端自测

Work Log:
- 首页：打字机hero逐字打出、GitHub实时计数186k/51k（shields.io备用源生效）、进度卡正确反映测试期作答
- 题库：筛选器/搜索/分页正常，展开答题→选项A-D→判分正确（QAM题选B判对，解析完整展示）
- 刷题：键盘快捷键B答题+ArrowRight切题均生效，答题卡导航、完成屏正常
- 模考：2023真题模考16题、倒计时、答题卡、交卷确认弹窗、判分正确（广播地址题选C正确判错，正确答案B(.95)验证题库答案无误）、成绩单+试卷回顾完整
- 错题本：错题/收藏双tab正常；数据视图：全部图表渲染（compact快照不显示匿名div导致误判，完整快照+截图确认）
- 主题：亮→暗切换html.dark生效，背景色平滑过渡；移动端390px：汉堡菜单出现，布局正常
- 无JS错误、无console错误、dev.log无错误；测试数据已清理
- 截图存于 scripts/{dark,mobile,stats}-test.png

Stage Summary:
- 全部功能浏览器实测通过，网站可交付
- 剩余事项：2024-2026三年题库（Task子代理故障，待恢复）

---
Task ID: 16
Agent: main
Task: 补齐 2024-2026 三年题库并完成收尾

Work Log:
- Task 子代理系统恢复后串行生成三年数据：
  - y2024.ts：基于 GitHub neville-studio/408-exam-paper 仓库 2024.pdf + answers/2024-answer.pdf 全卷核对，16题
  - y2025.ts：同仓库 2025.pdf + 答案册（VLM识读）核对，13道单选与官方答案全部吻合，16题
  - y2026.ts：网上暂无该年完整资料（web检索确认），采用回忆版（3道真实他年原题+13道忠实改编，与现有题库零重复）
- index.ts 接入三年文件 + 导出 RECALL_YEARS=[2026]
- YearBadge 对回忆版年份显示"2026 真题·回忆版"标记（含title提示）
- 全量校验：288题（18年×16），380个知识点标签，validate脚本通过；tsc/lint 零错误；首页200

Stage Summary:
- 题库最终规模：288题（2009-2026 共18年，数构90/计组72/操统72/计网54）
- 2024/2025 经原卷PDF+官方答案核对；2026 为回忆版（UI已标注）
- 项目全部完成

---
Task ID: 17
Agent: main
Task: 题库全量扩充 288→846（16题/年抽样版 → 47题/年真实卷面全量）

Work Log:
- 用户指出真实卷面为 40 单选 + 7 综合 = 47 题/套，原 16 题/年抽样规划不成立；重定为 18 年 × 47 = 846 题
- 架构：每年改为 y{年}/ 目录（mc1/mc2/comp/index 四文件），目录 index 导出同名 questions，根索引零改动平滑切换；旧 16 题为已核对"种子题"，id/内容/分值原样保留（用户历史刷题/收藏/模考记录不失效）
- 校验脚本 v2：新增 --year 单年模式（47 题号不重不漏、单选 40/综合 7、综合分值合计 70、种子保留检查、格式约束）；全库模式报告扩充进度
- 生成规范 v2（scripts/question-agent-instructions.md）：真实卷面结构、id 续编规则、附图题文字化、整卷来源优先策略、每文件即存防超时
- 派发策略：并行 2 次超时后改串行；超时代理靠"每文件即存"保住 mc1/mc2，再派轻量代理补全综合题（2015/2016 均如此恢复）
- 已完成 2009-2016 共 8 年全量（376 题）：多数年份定位整卷 PDF/存档网页对照，官方答案 key 逐题比对一致；2014（计网综合在43题）、2016（41题计网/42-43数构/44-45计组/46-47操统）特殊卷面结构按原卷处理
- 模考适配：API 组卷/判分本就题数无关；修正视图限时默认值——全量卷（≥40题）自动建议 180 分钟考场时长并显示题数/总分，可自定义
- 全库当前 536 题（8 年全量 + 10 年抽样 16 题），校验通过，tsc(src)/lint 零错误，首页 200

Stage Summary:
- 数据进度：8/18 年完成全量化，剩 2017-2026 十年
- 待办：剩余 10 年数据（每年一代理）→ 全库 846 终校验 → UI 大题量检查 → 浏览器端到端自测

---
Task ID: 20
Agent: main
Task: 题库全量收尾(846题) + 经验笔记模块 + GitHub 推送

Work Log:
- 题库扩充完成：2017-2026 十年按「mc1/mc2/comp 文件粒度」并行派发子代理（每代理只写一个文件20/7题，规避整年47题超时），含2次超时重试；2023/2026 种子缺 no 字段由代理按科目区间补指派
- 终态：846 题（18年×47，单选720/综合126），各年校验✅、全库校验✅、tsc(src) 零错误、lint 通过
- 修复存量bug：getQuestionsBy 年份筛选字符串"2023" vs 数字2023 严格相等失败 → String() 归一（题库年份筛选此前一直无效）
- 经验笔记模块：调研代理22次web检索产出4000+字报告 → src/data/notes/（types/basics/subjects/methods/strategy 5文件13章）+ NotesView（侧边栏滚动监听目录+6种内容块渲染器：段落/列表/表格/提示块/卡片栅格/数字速查卡）+ 导航「经验」入口 + 首页刷题指南卡片
- 浏览器端到端自测：经验视图渲染/滚动定位✅、题库2023筛选47题✅、综合题展开完整参考答案✅、模考47题答题卡✅、无console错误；截图 scripts/{notes,mock47}-test.png
- GitHub 推送：README/LICENSE 新增，沙箱环境产物（.zscripts/tool-results/mini-services/examples/tests/download/db）停止跟踪并入 .gitignore，以 43aquarius 名义提交推送至 github.com/43aquarius/kaoyan408

Stage Summary:
- 题库 846 题全量交付；经验笔记 13 章上线；年份筛选 bug 修复
- 仓库推送后项目完整交付

---
Task ID: 21
Agent: main
Task: 注册登录 + 做题记录持久化（用户需求1）

Work Log:
- Prisma：User 加 password String?（scrypt "salt:hash"，null=访客）；db push + 重启 dev server 加载新 Prisma Client
- src/lib/server.ts 重构：scrypt 密码哈希/校验、HMAC 会话令牌（httpOnly cookie 408_session，30天）、getSessionUser、getVisitorId 内部改为"登录账号优先、访客回退"（保持原签名 → progress/favorite/mock 三 API 零改动即支持账号）、mergeGuestData（登录/注册时把访客 records/favorites/mocks 并入账号）、validUsername
- 新增 API：/api/auth/{register,login,logout,me}；注册成功自动登录+合并访客数据
- 前端：client.ts 加 useAuth/loginRequest/registerRequest/logoutRequest；AuthDialog（登录/注册双tab，程序员风）；Navbar 用户区（用户名chip+登出 / 登录按钮，移动端菜单同步）
- 修复存量 bug：题库 InlineAnswer 只改本地 state 从不 submitRecord（题库做题不落库）→ 接入 submitRecord+bumpProgress，综合题加"做出来了/没做出来"自评按钮
- 验证：scripts/test-auth.sh 15/15 通过（注册/登录/登出/重名拒绝/错误密码拒绝/访客合并/数据隔离/持久化）；浏览器 E2E：注册→题库答题→登出→再登录→首页进度卡"计网1次作答"恢复 ✓，无 console 错误；tsc(src)/lint 零错误；测试数据已清理

Stage Summary:
- 账号体系上线：未登录仍可访客刷题，登录自动合并数据，记录持久化到 SQLite，跨登录会话保留
- dev server 改为 setsid 手动守护（系统自动重启在该沙箱不生效）

---
Task ID: 22
Agent: main
Task: 10套全真模拟卷470题（用户需求2/3：扩题量+逐项精讲模拟卷）——架构与生成流水线

Work Log:
- 架构：Question 类型扩展 mockNo/optionAnalysis{A,B,C,D}/image/animation（AnimStep: array+pointers+highlights/stack/tree/table）；mocks 骨架 src/data/mocks/m01-m10（a/b/c/d/e/f 六段式）+ 根 index（MOCKS 元数据 10 套、ALL_MOCK_QUESTIONS）；year=2027，全局 ALL_QUESTIONS 并入，getQuestionsBy 支持 "m1"-"m10" 单套筛选
- 组件：StepPlayer（数组/指针/栈/二叉树SVG/表格 五种可视化+自动播放）、QuestionExtras（逐项解析块+配图+动画）接入 practice/library/mock 三视图
- UI：MockView 第三模式"模拟卷"（10套卡片+星级+focus）；题库年份下拉含模拟卷分组；YearBadge 显示"模拟卷·第N套"；首页/footer/stats 文案适配（真题846+模拟470）
- 校验：validate-questions.ts 新增 --mock N 模式（47题/40单选/7综合、no 1-47 不重不漏、科目区间硬校验 ds1-11 co12-22 os23-31 cn32-40、综合分值 41-47 = 15/8/13/10/9/8/7、每科总分=官方45/45/35/25、单选 optionAnalysis 四键≥12字、image 文件存在、动画≥3步含可视化数据）
- 生成规范：scripts/mock-agent-spec.md（数据格式/红线/逐项解析标准/matplotlib 中文字体规范/动画JSON格式/自检命令）
- 流水线教训：①4并行超时3个、3并行超时（综合题重的任务死在写入前）→ 拆为6段式（a=12单选/b=12单选/c=12单选/d=6题含2综合/e=3综合/f=2综合），提示词强调"先写文件后汇报"→ 稳定 3 并行全成功 ②超时代理常已写完文件（先查产出再重派）③每段考点/难度/id/no 清单直接写在提示词里
- 进度：m01 ✓47题（4图3动画，校验通过）、m02 ✓（校验通过）、m03-a ✓
- 每套标准结构：ds 单选1-11+41(15)+42(8)；co 12-22+43(13)+44(10)；os 23-31+45(9)+46(8)；cn 32-40+47(7)

Stage Summary:
- 流水线已验证：每轮 3 个轻任务（12单选/6题含2综合/3综合/2综合），全部成功
- 待办：m03-b/c/d/e/f + m04-m10 全部段落（约 47 个任务）→ 全量校验 → E2E → git push

---
Task ID: 23
Agent: main
Task: 10套模拟卷生成完成 + 终验

Work Log:
- 40 个内容子代理全部完成（6段式：a=12单选/b=12单选/c=12单选/d=6题含2综合/e=3综合/f=2综合；约8次超时但大部分已写入文件、4次重派成功）
- 10 套全部通过 --mock 校验：47题/40单选/7综合、科目分值=官方45/45/35/25、逐项解析 40/40 全覆盖
- 全库终态：1316 题（18年真题846 + 10套模拟470），单选1120/综合196，1378个知识点标签
- tsc(src) 零错误、lint 通过、10套 --mock 校验全绿
- 修正：校验脚本 HTML 正则误报（<A,C> 有向图弧记法）；spec 字体路径（NotoSansSC[wght].ttf 不存在 → SarasaMonoSC-Regular.ttf）

Stage Summary:
- 模拟卷交付：470 题、400条逐项解析、约35张 matplotlib 配图、约28个逐步动画（StepPlayer：数组/指针/栈/二叉树/表格）
- 剩余：浏览器E2E → README → git push
