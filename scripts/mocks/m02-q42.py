# -*- coding: utf-8 -*-
# 全真模拟卷（二）· D 段 第 42 题配图：Dijkstra 加权有向图 G
# 题干参数：顶点 v0~v5；边 (v0,v1)=3, (v0,v3)=10, (v1,v2)=4, (v2,v3)=2, (v2,v5)=5, (v3,v4)=6, (v5,v4)=2
# 源点 v0；最终 dist：v1=3, v2=7, v3=9, v5=12, v4=14；加入次序 v0,v1,v2,v3,v5,v4
# 绿色实线 = 最短路径树上的边；灰色虚线 = 未入选的边；节点下方标注最终最短距离
# 输出: /home/z/my-project/public/mocks/m02/q42.png
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Bold.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8.6, 4.7), dpi=150, constrained_layout=True)
ax.set_xlim(0.1, 10.5)
ax.set_ylim(0.15, 6.05)
ax.axis('off')

R = 0.42  # 结点圆半径
pos = {
    'v0': (1.0, 3.0),
    'v1': (3.0, 1.6),
    'v2': (5.0, 3.2),
    'v3': (7.2, 5.0),
    'v5': (7.2, 1.4),
    'v4': (9.4, 3.2),
}
dist_label = {
    'v0': '源点',
    'v1': 'd = 3',
    'v2': 'd = 7',
    'v3': 'd = 9',
    'v4': 'd = 14',
    'v5': 'd = 12',
}

C_TREE, C_OTHER = '#10b981', '#9ca3af'
T_TREE, T_OTHER = '#065f46', '#6b7280'
C_NODE, T_NODE = '#2563eb', '#1e3a8a'
C_SRC = '#10b981'

# (起点, 终点, 权值, 是否最短路径树上的边)
edges = [
    ('v0', 'v1', 3, True),
    ('v1', 'v2', 4, True),
    ('v2', 'v3', 2, True),
    ('v2', 'v5', 5, True),
    ('v5', 'v4', 2, True),
    ('v0', 'v3', 10, False),
    ('v3', 'v4', 6, False),
]

# ---- 标题 ----
ax.text(5.3, 5.72, '题 42 图：带权有向图 G（源点 v0，绿色实线为最短路径树上的边）',
        ha='center', va='bottom', fontsize=13, fontweight='bold', color='#111827')

# ---- 边（带箭头）与权值标签 ----
for u, v, w, on_tree in edges:
    (x0, y0), (x1, y1) = pos[u], pos[v]
    dx, dyv = x1 - x0, y1 - y0
    L = (dx * dx + dyv * dyv) ** 0.5
    ux, uy = dx / L, dyv / L
    sx, sy = x0 + ux * R, y0 + uy * R
    ex, ey = x1 - ux * (R + 0.06), y1 - uy * (R + 0.06)
    color = C_TREE if on_tree else C_OTHER
    ls = '-' if on_tree else (0, (6, 4))
    ax.add_patch(mpatches.FancyArrowPatch(
        (sx, sy), (ex, ey), arrowstyle='-|>', mutation_scale=17,
        lw=2.2 if on_tree else 1.8, color=color, linestyle=ls, zorder=2))
    # 权值标签放在边中点，白色底框遮挡线条
    mx, my = (sx + ex) / 2, (sy + ey) / 2
    ax.text(mx, my, str(w), ha='center', va='center', fontsize=11.5,
            fontweight='bold', color=(T_TREE if on_tree else T_OTHER), zorder=4,
            bbox=dict(boxstyle='round,pad=0.18', facecolor='white',
                      edgecolor=(C_TREE if on_tree else C_OTHER), linewidth=1.4))

# ---- 结点 ----
for name, (x, y) in pos.items():
    if name == 'v0':
        ax.add_patch(mpatches.Circle((x, y), R, facecolor=C_SRC,
                                     edgecolor='#065f46', linewidth=2.2, zorder=3))
        ax.text(x, y, name, ha='center', va='center', fontsize=13,
                fontweight='bold', color='white', zorder=4)
    else:
        ax.add_patch(mpatches.Circle((x, y), R, facecolor='white',
                                     edgecolor=C_NODE, linewidth=2.2, zorder=3))
        ax.text(x, y, name, ha='center', va='center', fontsize=13,
                fontweight='bold', color=T_NODE, zorder=4)
    # 结点下方标注源点身份 / 最终最短距离
    ax.text(x, y - R - 0.22, dist_label[name], ha='center', va='top',
            fontsize=10.5, color='#4b5563', zorder=4)

# ---- 图例 ----
handles = [
    Line2D([0], [0], color=C_TREE, lw=2.2, linestyle='-',
           label='最短路径树上的边（松弛成功）'),
    Line2D([0], [0], color=C_OTHER, lw=1.8, linestyle=(0, (6, 4)),
           label='未入选的边'),
]
legend = ax.legend(handles=handles, loc='lower left', fontsize=10,
                   framealpha=0.95, edgecolor='#cbd5e1',
                   borderpad=0.7, handlelength=2.2)
legend.set_zorder(5)

fig.savefig('/home/z/my-project/public/mocks/m02/q42.png')
print('saved: /home/z/my-project/public/mocks/m02/q42.png')
