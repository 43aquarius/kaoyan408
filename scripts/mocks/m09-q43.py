# -*- coding: utf-8 -*-
"""全真模拟卷（九）第 43 题配图：智能家居网关存储系统框图（与题干参数一致）"""
import os
import matplotlib
matplotlib.use('Agg')
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

from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(10.5, 6.4), dpi=150, constrained_layout=True)
ax.set_xlim(0.1, 15.9)
ax.set_ylim(0.0, 9.5)
ax.axis('off')


def box(x, y, w, h, fc, ec, lw=1.8):
    r = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    ax.add_patch(r)
    return r


# ---- SoC 外框 ----
soc = Rectangle((0.4, 1.55), 9.9, 7.5, facecolor='#F8FAFC', edgecolor='#64748B',
                linewidth=1.6, linestyle=(0, (6, 4)), zorder=1)
ax.add_patch(soc)
ax.text(0.68, 8.6, '智能家居网关 SoC', fontsize=11, fontweight='bold',
        color='#334155', zorder=5)

# ---- 片内总线 ----
ax.plot([0.9, 9.9], [5.15, 5.15], color='#475569', linewidth=4.5,
        solid_capstyle='butt', zorder=2)
ax.text(1.0, 4.82, '片内总线（32 位）', fontsize=10, color='#475569',
        ha='left', zorder=5)

# ---- 上排：CPU / DMA / ROM ----
box(1.0, 6.35, 3.0, 1.85, '#DBEAFE', '#1D4ED8')
ax.text(2.5, 7.75, 'CPU 内核', fontsize=11.5, fontweight='bold', ha='center', color='#1E3A8A', zorder=5)
ax.text(2.5, 7.32, '32 位 RISC 处理器', fontsize=10, ha='center', color='#1E3A8A', zorder=5)
ax.text(2.5, 6.96, '主频 100 MHz', fontsize=10, ha='center', color='#1E3A8A', zorder=5)
ax.text(2.5, 6.62, '时钟周期 10 ns', fontsize=10, ha='center', color='#1E3A8A', zorder=5)

box(4.55, 6.6, 2.35, 1.35, '#DCFCE7', '#15803D')
ax.text(5.72, 7.45, 'DMA 控制器', fontsize=11, fontweight='bold', ha='center', color='#14532D', zorder=5)
ax.text(5.72, 7.02, '启动搬运 / 模块换入', fontsize=10, ha='center', color='#14532D', zorder=5)

box(7.35, 6.6, 2.4, 1.35, '#F1F5F9', '#475569')
ax.text(8.55, 7.45, '片上 ROM', fontsize=11, fontweight='bold', ha='center', color='#334155', zorder=5)
ax.text(8.55, 7.06, '32 KB', fontsize=10, ha='center', color='#334155', zorder=5)
ax.text(8.55, 6.76, 'BootLoader', fontsize=10, ha='center', color='#334155', zorder=5)

for x0, y0 in [(2.5, 6.35), (5.72, 6.6), (8.55, 6.6)]:
    ax.plot([x0, x0], [y0, 5.15], color='#64748B', linewidth=1.6, zorder=2)

# ---- 下排：SRAM（含分区）/ 外设接口 / QSPI 控制器 ----
box(1.0, 2.35, 4.75, 2.05, '#E0F2FE', '#0369A1')
ax.text(3.375, 4.02, '片上 SRAM 512 KB', fontsize=11.5, fontweight='bold',
        ha='center', color='#0C4A6E', zorder=5)
ax.text(3.375, 3.62, '零等待：1 时钟周期 / 32 位访问', fontsize=10,
        ha='center', color='#0C4A6E', zorder=5)

# SRAM 分区条（常驻区 375 / 覆盖区 125 / 剩余 12，宽度按 512 等比）
bar_x, bar_y, bar_w, bar_h = 1.15, 2.5, 4.45, 0.72
w1 = bar_w * 375 / 512.0
w2 = bar_w * 125 / 512.0
w3 = bar_w - w1 - w2
box(bar_x, bar_y, w1, bar_h, '#0284C7', '#075985', 1.5)
box(bar_x + w1, bar_y, w2, bar_h, '#F59E0B', '#B45309', 1.5)
box(bar_x + w1 + w2, bar_y, w3, bar_h, '#94A3B8', '#64748B', 1.5)
ax.text(bar_x + w1 / 2, bar_y + bar_h / 2, '常驻区 375 KB', fontsize=10,
        fontweight='bold', ha='center', va='center', color='white', zorder=6)
ax.text(bar_x + w1 + w2 / 2, bar_y + bar_h / 2, '覆盖区\n125 KB', fontsize=10,
        fontweight='bold', ha='center', va='center', color='white', zorder=6)
ax.annotate('剩余 12 KB（堆栈等）', xy=(bar_x + w1 + w2 + w3 / 2, bar_y),
            xytext=(5.75, 1.72), fontsize=10, color='#475569',
            arrowprops=dict(arrowstyle='->', linewidth=1.5, color='#475569'), zorder=6)

