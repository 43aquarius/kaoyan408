# -*- coding: utf-8 -*-
# 全真模拟卷（四）· A 段 第 5 题配图：中序线索二叉树（结点 + 孩子指针实线 / 线索指针虚线）
# 输出: /home/z/my-project/public/mocks/m04/q05.png
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

plt.rcParams['font.sans-serif'] = [_font_family, 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(9.5, 6.4), dpi=150, constrained_layout=True)

NODE_R = 0.34

# 结点坐标（与题干结构一致：A 根；A 左 B 右 C；B 左 D 右 E；E 只右孩子 G；
# G 只左孩子 H；C 只左孩子 F；D、H、F 为叶子）
pos = {
    'A': (7.0, 7.4),
    'B': (3.8, 5.7),
    'C': (11.6, 5.7),
    'D': (1.6, 4.0),
    'E': (6.2, 4.0),
    'F': (13.0, 4.0),
    'G': (7.6, 2.3),
    'H': (5.5, 0.8),
}

# 孩子指针（实线）
child_edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('E', 'G'), ('G', 'H'), ('C', 'F')]

# 线索指针（虚线，箭头）：起点 -> 终点，标注
threads = [
    ('D', 'B', 'D.rchild', (1.9, 5.05)),
    ('E', 'B', 'E.lchild', (4.55, 5.05)),
    ('H', 'E', 'H.lchild', (5.28, 2.45)),
    ('H', 'G', 'H.rchild', (6.72, 1.35)),
    ('G', 'A', 'G.rchild', (9.35, 4.9)),
    ('F', 'A', 'F.lchild', (10.6, 6.6)),
    ('F', 'C', 'F.rchild', (12.65, 5.0)),
]

for a, b in child_edges:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.plot([x1, x2], [y1, y2], color='#2c5f8a', lw=2.0, zorder=1)

for a, b, label, (lx, ly) in threads:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    rad = 0.22 if (a, b) != ('G', 'A') else -0.38
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#c2410c', lw=1.7,
                                linestyle=(0, (5, 3)), shrinkA=13, shrinkB=13,
                                connectionstyle=f'arc3,rad={rad}'),
                zorder=2)
    ax.text(lx, ly, label, fontsize=10, color='#c2410c', ha='center', va='center', zorder=5)

# 指向 NULL 的两条边界线索
ax.annotate('', xy=(-0.1, 4.0), xytext=pos['D'],
            arrowprops=dict(arrowstyle='->', color='#c2410c', lw=1.7,
                            linestyle=(0, (5, 3)), shrinkA=13, shrinkB=2), zorder=2)
ax.text(0.05, 4.42, 'D.lchild\nNULL', fontsize=10, color='#c2410c', ha='left', va='center')
ax.annotate('', xy=(14.9, 5.7), xytext=pos['C'],
            arrowprops=dict(arrowstyle='->', color='#c2410c', lw=1.7,
                            linestyle=(0, (5, 3)), shrinkA=13, shrinkB=2), zorder=2)
ax.text(14.75, 6.12, 'C.rchild\nNULL', fontsize=10, color='#c2410c', ha='right', va='center')

# 结点圆圈
for label, (x, y) in pos.items():
    c = plt.Circle((x, y), NODE_R, facecolor='#e8f1fb', edgecolor='#2c5f8a',
                   lw=1.9, zorder=3)
    ax.add_patch(c)
    ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold',
            color='#17324d', zorder=4)

# 图例说明
ax.plot([0.5, 1.5], [8.35, 8.35], color='#2c5f8a', lw=2.0)
ax.text(1.7, 8.35, '孩子指针（ltag/rtag = 0）', fontsize=10.5, color='#17324d', va='center')
ax.plot([6.4, 7.4], [8.35, 8.35], color='#c2410c', lw=1.7, linestyle=(0, (5, 3)))
ax.text(7.6, 8.35, '线索指针（ltag/rtag = 1，指向前驱/后继）', fontsize=10.5, color='#17324d', va='center')

# 中序序列
ax.text(7.4, -0.25, '中序序列：D → B → E → H → G → A → F → C', fontsize=11.5,
        color='#111827', ha='center', va='center', fontweight='bold')

ax.set_title('中序线索二叉树（实线为孩子，虚线为线索）', fontsize=13, color='#111827', pad=10)
ax.set_xlim(-0.4, 15.2)
ax.set_ylim(-0.8, 8.8)
ax.axis('off')

os.makedirs('/home/z/my-project/public/mocks/m04', exist_ok=True)
fig.savefig('/home/z/my-project/public/mocks/m04/q05.png')
print('saved: /home/z/my-project/public/mocks/m04/q05.png')
