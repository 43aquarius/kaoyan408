# -*- coding: utf-8 -*-
# 模拟卷七 A 段 第 5 题：AVL 插入 62 触发 RL 双旋转的前后对比图
# 插入序列：50, 30, 70, 20, 40, 60, 80, 65, 62
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

fig, axes = plt.subplots(1, 2, figsize=(10, 5.0), dpi=150, constrained_layout=True)

R = 0.042

# 结点样式：normal 普通 / unbal 最小失衡 / new 新插入 / fixed 旋转后子树
STYLES = {
    'normal': ('#dbeafe', '#2563eb', '#1e3a8a'),
    'unbal':  ('#fee2e2', '#dc2626', '#7f1d1d'),
    'new':    ('#fef9c3', '#d97706', '#713f12'),
    'fixed':  ('#dcfce7', '#16a34a', '#14532d'),
}


def draw_tree(ax, nodes, edges, title, note):
    for src, dst in edges:
        x1, y1 = nodes[src][0], nodes[src][1]
        x2, y2 = nodes[dst][0], nodes[dst][1]
        ax.annotate('', xy=(x2, y2 + R), xytext=(x1, y1 - R),
                    arrowprops=dict(arrowstyle='-', color='#64748b', lw=1.6))
    for key, (x, y, label, bf, style) in nodes.items():
        face, edge, tc = STYLES[style]
        ax.add_patch(plt.Circle((x, y), R, facecolor=face, edgecolor=edge,
                                lw=1.8, zorder=3))
        ax.text(x, y, label, ha='center', va='center', fontsize=10.5,
                color=tc, fontweight='bold', zorder=4)
        if bf is not None:
            bad = bf in ('+2', '-2')
            right = x <= 0.9
            ax.text(x + (R + 0.012 if right else -(R + 0.012)), y, 'BF=' + bf,
                    fontsize=10, color='#dc2626' if bad else '#475569',
                    fontweight='bold', ha='left' if right else 'right',
                    va='center', zorder=4)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.text(0.5, -0.05, note, ha='center', va='top', fontsize=10.5,
            color='#334155', bbox=dict(boxstyle='round,pad=0.4',
                                       facecolor='#f8fafc',
                                       edgecolor='#94a3b8', lw=1.2))
    ax.set_xlim(-0.03, 1.15)
    ax.set_ylim(-0.36, 1.06)
    ax.axis('off')


# 左图：插入 62 后（旋转前）
before = {
    '50': (0.50, 0.92, '50', '-2', 'normal'),
    '30': (0.20, 0.70, '30', '0', 'normal'),
    '70': (0.80, 0.70, '70', '+2', 'normal'),
    '20': (0.08, 0.48, '20', '0', 'normal'),
    '40': (0.32, 0.48, '40', '0', 'normal'),
    '60': (0.63, 0.48, '60', '-2', 'unbal'),
    '80': (0.95, 0.48, '80', '0', 'normal'),
    '65': (0.75, 0.27, '65', '+1', 'normal'),
    '62': (0.64, 0.07, '62', '0', 'new'),
}
before_edges = [('50', '30'), ('50', '70'), ('30', '20'), ('30', '40'),
                ('70', '60'), ('70', '80'), ('60', '65'), ('65', '62')]

# 右图：RL 双旋转后
after = {
    '50': (0.50, 0.92, '50', '-1', 'normal'),
    '30': (0.20, 0.70, '30', '0', 'normal'),
    '70': (0.80, 0.70, '70', '+1', 'normal'),
    '20': (0.08, 0.48, '20', '0', 'normal'),
    '40': (0.32, 0.48, '40', '0', 'normal'),
    '62': (0.63, 0.48, '62', '0', 'fixed'),
    '80': (0.95, 0.48, '80', '0', 'normal'),
    '60': (0.54, 0.27, '60', '0', 'fixed'),
    '65': (0.74, 0.27, '65', '0', 'fixed'),
}
after_edges = [('50', '30'), ('50', '70'), ('30', '20'), ('30', '40'),
               ('70', '62'), ('70', '80'), ('62', '60'), ('62', '65')]

draw_tree(
    axes[0], before, before_edges,
    '插入 62 后（旋转前）：最小失衡结点为 60',
    '红色结点 = 最小失衡结点（60，BF=-2）；黄色 = 新插入的 62\n'
    '62 插在 60 的右孩子 65 的左子树上，属 RL 型失衡\n'
    '70（BF=+2）、50（BF=-2）也随之失衡，应从离插入点最近的 60 调起',
)
draw_tree(
    axes[1], after, after_edges,
    'RL 双旋转后：62 升为子树根，恢复平衡',
    '先对 65 右旋（62 上移），再对 60 左旋（62 成为子树根）\n'
    '旋转后 60、62、65 的 BF 均为 0；70 变为 +1，50 变为 -1\n'
    '绿色 = 双旋转后得到的新子树（70 的左孩子由 60 换成 62）',
)

fig.suptitle('AVL 树插入 62：RL 双旋转前后对比（BF = 左子树高 - 右子树高）',
             fontsize=13, fontweight='bold')

fig.savefig('/home/z/my-project/public/mocks/m07/q05.png')
print('saved: /home/z/my-project/public/mocks/m07/q05.png')
