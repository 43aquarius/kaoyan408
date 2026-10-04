# -*- coding: utf-8 -*-
# 全真模拟卷（八）· E 段 第 43 题配图：主存扩展连接图
# 题干参数：CPU 16 位地址线 A15~A0、8 位数据线 D7~D0、按字节编址、MREQ' 低有效
#   ROM 区 0000H~0FFFH：4K×4 位芯片 2 片位扩展（ROM-1 接 D7~D4，ROM-2 接 D3~D0，共用 Y0'）
#   RAM 区 1000H~1FFFH：RAM-1（4K×8）；2000H~2FFFH：RAM-2（4K×8），字扩展分别接 Y1'、Y2'
#   74LS138：G1=+5V，G2A'=A15，G2B'=MREQ'，C B A = A14 A13 A12；Y3'~Y7' 未用（空闲区）
# 蓝色 = 地址线；绿色 = 数据线（双向）；红色 = 片选线；灰色虚线 = 分组框
# 输出: /home/z/my-project/public/mocks/m08/q43.png
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Bold.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False

C_ADDR, C_DATA, C_CS = '#2563eb', '#059669', '#dc2626'
C_GRAY = '#6b7280'

fig, ax = plt.subplots(figsize=(10.2, 7.5), dpi=150, constrained_layout=True)
ax.set_xlim(0, 14.6)
ax.set_ylim(0, 10.8)
ax.axis('off')

# ---- 标题 ----
ax.text(7.3, 10.45, '题 43 图：主存扩展连接图（ROM 2 片位扩展 + RAM 2 片字扩展，74LS138 片选）',
        ha='center', va='bottom', fontsize=12, fontweight='bold', color='#111827')

# ---- CPU ----
ax.add_patch(mpatches.Rectangle((0.5, 3.0), 2.1, 5.0, facecolor='#f8fafc',
                                edgecolor='#334155', linewidth=2))
ax.text(1.55, 7.45, 'CPU', ha='center', va='center', fontsize=13,
        fontweight='bold', color='#0f172a')
ax.text(1.55, 6.25, '地址线 A15~A0\n数据线 D7~D0\n控制线 MREQ\'', ha='center', va='center',
        fontsize=8.5, color='#475569', linespacing=1.7)
ax.text(2.72, 7.42, 'A15~A12', ha='left', va='bottom', fontsize=8, color=C_ADDR)
ax.text(2.72, 6.42, 'A11~A0', ha='left', va='bottom', fontsize=8, color=C_ADDR)

# ---- 74LS138 译码器 ----
ax.add_patch(mpatches.Rectangle((4.3, 6.6), 2.4, 2.9, facecolor='#fff7ed',
                                edgecolor='#c2410c', linewidth=2))
ax.text(5.5, 9.26, '74LS138', ha='center', va='center', fontsize=10,
        fontweight='bold', color='#9a3412')
ax.text(5.5, 9.0, '3-8 译码器', ha='center', va='center', fontsize=8, color='#9a3412')
for name, yy in [('G1', 8.6), ("G2A'", 8.2), ("G2B'", 7.8), ('C', 7.25), ('B', 6.98), ('A', 6.71)]:
    ax.text(4.42, yy, name, ha='left', va='center', fontsize=7.5, color='#7c2d12')
for name, yy in [("Y0'", 8.6), ("Y1'", 8.05), ("Y2'", 7.5), ("Y3'", 6.95)]:
    ax.text(6.58, yy, name, ha='right', va='center', fontsize=7.5, color='#7c2d12')
ax.text(6.58, 6.72, '⋮', ha='right', va='center', fontsize=9, color='#7c2d12')

