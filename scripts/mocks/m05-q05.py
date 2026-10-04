# -*- coding: utf-8 -*-
# 全真模拟卷（五）· A 段 第 5 题配图：4-路归并败者树（初始建树结果 + 调整路径示意）
# 数据与题干一致：F0={10,15,30} F1={9,20,25} F2={12,22,40} F3={5,18,35}
# 输出: /home/z/my-project/public/mocks/m05/q05.png
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
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = [_font_family, 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8.8, 6.6), dpi=150, constrained_layout=True)


def box(x, y, w, h, text, fc, ec, fs=10.5, lw=1.8):
    b = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                       boxstyle='round,pad=0.06',
                       facecolor=fc, edgecolor=ec, lw=lw, zorder=3)
    ax.add_patch(b)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs,
            color='#111827', zorder=4, fontweight='bold')


def arrow(p1, p2, color='#3a6ea5', lw=1.8, ls='solid', z=2):
    a = FancyArrowPatch(p1, p2, arrowstyle='-|>', color=color, lw=lw,
                        linestyle=ls, shrinkA=2, shrinkB=2, zorder=z)
    ax.add_patch(a)


# 结点坐标
CHAMP = (5.0, 8.35)   # 冠军位
FINAL = (5.0, 6.55)   # 决赛结点（根）
SEMI_L = (2.6, 4.75)  # 左半决赛结点
SEMI_R = (7.4, 4.75)  # 右半决赛结点
LEAF = {0: (1.3, 2.85), 1: (3.7, 2.85), 2: (6.1, 2.85), 3: (8.5, 2.85)}
RUN_Y = 0.95

C_GREEN = ('#dcfce7', '#15803d')
C_BLUE = ('#e8f1fb', '#2c5f8a')
C_YELLOW = ('#fef9c3', '#ca8a04')
C_GRAY = ('#f3f4f6', '#6b7280')

# 胜者上送的实线箭头
arrow((SEMI_L[0], SEMI_L[1] + 0.46), (4.32, FINAL[1] - 0.52))
ax.text(2.9, 5.55, '胜者 9 上送', fontsize=10, color='#3a6ea5', ha='center')
arrow((SEMI_R[0], SEMI_R[1] + 0.46), (5.68, FINAL[1] - 0.52))
ax.text(7.15, 5.55, '胜者 5 上送', fontsize=10, color='#3a6ea5', ha='center')
arrow((FINAL[0], FINAL[1] + 0.5), (CHAMP[0], CHAMP[1] - 0.5))
ax.text(5.95, 7.45, '胜者上送', fontsize=10, color='#3a6ea5', ha='left')

# 叶结点 → 半决赛结点
arrow((LEAF[0][0], LEAF[0][1] + 0.5), (2.16, SEMI_L[1] - 0.5))
arrow((LEAF[1][0], LEAF[1][1] + 0.5), (3.04, SEMI_L[1] - 0.5))
arrow((LEAF[2][0], LEAF[2][1] + 0.5), (6.96, SEMI_R[1] - 0.5))
arrow((LEAF[3][0], LEAF[3][1] + 0.5), (7.84, SEMI_R[1] - 0.5))
ax.text(1.9, 4.15, '比较', fontsize=10, color='#6b7280', ha='center')

# 调整路径（虚线，橙色）：叶 F3 → 右半决赛 → 决赛 → 冠军位
arrow((LEAF[3][0] + 0.35, LEAF[3][1] + 0.5), (7.95, SEMI_R[1] - 0.5),
      color='#ea580c', lw=1.8, ls=(0, (5, 3)), z=1)
arrow((7.75, SEMI_R[1] + 0.48), (5.78, FINAL[1] - 0.5),
      color='#ea580c', lw=1.8, ls=(0, (5, 3)), z=1)
arrow((5.42, FINAL[1] + 0.5), (5.42, CHAMP[1] - 0.5),
      color='#ea580c', lw=1.8, ls=(0, (5, 3)), z=1)
ax.text(9.35, 4.75, '调\n整\n路\n径', fontsize=10.5, color='#ea580c',
        ha='center', va='center', fontweight='bold')

# 归并段 → 叶结点（取当前记录）
for k in range(4):
    arrow((LEAF[k][0], RUN_Y + 0.44), (LEAF[k][0], LEAF[k][1] - 0.5),
          color='#9ca3af', lw=1.5)
ax.text(0.3, 2.0, '取当前记录', fontsize=10, color='#6b7280', ha='left')

# 结点绘制
box(CHAMP[0], CHAMP[1], 3.0, 0.95, '冠军位 ls[0]\n胜者：F3 (5)', *C_GREEN, fs=11)
box(FINAL[0], FINAL[1], 3.0, 0.95, '决赛结点（根）\n败者：F1 (9)', *C_BLUE, fs=11)
box(SEMI_L[0], SEMI_L[1], 2.4, 0.9, '半决赛结点\n败者：F0 (10)', *C_BLUE)
box(SEMI_R[0], SEMI_R[1], 2.4, 0.9, '半决赛结点\n败者：F2 (12)', *C_BLUE)

box(LEAF[0][0], LEAF[0][1], 1.2, 0.95, 'F0\n10', *C_GRAY)
box(LEAF[1][0], LEAF[1][1], 1.2, 0.95, 'F1\n9', *C_GRAY)
box(LEAF[2][0], LEAF[2][1], 1.2, 0.95, 'F2\n12', *C_GRAY)
box(LEAF[3][0], LEAF[3][1], 1.2, 0.95, 'F3\n5', *C_YELLOW)

RUNS = ['F0：10, 15, 30', 'F1：9, 20, 25', 'F2：12, 22, 40', 'F3：5, 18, 35']
for k in range(4):
    box(LEAF[k][0], RUN_Y, 2.25, 0.8, RUNS[k], '#ffffff', '#374151', fs=10)
ax.text(LEAF[3][0], 0.22, '下一记录：18', fontsize=10, color='#ea580c',
        ha='center', fontweight='bold')

ax.text(5.0, -0.35,
        '叶结点存放各段当前记录；内部结点存放对应比较的败者（较小者为胜、胜者上送）。\n'
        '虚线为输出 5 之后，新记录 18 进入叶结点后自叶到冠军位的调整路径。',
        fontsize=10.5, color='#4b5563', ha='center', va='center')

ax.set_title('4-路归并的败者树（初始建树结果）', fontsize=13, color='#111827', pad=10)
ax.set_xlim(-0.3, 10.0)
ax.set_ylim(-0.8, 9.1)
ax.axis('off')

os.makedirs('/home/z/my-project/public/mocks/m05', exist_ok=True)
fig.savefig('/home/z/my-project/public/mocks/m05/q05.png')
print('saved: /home/z/my-project/public/mocks/m05/q05.png')
