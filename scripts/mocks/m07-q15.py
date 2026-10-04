# -*- coding: utf-8 -*-
# 全真模拟卷七 · 第15题配图：4 路组相联 Cache 结构图（参数与题干一致）
# 8 组 × 4 路 × 每行 64 B = 2 KB；主存地址 = 23 位标记 + 3 位组号 + 6 位块内地址
import os
import matplotlib.font_manager as fm

font_path = '/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf'
if not os.path.exists(font_path):
    font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(font_path)

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7, 4.6), dpi=150, constrained_layout=True)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.7)
ax.axis('off')

EDGE = '#334155'
C_SET0 = '#fde68a'   # 组0 高亮
C_CELL = '#f1f5f9'   # 普通行
C_TAG = '#dbeafe'    # 标记列
C_DATA = '#dcfce7'   # 数据列
C_V = '#fef9c3'      # 有效位列
C_D = '#fee2e2'      # 脏位列

# 标题
ax.text(5, 6.38, '4 路组相联 Cache（8 组 × 4 行 × 64 B = 2 KB，写回法 + 按写分配 + LRU）',
        ha='center', va='center', fontsize=12, fontweight='bold')

# ---- 左侧：8 组 × 4 路概览（组0 在最上并高亮）----
gx, gy, cw, ch = 0.30, 1.55, 0.50, 0.40
ax.text(gx + 2 * cw, gy + 8 * ch + 0.26, 'Cache 全部 8 组（列 = 4 路）',
        ha='center', va='center', fontsize=10.5)
for g in range(8):
    row = 7 - g  # 组0 在最上
    ax.text(gx - 0.12, gy + row * ch + ch / 2, f'组{g}',
            ha='right', va='center', fontsize=10)
    for w in range(4):
        fc = C_SET0 if g == 0 else C_CELL
        ec = '#b45309' if g == 0 else '#94a3b8'
        lw = 2.0 if g == 0 else 1.2
        ax.add_patch(Rectangle((gx + w * cw, gy + row * ch), cw, ch, fc=fc, ec=ec, lw=lw))
ax.text(gx + 2 * cw, gy - 0.30, '块号 0、8、16、24、32、40\n（组号 = 块号 mod 8 = 0）',
        ha='center', va='center', fontsize=10, color='#b45309', linespacing=1.5)

# 放大箭头：组0 → 右侧详情
ax.add_patch(FancyArrowPatch((gx + 4 * cw + 0.06, gy + 7 * ch + ch / 2),
                             (3.52, 4.95), arrowstyle='-|>', mutation_scale=16,
                             lw=1.8, color='#b45309', connectionstyle='arc3,rad=0.25'))
ax.text(2.95, 5.22, '放大组 0', ha='center', va='center', fontsize=10, color='#b45309')

# ---- 右侧：组 0 中每一行的字段结构（初始为空：V=0）----
dx = 3.60
cols = [('路', 0.50, '#f8fafc'), ('V', 0.40, C_V), ('D', 0.40, C_D),
        ('标记 Tag（23 位）', 1.80, C_TAG), ('数据（64 B）', 2.25, C_DATA)]
hy, hh = 4.42, 0.34
x = dx
for name, w, fc in cols:
    ax.add_patch(Rectangle((x, hy), w, hh, fc=fc, ec=EDGE, lw=1.5))
    ax.text(x + w / 2, hy + hh / 2, name, ha='center', va='center', fontsize=10)
    x += w
row_h, gap = 0.50, 0.10
for r in range(4):
    y = hy - 0.16 - (r + 1) * row_h - r * gap
    x = dx
    values = [f'路{r}', '0', '0', '—', '—']
    for (name, w, fc), val in zip(cols, values):
        ax.add_patch(Rectangle((x, y), w, row_h, fc=fc, ec=EDGE, lw=1.5))
        ax.text(x + w / 2, y + row_h / 2, val, ha='center', va='center', fontsize=10)
        x += w
ax.text(dx + 2.675, hy + hh + 0.22, '组 0 中 4 行的字段结构（初始为空，V = 0）',
        ha='center', va='center', fontsize=10.5)
ax.text(dx + 2.675, hy - 0.16 - 4 * row_h - 3 * gap - 0.30,
        '替换算法 LRU；写回法：仅被替换行的 D = 1 时才写回主存\n写未命中按写分配：先调入行，再写 Cache 并将 D 置 1',
        ha='center', va='center', fontsize=10, color=EDGE, linespacing=1.6)

# ---- 底部：主存地址划分 ----
ay, ah = 0.34, 0.40
segs = [('标记 23 位', 6.22, '#e2e8f0'), ('组号\n3 位', 0.81, C_SET0), ('块内地址\n6 位', 1.62, '#bfdbfe')]
ax.text(4.63, ay + ah + 0.24, '主存地址 32 位的划分', ha='center', va='center',
        fontsize=10.5)
x = 0.30
for name, w, fc in segs:
    ax.add_patch(Rectangle((x, ay), w, ah, fc=fc, ec=EDGE, lw=1.5))
    ax.text(x + w / 2, ay + ah / 2, name, ha='center', va='center',
            fontsize=10, linespacing=1.3)
    x += w
ax.text(4.63, 0.13, '块号 = 地址 / 64；地址 0、512、1024、1536、2048、2560 的组号均为 0，全部映射到组 0',
        ha='center', va='center', fontsize=10, color=EDGE)

fig.savefig('/home/z/my-project/public/mocks/m07/q15.png')
print('saved q15.png')
