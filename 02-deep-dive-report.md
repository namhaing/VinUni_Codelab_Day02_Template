# 02 — Deep-Dive Report — AI hỗ trợ tìm kiếm chỗ đỗ xe tại Trung tâm Thương mại

> Phần này tổng hợp nội dung Phase 3 (DEEP-DIVE) và Phase 5 (EVALUATE) từ `01-worksheet.md`.
> **Mảng kinh doanh:** Vinhomes / Vincom Retail — Vận hành bãi đỗ xe tầng hầm tại trung tâm thương mại.
> **Bài toán:** Khách hàng lái xe không biết tầng/khu vực nào còn chỗ trống khi vào bãi đỗ xe TTTM, phải dò tìm thủ công gây ùn tắc và trải nghiệm khách hàng kém.

---

# 🏗️ Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow Mapping

Quy trình hiện tại khi một xe khách hàng vào bãi đỗ xe TTTM Vincom giờ cao điểm (cuối tuần):

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Xe qua cổng, │     │ Nhìn bảng LED│     │ Lái vòng qua │     │ Hỏi bảo vệ   │
│ barrier tự   │ ──→ │ hiển thị TỔNG│ ──→ │ từng tầng dò │ ──→ │ qua bộ đàm   │
│ động mở, lấy │  🔄 │ số chỗ trống │  🔄 │ chỗ trống    │  🔄 │ nếu không    │
│ vé/quét biển │     │ theo TẦNG    │     │ bằng mắt     │     │ tìm thấy chỗ │
│ số            │     │              │     │              │     │              │
│ Ai: Khách    │     │ Ai: Khách    │     │ Ai: Khách    │     │ Ai: Khách +  │
│ hàng         │     │ hàng         │     │ hàng         │     │ Bảo vệ       │
│ ⏱ 15 giây    │     │ ⏱ 10 giây    │     │ ⏱ 5-8 phút🔴 │     │ ⏱ 2-4 phút🔴 │
│ In: Biển số  │     │ In: Số liệu  │     │ In: Quan sát │     │ In: Câu hỏi  │
│ Out: Vé xe   │     │ đếm xe vào/ra│     │ trực quan    │     │ qua bộ đàm   │
│              │     │ Out: Số hiển │     │ Out: Vị trí  │     │ Out: Hướng   │
│              │     │ thị trên LED │     │ xe trong bãi │     │ dẫn miệng    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
🔴 = Bottleneck   🔄 = Handoff (khách tự xử lý / chuyển sang hỏi người khác)

⏱ Tổng thời gian xử lý trung bình: **~8-12 phút/lượt** vào giờ cao điểm
   (so với ~1-2 phút vào giờ vắng khách).
