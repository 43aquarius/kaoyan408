# -*- coding: utf-8 -*-
"""全真模拟卷（五）第 15 题：虚拟地址→TLB/页表→物理地址→Cache 访问全链路框图（标注各步骤耗时）"""
import os
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

GREEN = '#16a34a'   # 命中路径
RED = '#dc2626'     # 未命中路径
BLUE = '#2563eb'    # 地址 / 数据流
ORANGE = '#ea580c'  # 数据访问阶段
GRAY = '#475569'

fig, ax = plt.subplots(figsize=(8.8, 6.8), dpi=150, constrained_layout=True)
ax.set_xlim(0, 10.6)
ax.set_ylim(0.4, 13.2)
ax.axis('off')


def box(x, y, w, h, text, edge, face, fs=10.5, lw=2.0):
    p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.04',
                       linewidth=lw, edgecolor=edge, facecolor=face)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fs, color='#111827', linespacing=1.35)


def arrow(p1, p2, color, lw=2.2):
    a = FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=16,
                        linewidth=lw, color=color)
    ax.add_patch(a)


def seg(p1, p2, color, lw=2.2):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw,
            solid_capstyle='round')


# ── 主流程框（左列）─────────────────────────────────────────────
XC = 2.7  # 主列中心
box(XC - 1.8, 12.0, 3.6, 0.8, 'CPU 发出虚拟地址（32 位）', '#1e293b', '#f8fafc')
box(XC - 1.8, 10.3, 3.6, 0.8, '查 TLB（20 ns）\n命中率 95%', BLUE, '#dbeafe')
box(XC - 1.8, 8.4, 3.6, 1.0, '访问页表（100 ns）\n单级 · 不经过 Cache', BLUE, '#dbeafe')
box(XC - 1.8, 6.6, 3.6, 0.8, '形成物理地址', GREEN, '#dcfce7')
box(XC - 1.8, 4.7, 3.6, 0.8, '查 Cache（20 ns）\n命中率 90%', ORANGE, '#ffedd5')
box(XC - 1.8, 2.6, 3.6, 0.8, '访问主存（100 ns）', ORANGE, '#ffedd5')
box(XC - 1.8, 0.9, 3.6, 0.8, '数据返回 CPU', '#7c3aed', '#ede9fe')

# ── 箭头：主流程 ────────────────────────────────────────────────
arrow((XC, 12.0), (XC, 11.15), BLUE)                 # CPU → TLB
arrow((XC, 10.3), (XC, 9.45), RED)                   # TLB → 页表（未命中）
arrow((XC, 8.4), (XC, 7.45), BLUE)                   # 页表 → 物理地址
arrow((XC, 6.6), (XC, 5.55), BLUE)                   # 物理地址 → Cache
arrow((XC, 4.7), (XC, 3.45), RED)                    # Cache → 主存（未命中）
arrow((XC, 2.6), (XC, 1.75), BLUE)                   # 主存 → 数据

ax.text(XC + 0.18, 9.88, '未命中 5%', ha='left', va='center', fontsize=10, color=RED)
ax.text(XC + 0.18, 4.08, '未命中 10%', ha='left', va='center', fontsize=10, color=RED)
ax.text(XC + 0.18, 7.92, '取出页框号（装入 TLB）', ha='left', va='center',
        fontsize=10, color=GRAY)
ax.text(XC + 0.18, 2.18, '整块调入 Cache', ha='left', va='center', fontsize=10, color=GRAY)

# TLB 命中旁路（绿）：TLB → 物理地址
seg((XC + 1.8, 10.7), (5.5, 10.7), GREEN)
seg((5.5, 10.7), (5.5, 7.0), GREEN)
arrow((5.5, 7.0), (XC + 1.85, 7.0), GREEN)
ax.text(5.32, 8.85, '命中 95%', ha='center', va='center', fontsize=10,
        color=GREEN, rotation=90)