box(6.0, 2.7, 1.7, 1.55, '#F1F5F9', '#475569')
ax.text(6.85, 3.62, '外设接口', fontsize=11, fontweight='bold', ha='center', color='#334155', zorder=5)
ax.text(6.85, 3.14, 'UART / I2C\nI2S / GPIO', fontsize=10, ha='center', va='center', color='#334155', zorder=5)

box(8.0, 2.7, 2.05, 1.55, '#FEF9C3', '#CA8A04')
ax.text(9.02, 3.62, 'QSPI 控制器', fontsize=11, fontweight='bold', ha='center', color='#713F12', zorder=5)
ax.text(9.02, 3.12, '接口时钟 32 MHz\n4 条数据线', fontsize=10, ha='center', va='center', color='#713F12', zorder=5)

for x0, y0 in [(3.375, 4.4), (6.85, 4.25), (9.02, 4.25)]:
    ax.plot([x0, x0], [y0, 5.15], color='#64748B', linewidth=1.6, zorder=2)

# ---- 外挂 NOR Flash ----
box(11.3, 5.5, 4.3, 2.6, '#FFEDD5', '#C2410C', lw=2.0)
ax.text(13.45, 7.6, '外挂 NOR Flash', fontsize=12, fontweight='bold', ha='center', color='#7C2D12', zorder=5)
ax.text(13.45, 7.14, '容量 4 MB', fontsize=10.5, ha='center', color='#7C2D12', zorder=5)
ax.text(13.45, 6.72, '顺序读带宽 16×10^6 B/s', fontsize=10.5, ha='center', color='#7C2D12', zorder=5)
ax.text(13.45, 6.32, '支持就地执行 XIP', fontsize=10.5, ha='center', color='#7C2D12', zorder=5)
ax.text(13.45, 5.92, '（取 32 位指令约 25 周期）', fontsize=10, ha='center', color='#7C2D12', zorder=5)

# QSPI <-> Flash 双向箭头（数据通路，蓝色）
arr = FancyArrowPatch((10.05, 3.48), (11.3, 6.1), arrowstyle='<|-|>',
                      mutation_scale=16, linewidth=2.0, color='#2563EB', zorder=4)
ax.add_patch(arr)
ax.text(10.82, 4.72, '四线 SPI', fontsize=10, color='#1D4ED8', rotation=64,
        ha='center', va='center', zorder=6)

# ---- 网关外设 ----
grp = FancyBboxPatch((11.3, 0.55), 4.3, 4.35,
                     boxstyle='round,pad=0.02,rounding_size=0.08',
                     facecolor='#FAFAF9', edgecolor='#A8A29E', linewidth=1.6,
                     linestyle=(0, (5, 3)), zorder=2)
ax.add_patch(grp)
ax.text(13.45, 4.52, '网关外设', fontsize=11, fontweight='bold', ha='center', color='#57534E', zorder=5)
peripherals = [
    'Wi-Fi / 蓝牙通信模块',
    '传感器接口（温湿度 / 门磁）',
    '音频编解码器（麦克风 / 扬声器）',
    '继电器与状态指示灯',
]
py = 3.62
for name in peripherals:
    box(11.55, py, 3.8, 0.72, '#FAFAF9', '#78716C', lw=1.5)
    ax.text(13.45, py + 0.36, name, fontsize=10, ha='center', va='center',
            color='#44403C', zorder=5)
    py -= 0.8

# 外设接口 -> 外设组 箭头
arr2 = FancyArrowPatch((6.85, 2.7), (11.3, 2.05), arrowstyle='-|>',
                       mutation_scale=16, linewidth=1.8, color='#7C3AED', zorder=4)
ax.add_patch(arr2)

# ---- 底部说明框 ----
cap = FancyBboxPatch((0.4, 0.15), 9.9, 1.05,
                     boxstyle='round,pad=0.02,rounding_size=0.1',
                     facecolor='#FEFCE8', edgecolor='#CA8A04', linewidth=1.5, zorder=2)
ax.add_patch(cap)
ax.text(5.35, 0.82, '启动：BootLoader 经 DMA 把 A/B/E（375 KB）从 Flash 搬入 SRAM，约 24 ms；',
        fontsize=10, ha='center', color='#713F12', zorder=5)
ax.text(5.35, 0.42, '运行中按需换入 C / D（各 125 KB，约 8 ms；纯代码无须写回 Flash）。',
        fontsize=10, ha='center', color='#713F12', zorder=5)

ax.set_title('题 43 图：智能家居网关存储系统框图', fontsize=13, fontweight='bold',
             pad=10, color='#1E293B')

fig.savefig('/home/z/my-project/public/mocks/m09/q43.png')  # 禁止 bbox_inches='tight'
print('saved: /home/z/my-project/public/mocks/m09/q43.png')
