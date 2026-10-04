# -*- coding: utf-8 -*-
# 模拟卷六 A 段 第 5 题：哈夫曼树结构图（权值 A=4, B=7, C=10, D=15, E=18）
import os
import matplotlib.font_manager as fm

FONT_CANDIDATES = [
    '/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
]
for _p in FONT_CANDIDATES:
    if os.path.exists(_p):
        fm.fontManager.addfont(_p)

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7, 4), dpi=150, constrained_layout=True)

# 结点：(x, y, 显示标签)；内部结点为合并权值，叶结点为 符号:权值
nodes = {
    'root': (0.50, 0.88, '54'),
    'n21':  (0.28, 0.64, '21'),
    'n33':  (0.74, 0.64, '33'),
    'n11':  (0.15, 0.40, '11'),
    'C':    (0.44, 0.40, 'C:10'),
    'A':    (0.07, 0.20, 'A:4'),
    'B':    (0.26, 0.20, 'B:7'),
    'D':    (0.60, 0.40, 'D:15'),
    'E':    (0.88, 0.40, 'E:18'),
}
edges = [
    ('root', 'n21', '0'), ('root', 'n33', '1'),
    ('n21', 'n11', '0'), ('n21', 'C', '1'),
    ('n33', 'D', '0'), ('n33', 'E', '1'),
    ('n11', 'A', '0'), ('n11', 'B', '1'),
]
LEAVES = {'A', 'B', 'C', 'D', 'E'}
R = 0.052

# 连线与 0/1 编码标注
for src, dst, lab in edges:
    x1, y1, _ = nodes[src]
    x2, y2, _ = nodes[dst]
    ax.annotate(
        '', xy=(x2, y2 + R), xytext=(x1, y1 - R),
        arrowprops=dict(arrowstyle='-', color='#64748b', lw=1.6),
    )
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(
        mx + (0.014 if lab == '1' else -0.014), my, lab,
        fontsize=11, color='#dc2626', fontweight='bold',
        ha='left' if lab == '1' else 'right', va='center',
    )

# 结点圆圈：叶结点绿色，内部结点蓝色
for key, (x, y, label) in nodes.items():
    if key in LEAVES:
        face, edge, tc = '#dcfce7', '#16a34a', '#14532d'
    else:
        face, edge, tc = '#dbeafe', '#2563eb', '#1e3a8a'
    ax.add_patch(plt.Circle((x, y), R, facecolor=face, edgecolor=edge, lw=1.8, zorder=3))
    ax.text(x, y, label, ha='center', va='center', fontsize=10.5,
            color=tc, fontweight='bold', zorder=4)

ax.text(0.5, 0.995, '哈夫曼编码树（权值：A=4，B=7，C=10，D=15，E=18）',
        ha='center', va='top', fontsize=12, fontweight='bold')

ax.text(
    0.5, 0.015,
    'A=000，B=001（码长 3）；C=01，D=10，E=11（码长 2）\n'
    '编码总位数 WPL = 4×3 + 7×3 + 10×2 + 15×2 + 18×2 = 119',
    ha='center', va='bottom', fontsize=10.5, color='#334155',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#f1f5f9',
              edgecolor='#94a3b8', lw=1.2),
)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

fig.savefig('/home/z/my-project/public/mocks/m06/q05.png')
print('saved: /home/z/my-project/public/mocks/m06/q05.png')