```

**Ghi chú vận hành:**
* Bảng LED chỉ cập nhật **tổng số chỗ trống theo cả tầng** (ví dụ "Tầng B2: còn 12 chỗ"), không chia theo khu vực A/B/C trong tầng — nên khách vẫn có thể lái vào khu đã kín chỗ.
* Dữ liệu LED có độ trễ 3-5 phút do cập nhật theo chu kỳ quét thủ công/cảm biến rời rạc, không real-time.
* Bảo vệ tại các giao lộ phải kiêm nhiệm vừa phân luồng giao thông vừa trả lời câu hỏi khách qua bộ đàm — dễ quá tải giờ cao điểm.

---

## 3.2. Problem Statement (6-field) & Metrics

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Khách hàng tự lái xe (người chịu ảnh hưởng trực tiếp) và Nhân viên/bảo vệ bãi xe TTTM Vincom (người hỗ trợ xử lý khi khách hỏi). |
| **2. Current Workflow** | Xe vào bãi qua barrier tự động, khách nhìn bảng LED chỉ hiển thị *tổng* số chỗ trống theo từng tầng, sau đó tự lái vòng qua các tầng để dò tìm chỗ trống bằng mắt, và hỏi bảo vệ qua bộ đàm nếu không tìm được. 4 bước, phần lớn thủ công/quan sát trực quan, mất trung bình 8-12 phút/lượt giờ cao điểm. |
| **3. Bottleneck** | Bước 3 (dò tìm chỗ trống bằng mắt qua nhiều tầng) chiếm 5-8 phút vì hệ thống LED không cung cấp thông tin chỗ trống theo khu vực/thời gian thực, buộc khách phải tự đi khảo sát hoặc chờ bảo vệ trả lời qua bộ đàm (thêm 2-4 phút). |
| **4. Business Impact** | Tại một TTTM Vincom quy mô lớn, ước tính ~1.200-1.500 lượt xe/ngày cuối tuần. Nếu 30% lượt xe rơi vào giờ cao điểm mất thêm 6-8 phút/lượt so với bình thường, tổng thời gian lãng phí ước tính **~45-60 giờ khách hàng/ngày cuối tuần**. Hệ quả: ùn tắc dồn ngược ra cổng vào (ảnh hưởng giao thông khu vực), tăng phàn nàn trải nghiệm trên app đánh giá TTTM, và một số khách hàng bỏ cuộc quay xe ra ngoài tìm chỗ đỗ khác — thất thoát doanh thu gián tiếp cho các gian hàng thuê mặt bằng. |
| **5. Success Metric** | 1. Giảm thời gian trung bình tìm được chỗ đỗ từ 8-12 phút xuống **dưới 3 phút** vào giờ cao điểm (Efficiency).<br>2. Độ chính xác thông tin chỗ trống hiển thị theo khu vực đạt **≥ 95%** so với thực tế (Quality/Trust).<br>3. Giảm ≥ 50% số lượt khách phải hỏi bảo vệ qua bộ đàm (Ops load). |
| **6. Operational Boundary** | AI được phép: tổng hợp dữ liệu cảm biến/camera đếm chỗ trống theo thời gian thực, tính toán và hiển thị/điều hướng khách đến khu vực còn trống gần nhất, soạn tin nhắn/thông báo hướng dẫn dạng văn bản tự nhiên trên app hoặc màn hình chỉ dẫn. **CẤM:** AI không được tự ý điều khiển barrier/hệ thống vật lý (mở/đóng cổng, chặn làn xe); không được hiển thị số chỗ trống khi độ tin cậy dữ liệu cảm biến dưới ngưỡng an toàn (phải fallback về hiển thị theo tầng như hệ thống cũ thay vì hiển thị số liệu có thể sai); mọi thay đổi cấu hình ngưỡng/khu vực phải được nhân viên vận hành phê duyệt trước khi áp dụng lên hệ thống thật (không tự động deploy). |

---

## 3.3. Future-State Flow & AI Fit

### So sánh Rule vs LLM vs Agent

| Tiêu chí | Rule / State-Machine | LLM Feature | Agentic Loop |
|---|---|---|---|
| Bản chất bài toán | Đếm chỗ trống real-time từ cảm biến/camera + tìm khu trống gần nhất (bài toán tính toán xác định, không cần suy luận ngôn ngữ) | Diễn giải dữ liệu occupancy thành hướng dẫn tự nhiên, dễ hiểu, trả lời câu hỏi tự do của khách ("chỗ nào gần thang máy B?") | Cần chuỗi quyết định tự trị nhiều bước, gọi nhiều tool khác nhau theo ngữ cảnh thay đổi liên tục |
| Độ phù hợp với bài toán này | ✅ **Rất phù hợp** — đây là lõi xử lý chính, đảm bảo độ chính xác và độ trễ thấp | ✅ Phù hợp làm **lớp bổ trợ** (giao tiếp/hướng dẫn), không phải lõi quyết định | ❌ Không cần thiết — không có chuỗi tác vụ đa bước đòi hỏi lập kế hoạch tự trị |
| Rủi ro khi sai | Thấp nếu ngưỡng cảm biến được kiểm định kỹ; dễ audit/debug vì logic tường minh | Trung bình — có thể "ảo giác" hướng dẫn sai nếu không ràng buộc chặt vào dữ liệu occupancy gốc | Cao — khó kiểm soát hành vi, chi phí vận hành cao, không tương xứng với giá trị mang lại |
| **Kết luận AI-Fit** | ✅ Chọn làm **lõi xử lý** (occupancy engine + pathfinding) | ✅ Chọn làm **lớp giao tiếp/UX** (chuyển JSON occupancy → hướng dẫn tiếng Việt tự nhiên, trả lời câu hỏi khách qua chatbot/màn hình) | ❌ Không chọn cho bài toán này |

→ **Kiến trúc AI-Fit tổng thể:** *Rule/State-Machine (lõi) + LLM Feature (lớp hướng dẫn/giao tiếp)*. Không cần Agentic Loop vì rủi ro/chi phí không tương xứng với một bài toán có cấu trúc dữ liệu ổn định và ranh giới rõ ràng.

### Future-State Flow

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ 🔵 Bước 2    │     │ 🔵 Bước 3    │     │ 🟢 Bước 4    │
│ Xe qua cổng, │     │ Rule Engine  │     │ LLM soạn     │     │ Màn hình/app │
│ barrier tự   │ ──→ │ tổng hợp real│ ──→ │ hướng dẫn tự │ ──→ │ hiển thị chỉ │
│ động mở      │     │ -time occupancy│   │ nhiên: "Còn  │     │ dẫn cho khách│
│              │     │ theo từng khu│     │ 8 chỗ ở B2-C,│     │ (không cần   │
│              │     │ nhỏ (cảm biến│     │ gần thang máy│     │ duyệt vì chỉ │
│              │     │ + camera)    │     │ số 3"        │     │ là thông tin)│
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  ▼
                                           ↩️ Fallback:
                                           Nếu độ tin cậy dữ liệu
                                           cảm biến < ngưỡng an toàn,
                                           tự động quay về hiển thị
                                           tổng số chỗ trống theo
                                           tầng (như hệ thống LED cũ)
                                           thay vì đưa thông tin sai.

Ghi chú Human-in-the-loop: Nhân viên vận hành TTTM (Facility Ops) là
🟢 người **duyệt trước khi triển khai** mọi thay đổi ngưỡng cảm biến/
cấu hình khu vực mới lên hệ thống thật — không có HITL theo thời gian
thực trên từng lượt xe (vì đây chỉ là thông tin hiển thị, không phải
hành động có thể gây hại vật lý).
```

