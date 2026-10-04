# 全真模拟卷三 B 段 第15题（m03-co-04）配图：SRAM / DRAM / ROM 三类存储器对比
# 三列卡片：单元结构示意 + 特性标注 + 典型用途
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm

# 环境无 NotoSansSC-Regular.ttf，改用可用的文泉驿正黑（中文字体，已验证无缺字）
fm.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
fm.fontManager.addfont("/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon

plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "Sarasa Mono SC"]
plt.rcParams["axes.unicode_minus"] = False

WIRE = "#1f2937"
LW = 1.8

fig, ax = plt.subplots(figsize=(11, 7.2), dpi=150, constrained_layout=True)
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis("off")

CARDS = [
    {"x0": 0.3, "theme": "#d97706", "bg": "#fffbeb", "title": "SRAM（静态存储器）",
     "sub": "存储原理：双稳态触发器",
     "features": ["刷新：不需要（触发器自保持）", "读出：非破坏性，无需重写",
                  "速度：快，接近 CPU 节奏", "集成度：低，位成本高", "易失性：断电即丢失"],
     "usage": "Cache、寄存器组"},
    {"x0": 4.3, "theme": "#2563eb", "bg": "#eff6ff", "title": "DRAM（动态存储器）",
     "sub": "存储原理：1 管 1 电容",
     "features": ["刷新：需定期逐行再生", "读出：破坏性，读后须重写",
                  "速度：较 SRAM 慢", "集成度：高，位成本低", "易失性：断电即丢失"],
     "usage": "主存（内存条）、显存"},
    {"x0": 8.3, "theme": "#059669", "bg": "#ecfdf5", "title": "ROM（只读存储器）",
     "sub": "存储原理：交叉点是否制作管",
     "features": ["刷新：不需要（非易失）", "读出：随机读取较快",
                  "写入：整体或块擦写，受限", "集成度：高，位成本低", "易失性：断电仍保留"],
     "usage": "BIOS 固件、嵌入式程序"},
]


def draw_sram_cell(x0):
    # 两个交叉耦合的反相器（双稳态触发器）
    ax.plot([x0 + 0.55, x0 + 1.0], [6.7, 6.7], color=WIRE, lw=LW)          # 左输入线
    ax.plot([x0 + 2.4, x0 + 2.85], [6.7, 6.7], color=WIRE, lw=LW)          # 右输入线
    ax.add_patch(Polygon([(x0 + 1.0, 6.35), (x0 + 1.0, 7.05), (x0 + 1.62, 6.7)],
                         closed=True, facecolor="#fde68a", edgecolor=WIRE, lw=LW))
    ax.add_patch(Polygon([(x0 + 2.4, 6.35), (x0 + 2.4, 7.05), (x0 + 1.78, 6.7)],
                         closed=True, facecolor="#fde68a", edgecolor=WIRE, lw=LW))
    ax.plot([x0 + 1.62, x0 + 1.62, x0 + 2.85, x0 + 2.85], [6.7, 7.6, 7.6, 6.7],
            color=WIRE, lw=LW)                                              # 上反馈线
    ax.plot([x0 + 1.78, x0 + 1.78, x0 + 0.55, x0 + 0.55], [6.7, 5.85, 5.85, 6.7],
            color=WIRE, lw=LW)                                              # 下反馈线
    ax.add_patch(Circle((x0 + 0.55, 6.7), 0.05, facecolor=WIRE, edgecolor=WIRE))
    ax.add_patch(Circle((x0 + 2.85, 6.7), 0.05, facecolor=WIRE, edgecolor=WIRE))
    ax.text(x0 + 0.42, 6.98, "Q", ha="right", va="center", fontsize=11, color="#b45309")
    ax.text(xx := x0 + 2.98, 6.98, "Q′", ha="left", va="center", fontsize=11, color="#b45309")
    ax.text(x0 + 1.7, 5.42, "双稳态触发器（典型六管单元）", ha="center", va="center",
            fontsize=10, color="#374151")
    ax.text(x0 + 1.7, 5.08, "两反相器互锁，通电即自保持", ha="center", va="center",
            fontsize=10, color="#6b7280")


def draw_dram_cell(x0):
    # 1 管 1 电容单元
    ax.plot([x0 + 2.6, x0 + 2.6], [5.45, 7.75], color="#2563eb", lw=LW + 0.4)   # 位线
    ax.text(x0 + 2.6, 7.92, "位线", ha="center", va="center", fontsize=10.5, color="#1d4ed8")
    ax.plot([x0 + 0.55, x0 + 2.6], [5.45, 5.45], color="#2563eb", lw=LW + 0.4)  # 字线
    ax.text(x0 + 0.48, 5.45, "字线", ha="right", va="center", fontsize=10.5, color="#1d4ed8")
    ax.plot([x0 + 1.5, x0 + 2.6], [6.85, 6.85], color=WIRE, lw=LW)              # 管子到位线
    ax.plot([x0 + 1.5, x0 + 1.5], [6.15, 6.85], color=WIRE, lw=LW)              # 沟道
    ax.plot([x0 + 1.24, x0 + 1.24], [6.35, 6.65], color=WIRE, lw=3.0)           # 栅极
    ax.plot([x0 + 1.24, x0 + 0.8, x0 + 0.8], [6.5, 6.5, 5.45], color=WIRE, lw=LW)
    ax.add_patch(Circle((x0 + 1.5, 6.85), 0.05, facecolor=WIRE, edgecolor=WIRE))
    ax.plot([x0 + 1.5, x0 + 1.5], [6.15, 6.0], color=WIRE, lw=LW)
    ax.plot([x0 + 1.28, x0 + 1.72], [6.0, 6.0], color=WIRE, lw=2.4)             # 上极板
    ax.plot([x0 + 1.28, x0 + 1.72], [5.87, 5.87], color=WIRE, lw=2.4)          # 下极板
    ax.plot([x0 + 1.5, x0 + 1.5], [5.87, 5.75], color=WIRE, lw=LW)
    ax.plot([x0 + 1.33, x0 + 1.67], [5.75, 5.75], color=WIRE, lw=LW)           # 地
    ax.plot([x0 + 1.38, x0 + 1.62], [5.66, 5.66], color=WIRE, lw=LW)
    ax.plot([x0 + 1.43, x0 + 1.57], [5.57, 5.57], color=WIRE, lw=LW)
    ax.text(x0 + 1.06, 6.68, "T", ha="center", va="center", fontsize=10.5, color="#1f2937")
    ax.text(x0 + 1.82, 5.94, "C", ha="left", va="center", fontsize=10.5, color="#1f2937")
    ax.text(x0 + 1.7, 5.14, "1 管 1 电容：电荷泄漏，需定期刷新", ha="center", va="center",
            fontsize=10, color="#374151")


