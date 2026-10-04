# 模拟卷一 D段 第42题（m01-ds-13）配图：表达式二叉树
# 树结构：根 *，左子树 -（左孩子 a，右孩子 +，+ 的孩子为 b、c），右孩子 d
# 表达式：(a - (b + c)) * d；中序序列 a, -, b, +, c, *, d
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=150, constrained_layout=True)
ax.set_xlim(-0.5, 7.3)
ax.set_ylim(-0.75, 4.55)
ax.axis('off')

ax.text(3.4, 4.35, '第 42 题表达式二叉树：((a - (b + c)) * d)',
        ha='center', va='bottom', fontsize=12.5, fontweight='bold', color='#111827')

# ---- 结点坐标（值, x, y）----
nodes = {
    '*': (3.4, 3.4),
    '-': (1.9, 2.4),
    'd': (5.0, 2.4),
    'a': (0.9, 1.4),
    '+': (2.9, 1.4),
    'b': (1.9, 0.4),
    'c': (3.9, 0.4),
}
edges = [('*', '-'), ('*', 'd'), ('-', 'a'), ('-', '+'), ('+', 'b'), ('+', 'c')]

for u, v in edges:
    x1, y1 = nodes[u]
    x2, y2 = nodes[v]
    ax.plot([x1, x2], [y1, y2], color='#64748b', lw=1.8, zorder=1)

C_OP, C_LEAF = '#3b82f6', '#10b981'
for val, (x, y) in nodes.items():
    fc = C_OP if val in ('*', '-', '+', '/') else C_LEAF
    ax.add_patch(mpatches.Circle((x, y), 0.32, facecolor=fc,
                                 edgecolor='#111827', linewidth=1.8, zorder=2))
    ax.text(x, y, val, ha='center', va='center', fontsize=14, color='white',
            fontweight='bold', zorder=3)

# ---- 图例 ----
ax.add_patch(mpatches.Circle((5.05, 4.05), 0.14, facecolor=C_OP,
                             edgecolor='#111827', linewidth=1.5))
ax.text(5.3, 4.05, '运算符（分支结点）', ha='left', va='center',
        fontsize=10.5, color='#1e40af')
ax.add_patch(mpatches.Circle((5.05, 3.7), 0.14, facecolor=C_LEAF,
                             edgecolor='#111827', linewidth=1.5))
ax.text(5.3, 3.7, '操作数（叶子结点）', ha='left', va='center',
        fontsize=10.5, color='#065f46')

# ---- 层号标注（第 1 层为根）----
for lab, y in [('第 1 层', 3.4), ('第 2 层', 2.4), ('第 3 层', 1.4), ('第 4 层', 0.4)]:
    ax.text(-0.35, y, lab, ha='left', va='center', fontsize=10, color='#4b5563')

# ---- 底部说明 ----
ax.text(3.4, -0.2, '中序遍历序列：a, -, b, +, c, *, d（直接作中缀表达式有歧义）',
        ha='center', va='center', fontsize=10.5, color='#334155')
ax.text(3.4, -0.55, '完全加括号的中缀表达式：(a - (b + c)) * d',
        ha='center', va='center', fontsize=10.5, color='#b91c1c')

fig.savefig('/home/z/my-project/public/mocks/m01/q42.png')
print('saved: /home/z/my-project/public/mocks/m01/q42.png')
