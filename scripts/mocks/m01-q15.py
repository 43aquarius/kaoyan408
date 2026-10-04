# 模拟卷一 B段 第15题（m01-co-04）配图：直接映射 Cache 的主存地址划分
# 题干参数：主存地址 24 位；Cache 数据容量 64KB；块大小 64B；直接映射
# 划分：块内偏移 6 位 + Cache 行号 10 位 + 标记 8 位
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=150, constrained_layout=True)
ax.set_xlim(-7.8, 25.8)
ax.set_ylim(0.0, 1.12)
ax.axis('off')

C_TAG, C_IDX, C_OFF = '#f59e0b', '#3b82f6', '#10b981'
T_TAG, T_IDX, T_OFF = '#92400e', '#1e40af', '#065f46'

# ---- 标题 ----
ax.text(9.0, 1.05, '直接映射 Cache 的主存地址划分（主存地址 24 位，按字节编址）',
        ha='center', va='bottom', fontsize=12.5, fontweight='bold', color='#111827')

# ---- 地址条（宽度按位数比例：8 / 10 / 6）----
ybar, hbar = 0.76, 0.17
segments = [
    (0, 8, C_TAG, '标记 Tag', '8 位'),
    (8, 18, C_IDX, '块号（Cache 行号）', '10 位'),
    (18, 24, C_OFF, '块内偏移', '6 位'),
]
for x0, x1, fc, name, bits in segments:
    ax.add_patch(mpatches.Rectangle((x0, ybar), x1 - x0, hbar, facecolor=fc,
                                    edgecolor='#111827', linewidth=1.8, zorder=2))
    ax.text((x0 + x1) / 2, ybar + hbar / 2, name + '\n' + bits,
            ha='center', va='center', fontsize=11.5, color='white',
            fontweight='bold', linespacing=1.5, zorder=3)

# ---- 位编号标注 ----
for xb, lab in [(0, '位23'), (8, '位16|15'), (18, '位6|5'), (24, '位0')]:
    ax.text(xb, ybar + hbar + 0.02, lab, ha='center', va='bottom',
            fontsize=10, color='#4b5563')

# ---- 分隔虚线（贯穿两个示例行）----
for xv in (8, 18):
    ax.plot([xv, xv], [0.345, ybar], ls=(0, (4, 3)), lw=1.5, color='#9ca3af', zorder=1)

# ---- 示例地址分解 ----
def example(ybit, yval, addr, tag, idx, off, tagv, idxv, offv, addr_color):
    ax.text(-0.5, ybit, addr, ha='right', va='center', fontsize=11.5,
            color=addr_color, fontweight='bold')
    ax.text(4, ybit, tag, ha='center', va='center', fontsize=11.5, color=T_TAG, zorder=3)
    ax.text(13, ybit, idx, ha='center', va='center', fontsize=11.5, color=T_IDX, zorder=3)
    ax.text(21, ybit, off, ha='center', va='center', fontsize=11.5, color=T_OFF, zorder=3)
    ax.text(4, yval, tagv, ha='center', va='center', fontsize=10.5, color=T_TAG, zorder=3,
            bbox=dict(boxstyle='round,pad=0.32', fc='#fee2e2', ec='#b91c1c', lw=1.5))
    ax.text(13, yval, idxv, ha='center', va='center', fontsize=10.5, color=T_IDX, zorder=3,
            bbox=dict(boxstyle='round,pad=0.32', fc='#dbeafe', ec=C_IDX, lw=1.5))
    ax.text(21, yval, offv, ha='center', va='center', fontsize=10.5, color=T_OFF, zorder=3)

example(0.635, 0.545, '0x5A3B20', '01011010', '0011101100', '100000',
        '标记 0x5A', '行号 236', '偏移 32', '#111827')
example(0.475, 0.385, '0x5E3B00', '01011110', '0011101100', '000000',
        '标记 0x5E', '行号 236', '偏移 0', '#b91c1c')

# ---- 冲突说明 ----
ax.text(9.0, 0.295,
        '两个地址的行号字段同为 236，标记却不同（0x5A 与 0x5E）：直接映射下装入同一行，相互替换（冲突）',
        ha='center', va='center', fontsize=10.5, color='#b91c1c')

# ---- 底部参数说明框 ----
ax.add_patch(mpatches.Rectangle((0.0, 0.02), 24, 0.23, facecolor='#f8fafc',
                                edgecolor='#94a3b8', linewidth=1.5, zorder=1))
ax.text(12, 0.19, '块大小 64B = 2^6 B，块内偏移 6 位；Cache 行数 = 64KB / 64B = 1024 = 2^10，行号 10 位',
        ha='center', va='center', fontsize=10, color='#334155', zorder=3)
ax.text(12, 0.135, '标记 = 24 - 10 - 6 = 8 位；直接映射：Cache 行号 = 主存块号 mod 1024',
        ha='center', va='center', fontsize=10, color='#334155', zorder=3)
ax.text(12, 0.08, '示例：0x5A3B20 属主存块 0x168EC、0x5E3B00 属主存块 0x178EC，除以 1024 余数均为 236',
        ha='center', va='center', fontsize=10, color='#334155', zorder=3)

fig.savefig('/home/z/my-project/public/mocks/m01/q15.png')
print('saved: /home/z/my-project/public/mocks/m01/q15.png')
