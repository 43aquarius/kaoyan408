# 模拟卷六 第43题配图：线速收包数据通路（以太网链路 → 网卡 → PCIe 2.0 x1 → 主存 → 接收中断 → CPU）
# 参数与题干严格一致：
#   每帧线路 500 B（前导8 + 帧首14 + IP首部20 + UDP首部8 + 应用数据434 + FCS4 + IFG12）
#   1000 Mb/s 线速 → 250,000 帧/s（每帧 4 μs）；DMA 每帧 480 B → 120 MB/s
#   PCIe 2.0 x1：5 GT/s、8b/10b → 单向有效 500 MB/s（利用率 24%）
#   中断合并：每满 25 帧一次 → 10,000 次/s；ISR 40 μs/次 → CPU 占用率 40%
import os

import matplotlib.font_manager as fm

_font = '/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf'
if not os.path.exists(_font):
    _font = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(_font)

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

BLUE, GREEN, ORANGE, DARK, GRAY, RED = '#1d4ed8', '#15803d', '#c2410c', '#1f2937', '#6b7280', '#dc2626'

fig, ax = plt.subplots(figsize=(11, 7.4), dpi=150, constrained_layout=True)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10.6)
ax.axis('off')


def box(x, y, w, h, fc, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.10',
                                linewidth=2.0, edgecolor=ec, facecolor=fc))


def arr(p1, p2, color, lw=2.4, head=True, ls='-'):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>' if head else '-',
                                 mutation_scale=18, linewidth=lw, color=color,
                                 linestyle=ls, zorder=3))


# ================= 标题 =================
ax.text(8.0, 10.25, '线速收包数据通路：以太网帧 → 网卡 → PCIe → 主存 → 接收中断 → CPU',
        ha='center', va='center', fontsize=13, fontweight='bold', color=DARK)

# ================= 顶部：以太网帧线路构成条 =================
segs = [
    ('前导\n8 B', 1.30, '#e5e7eb', '#6b7280', 10),
    ('帧首部\n14 B', 1.30, '#dbeafe', '#2563eb', 10),
    ('IP 首部\n20 B', 1.30, '#bfdbfe', '#2563eb', 10),
    ('UDP 首部\n8 B', 1.25, '#93c5fd', '#2563eb', 10),
    ('应用数据\n434 B', 6.55, '#bbf7d0', '#15803d', 11),
    ('FCS\n4 B', 1.10, '#fed7aa', '#ea580c', 10),
    ('IFG\n12 B', 1.30, '#e5e7eb', '#6b7280', 10),
]
bx = 1.0
for label, w, fc, ec, fs in segs:
    ax.add_patch(Rectangle((bx, 9.05), w, 0.85, linewidth=1.5, edgecolor=ec, facecolor=fc))
    ax.text(bx + w / 2, 9.475, label, ha='center', va='center', fontsize=fs, color=DARK)
    bx += w
# MAC 帧范围括线（帧首部 ~ FCS，即 2.30 ~ 13.80）
ax.plot([2.30, 2.30], [8.92, 9.05], color=BLUE, lw=1.6)
ax.plot([13.80, 13.80], [8.92, 9.05], color=BLUE, lw=1.6)
ax.plot([2.30, 13.80], [8.92, 8.92], color=BLUE, lw=1.6)
ax.text(8.05, 8.56, 'MAC 帧 480 B：CRC 校验后由 DMA 写入主存（前导与 IFG 不写入）',
        ha='center', va='center', fontsize=10.5, color=BLUE)
ax.text(1.65, 8.56, '链路开销', ha='center', va='center', fontsize=10, color=GRAY)
ax.text(14.45, 8.56, '链路开销', ha='center', va='center', fontsize=10, color=GRAY)
ax.text(8.0, 8.12, '每帧占线路 500 B（含前导码与帧间间隙）；线速收包：10^9 bit/s ÷ (500 × 8) bit = 250,000 帧/s（每帧 4 μs）',
        ha='center', va='center', fontsize=10.5, color=DARK)

# ================= 中部主链 =================
# 千兆链路
box(0.5, 5.6, 2.2, 1.7, '#f5f3ff', '#7c3aed')
ax.text(1.6, 7.02, '千兆以太网链路', ha='center', va='center', fontsize=11.5, color=DARK, fontweight='bold')
ax.text(1.6, 6.58, '1000 Mb/s（10^9 b/s）', ha='center', va='center', fontsize=10, color='#374151')
ax.text(1.6, 6.18, '仅收包方向线速', ha='center', va='center', fontsize=10, color='#374151')

arr((2.7, 6.45), (4.1, 6.45), BLUE)
ax.text(3.4, 6.66, '250,000 帧/s', ha='center', va='center', fontsize=10, color=BLUE)
ax.text(3.4, 6.22, '①', ha='center', va='center', fontsize=11, color=BLUE)

