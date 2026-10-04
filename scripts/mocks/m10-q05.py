# 模拟卷十 A 段第 5 题配图：中序线索二叉树（实线孩子指针 / 虚线线索）
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8, 4.6), dpi=150, constrained_layout=True)

# 结点位置：x 取中序序号，y 取层次（根在最上层）
pos = {
    'G': (7, 3),
    'D': (4, 2), 'M': (10, 2),
    'B': (2, 1), 'E': (5, 1), 'H': (8, 1), 'N': (11, 1),
    'A': (1, 0), 'C': (3, 0), 'F': (6, 0), 'J': (9, 0),
}
r = 0.27

# ---- 实线：孩子指针 ----
children = [
    ('G', 'D'), ('G', 'M'),
    ('D', 'B'), ('D', 'E'),
    ('B', 'A'), ('B', 'C'),
    ('E', 'F'),
    ('M', 'H'), ('M', 'N'),
    ('H', 'J'),
]
for a, b in children:
    x1, y1 = pos[a]
    x2, y2 = pos[b]
    ax.plot([x1, x2], [y1, y2], color='#1565c0', lw=2.0, zorder=1)

# ---- 虚线：线索（前驱 / 后继） ----
threads = [
    ('A', 'B', 0.35),   # A 的后继线索 -> B
    ('C', 'B', 0.35),   # C 的前驱线索 -> B
    ('C', 'D', -0.25),  # C 的后继线索 -> D
    ('E', 'D', 0.30),   # E 的前驱线索 -> D
    ('F', 'E', 0.30),   # F 的前驱线索 -> E
    ('F', 'G', -0.30),  # F 的后继线索 -> G
    ('H', 'G', 0.30),   # H 的前驱线索 -> G
    ('J', 'H', 0.30),   # J 的前驱线索 -> H
    ('J', 'M', -0.25),  # J 的后继线索 -> M
    ('N', 'M', 0.30),   # N 的前驱线索 -> M
]
for a, b, rad in threads:
    x1, y1 = pos[a]
    x2, y2 = pos[b]
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle='arc3,rad=%.2f' % rad,
        linestyle='--', color='#d32f2f', lw=1.6,
        arrowstyle='-|>', mutation_scale=13,
        shrinkA=13, shrinkB=13, zorder=2,
    )
    ax.add_patch(arrow)

# ---- NULL 线索（首结点前驱 / 末结点后继） ----
ax.annotate(
    '', xy=(0.15, 0), xytext=(1 - r - 0.05, 0),
    arrowprops=dict(arrowstyle='-|>', linestyle='--', color='#d32f2f', lw=1.6),
)
ax.text(-0.15, 0, 'NULL', fontsize=10, color='#d32f2f', ha='center', va='center')
ax.annotate(
    '', xy=(11.85, 0), xytext=(11 + r + 0.05, 0),
    arrowprops=dict(arrowstyle='-|>', linestyle='--', color='#d32f2f', lw=1.6),
)
ax.text(12.15, 0, 'NULL', fontsize=10, color='#d32f2f', ha='center', va='center')

# ---- 结点 ----
for name, (x, y) in pos.items():
    circ = Circle((x, y), r, facecolor='white', edgecolor='#263238', lw=1.8, zorder=3)
    ax.add_patch(circ)
    ax.text(x, y, name, fontsize=13, fontweight='bold',
            ha='center', va='center', color='#263238', zorder=4)

# ---- 图例与标注 ----
legend_children = mpatches.Patch(color='#1565c0', label='孩子指针（ltag/rtag = 0）')
legend_thread = mpatches.Patch(color='#d32f2f', label='线索：前驱/后继（ltag/rtag = 1）')
ax.legend(handles=[legend_children, legend_thread], loc='lower left', fontsize=10, framealpha=0.95)

ax.text(6, -0.85, '中序序列：A  B  C  D  E  F  G  H  J  M  N', fontsize=11,
        ha='center', va='center', color='#37474f')
ax.set_title('中序线索二叉树（实线为孩子指针，虚线为线索）', fontsize=13, color='#212121')

ax.set_xlim(-0.8, 12.7)
ax.set_ylim(-1.25, 3.65)
ax.axis('off')

fig.savefig('/home/z/my-project/public/mocks/m10/q05.png')
print('saved: /home/z/my-project/public/mocks/m10/q05.png')
