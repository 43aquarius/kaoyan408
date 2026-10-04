# -*- coding: utf-8 -*-
# 全真模拟卷（四）· A 段 第 9 题配图：AOE 网（源点 V1、汇点 V6，弧上标注活动名与持续时间）
# 输出: /home/z/my-project/public/mocks/m04/q09.png
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

fig, ax = plt.subplots(figsize=(8.6, 5.4), dpi=150, constrained_layout=True)

NODE_R = 0.5

pos = {
    'V1': (1.4, 4.5),
    'V2': (5.0, 7.4),
    'V3': (5.0, 1.6),
    'V4': (9.6, 7.4),
    'V5': (9.6, 1.6),
    'V6': (13.2, 4.5),
}

# 弧：(起点, 终点, 活动名, 权, 弯曲, 标签偏移)
edges = [
    ('V1', 'V2', 'a1', 6, 0.0, (-0.15, 0.32)),
    ('V1', 'V3', 'a2', 4, 0.0, (-0.15, -0.34)),
    ('V2', 'V4', 'a3', 7, 0.0, (0.0, 0.34)),
    ('V2', 'V5', 'a4', 3, -0.25, (-0.55, 0.25)),
    ('V3', 'V5', 'a5', 9, 0.0, (0.0, -0.34)),
    ('V3', 'V4', 'a6', 5, -0.25, (0.62, -0.22)),
    ('V4', 'V6', 'a7', 4, 0.0, (0.12, 0.32)),
    ('V5', 'V6', 'a8', 2, 0.0, (0.12, -0.34)),
]

for a, b, name, w, rad, (dx, dy) in edges:
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color='#3a6ea5', lw=1.9,
                                shrinkA=15, shrinkB=15,
                                connectionstyle=f'arc3,rad={rad}'),
                zorder=1)
    mx, my = (x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy
    ax.text(mx, my, f'{name}={w}', fontsize=10.5, color='#b3261e',
            ha='center', va='center', zorder=4,
            bbox=dict(boxstyle='round,pad=0.18', facecolor='white',
                      edgecolor='#d8b4b0', lw=0.8, alpha=0.95))

# 顶点：V1 源点、V6 汇点特殊着色
for label, (x, y) in pos.items():
    if label == 'V1':
        fc, ec, tag = '#dcfce7', '#15803d', '源点'
    elif label == 'V6':
        fc, ec, tag = '#ffedd5', '#c2410c', '汇点'
    else:
        fc, ec, tag = '#e8f1fb', '#2c5f8a', None
    c = plt.Circle((x, y), NODE_R, facecolor=fc, edgecolor=ec, lw=2.0, zorder=3)
    ax.add_patch(c)
    ax.text(x, y, label, ha='center', va='center', fontsize=11.5, fontweight='bold',
            color='#17324d', zorder=4)
    if tag:
        ax.text(x, y - 0.85, tag, fontsize=10.5, color=ec, ha='center', va='center',
                fontweight='bold')

ax.text(7.3, 0.25, '弧上标注为“活动名 = 持续时间”；事件 Vj 的最早发生时间 ve(j) 由其入边活动决定，'
                   '工期 = 源点到汇点最长路径的长度',
        fontsize=10.5, color='#4b5563', ha='center', va='center')

ax.set_title('AOE 网（Activity On Edge）', fontsize=13, color='#111827', pad=10)
ax.set_xlim(0.2, 14.4)
ax.set_ylim(-0.3, 8.6)
ax.axis('off')

os.makedirs('/home/z/my-project/public/mocks/m04', exist_ok=True)
fig.savefig('/home/z/my-project/public/mocks/m04/q09.png')
print('saved: /home/z/my-project/public/mocks/m04/q09.png')