# ---- A15~A12 总线与分支（接 C/B/A 与 G2A'）----
ax.plot([2.6, 3.55], [7.3, 7.3], color=C_ADDR, lw=2.2, solid_capstyle='round')
ax.plot([3.55], [7.3], 'o', color=C_ADDR, markersize=4.5)
for yy, lab in [(8.2, 'A15'), (7.25, 'A14'), (6.98, 'A13'), (6.71, 'A12')]:
    ax.plot([3.55, 3.55, 4.3], [7.3, yy, yy], color=C_ADDR, lw=1.6)
    ax.text(3.88, yy + 0.08, lab, ha='left', va='bottom', fontsize=7, color=C_ADDR)
# G1 / G2B' 固定与控制信号（短线标注）
ax.plot([4.05, 4.3], [8.6, 8.6], color='#374151', lw=1.6)
ax.text(4.0, 8.6, '+5V', ha='right', va='center', fontsize=7.5, color='#374151')
ax.plot([4.05, 4.3], [7.8, 7.8], color='#374151', lw=1.6)
ax.text(4.17, 7.62, "MREQ'", ha='center', va='center', fontsize=7, color='#374151')

# ---- 片选线（红）----
ax.plot([6.7, 7.5], [8.6, 8.6], color=C_CS, lw=2)
ax.plot([7.5, 7.5], [8.6, 7.8], color=C_CS, lw=2)
ax.add_patch(mpatches.FancyArrowPatch((7.5, 7.8), (9.15, 7.8), arrowstyle='-|>',
                                      mutation_scale=15, lw=2, color=C_CS))
ax.text(7.08, 8.72, "Y0'", ha='center', va='bottom', fontsize=7.5, color=C_CS)
ax.plot([6.7, 7.15], [8.05, 8.05], color=C_CS, lw=2)
ax.plot([7.15, 7.15], [8.05, 4.2], color=C_CS, lw=2)
ax.add_patch(mpatches.FancyArrowPatch((7.15, 4.2), (9.4, 4.2), arrowstyle='-|>',
                                      mutation_scale=15, lw=2, color=C_CS))
ax.text(6.85, 8.17, "Y1'", ha='center', va='bottom', fontsize=7.5, color=C_CS)
ax.plot([6.7, 6.9], [7.5, 7.5], color=C_CS, lw=2)
ax.plot([6.9, 6.9], [7.5, 2.4], color=C_CS, lw=2)
ax.add_patch(mpatches.FancyArrowPatch((6.9, 2.4), (9.4, 2.4), arrowstyle='-|>',
                                      mutation_scale=15, lw=2, color=C_CS))
ax.text(6.82, 7.62, "Y2'", ha='center', va='bottom', fontsize=7.5, color=C_CS)

# ---- 片内地址总线（蓝）：水平干道 + 垂直分支进各芯片 ----
ax.plot([2.6, 8.75], [6.3, 6.3], color=C_ADDR, lw=3, solid_capstyle='round')
ax.plot([8.75, 8.75], [2.8, 8.5], color=C_ADDR, lw=3, solid_capstyle='round')
ax.plot([8.75], [6.3], 'o', color=C_ADDR, markersize=4.5)
ax.text(5.3, 6.42, 'A11~A0（片内地址）', ha='center', va='bottom', fontsize=8.5, color=C_ADDR)
for yy in [8.5, 6.9, 4.6, 2.8]:
    ax.add_patch(mpatches.FancyArrowPatch((8.75, yy), (9.4, yy), arrowstyle='-|>',
                                          mutation_scale=15, lw=2, color=C_ADDR))

# ---- 数据总线（绿，双向）----
ax.plot([1.55, 1.55], [3.0, 0.55], color=C_DATA, lw=2.5)
ax.plot([1.55, 13.9], [0.55, 0.55], color=C_DATA, lw=3, solid_capstyle='round')
ax.plot([13.9, 13.9], [0.55, 8.5], color=C_DATA, lw=3, solid_capstyle='round')
for yy in [8.5, 6.9, 4.6, 2.8]:
    ax.plot([13.2, 13.9], [yy, yy], color=C_DATA, lw=1.8)
