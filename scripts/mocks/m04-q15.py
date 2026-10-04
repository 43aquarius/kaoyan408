# -*- coding: utf-8 -*-
"""全真模拟卷（四）第 15 题：TLB-页表-Cache 访问流程判定图"""
import os
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

GREEN = '#16a34a'   # 命中路径
ORANGE = '#ea580c'  # 未命中路径
RED = '#dc2626'     # 缺页 / 异常
BLUE = '#2563eb'    # 地址 / 数据流

fig, ax = plt.subplots(figsize=(7.6, 4.4), dpi=150, constrained_layout=True)
ax.set_xlim(0, 10.6)
ax.set_ylim(0, 6.4)
ax.axis('off')


def box(x, y, w, h, text, edge, face, fs=10.5, lw=2.0):
    p = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.04',
                       linewidth=lw, edgecolor=edge, facecolor=face)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fs, color='#111827', linespacing=1.35)


def arrow(p1, p2, color, label='', lw=2.0, ls='-', rad=0.0, fs=9.5,
          lpos=0.5, dx=0.0, dy=0.12, ha='center'):
    a = FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=16,
                        linewidth=lw, color=color, linestyle=ls,
                        connectionstyle=f'arc3,rad={rad}')
    ax.add_patch(a)
    if label:
        mx = p1[0] + (p2[0] - p1[0]) * lpos + dx
        my = p1[1] + (p2[1] - p1[1]) * lpos + dy
        ax.text(mx, my, label, ha=ha, va='center', fontsize=fs,
                color=color, linespacing=1.25)


# ── 顶部：CPU 发出虚地址 ─────────────────────────────────────────
box(3.3, 5.35, 4.0, 0.85,
    'CPU 发出虚地址（20 位）\n① 0x2A4F   ② 0x5C21   ③ 0x03D8   ④ 0x1E09',
    '#1e293b', '#f8fafc', fs=10.5)

box(3.3, 4.35, 4.0, 0.62, '地址划分：虚页号 8 位 ＋ 页内偏移 12 位',
    '#1e293b', '#eef2ff', fs=10.5)

# ── 左列：TLB → 页表 → 缺页中断 ─────────────────────────────────
box(1.05, 2.95, 2.75, 0.9, '查 TLB\n（全相联 · 5 项）', '#1e293b', '#fef9c3', fs=11)
box(1.05, 1.62, 2.75, 0.9, '查主存中的页表\n（多 1 次访存）', '#1e293b', '#fef9c3', fs=11)
box(0.95, 0.18, 2.95, 1.0,
    '缺页中断（第④次 虚页 0001）\nOS 调页入页框 100、改页表\n返回重新执行',
    RED, '#fee2e2', fs=9.8)

# ── 右列：物理地址 → Cache → 主存 / 数据 ────────────────────────
box(5.15, 3.1, 3.1, 0.9,
    '形成物理地址（15 位）\n0x1A4F / 0x6C21 / 0x33D8 / 0x4E09',
    '#1e293b', '#e0f2fe', fs=10)
box(5.15, 1.7, 3.1, 0.9, '查 Cache\n（直接映射 16 行 × 32 B）', '#1e293b', '#f8fafc', fs=10.5)
box(5.15, 0.3, 3.1, 0.8, '访问主存，块调入 Cache', '#1e293b', '#f1f5f9', fs=10)
box(8.85, 1.7, 1.55, 0.9, '数据\n送 CPU', BLUE, '#dbeafe', fs=11)

# ── 箭头：地址流 ─────────────────────────────────────────────────
arrow((5.3, 5.35), (5.3, 4.97), BLUE, lw=2.2)
arrow((5.3, 4.35), (5.3, 3.9), BLUE, lw=2.2)

# TLB 命中 → 物理地址（绿）
arrow((3.8, 3.4), (5.15, 3.42), GREEN,
      '命中：第①②次\n0010→001、0101→110', lpos=0.5, dy=0.42, fs=9.5)

# TLB 未命中 → 页表（橙）
arrow((2.42, 2.95), (2.42, 2.52), ORANGE, '未命中：第③④次', lpos=0.5, dx=0.05, dy=0.16, fs=9.5)

# 页表 → 物理地址（蓝）
arrow((3.8, 2.07), (5.15, 3.05), BLUE,
      '有效位 = 1：第③次 0000→011\n（映射装入 TLB 空闲项）', lpos=0.55, dy=0.4, fs=9.5)

# 页表 → 缺页中断（红）
arrow((2.42, 1.62), (2.42, 1.18), RED, '有效位 = 0：第④次', lpos=0.5, dx=0.05, dy=0.16, fs=9.5)

# 缺页 → 重新执行（红虚线回到地址划分）
arrow((3.9, 0.62), (6.4, 4.35), RED,
      '重新执行（缺页处理不修改 TLB，仍查页表得页框 100）',
      ls='--', rad=-0.32, lpos=0.62, dx=0.35, dy=0.28, fs=9.2)

# 物理地址 → Cache
arrow((6.7, 3.1), (6.7, 2.6), BLUE, lw=2.2)

# Cache 命中 → 数据（绿）
arrow((8.25, 2.15), (8.85, 2.15), GREEN, '命中：第①次\n行 2 标记 001101', lpos=0.5, dy=0.44, fs=9.5)

# Cache 未命中 → 主存（橙）
arrow((6.7, 1.7), (6.7, 1.1), ORANGE, '未命中：第②③④次', lpos=0.5, dx=0.05, dy=0.15, fs=9.5)

# 主存 → 数据（蓝）
arrow((8.25, 0.72), (9.6, 1.7), BLUE, '取块并调入 Cache', lpos=0.5, dx=-0.55, dy=-0.12, fs=9.2)

# 物理地址划分注释
ax.text(6.7, 3.98, 'Cache 地址划分：标记 6 位 ｜ 行号 4 位 ｜ 块内偏移 5 位',
        ha='center', va='center', fontsize=9.2, color='#475569')

# ── 图例 ────────────────────────────────────────────────────────
lx, ly = 8.55, 5.55
ax.text(lx, ly + 0.32, '图例', fontsize=10, color='#111827', ha='left')
for i, (c, t) in enumerate([(GREEN, '命中路径'), (ORANGE, '未命中路径'),
                            (RED, '缺页 / 异常'), (BLUE, '地址 / 数据流')]):
    yy = ly - i * 0.34
    ax.plot([lx, lx + 0.42], [yy, yy], color=c, lw=2.2)
    ax.text(lx + 0.54, yy, t, fontsize=9.5, va='center', color='#111827')

ax.set_title('TLB-页表-Cache 访问流程判定（4 次访问的命中情况）', fontsize=13, color='#111827')

out = '/home/z/my-project/public/mocks/m04/q15.png'
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out)
print('saved:', out)
