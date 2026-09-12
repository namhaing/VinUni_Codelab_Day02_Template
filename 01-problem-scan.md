# 01 — Problem Scan & Quick Cards — Vin Smart Future

> Phần này tổng hợp nội dung Phase 1 (SCAN) và Phase 2 (QUICK-ASSESS) từ `01-worksheet.md`.
> Chủ đề nhóm lựa chọn đi sâu: **AI hỗ trợ tìm kiếm chỗ đỗ xe tại trung tâm thương mại (Vincom / Vinhomes Mall).**

---

# 🔍 Phase 1 — SCAN: Danh sách bài toán

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Vinhomes (Vincom Mall)** | Tốn thời gian | Khách hàng lái xe vòng vòng nhiều vòng qua các tầng hầm để tìm chỗ đỗ trống vào giờ cao điểm (cuối tuần, lễ Tết), gây ùn ứ ngay lối vào bãi xe. |
| 2 | **Vinhomes (Vincom Mall)** | Pain từ người khác | Bảo vệ/nhân viên trông xe phải liên tục dùng bộ đàm hỏi các tầng khác còn trống không vì bảng LED chỉ hiển thị tổng số chỗ trống theo tầng, không theo khu vực cụ thể, dẫn tới thông tin sai lệch, khách vẫn đi vào tầng đã đầy. |
| 3 | **Xanh SM** | Tốn thời gian | Điều phối viên xử lý thủ công các phản hồi khẩn cấp từ tài xế về sự cố sạc pin hoặc va chạm thực địa (mất 15-20 phút/lượt). |
| 4 | **Vinhomes** | Lặp lại | Phân loại và điều hướng thủ công các phản ánh của cư dân (mất nước, hỏng đèn, ồn ào...) gửi qua App Vinhomes Resident đến đúng ban quản lý từng tòa nhà. |
| 5 | **VinFast** | AI có thể tốt hơn | Khách hàng mô tả lỗi xe bằng tiếng Việt tự nhiên (ví dụ: "xe đi qua gờ giảm tốc kêu cụp cụp ở bánh trước"), tổng đài CSKH phải tự phân loại mã lỗi kỹ thuật ban đầu bằng tay. |

---

# 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Nhóm chọn **top 3** từ danh sách SCAN: **#1 (Tìm chỗ đỗ xe TTTM), #2 (Bảng LED sai lệch chỗ trống), #4 (Vinhomes CSKH phản ánh cư dân)**.

## Card #1 — AI hỗ trợ tìm kiếm chỗ đỗ xe tại trung tâm thương mại ⭐ (Bài toán chọn Deep-Dive)

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Khách hàng lái xe vào bãi đỗ TTTM Vincom không    │
│ biết tầng/khu vực nào còn chỗ trống, phải dò tìm thủ công.  │
│ Công ty thành viên: [x] Vinhomes (Vincom Retail)            │
│                                                             │
│ Ai đang đau (Actor)? Khách hàng lái xe (mất thời gian, bực  │
│ bội); Nhân viên bãi xe (quá tải trả lời bộ đàm liên tục).   │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Xe qua cổng, nhận vé từ  ──> 2. Nhìn bảng LED tổng số  │
│   trạm barrier tự động             chỗ trống toàn tầng      │
│   ──> 3. Lái vòng quanh từng tầng dò chỗ trống bằng mắt     │
│   ──> 4. Hỏi bảo vệ qua bộ đàm nếu không tìm thấy chỗ       │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 3 (⏱ 5-8 phút/lượt,   │
│ giờ cao điểm có thể tới 15 phút, dễ đi lạc vào tầng đã đầy) │
│ AI có thể hỗ trợ ở bước nào? Bước 2-3 (tổng hợp dữ liệu     │
│ cảm biến/camera theo thời gian thực, dẫn đường tới ô trống  │
│ gần nhất qua app/màn hình chỉ dẫn tại từng ngã rẽ)          │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ Giảm thời gian tìm chỗ đỗ từ 8 phút ──> dưới 2 phút;        │
│ Độ chính xác chỗ trống hiển thị đạt ≥ 95%.                  │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [ ] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