def draw_rom_cell(x0):
    # 存储矩阵：交叉点是否制作 MOS 管
    for bx in (x0 + 1.0, x0 + 1.85, x0 + 2.7):
        ax.plot([bx, bx], [5.7, 7.55], color="#059669", lw=LW + 0.4)
    ax.text(x0 + 2.7, 7.72, "位线", ha="center", va="center", fontsize=10.5, color="#047857")
    for wy in (7.35, 6.6, 5.85):
        ax.plot([x0 + 0.5, x0 + 3.05], [wy, wy], color="#059669", lw=LW + 0.4)
    ax.text(x0 + 0.44, 7.35, "字线", ha="right", va="center", fontsize=10.5, color="#047857")
    filled = [(x0 + 1.0, 7.35), (x0 + 2.7, 7.35), (x0 + 1.85, 6.6),
              (x0 + 1.0, 5.85), (x0 + 2.7, 5.85)]
    hollow = [(x0 + 1.85, 7.35), (x0 + 1.0, 6.6), (x0 + 2.7, 6.6), (x0 + 1.85, 5.85)]
    for (px, py) in filled:
        ax.add_patch(Circle((px, py), 0.075, facecolor="#065f46", edgecolor="#065f46", zorder=5))
    for (px, py) in hollow:
        ax.add_patch(Circle((px, py), 0.075, facecolor="white", edgecolor="#065f46",
                            lw=1.6, zorder=5))
    ax.add_patch(Circle((x0 + 0.58, 5.35), 0.075, facecolor="#065f46", edgecolor="#065f46"))
    ax.text(x0 + 0.74, 5.35, "接 MOS 管 = 存 1", ha="left", va="center", fontsize=10, color="#374151")
    ax.add_patch(Circle((x0 + 2.14, 5.35), 0.075, facecolor="white", edgecolor="#065f46", lw=1.6))
    ax.text(x0 + 2.3, 5.35, "不接 = 存 0", ha="left", va="center", fontsize=10, color="#374151")
    ax.text(x0 + 1.7, 5.05, "掩模 / 浮栅工艺决定内容", ha="center", va="center",
            fontsize=10, color="#6b7280")


CELLS = [draw_sram_cell, draw_dram_cell, draw_rom_cell]

for card, cell in zip(CARDS, CELLS):
    x0 = card["x0"]
    theme = card["theme"]
    ax.add_patch(FancyBboxPatch((x0, 0.3), 3.4, 9.35,
                                boxstyle="round,pad=0.02,rounding_size=0.14",
                                facecolor=card["bg"], edgecolor=theme, lw=2.0))
    ax.add_patch(FancyBboxPatch((x0, 8.75), 3.4, 0.9,
                                boxstyle="round,pad=0.02,rounding_size=0.14",
                                facecolor=theme, edgecolor=theme, lw=1.5))
    ax.text(x0 + 1.7, 9.2, card["title"], ha="center", va="center",
            fontsize=12.5, fontweight="bold", color="white")
    ax.text(x0 + 1.7, 8.5, card["sub"], ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=theme)
    ax.add_patch(Rectangle((x0 + 0.15, 4.85), 3.1, 3.35, facecolor="white",
                           edgecolor="#d1d5db", lw=1.2))
    cell(x0)
    for i, feat in enumerate(card["features"]):
        y = 4.55 - i * 0.5
        ax.add_patch(Rectangle((x0 + 0.25, y - 0.065), 0.13, 0.13, facecolor=theme, edgecolor=theme))
        ax.text(x0 + 0.5, y, feat, ha="left", va="center", fontsize=10.5, color="#1f2937")
    ax.add_patch(FancyBboxPatch((x0 + 0.15, 0.55), 3.1, 1.1,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=theme, edgecolor=theme, lw=1.5, alpha=0.12))
    ax.text(x0 + 1.7, 1.4, "典型用途", ha="center", va="center",
            fontsize=10, fontweight="bold", color=theme)
    ax.text(x0 + 1.7, 1.0, card["usage"], ha="center", va="center",
            fontsize=11.5, fontweight="bold", color="#111827")

fig.suptitle("三类半导体存储器对比：单元结构 · 关键特性 · 典型用途",
             fontsize=15, fontweight="bold", color="#111827")
fig.savefig("/home/z/my-project/public/mocks/m03/q15.png")
print("saved q15.png")
