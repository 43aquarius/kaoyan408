# -*- coding: utf-8 -*-
# 全真模拟卷六 · 第15题配图：网卡 — 系统总线 — 主存 数据通路（带宽参数与题干一致）
import os
import matplotlib.font_manager as fm

font_path = '/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf'
if not os.path.exists(font_path):
    font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(font_path)

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150, constrained_layout=True)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.4)
ax.axis('off')

C_NIC, C_BUS, C_MEM = '#dbeafe', '#fde68a', '#dcfce7'
EDGE, C_RX, C_TX = '#334155', '#2563eb', '#16a34a'


def box(x, y, w, h, text, fc, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.06',
                                fc=fc, ec=EDGE, lw=1.8))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=fs, linespacing=1.6)


def arrow(x1, y1, x2, y2, color):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>',
                                 mutation_scale=16, lw=2.0, color=color))


# 标题
ax.text(5, 6.12, '网卡 — 系统总线 — 主存 数据通路与带宽参数',
        ha='center', va='center', fontsize=13, fontweight='bold')

# 设备框
box(0.35, 4.25, 2.70, 1.30, '千兆网卡 1（全双工）\n收 125 MB/s\n发 125 MB/s', C_NIC)
box(0.35, 0.95, 2.70, 1.30, '千兆网卡 2（全双工）\n收 125 MB/s\n发 125 MB/s', C_NIC)
box(3.90, 0.95, 2.20, 4.60, '系统总线\n\n宽度 W 位\n时钟 100 MHz\n每周期\n传送 1 次', C_BUS, fs=10.5)
box(7.35, 2.10, 2.30, 2.30, '主存\n\n接收环形缓冲\n发送缓冲', C_MEM, fs=10.5)

# 网卡1 与总线之间（收：网卡→总线；发：总线→网卡）
arrow(3.05, 4.95, 3.90, 4.95, C_RX)
ax.text(3.475, 5.10, '收', ha='center', va='bottom', fontsize=10, color=C_RX)
arrow(3.90, 4.50, 3.05, 4.50, C_TX)
ax.text(3.475, 4.35, '发', ha='center', va='top', fontsize=10, color=C_TX)

# 网卡2 与总线之间
arrow(3.05, 1.75, 3.90, 1.75, C_RX)
ax.text(3.475, 1.90, '收', ha='center', va='bottom', fontsize=10, color=C_RX)
arrow(3.90, 1.30, 3.05, 1.30, C_TX)
ax.text(3.475, 1.15, '发', ha='center', va='top', fontsize=10, color=C_TX)

# 总线与主存之间
arrow(6.10, 3.55, 7.35, 3.55, C_RX)
ax.text(6.72, 3.70, '写帧', ha='center', va='bottom', fontsize=10, color=C_RX)
arrow(7.35, 2.95, 6.10, 2.95, C_TX)
ax.text(6.72, 2.80, '读帧', ha='center', va='top', fontsize=10, color=C_TX)

# 底部带宽参数说明（与题干一致）
ax.text(5, 0.72, '蓝色：接收方向（DMA 写主存）　绿色：发送方向（DMA 读主存）',
        ha='center', va='center', fontsize=10, color=EDGE)
ax.text(5, 0.44, '两网卡全双工聚合流量 = 2 × (125 + 125) = 500 MB/s',
        ha='center', va='center', fontsize=10.5, color='#b91c1c', fontweight='bold')
ax.text(5, 0.16, '总线带宽 = (W/8) B × 100 MHz，利用率约束：500 MB/s ÷ 总线带宽 ≤ 80%',
        ha='center', va='center', fontsize=10, color=EDGE)

fig.savefig('/home/z/my-project/public/mocks/m06/q15.png')
print('saved q15.png')
