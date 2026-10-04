# -*- coding: utf-8 -*-
# 全真模拟卷（二）· E 段 第 43 题配图：虚拟存储器一次访存的访问流程框图
# 题干参数：虚拟地址 32 位 / 物理地址 24 位（主存 16 MB）/ 页面 4 KB / 单级页表（查页表 = 1 次主存访问 50 ns）
#   TLB：16 行、2 路组相联，查找 2 ns，命中率 90%
#   Cache：数据区 32 KB、块 16 B、4 路组相联，物理地址访问，访问 10 ns，命中率 95%
#   主存：访问 50 ns（含整块调入与数据返回）；页表项装入 TLB 时间忽略；题设不发生缺页
# 颜色语义：绿色 = 命中快路径；橙色 = 缺失处理路径；蓝色 = 地址 / 数据流
# 输出: /home/z/my-project/public/mocks/m02/q43.png
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Bold.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8.8, 5.28), dpi=150, constrained_layout=True)
ax.set_xlim(0, 11)
ax.set_ylim(0, 6.6)
ax.axis('off')

# ---------------- 颜色 ----------------
C_FLOW = '#2563eb'    # 蓝：地址 / 数据流
C_HIT = '#059669'     # 绿：命中快路径
C_MISS = '#d97706'    # 橙：缺失处理路径
T_FLOW, T_HIT, T_MISS = '#1e40af', '#047857', '#b45309'
BOX_FAST_F, BOX_FAST_E = '#dcfce7', '#15803d'   # 快速存储部件（TLB / Cache）
BOX_SLOW_F, BOX_SLOW_E = '#ffedd5', '#c2410c'   # 慢速部件（页表 / 主存）
BOX_CPU_F, BOX_CPU_E = '#dbeafe', '#1d4ed8'     # CPU


def box(x, y, w, h, fc, ec, title, lines):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle='round,pad=0.06',
        facecolor=fc, edgecolor=ec, linewidth=2.0, zorder=3))
    ax.text(x + w / 2, y + h - 0.30, title, ha='center', va='center',
            fontsize=12.5, fontweight='bold', color=ec, zorder=4)
    ax.text(x + w / 2, y + 0.62, '\n'.join(lines), ha='center', va='center',
            fontsize=10, color='#374151', zorder=4, linespacing=1.4)


def arrow(p0, p1, color, lw=2.2, ls='-', rad=None, ms=16):
    style = '-|>'
    if rad is None:
        ax.add_patch(mpatches.FancyArrowPatch(
            p0, p1, arrowstyle=style, mutation_scale=ms,
            lw=lw, color=color, linestyle=ls, zorder=2))
    else:
        ax.add_patch(mpatches.FancyArrowPatch(
            p0, p1, arrowstyle=style, mutation_scale=ms,
            lw=lw, color=color, linestyle=ls, zorder=2,
            connectionstyle=f'arc3,rad={rad}'))


# ---------------- 标题 ----------------
ax.text(5.5, 6.30, '题 43 图：页式虚拟存储器一次访存的完整流程',
        ha='center', va='bottom', fontsize=13, fontweight='bold', color='#111827')

# ---------------- 框 ----------------
box(0.40, 3.55, 1.90, 1.60, BOX_CPU_F, BOX_CPU_E, 'CPU', ['发出 32 位', '虚拟地址 VA'])
box(3.60, 3.55, 2.30, 1.60, BOX_FAST_F, BOX_FAST_E, 'TLB',
    ['16 行 · 2 路组相联', '查找 2 ns', '命中率 90%'])
box(7.20, 3.55, 2.50, 1.60, BOX_FAST_F, BOX_FAST_E, 'Cache（物理地址）',
    ['32 KB · 4 路组相联', '访问 10 ns', '命中率 95%'])
box(3.60, 0.95, 2.30, 1.60, BOX_SLOW_F, BOX_SLOW_E, '页表（单级）',
    ['驻留主存', '查询 50 ns'])
box(7.20, 0.95, 2.50, 1.60, BOX_SLOW_F, BOX_SLOW_E, '主存（16 MB）',
    ['访问 50 ns', '（含整块调入）'])

