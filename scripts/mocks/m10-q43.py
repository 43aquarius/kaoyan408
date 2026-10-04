# 模拟卷（十）· 第 43 题配图：Cache—主存—磁盘三级存储层次图
# 输出: /home/z/my-project/public/mocks/m10/q43.png
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7.4, 5.2), dpi=150, constrained_layout=True)
ax.set_xlim(0, 12)
ax.set_ylim(0, 12.4)
ax.axis('off')

def level_box(x, y, w, h, title, lines, fc, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle='round,pad=0.10,rounding_size=0.16',
                                linewidth=1.8, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h - 0.42, title, ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1f2937')
    ax.text(x + w / 2, y + (h - 0.75) / 2 + 0.10, '\n'.join(lines),
            ha='center', va='center', fontsize=10, color='#111827', linespacing=1.55)

def arrow(x0, y0, x1, y1, color, style='-|>'):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style,
                                 mutation_scale=15, linewidth=1.8, color=color))

# ---- 三级存储层次（自上而下：速度递减、容量递增） ----
level_box(3.2, 10.35, 5.6, 1.35, 'CPU（MMU 内含 TLB）',
          ['TLB 16 项 · 全相联', '查 TLB 2 ns · 命中率 98%'],
          '#fef3c7', '#d97706')

level_box(3.2, 7.55, 5.6, 1.95, 'Cache（数据 Cache）',
          ['容量 32 KB · 2 路组相联 · 块大小 64 B', '命中时间 2 ns · 命中率 95%'],
          '#dcfce7', '#16a34a')

level_box(3.2, 4.75, 5.6, 1.95, '主存',
          ['容量 2^28 B = 256 MB · 访问一次 100 ns', '物理地址 28 位 · 页表常驻主存'],
          '#dbeafe', '#2563eb')

level_box(3.2, 1.85, 5.6, 1.95, '磁盘（虚拟存储器的后援存储器）',
          ['虚拟地址 32 位 · 页大小 4 KB', '缺页服务 8 ms/页 · 缺页率 0.0005%'],
          '#fee2e2', '#dc2626')

# ---- 层间箭头与标注 ----
# CPU -> Cache：送物理地址
arrow(6.0, 10.35, 6.0, 9.50, '#374151')
ax.text(6.25, 9.92, '送 28 位物理地址（TLB 命中 98%；\n未命中则查主存页表 100 ns）',
        ha='left', va='center', fontsize=10, color='#374151')

# Cache <-> 主存
arrow(7.7, 7.55, 7.7, 6.70, '#dc2626')   # 向下：未命中
ax.text(9.05, 7.12, 'Cache 未命中 5%：\n向下访问主存（100 ns）', ha='left', va='center',
        fontsize=10, color='#b91c1c')
arrow(4.3, 6.70, 4.3, 7.55, '#2563eb')   # 向上：调块
ax.text(2.95, 7.12, '整块 64 B\n调入 Cache', ha='right', va='center',
        fontsize=10, color='#1d4ed8')

# 主存 <-> 磁盘
arrow(7.7, 4.75, 7.7, 3.80, '#dc2626')   # 向下：缺页
ax.text(9.05, 4.28, '缺页 0.0005%：\n从磁盘读入一页（8 ms）', ha='left', va='center',
        fontsize=10, color='#b91c1c')
arrow(4.3, 3.80, 4.3, 4.75, '#2563eb')   # 向上：调页
ax.text(2.95, 4.28, '一页 4 KB\n装入主存', ha='right', va='center',
        fontsize=10, color='#1d4ed8')

# ---- 左侧趋势轴 ----
arrow(1.55, 2.35, 1.55, 11.35, '#6b7280', style='<|-|>')
ax.text(1.55, 11.75, '速度更快 · 容量更小 · 每位成本更高', ha='center', va='center',
        fontsize=10, color='#374151')
ax.text(1.55, 1.90, '速度更慢 · 容量更大 · 每位成本更低', ha='center', va='center',
        fontsize=10, color='#374151')

# ---- 底部访问路径提示 ----
ax.text(6.9, 0.75, '一次访存（串行）：查 TLB 2 ns → 访 Cache 2 ns → 未命中访主存 100 ns → 缺页调磁盘 8 ms',
        ha='center', va='center', fontsize=10, color='#374151',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#f3f4f6', edgecolor='#9ca3af', linewidth=1.2))

ax.set_title('题 43 图 · Cache—主存—磁盘三级存储层次（按速度自上而下）',
             fontsize=13, fontweight='bold', color='#111827', pad=10)

fig.savefig('/home/z/my-project/public/mocks/m10/q43.png')
print('saved: /home/z/my-project/public/mocks/m10/q43.png')
