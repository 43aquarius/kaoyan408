# -*- coding: utf-8 -*-
# 模拟卷八 A 段 第 8 题配图：4 顶点无向图 G 与其邻接矩阵 M 对照
# 顶点：A、B、C、D；边：(A,B) (B,C) (B,D) (C,D)
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

fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), dpi=150, constrained_layout=True)

# ---------- 左图：无向图 G ----------
ax = axes[0]
R = 0.075
V = {'A': (0.50, 0.86), 'B': (0.86, 0.50), 'C': (0.50, 0.14), 'D': (0.14, 0.50)}
E = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('B', 'D')]
for u, v in E:
    ax.annotate('', xy=V[v], xytext=V[u],
                arrowprops=dict(arrowstyle='-', color='#475569', lw=2.0,
                                shrinkA=40, shrinkB=40), zorder=2)
DEG = {'A': 1, 'B': 3, 'C': 2, 'D': 2}
DEG_POS = {'A': (0.50, 0.985), 'B': (0.975, 0.50),
           'C': (0.50, 0.015), 'D': (0.025, 0.50)}
for name, (x, y) in V.items():
    ax.add_patch(plt.Circle((x, y), R, facecolor='#dbeafe', edgecolor='#2563eb',
                            lw=2.0, zorder=3))
    ax.text(x, y, name, ha='center', va='center', fontsize=13, fontweight='bold',
            color='#1e3a8a', zorder=4)
for name, (x, y) in DEG_POS.items():
    ax.text(x, y, '度=' + str(DEG[name]), ha='center', va='center', fontsize=10.5,
            color='#dc2626', fontweight='bold', zorder=4)
ax.set_title('无向图 G：4 个顶点，4 条边', fontsize=12, fontweight='bold')
ax.set_xlim(-0.07, 1.10)
ax.set_ylim(-0.07, 1.07)
ax.axis('off')

# ---------- 右图：邻接矩阵 M ----------
ax2 = axes[1]
labels = ['A', 'B', 'C', 'D']
M = [[0, 1, 0, 0],
     [1, 0, 1, 1],
     [0, 1, 0, 1],
     [0, 1, 1, 0]]
cw, ch, hw, hh = 0.155, 0.15, 0.20, 0.165
x0, y_top = 0.09, 0.97

# 左上角：矩阵名 M
ax2.add_patch(plt.Rectangle((x0, y_top - hh), hw, hh, facecolor='#f1f5f9',
                            edgecolor='#64748b', lw=1.5))
ax2.text(x0 + hw / 2, y_top - hh / 2, 'M', ha='center', va='center',
         fontsize=12, fontweight='bold', color='#334155')
# 列表头
for j, lab in enumerate(labels):
    ax2.add_patch(plt.Rectangle((x0 + hw + j * cw, y_top - hh), cw, hh,
                                facecolor='#e2e8f0', edgecolor='#64748b', lw=1.5))
    ax2.text(x0 + hw + j * cw + cw / 2, y_top - hh / 2, lab, ha='center',
             va='center', fontsize=12, fontweight='bold', color='#334155')
# 数据行（B 行高亮：度 = 第 B 行元素之和）
for i, lab in enumerate(labels):
    top = y_top - hh - i * ch
    hl = (lab == 'B')
    ax2.add_patch(plt.Rectangle((x0, top - ch), hw, ch,
                                facecolor='#fef9c3' if hl else '#e2e8f0',
                                edgecolor='#64748b', lw=1.5))
    ax2.text(x0 + hw / 2, top - ch / 2, lab, ha='center', va='center',
             fontsize=12, fontweight='bold', color='#334155')
    for j in range(4):
        ax2.add_patch(plt.Rectangle((x0 + hw + j * cw, top - ch), cw, ch,
                                    facecolor='#fef9c3' if hl else 'white',
                                    edgecolor='#64748b', lw=1.5))
        val = M[i][j]
        ax2.text(x0 + hw + j * cw + cw / 2, top - ch / 2, str(val),
                 ha='center', va='center', fontsize=12.5,
                 fontweight='bold' if val == 1 else 'normal',
                 color='#1d4ed8' if val == 1 else '#94a3b8')

notes = ('M 为对称矩阵：无向边 (u,v) 使 M[u][v]=M[v][u]=1\n'
         '顶点的度 = 对应行元素之和，如第 B 行 1+1+1=3 = TD(B)\n'
         'M 的全部元素之和 = 2|E| = 2×4 = 8')
ax2.text(0.5, 0.175, notes, ha='center', va='top', fontsize=10, color='#334155',
         linespacing=1.6, bbox=dict(boxstyle='round,pad=0.45',
                                    facecolor='#f8fafc', edgecolor='#94a3b8', lw=1.2))
ax2.set_title('G 的邻接矩阵 M（行、列均按 A、B、C、D 排列）',
              fontsize=12, fontweight='bold')
ax2.set_xlim(0, 1)
ax2.set_ylim(-0.07, 1.02)
ax2.axis('off')

fig.suptitle('无向图 G 与其邻接矩阵 M：对称 · 度 = 行和 · 总和 = 2×边数',
             fontsize=13, fontweight='bold')

fig.savefig('/home/z/my-project/public/mocks/m08/q08.png')
print('saved: /home/z/my-project/public/mocks/m08/q08.png')
