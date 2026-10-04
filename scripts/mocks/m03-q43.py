# -*- coding: utf-8 -*-
# 全真模拟卷（三）· E 段 第 43 题配图：计算机存储系统的层次结构
# 内容：寄存器 - Cache - 主存 - 辅存 四级金字塔（自上而下：容量增大、速度下降、每位价格下降）
#   左侧箭头：越往上速度越快、每位价格越高；右侧箭头：越往下容量越大、每位价格越低
#   两个存储层次标注：Cache-主存层次（纯硬件，对所有程序员透明，解决速度与成本矛盾）
#                     主存-辅存层次（硬件+操作系统实现虚拟存储器，仅对应用程序员透明，解决容量矛盾）
#   底部说明：程序局部性原理（时间局部性 + 空间局部性）是层次结构有效的工作基础
# 颜色语义：CPU 蓝色；四层存储自暖（快/贵）到冷（慢/廉）渐变；层次说明框为虚线边框灰底
# 输出: /home/z/my-project/public/mocks/m03/q43.png
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Bold.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8.8, 5.5), dpi=150, constrained_layout=True)
ax.set_xlim(0, 13)
ax.set_ylim(0, 8.2)
ax.axis('off')

# ---------------- 颜色 ----------------
C_CPU_F, C_CPU_E = '#dbeafe', '#1d4ed8'      # CPU：蓝
C_L1_F, C_L1_E = '#fee2e2', '#b91c1c'        # 寄存器：暖红（最快、最贵）
C_L2_F, C_L2_E = '#ffedd5', '#c2410c'        # Cache：橙
C_L3_F, C_L3_E = '#fef9c3', '#a16207'        # 主存：黄
C_L4_F, C_L4_E = '#dcfce7', '#15803d'        # 辅存：绿（最慢、最廉）
C_ARR_UP, C_ARR_DOWN = '#b91c1c', '#15803d'  # 左右梯度箭头


def level_box(x, y, w, h, fc, ec, title, lines):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle='round,pad=0.04',
        facecolor=fc, edgecolor=ec, linewidth=2.0, zorder=3))
    ax.text(x + w / 2, y + h - 0.20, title, ha='center', va='center',
            fontsize=12, fontweight='bold', color=ec, zorder=4)
    ax.text(x + w / 2, y + (h - 0.26) / 2 + 0.03, '\n'.join(lines), ha='center',
            va='center', fontsize=10, color='#374151', zorder=4, linespacing=1.4)


# ---------------- 标题 ----------------
ax.text(6.5, 7.92, '题 43 图：计算机存储系统的层次结构（容量 / 速度 / 价格梯度）',
        ha='center', va='bottom', fontsize=13, fontweight='bold', color='#111827')

# ---------------- CPU 与四级存储（金字塔，越往下越宽） ----------------
CX = 6.5
level_box(CX - 1.00, 6.66, 2.00, 0.50, C_CPU_F, C_CPU_E, 'CPU', [])
level_box(CX - 1.85, 5.48, 3.70, 0.86, C_L1_F, C_L1_E,
          '寄存器（触发器实现）', ['容量 < 1 KB · 与 CPU 同节拍', '每位价格最高'])
level_box(CX - 2.45, 4.28, 4.90, 0.86, C_L2_F, C_L2_E,
          'Cache（SRAM）', ['容量 KB ~ MB 级 · 约 1 ~ 20 ns', '每位价格高'])
level_box(CX - 3.05, 3.08, 6.10, 0.86, C_L3_F, C_L3_E,
          '主存（DRAM）', ['容量 GB 级 · 约 50 ~ 100 ns', '每位价格较低'])
level_box(CX - 3.65, 1.88, 7.30, 0.86, C_L4_F, C_L4_E,
          '辅存（磁盘 / 固态盘）', ['容量 TB 级 · μs ~ ms 级（CPU 不能直接访问）', '每位价格最低'])

