# 模拟卷十 B 段第 15 题配图：2 路组相联 Cache—主存映射结构图
# 参数与题干严格一致：主存 32 位地址、块 128 B、Cache 16 KB、2 路组相联、64 组
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(9.5, 6.0), dpi=150, constrained_layout=True)

# ---------- 顶部：主存地址 32 位划分 ----------
bar_y, bar_h = 5.35, 0.5
fields = [
    (0.6, 4.4, '#ef9a9a', '标记 19 位（地址 31-13）'),
    (5.0, 2.0, '#ffcc80', '组号 6 位（12-7）'),
    (7.0, 2.4, '#a5d6a7', '块内地址 7 位（6-0）'),
]
for x, w, c, t in fields:
    ax.add_patch(Rectangle((x, bar_y), w, bar_h, facecolor=c, edgecolor='#37474f', lw=1.6))
    ax.text(x + w / 2, bar_y + bar_h / 2, t, fontsize=10.5, ha='center', va='center', color='#212121')
ax.text(5.0, 6.05, '主存地址 32 位（按字节编址）', fontsize=11.5, ha='center', va='center',
        fontweight='bold', color='#212121')
ax.text(2.8, 5.16, '与 Cache 行内的标记比较', fontsize=10, ha='center', va='center', color='#546e7a')
ax.text(6.0, 5.16, '作组索引', fontsize=10, ha='center', va='center', color='#546e7a')
ax.text(8.2, 5.16, '块内偏移', fontsize=10, ha='center', va='center', color='#546e7a')

# ---------- 左侧：主存 ----------
ax.add_patch(Rectangle((0.6, 0.7), 2.8, 4.3, facecolor='#eceff1', edgecolor='#37474f', lw=2.0))
ax.text(2.0, 4.78, '主存（4 GB，2^25 块）', fontsize=11, ha='center', va='center',
        fontweight='bold', color='#212121')

blocks = [
    ('块 0', 4.30, '#2e7d32'),
    ('块 1', 3.80, '#6a1b9a'),
    ('块 64', 3.00, '#1565c0'),
    ('块 128', 2.25, '#e64a19'),
]
for label, y, color in blocks:
    ax.add_patch(Rectangle((0.85, y - 0.21), 2.3, 0.42, facecolor='white', edgecolor=color, lw=1.8))
    ax.text(2.0, y, label, fontsize=10.5, ha='center', va='center', color='#212121')
for y in (3.40, 2.63, 1.85):
    ax.text(2.0, y, '……', fontsize=10, ha='center', va='center', color='#607d8b')
ax.text(2.0, 1.28, '0x00000000、0x00002000、\n0x00004000、0x00000080\n依次对应块 0、64、128、1',
        fontsize=10, ha='center', va='center', color='#455a64')

# ---------- 右侧：Cache ----------
ax.add_patch(Rectangle((5.6, 0.7), 3.8, 4.3, facecolor='#ffffff', edgecolor='#37474f', lw=2.0))
ax.text(7.5, 4.78, 'Cache 数据区（16 KB = 64 组 × 2 行 × 128 B）', fontsize=11,
        ha='center', va='center', fontweight='bold', color='#212121')


def draw_group(y_bottom, name, face):
    ax.add_patch(Rectangle((5.75, y_bottom), 3.5, 0.9, facecolor=face, edgecolor='#37474f', lw=1.8))
    ax.text(6.05, y_bottom + 0.45, name, fontsize=10.5, ha='center', va='center',
            fontweight='bold', color='#212121')
    for i in range(2):
        ry = y_bottom + 0.06 + i * 0.42
        ax.add_patch(Rectangle((6.35, ry), 2.8, 0.38, facecolor='#e3f2fd', edgecolor='#546e7a', lw=1.5))
        ax.text(7.75, ry + 0.19, 'V · 标记 19 位 · 128 B 数据', fontsize=10,
                ha='center', va='center', color='#212121')


draw_group(3.62, '组 0', '#fffde7')   # 块 0、64、128 竞争的组，高亮
draw_group(2.47, '组 1', '#ffffff')
ax.text(7.5, 2.62, '……', fontsize=10, ha='center', va='center', color='#607d8b')
draw_group(1.02, '组 63', '#ffffff')

# ---------- 映射箭头 ----------
arrows = [
    (3.18, 4.30, 5.73, 4.30, '#2e7d32', 0.02),   # 块 0 → 组 0
    (3.18, 3.00, 5.73, 4.05, '#1565c0', -0.18),  # 块 64 → 组 0
    (3.18, 2.25, 5.73, 3.80, '#e64a19', -0.30),  # 块 128 → 组 0
    (3.18, 3.80, 5.73, 2.92, '#6a1b9a', 0.15),   # 块 1 → 组 1
]
for x1, y1, x2, y2, color, rad in arrows:
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), connectionstyle='arc3,rad=%.2f' % rad,
                                 color=color, lw=2.0, arrowstyle='-|>', mutation_scale=14,
                                 shrinkA=2, shrinkB=2, zorder=5))
ax.text(4.45, 4.72, '按 块号 mod 64\n确定组号', fontsize=10, ha='center', va='center', color='#455a64')

# ---------- 底部说明 ----------
ax.text(5.0, 0.28,
        '映射规则：主存块号 mod 64 = 组号，映射到同一组的主存块共 2^19 = 524288 个。\n'
        '块 0、块 64、块 128（余数均为 0）竞争组 0 的 2 行，由 LRU 决定去留；块 1（余数 1）映射到组 1。',
        fontsize=10.5, ha='center', va='center', color='#37474f')

ax.set_title('2 路组相联 Cache 与主存的映射结构（Cache 16 KB，块 128 B，共 64 组）',
             fontsize=12.5, color='#212121')
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.55)
ax.axis('off')

fig.savefig('/home/z/my-project/public/mocks/m10/q15.png')
print('saved: /home/z/my-project/public/mocks/m10/q15.png')
