# -*- coding: utf-8 -*-
# 全真模拟卷（二）· B 段 第 15 题配图：4 路组相联 Cache 的地址划分与组内映射示意图
# 题干参数：主存地址 28 位，按字节编址；Cache 数据容量 128KB；块大小 32B；4 路组相联
# 划分：标记 13 位 + 组号 10 位 + 块内偏移 5 位；行数 4096，组数 = 4096/4 = 1024
# 访问序列：0x8005548、0x8005558、0xC005540、0x8005548、0x800D55C（命中 2 次）
# 输出: /home/z/my-project/public/mocks/m02/q15.png
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Bold.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(9.6, 6.4), dpi=150, constrained_layout=True)
ax.set_xlim(-0.6, 28.6)
ax.set_ylim(0.0, 10.6)
ax.axis('off')

C_TAG, C_IDX, C_OFF = '#f59e0b', '#3b82f6', '#10b981'
T_TAG, T_IDX, T_OFF = '#92400e', '#1e40af', '#065f46'

# ---- 标题 ----
ax.text(14.0, 10.18, '4 路组相联 Cache：主存地址划分与组内映射（主存地址 28 位，按字节编址）',
        ha='center', va='bottom', fontsize=12.5, fontweight='bold', color='#111827')

# ---- 地址条（宽度按位数比例：13 / 10 / 5）----
ybar, hbar = 8.72, 0.9
segments = [
    (0, 13, C_TAG, '标记 Tag', '13 位'),
    (13, 23, C_IDX, '组号（Cache 组号）', '10 位'),
    (23, 28, C_OFF, '块内偏移', '5 位'),
]
for x0, x1, fc, name, bits in segments:
    ax.add_patch(mpatches.Rectangle((x0, ybar), x1 - x0, hbar, facecolor=fc,
                                    edgecolor='#111827', linewidth=1.8, zorder=2))
    ax.text((x0 + x1) / 2, ybar + hbar / 2, name + '\n' + bits,
            ha='center', va='center', fontsize=11.5, color='white',
            fontweight='bold', linespacing=1.5, zorder=3)

# ---- 位编号标注 ----
for xb, lab in [(0, '位27'), (13, '位15|位14'), (23, '位5|位4'), (28, '位0')]:
    ax.text(xb, ybar + hbar + 0.04, lab, ha='center', va='bottom',
            fontsize=10, color='#4b5563')

# ---- 分隔虚线（向下延伸到示例行）----
for xv in (13, 23):
    ax.plot([xv, xv], [7.28, ybar], ls=(0, (4, 3)), lw=1.5, color='#9ca3af', zorder=1)

# ---- 示例地址分解 ----
ax.text(0.0, 6.55, '示例：第 1 次访问 0x8005548（主存块 0x4002AA）的地址字段分解：',
        ha='left', va='center', fontsize=10.5, color='#111827')
val_boxes = [
    (0.2, 12.6, '#fef3c7', C_TAG, T_TAG, '标记 = 0x1000'),
    (13.2, 9.6, '#dbeafe', C_IDX, T_IDX, '组号 = 0x2AA'),
    (23.2, 4.6, '#d1fae5', C_OFF, T_OFF, '偏移 = 0x08'),
]
for x0, w, fc, ec, tc, txt in val_boxes:
    ax.add_patch(mpatches.Rectangle((x0, 7.28), w, 0.82, facecolor=fc,
                                    edgecolor=ec, linewidth=1.6, zorder=2))
    ax.text(x0 + w / 2, 7.28 + 0.41, txt, ha='center', va='center',
            fontsize=11, color=tc, fontweight='bold', zorder=3)

# ---- 左列：主存块 ----
ax.text(4.6, 6.12, '主存（块号 = 地址 ÷ 32）', ha='center', va='center',
        fontsize=10.5, color='#374151', fontweight='bold')
mem_blocks = [
    (4.72, 5.72, '主存块 0x4002AA', '字节 0x8005540 ～ 0x800555F', '#eef2ff', '#6366f1'),
    (3.37, 4.37, '主存块 0x6002AA', '字节 0xC005540 ～ 0xC00555F', '#fdf2f8', '#db2777'),
    (2.02, 3.02, '主存块 0x4006AA', '字节 0x800D540 ～ 0x800D55F', '#ecfeff', '#0891b2'),
]
for y0, y1, t1, t2, fc, ec in mem_blocks:
    ax.add_patch(mpatches.Rectangle((0.6, y0), 8.0, y1 - y0, facecolor=fc,
                                    edgecolor=ec, linewidth=1.8, zorder=2))
    ax.text(4.6, y0 + (y1 - y0) * 0.62, t1, ha='center', va='center',
            fontsize=11, fontweight='bold', color='#111827', zorder=3)
    ax.text(4.6, y0 + (y1 - y0) * 0.26, t2, ha='center', va='center',
            fontsize=10, color='#4b5563', zorder=3)