# CPU 与寄存器之间的短箭头
ax.add_patch(mpatches.FancyArrowPatch(
    (CX, 6.64), (CX, 6.36), arrowstyle='-|>', mutation_scale=16,
    lw=2.0, color=C_CPU_E, zorder=2))

# ---------------- 两个存储层次（虚线说明框，位于层间空档） ----------------
def hier_box(x, y, w, h, text):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle='round,pad=0.03',
        facecolor='#f3f4f6', edgecolor='#9ca3af', linewidth=1.6,
        linestyle=(0, (5, 3)), zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
            fontsize=10.5, color='#1f2937', zorder=4)

hier_box(1.60, 5.17, 9.90, 0.28,
         'Cache—主存层次：全部由硬件实现，对所有程序员透明（解决速度与成本的矛盾）')
hier_box(1.60, 2.77, 9.90, 0.28,
         '主存—辅存层次：硬件 + 操作系统实现虚拟存储器，仅对应用程序员透明（解决容量矛盾）')

# ---------------- 左右梯度箭头 ----------------
ax.add_patch(mpatches.FancyArrowPatch(
    (1.05, 2.05), (1.05, 6.30), arrowstyle='-|>', mutation_scale=20,
    lw=2.2, color=C_ARR_UP, zorder=2))
ax.text(0.70, 4.18, '越往上：速度越快\n每位价格越高', ha='center', va='center',
        rotation=90, fontsize=10.5, fontweight='bold', color=C_ARR_UP, zorder=5)

ax.add_patch(mpatches.FancyArrowPatch(
    (11.95, 6.30), (11.95, 2.05), arrowstyle='-|>', mutation_scale=20,
    lw=2.2, color=C_ARR_DOWN, zorder=2))
ax.text(12.30, 4.18, '越往下：容量越大\n每位价格越低', ha='center', va='center',
        rotation=90, fontsize=10.5, fontweight='bold', color=C_ARR_DOWN, zorder=5)

# ---------------- 底部：程序局部性原理说明 ----------------
ax.add_patch(mpatches.FancyBboxPatch(
    (1.10, 0.30), 10.80, 1.35, boxstyle='round,pad=0.05',
    facecolor='#eff6ff', edgecolor=C_CPU_E, linewidth=1.8, zorder=3))
ax.text(6.50, 1.42, '共同的工作基础：程序局部性原理', ha='center', va='center',
        fontsize=11.5, fontweight='bold', color=C_CPU_E, zorder=4)
ax.text(6.50, 0.80,
        '时间局部性：刚被访问的单元，不久后很可能再次被访问（循环、热点数据）\n'
        '空间局部性：刚被访问的单元，其邻近单元很可能被访问（顺序执行、数组遍历）\n'
        '层间命中率足够高 → 整体平均速度接近最上层，平均每位价格与总容量接近最下层',
        ha='center', va='center', fontsize=10, color='#374151', zorder=4, linespacing=1.55)

# ---------------- 图例（横排，置于标题下方、CPU 上方的空档） ----------------
handles = [
    Line2D([0], [0], marker='s', color='none', markerfacecolor='#f3f4f6',
           markeredgecolor='#9ca3af', markersize=10, linestyle='--',
           markeredgewidth=1.5, label='存储层次（层间调度方式）'),
    Line2D([0], [0], color=C_ARR_UP, lw=2.2, label='速度 / 价格梯度'),
    Line2D([0], [0], color=C_ARR_DOWN, lw=2.2, label='容量梯度'),
]
legend = ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 0.965),
                   ncol=3, fontsize=9.5, framealpha=0.95, edgecolor='#cbd5e1',
                   borderpad=0.55, handlelength=1.7, columnspacing=1.2)
legend.set_zorder(6)

fig.savefig('/home/z/my-project/public/mocks/m03/q43.png')
print('saved: /home/z/my-project/public/mocks/m03/q43.png')