## Card #2 — Bảng chỉ dẫn chỗ trống LED sai lệch theo khu vực

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Bảng LED chỉ hiển thị tổng số chỗ trống/tầng nên  │
│ khách vẫn đi vào khu vực đã kín chỗ, gây ùn tắc lối đi nội  │
│ bộ trong bãi xe.                                            │
│ Công ty thành viên: [x] Vinhomes (Vincom Retail)            │
│                                                             │
│ Ai đang đau (Actor)? Khách hàng, Bảo vệ bãi xe.             │
│                                                             │
│ Workflow thủ công hiện tại (3 bước):                        │
│   1. Cảm biến đếm xe vào/ra theo tầng ──> 2. Cập nhật số    │
│   tổng lên bảng LED mỗi vài phút ──> 3. Bảo vệ đứng tại các │
│   giao lộ hướng dẫn thủ công khi khách hỏi                  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 (⏱ dữ liệu trễ 3-5  │
│ phút, không chia theo từng khu A/B/C trong tầng)            │
│ AI có thể hỗ trợ ở bước nào? Bước 2 (tổng hợp real-time từ  │
│ nhiều cảm biến/camera theo từng khu nhỏ, dự đoán khu nào sẽ │
│ trống trong 2-3 phút tới)                                   │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ Độ trễ cập nhật dữ liệu chỗ trống giảm từ 5 phút ──> <30s.  │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [ ] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

## Card #3 — Vinhomes CSKH phân loại phản ánh cư dân

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Phản ánh của cư dân qua App Vinhomes Resident bị  │
│ định tuyến sai ban quản lý, phải chuyển tay nhiều lần.      │
│ Công ty thành viên: [x] Vinhomes                            │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên CSKH tổng đài, cư dân.       │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                        │
│   1. Cư dân gửi phản ánh text tự do ──> 2. Nhân viên đọc và │
│   đoán đúng danh mục ──> 3. Chuyển tay tới ban quản lý tòa  │
│   ──> 4. Ban quản lý phản hồi lại cư dân (thường sau 12h)   │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2 (⏱ 3-5 phút/lượt,   │
│ tỉ lệ định tuyến sai ước tính ~20%)                          │
│ AI có thể hỗ trợ ở bước nào? Bước 2 (phân loại tự động nội  │
│ dung phản ánh và gợi ý đúng ban quản lý phụ trách)          │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                        │
│ Giảm thời gian phản hồi đầu tiên từ 12h ──> dưới 2h;        │
│ Độ chính xác phân loại đạt ≥ 90%.                            │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

---

# 🗳️ Quyết định lựa chọn của nhóm

Nhóm quyết định chọn **Card #1 — AI hỗ trợ tìm kiếm chỗ đỗ xe tại trung tâm thương mại** để thực hiện Deep-Dive.

## Lý do lựa chọn và loại bỏ các thẻ khác:
* **Card #2 (Bảng LED sai lệch):** Thực chất là một phần dữ liệu nền (data layer) phục vụ trực tiếp cho Card #1 — nếu giải quyết được bài toán dẫn đường chỗ trống ở Card #1 thì Card #2 gần như được giải quyết theo. Gộp chung để tránh trùng lặp phạm vi.
* **Card #3 (Vinhomes CSKH):** Có giá trị nhưng rủi ro xử lý sai thông tin liên quan tới phí quản lý/tranh chấp căn hộ đòi hỏi thêm dữ liệu lịch sử phân loại để huấn luyện/đánh giá trước khi triển khai — cần thêm thời gian chuẩn bị dữ liệu (NOT YET), nên ưu tiên thấp hơn trong lab này.

**Bài toán được chọn để Deep-Dive: Card #1 — AI hỗ trợ tìm kiếm chỗ đỗ xe tại trung tâm thương mại (chi tiết tại `02-deep-dive-report.md`).**