# ---- 左下说明 ----
ax.add_patch(mpatches.Rectangle((0.6, 0.78), 8.0, 1.0, facecolor='#f8fafc',
                                edgecolor='#94a3b8', linewidth=1.5, zorder=1))
ax.text(4.6, 1.28, '组号 = 主存块号 mod 1024', ha='center', va='center',
        fontsize=10, color='#334155', zorder=3)
ax.text(4.6, 1.02, '三个块 mod 1024 均为 0x2AA，映射到同一组',
        ha='center', va='center', fontsize=10, color='#334155', zorder=3)

# ---- 右侧：Cache 组面板 ----
ax.text(20.0, 6.12, 'Cache 组 0x2AA（1024 组 × 4 路 = 4096 行，LRU）',
        ha='center', va='center', fontsize=10.5, color='#374151', fontweight='bold')
ax.add_patch(mpatches.Rectangle((12.0, 0.78), 16.0, 5.07, facecolor='#f8fafc',
                                edgecolor='#475569', linewidth=1.8, zorder=1))

rows = [
    (4.88, 5.78, '1', '0x1000', '← 主存块0x4002AA（第2、4次命中）', True),
    (3.78, 4.68, '1', '0x1800', '← 主存块0x6002AA（第3次装入）', True),
    (2.68, 3.58, '1', '0x1001', '← 主存块0x4006AA（第5次装入）', True),
    (1.58, 2.48, '0', '——', '空行（未被占用）', False),
]
for y0, y1, v, tag, note, valid in rows:
    fc = '#ecfdf5' if valid else '#f1f5f9'
    ec = '#10b981' if valid else '#94a3b8'
    ax.add_patch(mpatches.Rectangle((12.3, y0), 15.4, y1 - y0, facecolor=fc,
                                    edgecolor=ec, linewidth=1.6, zorder=2))
    # 有效位
    ax.add_patch(mpatches.Rectangle((12.45, y0 + 0.1), 2.6, y1 - y0 - 0.2,
                                    facecolor='#ffffff', edgecolor=ec, linewidth=1.5, zorder=3))
    ax.text(13.75, (y0 + y1) / 2, '有效 ' + v, ha='center', va='center',
            fontsize=10, color=('#065f46' if valid else '#64748b'), zorder=4)
    # 标记
    ax.add_patch(mpatches.Rectangle((15.25, y0 + 0.1), 4.6, y1 - y0 - 0.2,
                                    facecolor='#ffffff', edgecolor=ec, linewidth=1.5, zorder=3))
    ax.text(17.55, (y0 + y1) / 2, '标记 ' + tag, ha='center', va='center',
            fontsize=10.5, color=('#065f46' if valid else '#64748b'),
            fontweight='bold', zorder=4)
    # 说明
    ax.text(20.3, (y0 + y1) / 2, note, ha='left', va='center',
            fontsize=10, color='#334155', zorder=4)

# 组内并行比较说明
ax.text(20.0, 1.16, '命中判定：组内4行标记并行比较，有效位=1且标记相等 → 命中',
        ha='center', va='center', fontsize=10, color='#1e40af', zorder=3)
ax.text(20.0, 0.94, '第1、3、5次缺失（装入不同行），第2、4次命中，共命中2次',
        ha='center', va='center', fontsize=10, color='#065f46', zorder=3)

# ---- 主存块 → Cache 行 的映射箭头 ----
arrow_style = dict(arrowstyle='-|>', mutation_scale=16, lw=1.8, color='#2563eb')
arrows = [
    ((8.6, 5.22), (12.3, 5.33), arrow_style),
    ((8.6, 3.87), (12.3, 4.23), dict(arrow_style, color='#db2777')),
    ((8.6, 2.52), (12.3, 3.13), dict(arrow_style, color='#0891b2')),
]
for (x0, y0), (x1, y1), sty in arrows:
    ax.add_patch(mpatches.FancyArrowPatch((x0, y0), (x1, y1), **sty, zorder=5))
ax.text(10.4, 5.62, '装入行 0', ha='center', va='center', fontsize=10, color='#2563eb')
ax.text(10.4, 4.35, '装入行 1', ha='center', va='center', fontsize=10, color='#db2777')
ax.text(10.4, 3.02, '装入行 2', ha='center', va='center', fontsize=10, color='#0891b2')

fig.savefig('/home/z/my-project/public/mocks/m02/q15.png')
print('saved: /home/z/my-project/public/mocks/m02/q15.png')