---

# 🏁 Phase 5 — EVALUATE

### AI Readiness Checklist:
1. [x] Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test? — *Có một phần*: TTTM đã có hệ thống cảm biến đếm xe vào/ra theo tầng (phục vụ bảng LED hiện tại) và camera an ninh sẵn có ở các tầng hầm; cần bổ sung/hiệu chỉnh để chia nhỏ theo khu vực thay vì theo cả tầng.
2. [x] Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)? — Có; rủi ro cao nhất là hiển thị sai chỗ trống, đã có cơ chế Fallback về chế độ hiển thị theo tầng (an toàn, không gây tai nạn) và AI không được phép điều khiển barrier vật lý.
3. [x] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ? — Có; Ban quản lý TTTM và đội vận hành bãi xe đã xác nhận mong muốn giảm tải công việc trả lời bộ đàm và cải thiện đánh giá trải nghiệm khách hàng.

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:
[x] **GO (Bắt đầu xây dựng Prototype):** Bắt đầu phát triển với scope hẹp.
[ ] **NOT YET (Cần tích lũy thêm dữ liệu/xác lập baseline):** Trì hoãn để chuẩn bị thêm.
[ ] **NO-GO (Không khả thi / Rule-based tốt hơn):** Hủy bỏ dự án AI này.

**Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí):**
> Dự án được đánh giá đạt mức **GO** với **scope hẹp: pilot 1 tầng hầm (B2) trong 4 tuần** trước khi nhân rộng, vì các lý do sau:
> 1. **Hạ tầng dữ liệu đã có sẵn phần lớn** (cảm biến đếm xe, camera an ninh) — chi phí triển khai chủ yếu là tích hợp và chia nhỏ vùng đếm, không phải xây mới từ đầu.
> 2. **Kiến trúc đơn giản, chi phí thấp:** lõi xử lý là Rule/State-Machine (đã được kiểm chứng ở nhiều bãi xe thông minh khác), lớp LLM chỉ đóng vai trò diễn giải dữ liệu thành hướng dẫn tự nhiên — không cần Agentic Loop tốn kém và khó kiểm soát.
> 3. **Rủi ro nằm trong tầm kiểm soát:** cơ chế Fallback (quay về hiển thị theo tầng) đảm bảo trải nghiệm khách không bị tệ hơn hiện tại ngay cả khi hệ thống mới gặp lỗi; AI hoàn toàn không có quyền điều khiển thiết bị vật lý (barrier, đèn tín hiệu) nên không phát sinh rủi ro an toàn.
> 4. **Metric rõ ràng và đo lường được:** thời gian tìm chỗ đỗ và độ chính xác hiển thị đều có thể đo trực tiếp qua dữ liệu cảm biến hiện có, giúp đánh giá khách quan sau giai đoạn pilot trước khi quyết định nhân rộng ra toàn bộ hệ thống TTTM Vincom.