# 网卡 NIC（外框 + 标题 + 三个内部模块）
box(4.1, 5.15, 4.4, 2.65, '#eff6ff', '#1d4ed8')
ax.text(6.3, 7.50, '网卡（NIC）', ha='center', va='center', fontsize=12, color=DARK, fontweight='bold')
for my, mt, fc, ec in [
    (6.72, '接收 MAC · CRC 校验，剥去前导/IFG', '#dbeafe', '#3b82f6'),
    (6.02, 'DMA 引擎（成组突发传送）', '#dbeafe', '#3b82f6'),
    (5.32, '中断合并计数器：每满 25 帧触发', '#fee2e2', '#dc2626'),
]:
    ax.add_patch(FancyBboxPatch((4.35, my), 3.9, 0.56, boxstyle='round,pad=0.06',
                                linewidth=1.5, edgecolor=ec, facecolor=fc))
    ax.text(6.30, my + 0.28, mt, ha='center', va='center', fontsize=10, color='#374151')

# PCIe 2.0 x1
box(9.0, 5.6, 2.6, 1.7, '#fef9c3', '#a16207')
ax.text(10.3, 7.02, 'PCIe 2.0 x1', ha='center', va='center', fontsize=11.5, color=DARK, fontweight='bold')
ax.text(10.3, 6.58, '5 GT/s · 8b/10b 编码', ha='center', va='center', fontsize=10, color='#374151')
ax.text(10.3, 6.18, '单向有效 500 MB/s', ha='center', va='center', fontsize=10, color='#374151')

arr((8.5, 6.45), (9.0, 6.45), BLUE)
ax.text(8.75, 6.22, '②', ha='center', va='center', fontsize=11, color=BLUE)
arr((11.6, 6.45), (12.2, 6.45), BLUE)
ax.text(11.9, 6.22, '③', ha='center', va='center', fontsize=11, color=BLUE)
ax.text(10.0, 5.00, 'DMA 流量：480 B/帧 × 250,000 帧/s = 120 MB/s',
        ha='center', va='center', fontsize=10, color=BLUE)

# 主存
box(12.2, 5.15, 3.4, 2.65, '#ffedd5', '#ea580c')
ax.text(13.9, 7.50, '主存', ha='center', va='center', fontsize=12, color=DARK, fontweight='bold')
ax.text(13.9, 6.95, '接收环形缓冲区', ha='center', va='center', fontsize=10.5, color='#374151')
ax.text(13.9, 6.50, '总线利用率 120/500 = 24%', ha='center', va='center', fontsize=10.5, color='#374151')

# ================= 下部：中断与 CPU =================
arr((5.5, 5.15), (5.5, 3.25), RED, lw=2.6)
ax.text(5.75, 4.62, '④', ha='center', va='center', fontsize=11, color=RED)
ax.text(5.95, 4.30, '接收中断（每满 25 帧一次）\n10,000 次/s',
        ha='left', va='center', fontsize=10, color=RED, linespacing=1.5)

box(3.7, 1.75, 3.4, 1.5, '#dcfce7', '#15803d')
ax.text(5.4, 2.88, 'CPU', ha='center', va='center', fontsize=12, color=DARK, fontweight='bold')
ax.text(5.4, 2.45, '中断服务程序 40 μs/次', ha='center', va='center', fontsize=10, color='#374151')
ax.text(5.4, 2.06, 'CPU 占用率 40%', ha='center', va='center', fontsize=10, color='#374151')

# 主存 → CPU：协议栈读取（灰色返回线）
arr((13.9, 5.15), (13.9, 2.50), GRAY, lw=1.8, head=False)
arr((13.9, 2.50), (7.1, 2.50), GRAY, lw=1.8)
ax.text(10.5, 2.74, '协议栈与应用进程随后读取接收缓冲区（本题不计 CPU 开销）',
        ha='center', va='center', fontsize=10, color=GRAY)
ax.text(10.5, 2.26, '⑤', ha='center', va='center', fontsize=11, color=GRAY)

# ================= 底部说明 =================
ax.text(0.5, 1.15, '通路：① 帧到达网卡 → ② CRC 校验、剥去前导/IFG，DMA 经 PCIe 写入 → ③ 进入主存接收缓冲 → ④ 每满 25 帧向 CPU 发一次中断 → ⑤ 协议栈读取',
        ha='left', va='center', fontsize=10, color=GRAY)
ax.text(0.5, 0.65, '中断开销：10,000 次/s × 40 μs = 0.4 s → CPU 占用率 40%；若不合并（每帧一次）：250,000 × 40 μs = 10 s，CPU 将被中断淹没',
        ha='left', va='center', fontsize=10, color=GRAY)

fig.savefig('/home/z/my-project/public/mocks/m06/q43.png')
print('saved: /home/z/my-project/public/mocks/m06/q43.png')
