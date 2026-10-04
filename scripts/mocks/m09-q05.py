# -*- coding: utf-8 -*-
# 全真模拟卷（九）· A 段 第 5 题配图：文件系统目录树的双亲表示法存储图（结点数组 + 双亲指针）
# 输出: /home/z/my-project/public/mocks/m09/q05.png
import os

import matplotlib.font_manager as fm

_FONT_CANDIDATES = [
    ('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf', 'Sarasa Mono SC'),
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
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams['font.sans-serif'] = [_font_family, 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7.7, 6.2), dpi=150, constrained_layout=True)

# ---------------- 数据（下标即数组位置 0..8） ----------------
nodes = [
    ('/', -1),     # 0 根目录
    ('home', 0),   # 1
    ('etc', 0),    # 2
    ('user1', 1),  # 3
    ('user2', 1),  # 4
    ('docs', 3),   # 5
    ('pics', 3),   # 6
    ('src', 5),    # 7 当前目录
    ('bin', 0),    # 8
]
edges = [(0, 1), (0, 2), (0, 8), (1, 3), (1, 4), (3, 5), (3, 6), (5, 7)]

# 目录树结点坐标 (x, y)，自上而下 5 层
pos = {
    0: (2.40, 9.50),
    1: (0.90, 8.20), 2: (2.40, 8.20), 8: (3.90, 8.20),
    3: (0.50, 6.90), 4: (1.90, 6.90),
    5: (0.05, 5.60), 6: (1.25, 5.60),
    7: (0.05, 4.30),
}

# ---------------- 左侧：目录树 ----------------
for a, b in edges:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.plot([x1, x2], [y1 - 0.27, y2 + 0.27], color='#3a6ea5', lw=1.8, zorder=1)

for idx, (name, _) in enumerate(nodes):
    x, y = pos[idx]
    is_cur = (idx == 7)
    box = FancyBboxPatch((x - 0.5, y - 0.26), 1.0, 0.52,
                         boxstyle='round,pad=0.02,rounding_size=0.10',
                         facecolor='#dcfce7' if is_cur else '#e8f1fb',
                         edgecolor='#15803d' if is_cur else '#2c5f8a',
                         lw=2.0 if is_cur else 1.6, zorder=2)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=10.5,
            fontweight='bold', color='#14532d' if is_cur else '#17324d', zorder=3)
    ax.text(x - 0.62, y, str(idx), ha='right', va='center', fontsize=10,
            color='#334155', zorder=3,
            bbox=dict(boxstyle='round,pad=0.18', facecolor='#f8fafc',
                      edgecolor='#94a3b8', lw=0.9))

ax.text(1.95, 10.80, '目录树（结点左侧数字为数组下标）', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#334155')

# ---------------- 右侧：双亲表示法结点数组 ----------------
COLS = [('下标', 5.30, 6.30), ('data 域', 6.30, 8.00), ('parent 域', 8.00, 9.20)]
HEAD_Y0, HEAD_Y1 = 9.95, 10.55
ROW_H = 0.62


def row_y(i):
    return 9.50 - 0.75 * i


for (label, x0, x1) in COLS:
    ax.add_patch(Rectangle((x0, HEAD_Y0), x1 - x0, HEAD_Y1 - HEAD_Y0,
                           facecolor='#1f3b57', edgecolor='#0f2437', lw=1.3, zorder=2))
    ax.text((x0 + x1) / 2, (HEAD_Y0 + HEAD_Y1) / 2, label, ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#ffffff', zorder=3)

for i, (name, par) in enumerate(nodes):
    y = row_y(i)
    y0, y1 = y - ROW_H / 2, y + ROW_H / 2
    base = '#dcfce7' if i == 7 else ('#f1f5f9' if i % 2 == 1 else '#ffffff')
    for (_label, x0, x1) in COLS:
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=base,
                               edgecolor='#64748b', lw=1.2, zorder=2))
    ax.text(5.80, y, str(i), ha='center', va='center', fontsize=10.5,
            fontweight='bold', color='#0f172a', zorder=3)
    ax.text(7.15, y, name, ha='center', va='center', fontsize=10.5,
            color='#0f172a', zorder=3)
    ax.text(8.60, y, str(par), ha='center', va='center', fontsize=10.5,
            fontweight='bold', color='#b45309', zorder=3)

ax.text(7.25, 10.80, '双亲表示法：结点数组（data 域 + parent 域）',
        ha='center', va='center', fontsize=11, fontweight='bold', color='#334155')

# ---------------- 双亲指针箭头（parent 域 → 双亲所在行） ----------------
ARROW_RAD = {1: -0.75, 2: -0.42, 3: -0.38, 4: -0.30, 5: -0.38, 6: -0.30, 7: -0.38, 8: -0.13}
for i in range(1, 9):
    par = nodes[i][1]
    arrow = FancyArrowPatch((9.26, row_y(i)), (9.26, row_y(par)),
                            connectionstyle='arc3,rad=%.2f' % ARROW_RAD[i],
                            arrowstyle='-|>', mutation_scale=13,
                            lw=1.6, color='#d97706', zorder=4)
    ax.add_patch(arrow)

# ---------------- 标题与图注 ----------------
ax.set_title('目录树的双亲表示法存储（结点数组 + 双亲指针）',
             fontsize=12.5, color='#111827', pad=8)
ax.text(4.65, 2.62, 'parent 域存放双亲结点的数组下标（根结点为 -1）；橙色箭头由 parent 域指向双亲所在行。',
        ha='center', va='center', fontsize=10, color='#475569')
ax.text(4.65, 2.18, '绿色高亮为当前工作目录 src（下标 7）；其向上路径为 src → docs → user1 → home → /。',
        ha='center', va='center', fontsize=10, color='#475569')

ax.set_xlim(-0.95, 10.60)
ax.set_ylim(1.85, 11.15)
ax.axis('off')

os.makedirs('/home/z/my-project/public/mocks/m09', exist_ok=True)
fig.savefig('/home/z/my-project/public/mocks/m09/q05.png')
print('saved: /home/z/my-project/public/mocks/m09/q05.png')
