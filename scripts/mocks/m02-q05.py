# -*- coding: utf-8 -*-
# 全真模拟卷（二）· A 段 第 5 题配图：BST 结构图（依次插入 50,33,72,18,41,60,85,8,25）
# 输出: /home/z/my-project/public/mocks/m02/q05.png
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

fig, ax = plt.subplots(figsize=(7, 4), dpi=150, constrained_layout=True)

# ---- 结点坐标（根 50 在第 1 层，y 值即层数）----
nodes = {
    50: (5.0, 4.0),
    33: (2.5, 3.0), 72: (7.5, 3.0),
    18: (1.25, 2.0), 41: (3.75, 2.0), 60: (6.25, 2.0), 85: (8.75, 2.0),
    8: (0.65, 1.0), 25: (1.85, 1.0),
}
edges = [(50, 33), (50, 72), (33, 18), (33, 41),
         (72, 60), (72, 85), (18, 8), (18, 25)]

# ---- 层标志虚线与层标签 ----
for lvl, y in [(1, 1.0), (2, 2.0), (3, 3.0), (4, 4.0)]:
    ax.axhline(y, color='#b9c4d0', lw=1.2, ls='--', zorder=0)
    ax.text(-0.55, y, '第 ' + str(lvl) + ' 层', ha='right', va='center',
            fontsize=10.5, color='#5b6b7c')

# ---- 树枝 ----
for a, b in edges:
    (x1, y1), (x2, y2) = nodes[a], nodes[b]
    ax.plot([x1, x2], [y1, y2], color='#3a6ea5', lw=1.8, zorder=1)

# ---- 结点（圆圈 + 关键字）----
for val, (x, y) in nodes.items():
    circle = plt.Circle((x, y), 0.32, facecolor='#e8f1fb',
                        edgecolor='#2c5f8a', lw=1.8, zorder=2)
    ax.add_patch(circle)
    ax.text(x, y, str(val), ha='center', va='center', fontsize=11.5,
            fontweight='bold', color='#17324d', zorder=3)

# ---- 标题与图注 ----
ax.set_title('依次插入 {50, 33, 72, 18, 41, 60, 85, 8, 25} 得到的二叉排序树',
             fontsize=12.5, color='#111827', pad=10)
ax.text(5.0, 0.35, '注：结点内数字为关键字，根结点 50 位于第 1 层。',
        ha='center', va='center', fontsize=10, color='#6b7280')

ax.set_xlim(-1.7, 10.1)
ax.set_ylim(0.0, 4.75)
ax.axis('off')

os.makedirs('/home/z/my-project/public/mocks/m02', exist_ok=True)
fig.savefig('/home/z/my-project/public/mocks/m02/q05.png')
print('saved: /home/z/my-project/public/mocks/m02/q05.png')
