# 模拟卷五 第43题配图：一次数据访存全链路框图（CPU → TLB → 页表 → Cache → 主存）
# 参数与题干严格一致：TLB 2ns/90%；页表 20ns（直接访问主存，不经过 Cache）；Cache 5ns/95%；主存 20ns
import matplotlib.font_manager as fm

fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

BLUE, GREEN, ORANGE, DARK, GRAY = '#1d4ed8', '#15803d', '#c2410c', '#1f2937', '#6b7280'

fig, ax = plt.subplots(figsize=(11, 6.6), dpi=150, constrained_layout=True)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9.4)
ax.axis('off')


def box(x, y, w, h, title, subs, fc, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.10',
                                linewidth=2.0, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h * 0.70, title, ha='center', va='center',
            fontsize=12, color=DARK, fontweight='bold')
    for k, s in enumerate(subs):
        ax.text(x + w / 2, y + h * (0.42 - k * 0.24), s, ha='center', va='center',
                fontsize=10, color='#374151')


def arr(p1, p2, color, lw=2.2, head=True, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2,
                                 arrowstyle='-|>' if head else '-',
                                 mutation_scale=18, linewidth=lw, color=color,
                                 connectionstyle='arc3,rad=%.2f' % rad, zorder=3))


# ---- 主链（第一行）：CPU → TLB → Cache ----
box(0.5, 5.0, 2.0, 1.7, 'CPU', ['执行访存', '指令'], '#eef2ff', '#4f46e5')
box(4.8, 5.0, 2.7, 1.7, 'TLB', ['命中率 90%', '访问 2 ns'], '#fef9c3', '#a16207')
box(10.0, 5.0, 2.7, 1.7, 'Cache', ['命中率 95%', '访问 5 ns'], '#ecfeff', '#0e7490')
# ---- 未命中支路（第二行）：页表、主存 ----
box(4.8, 1.0, 2.7, 1.7, '页表', ['驻留主存', '查找 20 ns 不过 Cache'], '#f3f4f6', '#4b5563')
box(10.0, 1.0, 2.7, 1.7, '主存', ['访问 20 ns'], '#fee2e2', '#b91c1c')

# ---- 箭头 ----
# ① CPU -> TLB（发虚拟地址）
arr((2.5, 5.85), (4.8, 5.85), BLUE)
ax.text(3.65, 6.02, '① 发虚拟地址 VA', ha='center', va='bottom', fontsize=10, color=BLUE)
# ② TLB 命中 -> Cache
arr((7.5, 5.85), (10.0, 5.85), GREEN, lw=2.6)
ax.text(8.75, 6.02, '② TLB 命中 90%\n得页框号，成 PA', ha='center', va='bottom',
        fontsize=10, color=GREEN, linespacing=1.4)
# ③ TLB 未命中 -> 页表
arr((6.15, 5.0), (6.15, 2.7), ORANGE)
ax.text(6.0, 3.85, '③ TLB 未命中 10%\n访主存查页表 20 ns', ha='right', va='center',
        fontsize=10, color=ORANGE, linespacing=1.4)
# 页表查得页框号后回到 Cache 访问流程
arr((7.5, 1.85), (10.8, 5.0), ORANGE, rad=0.08)
ax.text(9.35, 3.15, '查得后继续流程④', ha='left', va='center', fontsize=10, color=ORANGE)
# ⑤ Cache 未命中 -> 主存
arr((11.35, 5.0), (11.35, 2.7), ORANGE)
ax.text(11.5, 3.85, '⑤ Cache 未命中 5%\n访问主存 20 ns', ha='left', va='center',
        fontsize=10, color=ORANGE, linespacing=1.4)
# ④ Cache 命中 -> 顶部数据返回总线
arr((11.35, 6.7), (11.35, 7.6), GREEN, lw=2.4)
ax.text(11.35, 7.75, '④ Cache 命中 95%：数据返回 CPU（共 5 ns）', ha='center', va='bottom',
        fontsize=10, color=GREEN)
# ⑤ 主存 -> 右侧返回线 -> 顶部数据返回总线
arr((12.7, 1.85), (14.5, 1.85), ORANGE, head=False)
arr((14.5, 1.85), (14.5, 7.6), ORANGE, head=False)
# 数据返回总线：自右向左回到 CPU
arr((14.5, 7.6), (1.5, 7.6), DARK, lw=2.2, head=False)
arr((1.5, 7.6), (1.5, 6.7), DARK, lw=2.2)
ax.text(14.92, 4.7, '⑤ 未命中：读主存 20 ns，\n装块入 Cache 并返回', ha='center', va='center',
        fontsize=10, color=ORANGE, rotation=90, linespacing=1.4)
ax.text(6.5, 7.82, '数据返回通路', ha='center', va='bottom', fontsize=10, color=DARK)

# ---- 标题与说明 ----
ax.text(8.0, 9.05, '一次数据访存全链路框图（CPU → TLB → 页表 → Cache → 主存）',
        ha='center', va='center', fontsize=13, fontweight='bold', color=DARK)
ax.text(0.4, 0.42,
        '说明：各环节串行进行，不考虑缺页。访问 TLB 2 ns（命中率 90%）；TLB 未命中时查页表 20 ns（直接访问主存，不经过 Cache）；\n'
        '访问 Cache 5 ns（命中率 95%）；Cache 未命中时再访问主存 20 ns。',
        ha='left', va='center', fontsize=10, color=GRAY, linespacing=1.6)

fig.savefig('/home/z/my-project/public/mocks/m05/q43.png')
print('saved: /home/z/my-project/public/mocks/m05/q43.png')