ax.text(1.78, 1.75, 'D7~D0（双向）', ha='left', va='center', fontsize=8, color=C_DATA)
ax.text(7.6, 0.72, '数据总线 D7~D0（双向）', ha='center', va='bottom', fontsize=9, color=C_DATA)
for lab, yy in [('D7~D4', 8.62), ('D3~D0', 7.02), ('D7~D0', 4.72), ('D7~D0', 2.92)]:
    ax.text(13.55, yy, lab, ha='center', va='bottom', fontsize=7, color=C_DATA)

# ---- ROM 组（位扩展，2 片）----
ax.add_patch(mpatches.Rectangle((9.15, 6.1), 4.3, 3.2, fill=False,
                                edgecolor=C_GRAY, linewidth=1.5, linestyle=(0, (6, 4))))
ax.text(11.3, 9.42, 'ROM 组：2 片 4K×4 位位扩展 → 4K×8 位', ha='center', va='bottom',
        fontsize=8.5, color='#374151')
ax.text(9.32, 7.68, "CS'←Y0'（两片共用）", ha='left', va='center', fontsize=7.5, color=C_CS)
for y0, name, rng, dat in [(7.9, 'ROM-1（4K×4 位）', '地址 0000H~0FFFH', '数据线 D7~D4'),
                           (6.3, 'ROM-2（4K×4 位）', '地址 0000H~0FFFH', '数据线 D3~D0')]:
    ax.add_patch(mpatches.Rectangle((9.4, y0), 3.8, 1.2, facecolor='#eef2ff',
                                    edgecolor='#4338ca', linewidth=1.8))
    ax.text(11.3, y0 + 0.82, name, ha='center', va='center', fontsize=9,
            fontweight='bold', color='#312e81')
    ax.text(11.3, y0 + 0.48, rng, ha='center', va='center', fontsize=8, color='#1e293b')
    ax.text(11.3, y0 + 0.18, dat, ha='center', va='center', fontsize=8, color='#1e293b')

# ---- RAM-1 / RAM-2（字扩展）----
for y0, name, rng, cs in [(3.9, 'RAM-1（4K×8 位）', '地址 1000H~1FFFH', "CS'←Y1'"),
                          (2.1, 'RAM-2（4K×8 位）', '地址 2000H~2FFFH', "CS'←Y2'")]:
    ax.add_patch(mpatches.Rectangle((9.4, y0), 3.8, 1.4, facecolor='#ecfdf5',
                                    edgecolor='#047857', linewidth=1.8))
    ax.text(11.3, y0 + 1.02, name, ha='center', va='center', fontsize=9,
            fontweight='bold', color='#064e3b')
    ax.text(11.3, y0 + 0.66, rng, ha='center', va='center', fontsize=8, color='#1e293b')
    ax.text(9.58, y0 + 0.28, cs, ha='left', va='center', fontsize=7.5, color=C_CS)

# ---- 底部说明与图例 ----
ax.text(0.55, 0.1, "注：G1=+5V；G2A'=A15（A15=0 才使能，8000H~FFFFH 不选中任何芯片）；"
                   "G2B'=MREQ'（CPU 访存请求，低有效）；Y3'~Y7' 对应 3000H~7FFFH 空闲区，未接芯片。",
        ha='left', va='bottom', fontsize=7.5, color=C_GRAY)
handles = [
    Line2D([0], [0], color=C_ADDR, lw=2.5, label='地址线'),
    Line2D([0], [0], color=C_DATA, lw=2.5, label='数据线（双向）'),
    Line2D([0], [0], color=C_CS, lw=2, label='片选线'),
    Line2D([0], [0], color=C_GRAY, lw=1.5, linestyle=(0, (6, 4)), label='分组框'),
]
legend = ax.legend(handles=handles, loc='upper left', fontsize=8, framealpha=0.95,
                   edgecolor='#cbd5e1', borderpad=0.6, handlelength=2.0)
legend.set_zorder(6)

fig.savefig('/home/z/my-project/public/mocks/m08/q43.png')
print('saved: /home/z/my-project/public/mocks/m08/q43.png')
