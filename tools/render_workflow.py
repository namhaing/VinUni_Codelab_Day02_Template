"""Render the parking current/future workflow deliverable as a PNG."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "04-workflow-diagram.png"
W, H = 2000, 1280


def font(size: int, bold: bool = False):
    name = "seguisb.ttf" if bold else "segoeui.ttf"
    path = Path("C:/Windows/Fonts") / name
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


F_TITLE = font(52, True)
F_SUB = font(31, True)
F_BOX = font(24, True)
F_BODY = font(20)
F_SMALL = font(17)


def rounded_box(draw, xy, title, lines, fill, outline, badge=None):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=22, fill=fill, outline=outline, width=4)
    draw.text((x1 + 20, y1 + 16), title, font=F_BOX, fill="#10243e")
    y = y1 + 58
    for line in lines:
        draw.text((x1 + 20, y), line, font=F_SMALL, fill="#334155")
        y += 27
    if badge:
        label, color = badge
        bx2, by2 = x2 - 14, y1 + 40
        tw = draw.textlength(label, font=F_SMALL)
        draw.rounded_rectangle((bx2 - tw - 22, y1 + 12, bx2, by2), radius=12, fill=color)
        draw.text((bx2 - tw - 11, y1 + 16), label, font=F_SMALL, fill="white")


def arrow(draw, start, end, color="#64748b"):
    draw.line((start, end), fill=color, width=6)
    ex, ey = end
    sx, sy = start
    if abs(ex - sx) >= abs(ey - sy):
        pts = [(ex, ey), (ex - 18, ey - 12), (ex - 18, ey + 12)]
    else:
        pts = [(ex, ey), (ex - 12, ey - 18), (ex + 12, ey - 18)]
    draw.polygon(pts, fill=color)


img = Image.new("RGB", (W, H), "#f8fafc")
d = ImageDraw.Draw(img)
d.rectangle((0, 0, W, 118), fill="#082f49")
d.text((70, 25), "QR PARKING ASSISTANT — WORKFLOW MAP", font=F_TITLE, fill="white")
d.text((70, 88), "Vin Smart Future | Vincom shopping-mall parking", font=F_SMALL, fill="#bae6fd")

d.text((70, 150), "CURRENT STATE — khách tự tìm chỗ", font=F_SUB, fill="#7f1d1d")
current = [
    ("1. Vào bãi", ["Barrier ghi nhận", "xe/vé"], "0,5 phút"),
    ("2. Xem biển tầng", ["Chỉ có tổng số", "chỗ còn lại"], "1 phút"),
    ("3. Chạy vào zone", ["Tự chọn hướng", "theo biển"], "2–4 phút"),
    ("4. Tìm từng dãy", ["Quan sát thủ công", "không biết ô cụ thể"], "4–8 phút"),
    ("5. Ô bị chiếm", ["Quay lại / đổi dãy", "dữ liệu có thể chậm"], "2–4 phút"),
    ("6. Hỏi nhân viên", ["Handoff thủ công", "qua cử chỉ/bộ đàm"], "2 phút"),
]
x0, y0, bw, bh, gap = 70, 205, 280, 160, 38
for i, (title, lines, timing) in enumerate(current):
    x = x0 + i * (bw + gap)
    bottleneck = i in (3, 4)
    rounded_box(d, (x, y0, x + bw, y0 + bh), title, lines, "#fff1f2" if bottleneck else "white", "#ef4444" if bottleneck else "#cbd5e1", ("BOTTLENECK", "#dc2626") if bottleneck else None)
    d.text((x + 20, y0 + 125), f"Time: {timing}", font=F_SMALL, fill="#475569")
    if i < len(current) - 1:
        arrow(d, (x + bw + 4, y0 + bh // 2), (x + bw + gap - 6, y0 + bh // 2))

d.rounded_rectangle((70, 392, 1930, 452), radius=18, fill="#fee2e2")
d.text((95, 408), "Giả thuyết baseline: 8–15 phút giờ cao điểm | Pain: chạy vòng, ùn giao cắt, tăng workload điều phối", font=F_BODY, fill="#7f1d1d")

d.text((70, 505), "FUTURE STATE — grounded guidance, có fallback", font=F_SUB, fill="#14532d")
future = [
    ("1. Quét QR", ["Xác định anchor +", "nhu cầu đỗ xe"], "HUMAN", "#e0f2fe", "#0284c7"),
    ("2. Occupancy", ["Camera / sensor", "state + freshness"], "SYSTEM", "#f1f5f9", "#64748b"),
    ("3. Safety rules", ["Lọc reserved, EV,", "accessible, lối đóng"], "RULE", "#fef3c7", "#d97706"),
    ("4. Rank + route", ["Chọn candidate", "và route hợp lệ"], "ENGINE", "#ede9fe", "#7c3aed"),
    ("5. AI draft", ["Diễn giải route", "không bịa dữ liệu"], "AI", "#dbeafe", "#2563eb"),
    ("6. Xác nhận đỗ", ["Lưu spot/zone vào", "session ẩn danh"], "HUMAN", "#dcfce7", "#16a34a"),
]
y1 = 565
for i, (title, lines, badge, fill, outline) in enumerate(future):
    x = x0 + i * (bw + gap)
    rounded_box(d, (x, y1, x + bw, y1 + bh), title, lines, fill, outline, (badge, outline))
    if i < len(future) - 1:
        arrow(d, (x + bw + 4, y1 + bh // 2), (x + bw + gap - 6, y1 + bh // 2), "#16a34a")

# return-to-car journey
d.rounded_rectangle((70, 755, 1930, 805), radius=16, fill="#ecfccb", outline="#65a30d", width=3)
d.text((95, 766), "KHI RA VỀ: quét QR gần thang máy → xác minh session → tuyến đi bộ → vị trí xe đã lưu → xóa session khi xe ra", font=F_BODY, fill="#365314")

# fallback row
d.rounded_rectangle((70, 830, 1930, 1000), radius=24, fill="#fff7ed", outline="#ea580c", width=4)
d.text((100, 848), "FALLBACK & OPERATIONAL BOUNDARIES", font=F_SUB, fill="#9a3412")
fallback_lines = [
    "• Dữ liệu >10 giây, confidence <0,95 hoặc thiếu >5%: không gợi ý ô cụ thể → dùng biển/nhân viên.",
    "• Không bịa spot_id/route, không tuyên bố giữ chỗ, không điều khiển xe hoặc barrier.",
    "• One-way, closed aisle, accessible, EV-only và reserved là hard rules ngoài LLM.",
    "• Ô bị chiếm: re-route; QR/session lỗi: không đoán vị trí; mất mạng/camera: dùng biển/nhân viên.",
]
for i, line in enumerate(fallback_lines):
    d.text((105, 892 + i * 25), line, font=F_SMALL, fill="#7c2d12")

d.rounded_rectangle((70, 1030, 1930, 1190), radius=24, fill="#ecfeff", outline="#0891b2", width=4)
d.text((100, 1055), "SUCCESS METRICS (PROPOSED — CẦN ĐO BASELINE)", font=F_SUB, fill="#164e63")
metrics = [
    "Median entry-to-park < 5 phút", "Occupancy precision/recall ≥ 95%", "State freshness p95 ≤ 10 giây",
    "Scan-to-guidance < 10 giây", "Tìm lại đúng zone ≥ 95%", "0 route safety violation",
]
for i, metric in enumerate(metrics):
    col, row = i % 3, i // 3
    d.text((110 + col * 600, 1110 + row * 34), "- " + metric, font=F_BODY, fill="#155e75")

d.text((70, 1230), "RED = Bottleneck   |   Arrows = Handoff   |   BLUE = AI step   |   GREEN = Human responsibility", font=F_SMALL, fill="#475569")
img.save(OUT, quality=95)
print(OUT)
