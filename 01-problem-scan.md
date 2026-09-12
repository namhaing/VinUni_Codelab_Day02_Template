# 01 — Problem Scan & Quick Problem Cards

**Vai trò:** AI Product Engineer tại Vin Smart Future  
**Mảng ưu tiên:** Vincom Retail/Vingroup — vận hành bãi đỗ xe trung tâm thương mại

> Tất cả thời gian, lưu lượng và tỷ lệ trong bài là **baseline giả thuyết phục vụ scoping**, không phải số liệu nội bộ đã xác minh. Nhóm cần đo lại bằng camera/sensor logs, vé xe và khảo sát vận hành trước khi triển khai.

## Phase 1 — SCAN

| # | Đơn vị | Lens | Vấn đề vận hành |
|---:|---|---|---|
| 1 | Vincom | Stakeholder Pain | Khách mất nhiều thời gian chạy vòng để tìm ô đỗ còn trống, đặc biệt cuối tuần và giờ cao điểm. |
| 2 | Vincom | Time-consuming | Nhân viên điều phối phải quan sát camera/bộ đàm rồi hướng từng xe đến khu còn chỗ. |
| 3 | Vincom | AI-upgrade | Biển điện tử chỉ báo số chỗ theo tầng nhưng không hiểu nhu cầu như gần thang máy, chỗ xe điện hoặc chỗ tiếp cận. |
| 4 | Vincom | Repetitive | Nhân viên tổng hợp thủ công tình trạng đầy/chỗ trống và thời gian tìm chỗ theo ca vận hành. |
| 5 | Vincom | Stakeholder Pain | Khách quên vị trí xe và phải nhờ bảo vệ dò tìm theo biển số/khu vực nhớ mang máng. |
| 6 | Vincom | Time-consuming | Xử lý xe đi nhầm làn, ùn tại điểm giao cắt và phân luồng lại khi một khu bất ngờ đầy. |

## Phase 2 — QUICK-ASSESS

### Quick Problem Card #1 — QR Parking Assistant: tìm ô và ghi nhớ vị trí xe

| Thành phần | Nội dung |
|---|---|
| **Bài toán** | Khách quét QR tại cổng/cột mốc để mở web app, tìm ô phù hợp; sau khi đỗ, hệ thống lưu vị trí để dẫn khách quay lại xe. |
| **Actor** | Người lái xe; nhân viên điều phối bãi xe. |
| **Workflow hiện tại** | (1) Xe vào bãi → (2) xem biển tầng → (3) chạy tìm → (4) gặp khu đầy → (5) hỏi nhân viên/quay lại → (6) tự nhớ/chụp vị trí → (7) lúc về tìm lại xe. |
| **Bottleneck** | Bước 3–5; baseline giả thuyết 8–15 phút vào giờ cao điểm. |
| **AI hỗ trợ** | QR xác định điểm bắt đầu; camera/sensor xác nhận occupancy; routing chọn tuyến; web app lưu phiên đỗ; AI hội thoại hiểu nhu cầu và giải thích ngắn. |
| **Metric đề xuất** | Scan-to-guidance <10 giây; median search time <5 phút; ≥95% đề xuất còn trống; ≥95% phiên đã xác nhận có thể dẫn lại đúng zone xe. |
| **Kiến trúc** | **QR Anchor + CV/Sensor + Rule + Routing + Session Store + LLM Feature**. |
| **Rủi ro** | Dữ liệu chậm khiến hướng nhiều xe tới cùng ô; chỉ dẫn gây mất tập trung; không bảo đảm ô cho người khuyết tật/EV. |

### Quick Problem Card #2 — Tìm lại xe trong bãi

| Thành phần | Nội dung |
|---|---|
| **Bài toán** | Giúp khách tìm khu vực đã đỗ dựa trên biển số và hành trình hợp lệ. |
| **Actor** | Khách hàng và nhân viên an ninh/bãi xe. |
| **Workflow hiện tại** | (1) Khách báo quên vị trí → (2) cung cấp biển số → (3) nhân viên dò camera/log → (4) xác minh chủ xe → (5) hướng dẫn tới khu vực. |
| **Bottleneck** | Dò nhiều màn hình camera và xác minh; giả thuyết 15–30 phút/lượt. |
| **AI hỗ trợ** | Tra log nhận diện biển số và tóm tắt tuyến đến khu vực xe. |
| **Metric đề xuất** | 90% case xác định đúng zone dưới 3 phút; 100% case phải xác minh quyền truy cập. |
| **Kiến trúc** | **ANPR/CV + Search + Rule**, LLM chỉ giải thích. |
| **Rủi ro** | Lộ vị trí xe cho người không phải chủ xe; nhận diện sai biển số. |

### Quick Problem Card #3 — Dự báo đầy bãi và hỗ trợ phân luồng

| Thành phần | Nội dung |
|---|---|
| **Bài toán** | Cảnh báo sớm khu/tầng sắp đầy để nhân viên chủ động đổi biển báo và phân luồng xe. |
| **Actor** | Trưởng ca và nhân viên điều phối bãi xe. |
| **Workflow hiện tại** | (1) Theo dõi camera/đếm xe → (2) nhận báo khu đầy → (3) liên lạc bộ đàm → (4) đổi hướng xe → (5) cập nhật biển. |
| **Bottleneck** | Phản ứng sau khi ùn tắc đã hình thành; dữ liệu phân tán. |
| **AI hỗ trợ** | Forecast occupancy 15–30 phút và gợi ý kế hoạch phân luồng dạng nháp. |
| **Metric đề xuất** | Cảnh báo trước ≥15 phút; giảm thời gian ùn tại điểm giao cắt 25%; false alarm dưới ngưỡng vận hành. |
| **Kiến trúc** | **Forecasting + Rule + Optimization**. |
| **Rủi ro** | Dự báo sai làm chuyển ùn tắc sang khu khác; không phù hợp prompt-only prototype. |

## Lựa chọn

| Tiêu chí (1–5) | Card #1 Tìm ô | Card #2 Tìm xe | Card #3 Dự báo đầy |
|---|---:|---:|---:|
| Tác động trải nghiệm | 5 | 4 | 5 |
| Workflow dễ quan sát | 5 | 4 | 4 |
| Metric đo được | 5 | 4 | 4 |
| MVP khả thi | 4 | 4 | 3 |
| Rủi ro kiểm soát được | 4 | 3 | 3 |
| Phù hợp bài lab | 5 | 4 | 3 |
| **Tổng** | **28** | **23** | **22** |

Chọn **Card #1 — QR Parking Assistant**. MVP có ba chức năng cốt lõi: (1) quét QR để xác định vị trí hiện tại và nhận hướng dẫn tới ô phù hợp, (2) xác nhận “Tôi đã đỗ” hoặc quét QR tại cột/zone để lưu vị trí xe, và (3) khi ra về, quét QR gần thang máy để nhận tuyến đi bộ tới vị trí đã lưu. Hệ thống không giữ chỗ và không điều khiển phương tiện.
