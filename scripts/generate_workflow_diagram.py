"""
One-off script to render 04-workflow-diagram.png for the parking-spot-finder
deep-dive report (Current-State workflow, top half; Future-State flow, bottom half).
Not part of the graded prompt_prototype.py exercise.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

fig, axes = plt.subplots(2, 1, figsize=(13, 9))
fig.suptitle("AI hỗ trợ tìm kiếm chỗ đỗ xe tại Trung tâm Thương mại (Vincom Mall)",
             fontsize=15, fontweight="bold")

def draw_box(ax, x, y, w, h, title, lines, color, bottleneck=False):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.02",
                          linewidth=1.5, edgecolor="#333333", facecolor=color)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h - 0.10, title, ha="center", va="top",
            fontsize=10.5, fontweight="bold")
    ty = y + h - 0.28
    for line in lines:
        ax.text(x + w / 2, ty, line, ha="center", va="top", fontsize=8.7)
        ty -= 0.145
    if bottleneck:
        ax.text(x + w - 0.14, y + h - 0.10, "BOTTLENECK", ha="right", va="top",
                fontsize=6.5, fontweight="bold", color="#a11")

def draw_arrow(ax, x1, y, x2, handoff=False):
    arr = FancyArrowPatch((x1, y), (x2, y), arrowstyle="-|>", mutation_scale=16,
                           linewidth=1.5, color="#333333")
    ax.add_patch(arr)
    if handoff:
        ax.text((x1 + x2) / 2, y + 0.09, "HANDOFF", ha="center", fontsize=6.5, color="#555")

# ---------------- Current-State (top) ----------------
ax = axes[0]
ax.set_xlim(0, 13); ax.set_ylim(0, 2.2); ax.axis("off")
ax.set_title("Current-State Workflow — Tổng thời gian ~8-12 phút/lượt (giờ cao điểm)",
             fontsize=11, loc="left", color="#7a1f1f")

box_w, box_h, gap, y0 = 2.6, 1.7, 0.55, 0.25
steps_cur = [
    ("Bước 1", ["Xe qua cổng,", "barrier tự động mở", "15 giây"], "#eef3fb", False),
    ("Bước 2", ["Nhìn bảng LED", "tổng số chỗ trống/tầng", "10 giây"], "#eef3fb", False),
    ("Bước 3", ["Lái vòng dò chỗ", "trống bằng mắt", "5-8 phút"], "#fbe4e4", True),
    ("Bước 4", ["Hỏi bảo vệ qua", "bộ đàm nếu ko thấy", "2-4 phút"], "#fbe4e4", True),
]
x = 0.3
xs = []
for title, lines, color, bn in steps_cur:
    draw_box(ax, x, y0, box_w, box_h, title, lines, color, bn)
    xs.append(x)
    x += box_w + gap
for i in range(len(xs) - 1):
    draw_arrow(ax, xs[i] + box_w, y0 + box_h / 2, xs[i + 1], handoff=True)

legend_cur = [Line2D([0], [0], marker='o', color='w', label='Bottleneck', markerfacecolor='#fbe4e4', markeredgecolor='#333', markersize=12),
              Line2D([0], [0], marker='o', color='w', label='Handoff', markerfacecolor='#eef3fb', markeredgecolor='#333', markersize=12)]
ax.legend(handles=legend_cur, loc="lower right", fontsize=8, frameon=False)

# ---------------- Future-State (bottom) ----------------
ax2 = axes[1]
ax2.set_xlim(0, 13); ax2.set_ylim(0, 2.4); ax2.axis("off")
ax2.set_title("Future-State Flow — Mục tiêu: dưới 3 phút/lượt (Rule Engine + LLM Feature)",
              fontsize=11, loc="left", color="#1f5c2e")

steps_fut = [
    ("Bước 1", ["Xe qua cổng,", "barrier tự động mở"], "#eef3fb"),
    ("[AI] Bước 2", ["Rule Engine: tổng hợp", "occupancy real-time", "theo từng khu nhỏ"], "#dbe9ff"),
    ("[AI] Bước 3", ["LLM soạn hướng dẫn:", "\"Còn 8 chỗ ở B2-C,", "gần thang máy số 3\""], "#dbe9ff"),
    ("[Human] Bước 4", ["Màn hình/app hiển thị", "chỉ dẫn cho khách"], "#e1f5e6"),
]
x = 0.3
xs2 = []
for title, lines, color in steps_fut:
    draw_box(ax2, x, y0 + 0.3, box_w, box_h, title, lines, color, False)
    xs2.append(x)
    x += box_w + gap
for i in range(len(xs2) - 1):
    draw_arrow(ax2, xs2[i] + box_w, y0 + 0.3 + box_h / 2, xs2[i + 1])

# Fallback annotation under step 3
fx = xs2[2]
ax2.annotate("Fallback: nếu độ tin cậy cảm biến thấp → quay về\nhiển thị tổng số chỗ trống theo tầng (như hệ thống cũ)",
             xy=(fx + box_w / 2, y0 + 0.3), xytext=(fx + box_w / 2, 0.15),
             ha="center", fontsize=8.3, color="#8a4b00",
             arrowprops=dict(arrowstyle="-|>", color="#8a4b00", lw=1.2))

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("04-workflow-diagram.png", dpi=170)
print("Saved 04-workflow-diagram.png")