# Cache 命中旁路（绿）：Cache → 数据
seg((XC + 1.8, 5.1), (5.5, 5.1), GREEN)
seg((5.5, 5.1), (5.5, 1.3), GREEN)
arrow((5.5, 1.3), (XC + 1.85, 1.3), GREEN)
ax.text(5.32, 3.2, '命中 90%', ha='center', va='center', fontsize=10,
        color=GREEN, rotation=90)

# ── 左侧阶段标注 ────────────────────────────────────────────────
ax.plot([0.82, 0.82], [8.4, 11.1], color=BLUE, lw=1.8)
ax.plot([0.82, 0.9], [11.1, 11.1], color=BLUE, lw=1.8)
ax.plot([0.82, 0.9], [8.4, 8.4], color=BLUE, lw=1.8)
ax.text(0.55, 9.75, '地址翻译阶段', ha='center', va='center', fontsize=10.5,
        color=BLUE, rotation=90)
ax.plot([0.82, 0.82], [2.6, 5.5], color=ORANGE, lw=1.8)
ax.plot([0.82, 0.9], [5.5, 5.5], color=ORANGE, lw=1.8)
ax.plot([0.82, 0.9], [2.6, 2.6], color=ORANGE, lw=1.8)
ax.text(0.55, 4.05, '数据访问阶段', ha='center', va='center', fontsize=10.5,
        color=ORANGE, rotation=90)

# ── 右侧：四种路径耗时面板 ──────────────────────────────────────
panel = FancyBboxPatch((6.2, 0.9), 4.2, 11.9, boxstyle='round,pad=0.05',
                       linewidth=1.8, edgecolor='#94a3b8', facecolor='#f8fafc')
ax.add_patch(panel)
ax.text(8.3, 12.3, '四种路径耗时（串行累加）', ha='center', va='center',
        fontsize=11.5, color='#111827', fontweight='bold')

PX = 6.5
rows = [
    ('① TLB 命中 + Cache 命中', '20 + 20 = 40 ns（概率 0.855）', 11.45),
    ('② TLB 命中 + Cache 缺失', '20 + 20 + 100 = 140 ns（0.095）', 10.25),
    ('③ TLB 缺失 + Cache 命中', '20 + 100 + 20 = 140 ns（0.045）', 9.05),
    ('④ TLB 缺失 + Cache 缺失', '20 + 100 + 20 + 100 = 240 ns（0.005）', 7.85),
]
for title, expr, yy in rows:
    ax.text(PX, yy, title, ha='left', va='center', fontsize=10.5, color='#1e3a8a')
    ax.text(PX, yy - 0.45, expr, ha='left', va='center', fontsize=10, color=GRAY)

ax.plot([PX, 10.15], [7.05, 7.05], color='#94a3b8', lw=1.5)

ax.text(PX, 6.35, '平均访问时间 =', ha='left', va='center', fontsize=10.5, color='#111827')
ax.text(PX, 5.85, '0.855 × 40 + 0.095 × 140', ha='left', va='center', fontsize=10, color=GRAY)
ax.text(PX, 5.42, '+ 0.045 × 140 + 0.005 × 240', ha='left', va='center', fontsize=10, color=GRAY)
ax.text(PX, 4.75, '= ？ ns（请计算）', ha='left', va='center', fontsize=12,
        color=GREEN, fontweight='bold')

ax.text(PX, 3.6, '注：页面均在主存，不发生缺页；', ha='left', va='center', fontsize=10, color=GRAY)
ax.text(PX, 3.18, '查 TLB / 页表 / Cache / 主存串行计时；', ha='left', va='center',
        fontsize=10, color=GRAY)
ax.text(PX, 2.76, 'TLB 命中直接得物理地址，', ha='left', va='center', fontsize=10, color=GRAY)
ax.text(PX, 2.34, '未命中才访问一次页表。', ha='left', va='center', fontsize=10, color=GRAY)

ax.set_title('虚拟地址 → TLB/页表 → 物理地址 → Cache 全链路（标注各步骤耗时）',
             fontsize=13, color='#111827')

out = '/home/z/my-project/public/mocks/m05/q15.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out)
print('saved:', out)
