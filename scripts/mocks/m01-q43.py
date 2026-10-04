# 模拟卷一 E段 第43题（m01-co-12）配图：Cache-主存地址映射结构图
# 题目参数：主存地址 32 位、按字节编址；Cache 数据区 32KB、块 64B、4 路组相联、LRU、写回法
# 地址划分：标记 19 位（位 31~13）| 组号 7 位（位 12~6）| 块内地址 6 位（位 5~0）
# 映射关系：组号 = 主存块号 mod 128；同组 2^19 个主存块（如块 0、128、256、384……）映射到组 0 的 4 行
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7.6, 5.6), dpi=150, constrained_layout=True)
ax.set_xlim(0, 10)
ax.set_ylim(0, 7.6)
ax.axis('off')

C_TAG, E_TAG = '#dbeafe', '#1d4ed8'
C_SET, E_SET = '#fef3c7', '#b45309'
C_OFF, E_OFF = '#d1fae5', '#047857'

# ---- 标题与地址条 ----
ax.text(5, 7.35, '第 43 题 Cache-主存地址映射结构（4 路组相联，块 64B）',
        ha='center', va='center', fontsize=12.5, fontweight='bold', color='#111827')
ax.text(5, 6.95, '32 位主存地址（按字节编址）', ha='center', va='center',
        fontsize=11, color='#334155')

x0, w = 1.0, 8.0
w_tag, w_set, w_off = w * 19 / 32, w * 7 / 32, w * 6 / 32
y_b, h_b = 6.3, 0.55
segs = [
    (x0, w_tag, C_TAG, E_TAG, '标记 Tag 19 位', '第 31 ~ 13 位'),
    (x0 + w_tag, w_set, C_SET, E_SET, '组号 7 位', '第 12 ~ 6 位'),
    (x0 + w_tag + w_set, w_off, C_OFF, E_OFF, '块内地址 6 位', '第 5 ~ 0 位'),
]
for sx, sw, fc, ec, t1, t2 in segs:
    ax.add_patch(mpatches.Rectangle((sx, y_b), sw, h_b, facecolor=fc,
                                    edgecolor=ec, linewidth=1.8))
    ax.text(sx + sw / 2, y_b + h_b * 0.64, t1, ha='center', va='center',
            fontsize=10.5, color='#111827')
    ax.text(sx + sw / 2, y_b + h_b * 0.24, t2, ha='center', va='center',
            fontsize=10, color='#374151')

# ---- 三个字段的用途箭头与说明 ----
notes = [
    (x0 + w_tag / 2, '与选中组中 4 行的标记比较', E_TAG),
    (x0 + w_tag + w_set / 2, '组译码：选中 1 组', E_SET),
    (x0 + w_tag + w_set + w_off / 2, '在块内选字节', E_OFF),
]
for cx, txt, c in notes:
    ax.annotate('', xy=(cx, 5.78), xytext=(cx, y_b - 0.03),
                arrowprops=dict(arrowstyle='-|>', lw=1.8, color=c))
    ax.text(cx, 5.6, txt, ha='center', va='center', fontsize=10, color=c)

# ---- 主存框 ----
ax.add_patch(mpatches.FancyBboxPatch((0.4, 1.15), 3.05, 3.85,
                                     boxstyle='round,pad=0.05',
                                     facecolor='#f8fafc', edgecolor='#475569',
                                     linewidth=1.8))
