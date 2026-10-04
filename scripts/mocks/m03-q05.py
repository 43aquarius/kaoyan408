# -*- coding: utf-8 -*-
# 全真模拟卷（三）· A 段 第 5 题配图：四种易混二叉树对比（满 / 完全 / 二叉排序树 / 平衡二叉树）
# 输出: /home/z/my-project/public/mocks/m03/q05.png
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

fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.8), dpi=150, constrained_layout=True)


def draw_tree(ax, title, nodes, edges, note, dashed=(), extras=(), xlim=(0, 8), ylim=(1.55, 4.75)):
    """nodes: {label: (x, y)}; edges: [(a, b)]; note: 面板底部说明;
    dashed: 缺失结点位置; extras: [(x, y, text)] 附加标注"""
    ax.set_title(title, fontsize=12.5, color='#111827', pad=8)
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        ax.plot([x1, x2], [y1, y2], color='#3a6ea5', lw=1.8, zorder=1)
    for (x, y) in dashed:
        c = plt.Circle((x, y), 0.30, facecolor='none', edgecolor='#9aa5b1',
                       lw=1.5, ls='--', zorder=2)
        ax.add_patch(c)
    for label, (x, y) in nodes.items():
        c = plt.Circle((x, y), 0.30, facecolor='#e8f1fb',
                       edgecolor='#2c5f8a', lw=1.8, zorder=3)
        ax.add_patch(c)
        ax.text(x, y, str(label), ha='center', va='center', fontsize=10.5,
                fontweight='bold', color='#17324d', zorder=4)
    for (x, y, text) in extras:
        ax.text(x, y, text, ha='center', va='center', fontsize=10,
                color='#b3261e', fontweight='bold', zorder=5)
    ax.text(0.5, 0.015, note, transform=ax.transAxes, ha='center', va='bottom',
            fontsize=10, color='#4b5563')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis('off')


# ---- 左上：满二叉树（高度 3，7 个结点）----
full_nodes = {1: (4.0, 4.0), 2: (2.0, 3.0), 3: (6.0, 3.0),
              4: (1.0, 2.0), 5: (3.0, 2.0), 6: (5.0, 2.0), 7: (7.0, 2.0)}
full_edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]
full_levels = [(0.15, 4.0, '第1层'), (0.15, 3.0, '第2层'), (0.15, 2.0, '第3层')]

ax00 = axes[0][0]
draw_tree(ax00, '满二叉树（高度 h = 3）', full_nodes, full_edges,
          '每层都满：第 k 层 2^(k-1) 个结点，共 2^h - 1 = 7 个；不存在度为 1 的结点',
          extras=[], xlim=(0, 8), ylim=(1.55, 4.75))

# ---- 右上：完全二叉树（n = 10，高度 4）----
comp_nodes = {1: (4.5, 5.0), 2: (2.5, 4.0), 3: (6.5, 4.0),
              4: (1.5, 3.0), 5: (3.5, 3.0), 6: (5.5, 3.0), 7: (7.5, 3.0),
              8: (1.0, 2.0), 9: (2.0, 2.0), 10: (3.0, 2.0)}
comp_edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10)]
ax01 = axes[0][1]
draw_tree(ax01, '完全二叉树（n = 10，高度 4）', comp_nodes, comp_edges,
          '编号连续（与同高度满二叉树一致）；最底层缺位只能靠右留空（5 号缺右孩子）',
          dashed=[(4.0, 2.0)], extras=[(4.0, 1.45, '缺位')],
          xlim=(0.2, 8.3), ylim=(1.15, 5.75))

# ---- 左下：二叉排序树（依次插入 20, 10, 30, 5, 3）----
bst_nodes = {20: (4.0, 4.0), 10: (2.2, 3.0), 30: (6.0, 3.0), 5: (1.1, 2.0), 3: (0.35, 1.0)}
bst_edges = [(20, 10), (20, 30), (10, 5), (5, 3)]
ax10 = axes[1][0]
draw_tree(ax10, '二叉排序树（依次插入 20, 10, 30, 5, 3）', bst_nodes, bst_edges,
          '中序序列 3,5,10,20,30 递增；形态随插入次序改变，最坏退化为斜链（本例高度 4）',
          xlim=(0, 8), ylim=(0.55, 4.75))

# ---- 右下：平衡二叉树 AVL（标注平衡因子 BF）----
avl_nodes = {30: (4.0, 4.0), 20: (2.0, 3.0), 40: (6.0, 3.0),
             10: (1.0, 2.0), 25: (3.0, 2.0), 35: (5.0, 2.0)}
avl_edges = [(30, 20), (30, 40), (20, 10), (20, 25), (40, 35)]
avl_bf = [(4.45, 3.72, 'BF=0'), (2.45, 2.72, 'BF=0'), (6.45, 2.72, 'BF=+1'),
          (1.45, 1.72, 'BF=0'), (3.45, 1.72, 'BF=0'), (5.45, 1.72, 'BF=0')]
ax11 = axes[1][1]
draw_tree(ax11, '平衡二叉树 AVL（旁注平衡因子 BF）', avl_nodes, avl_edges,
          '任一结点 |BF| <= 1；中序 10,20,25,30,35,40 有序；本例非完全二叉树（40 只有左孩子）',
          extras=avl_bf, xlim=(0, 8), ylim=(1.55, 4.75))

# ---- 层标注（满二叉树面板，灰色）----
for (x, y, text) in full_levels:
    ax00.text(x, y, text, ha='right', va='center', fontsize=10, color='#6b7280')

fig.suptitle('四种易混二叉树对比：满二叉树 / 完全二叉树 / 二叉排序树 / 平衡二叉树（AVL）',
             fontsize=13, color='#111827')

os.makedirs('/home/z/my-project/public/mocks/m03', exist_ok=True)
fig.savefig('/home/z/my-project/public/mocks/m03/q05.png')
print('saved: /home/z/my-project/public/mocks/m03/q05.png')
