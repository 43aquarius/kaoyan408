# -*- coding: utf-8 -*-
# 全真模拟卷（一）· A 段 第 5 题配图：10 个结点的完全二叉树示意图
# 输出: /home/z/my-project/public/mocks/m01/q05.png
import os

# 中文字体：优先使用规范指定的 Noto Sans SC，若不存在则回退到本机可用的中文字体
import matplotlib.font_manager as fm

_FONT_CANDIDATES = [
    ('/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf', 'Noto Sans SC'),
    ('/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Regular.ttf', 'Noto Serif SC'),
    ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 'WenQuanYi Zen Hei'),
]
_font_family = None
for _path, _fam in _FONT_CANDIDATES:
    if os.path.exists(_path):
        try:
            fm.fontManager.addfont(_path)
            _font_family = _fam
            break
        except Exception:
            continue
if _font_family is None:
    raise RuntimeError('no available Chinese font found')

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = [_font_family, 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150, constrained_layout=True)

# ---- 结点坐标（层序编号 1~10，根 A 在第 1 层）----
nodes = {
    'A': (7, 3),
    'B': (3, 2), 'C': (11, 2),
    'D': (1, 1), 'E': (5, 1), 'F': (9, 1), 'G': (13, 1),
    'H': (0, 0), 'I': (2, 0), 'J': (4, 0),
}
# 第 4 层剩余的 5 个空位（层序编号 11~15）
slots = [(6, 0), (8, 0), (10, 0), (12, 0), (14, 0)]

edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'),
         ('C', 'F'), ('C', 'G'), ('D', 'H'), ('D', 'I'), ('E', 'J')]

# ---- 实边 ----
for a, b in edges:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    ax.plot([x1, x2], [y1, y2], color='#334155', lw=1.8, zorder=1)

# ---- 指向空位的虚边（E、F、G 还可以继续扩展）----
slot_parents = [nodes['E'], nodes['F'], nodes['F'], nodes['G'], nodes['G']]
for (x1, y1), (x2, y2) in zip(slot_parents, slots):
    ax.plot([x1, x2], [y1, y2], color='#9ca3af', lw=1.5, ls='--', zorder=1)

# ---- 实结点 ----
xs = [p[0] for p in nodes.values()]
ys = [p[1] for p in nodes.values()]
ax.scatter(xs, ys, s=900, c='#dbeafe', edgecolors='#1d4ed8', linewidths=2, zorder=2)
for name, (x, y) in nodes.items():
    ax.text(x, y, name, ha='center', va='center', fontsize=13,
            fontweight='bold', color='#1e3a8a', zorder=3)

# ---- 结点层序编号（小号灰字，位于结点下方）----
order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
for i, name in enumerate(order):
    x, y = nodes[name]
    ax.text(x, y - 0.34, str(i + 1), ha='center', va='top',
            fontsize=10, color='#64748b', zorder=3)

# ---- 空位（灰色空心圆）----
sx = [p[0] for p in slots]
ax.scatter(sx, [0] * len(slots), s=900, c='none', edgecolors='#9ca3af',
           linewidths=1.8, zorder=2)
for i, (x, y) in enumerate(slots):
    ax.text(x, y - 0.34, str(11 + i), ha='center', va='top',
            fontsize=10, color='#9ca3af', zorder=3)

# ---- 层次标签（左侧）----
for lvl, y in [(1, 3), (2, 2), (3, 1), (4, 0)]:
    ax.text(-2.0, y, '第 ' + str(lvl) + ' 层', ha='right', va='center',
            fontsize=11, color='#475569')

# ---- 标题与图注 ----
ax.set_title('二叉树示意图（共 10 个结点，根结点 A 位于第 1 层）',
             fontsize=13, color='#111827', pad=12)
ax.text(6.1, -1.2, '注：结点下方的数字为层序编号；灰色空心圆表示第 4 层剩余的 5 个空位（编号 11 ~ 15）。',
        ha='center', va='center', fontsize=10, color='#6b7280')

ax.set_xlim(-3.6, 15.7)
ax.set_ylim(-1.7, 3.75)
ax.axis('off')

os.makedirs('/home/z/my-project/public/mocks/m01', exist_ok=True)
fig.savefig('/home/z/my-project/public/mocks/m01/q05.png')
print('saved: /home/z/my-project/public/mocks/m01/q05.png')
