# -*- coding: utf-8 -*-
# 全真模拟卷九 · 第15题配图：手机 SoC 三级 Cache 存储层次（容量/延迟参数与题干一致）
import os
import matplotlib.font_manager as fm

font_path = '/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf'
if not os.path.exists(font_path):
    font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(font_path)

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7, 5.2), dpi=150, constrained_layout=True)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8.4)
ax.axis('off')

EDGE = '#334155'
C_MISS, C_HIT = '#dc2626', '#2563eb'

# 标题
ax.text(5, 8.12, '手机 SoC 三级 Cache 存储层次（块大小 64 B）',
        ha='center', va='center', fontsize=13, fontweight='bold')

levels = [
    ('CPU 内核\n（游戏物理引擎，60 fps）', '#fef3c7'),
    ('L1 数据 Cache\n32 KB · 直接映射 · 命中 4 周期', '#dcfce7'),
    ('L2 Cache\n512 KB · 命中 12 周期', '#dbeafe'),
    ('L3 Cache（八核共享）\n4 MB · 命中 40 周期', '#ffedd5'),
    ('DRAM 主存\n访问 150 周期', '#e5e7eb'),
]

x, w = 2.55, 4.90
h, gap = 1.02, 0.56
y_top = 7.85
edges = []
for i, (text, fc) in enumerate(levels):
    y = y_top - (i + 1) * h - i * gap
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.06',
                                fc=fc, ec=EDGE, lw=1.8))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=10.5, linespacing=1.6)
    edges.append((y, y + h))  # (底边, 顶边)

for i in range(len(levels) - 1):
    y_cur_bottom = edges[i][0]        # 上一级框的底边
    y_next_top = edges[i + 1][1]      # 下一级框的顶边
    y_mid = (y_cur_bottom + y_next_top) / 2
    # 请求向下（未命中）
    ax.add_patch(FancyArrowPatch((x + 1.25, y_cur_bottom), (x + 1.25, y_next_top),
                                 arrowstyle='-|>', mutation_scale=16,
                                 lw=2.0, color=C_MISS))
    ax.text(x + 1.05, y_mid, '未命中', ha='right', va='center',
            fontsize=10, color=C_MISS)
    # 数据返回向上
    ax.add_patch(FancyArrowPatch((x + w - 1.25, y_next_top), (x + w - 1.25, y_cur_bottom),
                                 arrowstyle='-|>', mutation_scale=16,
                                 lw=2.0, color=C_HIT))
    ax.text(x + w - 1.05, y_mid, '取数返回', ha='left', va='center',
            fontsize=10, color=C_HIT)

ax.text(5, 0.24, '红色：未命中时的访问请求　　蓝色：数据返回（任一级命中即原路返回）',
        ha='center', va='center', fontsize=10, color=EDGE)

fig.savefig('/home/z/my-project/public/mocks/m09/q15.png')
print('saved q15.png')
