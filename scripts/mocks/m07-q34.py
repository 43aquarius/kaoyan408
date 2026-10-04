# -*- coding: utf-8 -*-
# 全真模拟卷（七）· C 段 第 34 题配图：路由聚合的二进制前缀对齐
# 4 个网段 192.168.{72,73,74,76}.0/24 的第三字节二进制对齐，
# 标注公共前缀 01001（/21）与 /22 的覆盖范围差异、聚合结果
# 输出: /home/z/my-project/public/mocks/m07/q34.png
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
from matplotlib.patches import Rectangle, FancyBboxPatch

plt.rcParams['font.sans-serif'] = [_font_family, 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(9.4, 6.2), dpi=150, constrained_layout=True)

# ---------- 上半部分：四个网段第三字节的二进制对齐 ----------
rows = [
    ('192.168.72.0/24', '01001000'),
    ('192.168.73.0/24', '01001001'),
    ('192.168.74.0/24', '01001010'),
    ('192.168.76.0/24', '01001100'),
]
X0, CW, CH = 4.3, 0.78, 0.62
row_y = [10.0, 9.15, 8.3, 7.45]

for (label, bits), y in zip(rows, row_y):
    ax.text(X0 - 0.35, y + CH / 2, label, fontsize=11, ha='right', va='center',
            color='#17324d')
    for i, b in enumerate(bits):
        x = X0 + i * CW
        if i < 5:
            fc, ec, tc = '#dcfce7', '#15803d', '#14532d'      # 公共前缀 01001
        elif label.startswith('192.168.76') and i == 5:
            fc, ec, tc = '#fee2e2', '#b91c1c', '#7f1d1d'      # 76 在第 6 位分歧
        else:
            fc, ec, tc = '#f3f4f6', '#9ca3af', '#374151'
        ax.add_patch(Rectangle((x, y), CW - 0.08, CH, facecolor=fc, edgecolor=ec, lw=1.6))
        ax.text(x + (CW - 0.08) / 2, y + CH / 2, b, fontsize=11.5,
                ha='center', va='center', color=tc)

# 公共前缀括线（第三字节前 5 位）
px0, px1 = X0, X0 + 5 * CW - 0.08
py = row_y[0] + CH + 0.3
ax.plot([px0, px1], [py, py], color='#15803d', lw=2.0)
ax.plot([px0, px0], [py - 0.14, py + 0.06], color='#15803d', lw=2.0)
ax.plot([px1, px1], [py - 0.14, py + 0.06], color='#15803d', lw=2.0)
ax.text((px0 + px1) / 2, py + 0.2, '公共前缀 01001（第三字节前 5 位）',
        fontsize=11.5, color='#15803d', ha='center', va='bottom', fontweight='bold')

# 变化位标注（虚线括线）
vx0, vx1 = X0 + 5 * CW, X0 + 8 * CW - 0.08
ax.plot([vx0, vx1], [py, py], color='#6b7280', lw=1.8, ls=(0, (4, 3)))
ax.plot([vx0, vx0], [py - 0.14, py + 0.06], color='#6b7280', lw=1.8, ls=(0, (4, 3)))
ax.plot([vx1, vx1], [py - 0.14, py + 0.06], color='#6b7280', lw=1.8, ls=(0, (4, 3)))
ax.text((vx0 + vx1) / 2, py + 0.2, '变化位', fontsize=11, color='#6b7280',
        ha='center', va='bottom')

# 76 第 6 位分歧说明
ax.annotate('76 的第 6 位为 1\n与 72~74 不同',
            xy=(X0 + 5 * CW + 0.35, row_y[3]), xytext=(10.9, 6.85),
            fontsize=10.5, color='#b91c1c', ha='left', va='top',
            arrowprops=dict(arrowstyle='->', color='#b91c1c', lw=1.6))

# ---------- 下半部分：/22 与 /21 的覆盖范围 ----------
ax.text(0.55, 6.72, '两种候选前缀对第三字节 72~79 的覆盖范围：',
        fontsize=12, color='#111827', fontweight='bold', ha='left')

by = 5.2
for i, v in enumerate(range(72, 80)):
    x = X0 + i * CW
    if v in (72, 73, 74, 76):
        fc, ec, tc = '#dbeafe', '#1d4ed8', '#1e3a8a'   # 已分配网段
    else:
        fc, ec, tc = 'white', '#9ca3af', '#6b7280'      # 未分配网段
    ax.add_patch(Rectangle((x, by), CW - 0.08, CH, facecolor=fc, edgecolor=ec, lw=1.8))
    ax.text(x + (CW - 0.08) / 2, by + CH / 2, str(v), fontsize=11.5,
            ha='center', va='center', color=tc, fontweight='bold')

ax.text(X0 - 0.35, by + CH / 2, '第三字节', fontsize=11, ha='right', va='center',
        color='#17324d')
ax.text(10.95, by + CH / 2, '蓝色：已分配网段\n白色：未分配网段', fontsize=10.5,
        color='#4b5563', ha='left', va='center')

# /22 括线：只覆盖 72~75
b1x0, b1x1 = X0, X0 + 4 * CW - 0.08
b1y = by - 0.28
ax.plot([b1x0, b1x1], [b1y, b1y], color='#b91c1c', lw=2.0)
ax.plot([b1x0, b1x0], [b1y + 0.12, b1y - 0.06], color='#b91c1c', lw=2.0)
ax.plot([b1x1, b1x1], [b1y + 0.12, b1y - 0.06], color='#b91c1c', lw=2.0)
ax.text((b1x0 + b1x1) / 2, b1y - 0.16,
        '/22（010010xx）：只覆盖 72~75，漏掉网段 76，聚合不完整',
        fontsize=11, color='#b91c1c', ha='center', va='top')

# /21 括线：覆盖 72~79
b2x0, b2x1 = X0, X0 + 8 * CW - 0.08
b2y = b1y - 0.94
ax.plot([b2x0, b2x1], [b2y, b2y], color='#15803d', lw=2.2)
ax.plot([b2x0, b2x0], [b2y + 0.12, b2y - 0.06], color='#15803d', lw=2.2)
ax.plot([b2x1, b2x1], [b2y + 0.12, b2y - 0.06], color='#15803d', lw=2.2)
ax.text((b2x0 + b2x1) / 2, b2y - 0.16,
        '/21（01001xxx）：覆盖 72~79 共 8 个 /24，其中 4 个未分配',
        fontsize=11, color='#15803d', ha='center', va='top')

# 结果框
ax.add_patch(FancyBboxPatch((2.4, 1.9), 7.6, 0.9, boxstyle='round,pad=0.12',
                            facecolor='#dcfce7', edgecolor='#15803d', lw=2.0))
ax.text(6.2, 2.35, '最短聚合前缀：192.168.72.0/21', fontsize=13.5, color='#14532d',
        ha='center', va='center', fontweight='bold')

ax.set_title('路由聚合：第三字节的二进制前缀对齐', fontsize=13.5, color='#111827', pad=10)
ax.set_xlim(0.2, 13.6)
ax.set_ylim(1.4, 11.8)
ax.axis('off')

os.makedirs('/home/z/my-project/public/mocks/m07', exist_ok=True)
fig.savefig('/home/z/my-project/public/mocks/m07/q34.png')
print('saved: /home/z/my-project/public/mocks/m07/q34.png')