# ---------------- 箭头与标注 ----------------
# 1) CPU -> TLB
arrow((2.30, 4.35), (3.60, 4.35), C_FLOW)
ax.text(2.95, 4.66, '① 虚拟地址', ha='center', va='center',
        fontsize=10.5, fontweight='bold', color=T_FLOW, zorder=5)

# 2) TLB -> Cache（命中快路径）
arrow((5.90, 4.35), (7.20, 4.35), C_HIT)
ax.text(6.55, 4.66, '② 命中 90%', ha='center', va='center',
        fontsize=10.5, fontweight='bold', color=T_HIT, zorder=5)
ax.text(6.55, 4.06, '物理地址', ha='center', va='center',
        fontsize=10, color=T_HIT, zorder=5)

# 3) TLB -> 页表（缺失，向下）
arrow((4.35, 3.55), (4.35, 2.55), C_MISS)
ax.text(4.20, 3.05, '③ 缺失 10%\n查页表 50 ns', ha='right', va='center',
        fontsize=10, fontweight='bold', color=T_MISS, zorder=5, linespacing=1.4)

# 4) 页表 -> TLB（装入，虚线，向上）
arrow((5.15, 2.55), (5.15, 3.55), C_MISS, lw=1.8, ls=(0, (5, 3)))
ax.text(5.30, 3.05, '装入 TLB\n（时间忽略）', ha='left', va='center',
        fontsize=10, color=T_MISS, zorder=5, linespacing=1.4)

# 5) 页表 -> Cache（形成物理地址，斜向）
arrow((5.90, 1.90), (7.60, 3.55), C_MISS)
ax.text(6.05, 2.68, '④ 形成物理地址', ha='right', va='center',
        fontsize=10, fontweight='bold', color=T_MISS, zorder=5)

# 6) Cache -> CPU（命中快路径，顶部弧线）
arrow((8.45, 5.15), (1.35, 5.15), C_HIT, rad=0.45)
ax.text(4.90, 5.40, '⑤ Cache 命中 95%：数据返回 CPU', ha='center', va='center',
        fontsize=10.5, fontweight='bold', color=T_HIT, zorder=5)

# 7) Cache -> 主存（缺失，向下）
arrow((8.45, 3.55), (8.45, 2.55), C_MISS)
ax.text(8.60, 3.22, '⑥ 缺失 5%', ha='left', va='center',
        fontsize=10, fontweight='bold', color=T_MISS, zorder=5)
ax.text(8.60, 2.90, '整块调入 50 ns', ha='left', va='center',
        fontsize=10, color=T_MISS, zorder=5)

# 8) 主存 -> CPU（数据返回，底部折线）
ax.add_line(Line2D([8.45, 8.45], [0.95, 0.42], color=C_FLOW, lw=2.2, zorder=2))
ax.add_line(Line2D([8.45, 0.55], [0.42, 0.42], color=C_FLOW, lw=2.2, zorder=2))
arrow((0.55, 0.42), (0.55, 3.55), C_FLOW)
ax.text(4.90, 0.16, '⑦ 整块数据装入 Cache 并送 CPU', ha='center', va='center',
        fontsize=10.5, fontweight='bold', color=T_FLOW, zorder=5)

# 9) 脚注
ax.text(10.95, 0.15, '注：题设不发生缺页（所有页表项有效位均为 1）',
        ha='right', va='center', fontsize=10, color='#6b7280', zorder=5)

# ---------------- 图例 ----------------
handles = [
    Line2D([0], [0], color=C_HIT, lw=2.2, linestyle='-', label='命中快路径'),
    Line2D([0], [0], color=C_MISS, lw=2.2, linestyle='-', label='缺失处理路径'),
    Line2D([0], [0], color=C_FLOW, lw=2.2, linestyle='-', label='地址 / 数据流'),
]
legend = ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(0.085, 0.24),
                   fontsize=10, framealpha=0.95, edgecolor='#cbd5e1',
                   borderpad=0.7, handlelength=1.9)
legend.set_zorder(5)

fig.savefig('/home/z/my-project/public/mocks/m02/q43.png')
print('saved: /home/z/my-project/public/mocks/m02/q43.png')