ax.text(1.925, 4.78, '主存：2^32 B = 2^26 块', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#111827')
blocks = ['主存块 0', '主存块 128', '主存块 256', '主存块 384']
bys = [4.24, 3.78, 3.32, 2.86]
for t, by in zip(blocks, bys):
    ax.add_patch(mpatches.Rectangle((0.7, by), 2.05, 0.38, facecolor='#e2e8f0',
                                    edgecolor='#475569', linewidth=1.5))
    ax.text(1.725, by + 0.19, t, ha='center', va='center', fontsize=10,
            color='#111827')
ax.text(1.725, 2.56, '……', ha='center', va='center', fontsize=12, color='#475569')
ax.text(1.725, 2.22, '共 2^19 个块映射到组 0', ha='center', va='center',
        fontsize=10, color='#b91c1c')
ax.text(1.725, 1.83, '（这些块号 mod 128 = 0）', ha='center', va='center',
        fontsize=10, color='#475569')
ax.text(1.725, 1.44, '标记 = 块号的高 19 位', ha='center', va='center',
        fontsize=10, color='#1d4ed8')

# ---- 主存到 Cache 的映射箭头 ----
ax.add_patch(mpatches.FancyArrowPatch((3.5, 3.55), (4.62, 3.55),
                                      arrowstyle='-|>', mutation_scale=18,
                                      lw=2.0, color='#b91c1c'))
ax.text(4.06, 3.98, '全部映射', ha='center', va='center',
        fontsize=10, color='#b91c1c')
ax.text(4.06, 3.74, '到组 0', ha='center', va='center',
        fontsize=10, color='#b91c1c')

# ---- Cache 框 ----
ax.add_patch(mpatches.FancyBboxPatch((4.65, 1.15), 4.95, 3.85,
                                     boxstyle='round,pad=0.05',
                                     facecolor='#ffffff', edgecolor='#1d4ed8',
                                     linewidth=1.8))
ax.text(7.125, 4.78, 'Cache 数据区 32KB（512 行 = 128 组 x 4 行）',
        ha='center', va='center', fontsize=11, fontweight='bold', color='#111827')

# 组 0 子框（4 行结构展开）
ax.add_patch(mpatches.FancyBboxPatch((4.85, 1.85), 4.55, 2.7,
                                     boxstyle='round,pad=0.04',
                                     facecolor='#f0f7ff', edgecolor='#1d4ed8',
                                     linewidth=1.5))
ax.text(7.125, 4.4, '组 0（其余 127 组结构相同）', ha='center', va='center',
        fontsize=10.5, color='#1d4ed8')

# 列标题
ax.text(5.15, 4.06, '行', ha='center', va='center', fontsize=10, color='#334155')
ax.text(5.62, 4.06, 'V', ha='center', va='center', fontsize=10, color='#334155')
ax.text(6.12, 4.06, 'D', ha='center', va='center', fontsize=10, color='#334155')
ax.text(7.05, 4.06, '标记（19 位）', ha='center', va='center', fontsize=10,
        color='#1d4ed8')
ax.text(8.5, 4.06, '数据（64B）', ha='center', va='center', fontsize=10,
        color='#047857')

row_ys = [3.5, 3.02, 2.54, 2.06]
for i, ry in enumerate(row_ys):
    ax.text(5.15, ry + 0.2, '行' + str(i), ha='center', va='center',
            fontsize=10, color='#334155')
    ax.add_patch(mpatches.Rectangle((5.37, ry), 0.5, 0.4, facecolor='#e5e7eb',
                                    edgecolor='#475569', linewidth=1.5))
    ax.text(5.62, ry + 0.2, 'V', ha='center', va='center', fontsize=10,
            color='#111827')
    ax.add_patch(mpatches.Rectangle((5.87, ry), 0.5, 0.4, facecolor='#fee2e2',
                                    edgecolor='#b91c1c', linewidth=1.5))
    ax.text(6.12, ry + 0.2, 'D', ha='center', va='center', fontsize=10,
            color='#111827')
    ax.add_patch(mpatches.Rectangle((6.37, ry), 1.35, 0.4, facecolor=C_TAG,
                                    edgecolor=E_TAG, linewidth=1.5))
    ax.text(7.045, ry + 0.2, '标记 19 位', ha='center', va='center',
            fontsize=10, color='#111827')
    ax.add_patch(mpatches.Rectangle((7.72, ry), 1.55, 0.4, facecolor=C_OFF,
                                    edgecolor=E_OFF, linewidth=1.5))
    ax.text(8.495, ry + 0.2, '数据 64B', ha='center', va='center',
            fontsize=10, color='#111827')

ax.text(7.125, 1.62, 'V = 有效位（1 位）；D = 脏位（1 位，写回法用）',
        ha='center', va='center', fontsize=10, color='#334155')
ax.text(7.125, 1.35, '替换算法：LRU',
        ha='center', va='center', fontsize=10, color='#334155')

# ---- 底部说明 ----
ax.text(5, 0.55, '组号 = 主存块号 mod 128（地址第 12~6 位）；同组的 2^19 个主存块竞争该组的 4 行，由 LRU 决定替换',
        ha='center', va='center', fontsize=10.5, color='#334155')

fig.savefig('/home/z/my-project/public/mocks/m01/q43.png')
print('saved: /home/z/my-project/public/mocks/m01/q43.png')
