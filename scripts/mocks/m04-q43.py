# 模拟卷四 第43题配图：五段流水线时空图（8 条指令，Load-Use 停顿标注）
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(11.8, 6.0), dpi=150, constrained_layout=True)

STAGE_COLORS = {
    'IF':  '#BFDBFE',   # 浅蓝
    'ID':  '#A5F3FC',   # 浅青
    'EX':  '#FDE68A',   # 浅黄
    'MEM': '#BBF7D0',   # 浅绿
    'WB':  '#DDD6FE',   # 浅紫
}
STALL_COLOR = '#FECACA'   # 停顿：浅红
EDGE = '#374151'

# 每行: (指令标签, [(周期, 段名, 是否停顿)])
rows = [
    ('I1  lw R1,0(R2)',  [(1, 'IF', False), (2, 'ID', False), (3, 'EX', False), (4, 'MEM', False), (5, 'WB', False)]),
    ('I2  add R3,R4,R5', [(2, 'IF', False), (3, 'ID', False), (4, 'EX', False), (5, 'MEM', False), (6, 'WB', False)]),
    ('I3  sub R6,R1,R3', [(3, 'IF', False), (4, 'ID', False), (5, 'ID停', True), (6, 'EX', False), (7, 'MEM', False), (8, 'WB', False)]),
    ('I4  and R7,R6,R4', [(4, 'IF', False), (5, 'IF等', True), (6, 'ID', False), (7, 'EX', False), (8, 'MEM', False), (9, 'WB', False)]),
    ('I5  beq R7,R0',    [(6, 'IF', False), (7, 'ID', False), (8, 'EX', False), (9, 'MEM', False), (10, 'WB', False)]),
    ('I6  sll R8,R1,2',  [(7, 'IF', False), (8, 'ID', False), (9, 'EX', False), (10, 'MEM', False), (11, 'WB', False)]),
    ('I7  or R9,R8,R7',  [(8, 'IF', False), (9, 'ID', False), (10, 'EX', False), (11, 'MEM', False), (12, 'WB', False)]),
    ('I8  sw R6,4(R9)',  [(9, 'IF', False), (10, 'ID', False), (11, 'EX', False), (12, 'MEM', False), (13, 'WB', False)]),
]

N = len(rows)
CYCLES = 13
Y_TOP = 8.0      # 行区顶部
Y_NOTE = 9.15    # 顶部注释带

# 停顿周期（第 5 拍）整列淡红高亮
ax.axvspan(4, 5, ymin=0.0, ymax=Y_TOP / 9.6, color='#EF4444', alpha=0.10, zorder=0)

# 网格线
for i in range(CYCLES + 1):
    ax.axvline(i, color='#E5E7EB', lw=1.0, zorder=0)
for j in range(N + 1):
    ax.axhline(j, color='#E5E7EB', lw=1.0, zorder=0)

# 绘制各指令的段格
for r, (label, cells) in enumerate(rows):
    y0 = N - 1 - r          # 该行底边
    for (c, stage, stall) in cells:
        color = STALL_COLOR if stall else STAGE_COLORS[stage]
        rect = mpatches.Rectangle(
            (c - 1 + 0.05, y0 + 0.1), 0.90, 0.80,
            facecolor=color, edgecolor=('#DC2626' if stall else EDGE), linewidth=1.6,
            hatch=('///' if stall else None), zorder=2,
        )
        ax.add_patch(rect)
        ax.text(c - 0.5, y0 + 0.5, stage, ha='center', va='center',
                fontsize=10, color=('#B91C1C' if stall else '#1F2937'),
                fontweight='bold' if stall else 'normal', zorder=3)

# 坐标轴
ax.set_xticks([i + 0.5 for i in range(CYCLES)])
ax.set_xticklabels([str(i + 1) for i in range(CYCLES)], fontsize=10)
ax.set_yticks([N - 0.5 - r for r in range(N)])
ax.set_yticklabels([rows[r][0] for r in range(N)], fontsize=10)
ax.set_xlabel('时钟周期', fontsize=11)
ax.set_ylabel('指令', fontsize=11)
ax.set_xlim(-0.05, CYCLES + 0.1)
ax.set_ylim(-0.35, 9.6)
ax.tick_params(length=0)

# 顶部注释 1：停顿拍
ax.annotate(
    '第 5 拍：Load-Use 停顿（气泡）',
    xy=(4.5, Y_TOP + 0.05), xytext=(0.9, 9.0),
    ha='left', va='center', fontsize=11, color='#B91C1C', fontweight='bold',
    arrowprops=dict(arrowstyle='-|>', lw=1.8, color='#DC2626'),
)

# 左下注释 2：停顿原因（箭头指向 I4 滞留 IF 的格）
ax.annotate(
    'I3 在 ID 段停顿 1 拍：等 I1 从\nMEM 段取回的 R1（Load-Use 相关）；\nI4 因 ID 段被占而滞留 IF 段',
    xy=(4.42, 4.08), xytext=(0.12, 2.2),
    ha='left', va='top', fontsize=10, color='#B91C1C',
    arrowprops=dict(arrowstyle='-|>', lw=1.8, color='#DC2626',
                    connectionstyle='arc3,rad=-0.08'),
)

# I5 行右侧注释 3：分支判定（沿 beq 自身行指回其 EX 段）
ax.annotate(
    '第 8 拍（EX 段末）判明不转移：\n预取的 I6、I7 均有效，无冲刷',
    xy=(8.0, 3.5), xytext=(10.02, 3.5),
    ha='left', va='center', fontsize=10, color='#15803D',
    arrowprops=dict(arrowstyle='-|>', lw=1.8, color='#16A34A'),
)

# 图例
handles = [mpatches.Patch(facecolor=STAGE_COLORS[s], edgecolor=EDGE, lw=1.5, label=s)
           for s in ['IF', 'ID', 'EX', 'MEM', 'WB']]
handles.append(mpatches.Patch(facecolor=STALL_COLOR, edgecolor='#DC2626', lw=1.5,
                              hatch='///', label='停顿（气泡）'))
ax.legend(handles=handles, loc='upper right', bbox_to_anchor=(1.0, 1.0),
          ncols=3, fontsize=10, frameon=True, edgecolor='#9CA3AF')

ax.set_title('五段流水线时空图：8 条指令，1 个 Load-Use 气泡，beq 不转移', fontsize=12.5, pad=10)

fig.savefig('/home/z/my-project/public/mocks/m04/q43.png')
print('saved q43.png')
