# 模拟卷（七）第 43 题配图：12 位自定义浮点格式位段图（数符/阶码/尾数 宽度与权重标注）
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/truetype/chinese/SarasaMonoSC-Regular.ttf')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Sarasa Mono SC', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(7.8, 4.8), dpi=150, constrained_layout=True)
ax.set_xlim(0, 12.04)
ax.set_ylim(0, 8.6)
ax.axis('off')

# ---------------- 基本几何参数 ----------------
uw, gap = 0.92, 0.20                 # 每位宽度 / 字段间空隙
y0, y1 = 4.55, 5.85                  # 单元格纵向范围
xs = 0.30                            # 数符起点
xe = xs + uw + gap                   # 阶码起点
xm = xe + 4 * uw + gap               # 尾数起点
x_end = xm + 7 * uw                  # 总右边界
xc_all = (xs + x_end) / 2

c_sign, e_sign = '#fee2e2', '#b91c1c'
c_exp, e_exp = '#dbeafe', '#1d4ed8'
c_mant, e_mant = '#d1fae5', '#047857'


def cell(x, fc, ec):
    ax.add_patch(plt.Rectangle((x, y0), uw, y1 - y0, facecolor=fc, edgecolor=ec, lw=1.8))


cell(xs, c_sign, e_sign)
for i in range(4):
    cell(xe + i * uw, c_exp, e_exp)
for i in range(7):
    cell(xm + i * uw, c_mant, e_mant)

# ---------------- 示例机器码 0 1011 1101000B = 5E8H（+6.5，与题中小题数据不重合） ----------------
yc = (y0 + y1) / 2
ax.text(xs + uw / 2, yc, '0', ha='center', va='center', fontsize=17, fontweight='bold', color=e_sign)
for i, b in enumerate('1011'):
    ax.text(xe + i * uw + uw / 2, yc, b, ha='center', va='center', fontsize=17, fontweight='bold', color=e_exp)
for i, b in enumerate('1101000'):
    ax.text(xm + i * uw + uw / 2, yc, b, ha='center', va='center', fontsize=17, fontweight='bold', color=e_mant)

# ---------------- 位编号 ----------------
ax.text(xs + uw / 2, y1 + 0.13, '11', ha='center', va='center', fontsize=10, color='#374151')
for i in range(4):
    ax.text(xe + i * uw + uw / 2, y1 + 0.13, str(10 - i), ha='center', va='center', fontsize=10, color='#374151')
for i in range(7):
    ax.text(xm + i * uw + uw / 2, y1 + 0.13, str(6 - i), ha='center', va='center', fontsize=10, color='#374151')

# ---------------- 字段分组标注与括线 ----------------
def bracket(xa, xb, label, color):
    ax.plot([xa, xb], [6.40, 6.40], color=color, lw=1.8, solid_capstyle='round')
    ax.plot([xa, xa], [6.22, 6.40], color=color, lw=1.8)
    ax.plot([xb, xb], [6.22, 6.40], color=color, lw=1.8)
    ax.text((xa + xb) / 2, 6.56, label, ha='center', va='center', fontsize=11.5, fontweight='bold', color=color)

bracket(xs, xs + uw, '数符 S（1 位）', e_sign)
bracket(xe, xe + 4 * uw, '阶码字段（4 位，移码）', e_exp)
bracket(xm, xm + 7 * uw, '尾数数值字段（7 位，原码小数）', e_mant)

# ---------------- 各字段位权标注 ----------------
ax.text(xs + uw / 2, y0 - 0.27, '0 正\n1 负', ha='center', va='top', fontsize=10, color=e_sign, linespacing=1.2)
for i, w in enumerate(['8', '4', '2', '1']):
    ax.text(xe + i * uw + uw / 2, y0 - 0.27, w, ha='center', va='top', fontsize=10.5, color=e_exp)
ax.text(xm - 0.14, y0 - 0.27, '0.', ha='right', va='top', fontsize=12, fontweight='bold', color=e_mant)
for i in range(7):
    ax.text(xm + i * uw + uw / 2, y0 - 0.27, '$2^{-%d}$' % (i + 1), ha='center', va='top', fontsize=10.5, color=e_mant)

# ---------------- 语义说明框 ----------------
box_w = x_end - xs
ax.add_patch(plt.Rectangle((xs, 2.30), box_w, 1.50, facecolor='#fef3c7', edgecolor='#b45309', lw=1.5))
ax.text(xs + 0.25, 3.48, '阶码：移码，偏置 2^3 = 8，E = 阶码字段值 − 8，范围 −8 ~ +7（无全 0 / 全 1 特殊编码）',
        fontsize=10.5, color='#7c2d12', va='center')
ax.text(xs + 0.25, 3.03, '尾数：规格化原码小数 M = 0.1xxxxxxB，首位必须为 1 且显式存储（无隐藏位），1/2 ≤ M ≤ 127/128',
        fontsize=10.5, color='#7c2d12', va='center')
ax.text(xs + 0.25, 2.58, '真值：N = (−1)^S × M × 2^E（S 为数符，M 为尾数，E 为阶码真值）',
        fontsize=10.5, color='#7c2d12', va='center')

# ---------------- 示例解读框 ----------------
ax.add_patch(plt.Rectangle((xs, 0.35), box_w, 1.60, facecolor='#f3f4f6', edgecolor='#6b7280', lw=1.5))
ax.text(xs + 0.25, 1.64, '示例（图中单元格内的位）：机器码 0 1011 1101000B = 5E8H',
        fontsize=11, fontweight='bold', color='#111827', va='center')
ax.text(xs + 0.25, 1.13, 'S = 0（正）；阶码字段 1011B = 11，E = 11 − 8 = +3；尾数 M = 0.1101000B = 13/16',
        fontsize=10.5, color='#111827', va='center')
ax.text(xs + 0.25, 0.66, 'N = +13/16 × 2^3 = +6.5',
        fontsize=10.5, color='#111827', va='center')

# ---------------- 总标题 ----------------
ax.text(xc_all, 8.20, '12 位自定义浮点数格式（非 IEEE 754）', ha='center', va='center',
        fontsize=13.5, fontweight='bold', color='#111827')

fig.savefig('/home/z/my-project/public/mocks/m07/q43.png')
print('saved: /home/z/my-project/public/mocks/m07/q43.png')
