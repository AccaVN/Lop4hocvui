# Học Vui Lớp 4 — 1 repo, 1 project Vercel (Neon)

> Bản lớp 4, bám theo bộ sách **Kết nối tri thức với cuộc sống** (Toán 4, Tiếng Việt 4)
> và **Tiếng Anh 4 Global Success**. Câu hỏi và bài đọc được soạn mới theo từng bài/chủ điểm
> của sách (không chép nguyên văn sách).
>
> - **Toán**: 8 chặng × 6 bài — ôn tập số đến 100 000, số chẵn – số lẻ, biểu thức chứa chữ, bài toán ba bước;
>   góc nhọn – tù – bẹt; số có nhiều chữ số, hàng và lớp, lớp triệu, làm tròn; yến – tạ – tấn, dm² – m² – mm², giây – thế kỉ;
>   cộng trừ số có nhiều chữ số, tính chất phép cộng, tổng – hiệu; vuông góc, song song, hình bình hành, hình thoi;
>   nhân chia với số có một, hai chữ số, nhân chia với 10, 100, 1 000, tính chất phép nhân; trung bình cộng, rút về đơn vị,
>   biểu đồ cột, số lần xuất hiện của sự kiện; phân số (rút gọn, quy đồng, so sánh) và cộng – trừ – nhân – chia phân số.
> - **Tiếng Việt**: 16 chặng × 3 bài (Đọc hiểu · Luyện từ, chính tả · Luyện câu, dấu câu), theo 8 chủ điểm:
>   Mỗi người một vẻ, Trải nghiệm và khám phá, Niềm vui sáng tạo, Chắp cánh ước mơ (Tập 1);
>   Sống để yêu thương, Uống nước nhớ nguồn, Quê hương trong tôi, Vì một thế giới bình yên (Tập 2).
>   Luyện từ và câu: danh từ, động từ, tính từ, nhân hoá, viết hoa tên riêng, dấu gạch ngang, chủ ngữ – vị ngữ, trạng ngữ, dấu ngoặc kép, ngoặc đơn.
> - **English**: 16 bài phủ 20 unit của Tiếng Anh 4 (gộp Unit 7–8, 14–15, 16–17, 19–20), mỗi bài 3 phần
>   Vocabulary · Listening · Sentences (có hỏi – đáp theo mẫu câu của unit), đề song ngữ Anh – Việt.
> - Ngân hàng: Toán 20 câu/bài, Tiếng Việt và English 15 câu/bài; mỗi lượt chơi lấy ngẫu nhiên 10 câu (tổng 2.400 câu).
> - Phân số hiển thị dạng tử/mẫu chồng lên nhau; số nhiều chữ số được viết theo nhóm 3 chữ số (123 456 789);
>   ô nhập đáp số nhận tới 9 chữ số.
> - Nên dùng **database Neon và project Vercel riêng** cho bản lớp 4.
>   Trình duyệt lưu dữ liệu với khóa `lop4_hoc_vui_v1`, `hv4_token` nên không lẫn với app lớp 1, 2, 3.
> - Giọng đọc: mặc định dùng giọng chuẩn qua mạng (admin chọn 1 giọng nữ + 1 giọng nam); mất mạng thì tự dùng giọng của
>   thiết bị hoặc giọng thu sẵn (`voice-data.json`). Máy đọc đúng phân số (“3 phần 4”), số lớn, m², độ.
> - Muốn sửa/thêm câu hỏi: xem `tools/gen-lop4/` (Python), sửa dữ liệu (`m4a.py`, `m4b.py` Toán, `tv4a–tv4d.py` Tiếng Việt,
>   `en4.py` English) rồi chạy `cd tools/gen-lop4 && python3 update_banks.py` (ghi thẳng vào `public/index.html`).
>   `python3 check_m4.py` tự tính lại và kiểm tra toàn bộ đáp án Toán.

Toàn bộ app (frontend + backend) nằm trong **1 thư mục duy nhất**, deploy bằng **1 project
Vercel duy nhất** — Vercel tự nhận diện: các file trong `public/` là trang web tĩnh, các file
trong `api/` là backend (serverless function). Không cần 2 project, không cần cấu hình CORS
thủ công vì frontend và backend chung 1 domain.

```
hocvui-monorepo/
├── public/
│   ├── index.html        ← app (giao diện + toàn bộ logic học tập)
│   └── voice-data.json    ← dữ liệu âm thanh (tải nền, tách riêng cho nhẹ trang)
├── api/
│   └── index.js           ← cửa vào cho toàn bộ API (Vercel gọi file này)
├── src/                   ← code backend thật (routes, db, auth...)
├── schema.sql              ← chạy 1 lần trên Neon để tạo bảng
├── scripts/create-admin.js
├── server.js               ← chỉ dùng khi chạy thử ở máy local
└── vercel.json              ← nói cho Vercel biết cái nào là web, cái nào là API
```

## 1. Tạo database trên Neon

1. Tạo project mới tại https://neon.tech
2. Vào **SQL Editor**, dán toàn bộ nội dung `schema.sql` và chạy 1 lần.
3. Vào **Connection Details**, copy connection string dạng **pooled connection**
   (`...-pooler...neon.tech...`) — dùng cho `DATABASE_URL` ở bước sau.

## 2. Đẩy lên GitHub (1 repo duy nhất)

Từ thư mục `hocvui-monorepo` này:
```bash
git init
git add .
git commit -m "init"
git remote add origin https://github.com/AccaVN/Lop4hocvui.git
git push -u origin main
```

## 3. Deploy lên Vercel

1. Vào https://vercel.com, đăng nhập bằng GitHub.
2. **Add New > Project**, chọn repo vừa đẩy lên. Vercel tự đọc `vercel.json`, không cần
   chỉnh Build Command hay Output Directory gì cả.
3. Thêm biến môi trường (**Environment Variables**):
   - `DATABASE_URL` = chuỗi pooled connection từ Neon (bước 1)
   - `JWT_SECRET` = chuỗi ngẫu nhiên dài (tạo bằng `openssl rand -hex 32`, hoặc dùng trang
     randomkeygen.com nếu không có terminal)
4. Bấm **Deploy**. Xong sẽ có 1 URL duy nhất, ví dụ `https://hocvui4-honghoa.vercel.app`
   — mở URL đó là vào thẳng app, API cũng nằm sẵn dưới `/api/...` trên cùng URL này.

Từ giờ, mỗi lần sửa gì (frontend hay backend) chỉ cần `git push` — Vercel tự deploy lại
đúng phần đã đổi.

**Không cần sửa `API_BASE` trong `public/index.html`** — đã để sẵn `/api` (đường dẫn tương
đối), tự động trỏ đúng vào backend vì cùng domain.

## 4. Tạo tài khoản admin đầu tiên

Không có route tự đăng ký admin (tránh ai đó tự tạo quyền admin qua API công khai).

**Cách nhanh nhất — chèn thẳng qua Neon SQL Editor** (không cần cài gì, đổi email/mật khẩu trước khi chạy):
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
INSERT INTO users (email, password_hash, role, display_name)
VALUES ('admin@hocvui4.vn', crypt('MatKhauAdmin123', gen_salt('bf', 10)), 'admin', 'Quản trị')
ON CONFLICT (email) DO UPDATE SET password_hash = EXCLUDED.password_hash, role = 'admin';
```

**Hoặc chạy script** từ máy có Node, trỏ `DATABASE_URL` vào Neon:
```bash
DATABASE_URL="postgres://..." node scripts/create-admin.js admin@cafe.vn mat_khau_manh
```

## 5. Luồng nghiệp vụ

- **Học sinh** tự đăng ký (`/api/auth/register/student`) → hệ thống tạo hồ sơ `students`
  kèm `join_code` (mã nội bộ, không còn dùng để liên kết phụ huynh).
- **Không còn tài khoản phụ huynh (10/2026).** Bố mẹ xem kết quả của con ở mục **👪 Phụ huynh** trên máy của con
  (có phép nhân để trẻ không tự vào). Tài khoản phụ huynh cũ được tự chuyển thành tài khoản học sinh
  (giữ email, mật khẩu); đăng ký và admin chỉ tạo được tài khoản học sinh/admin.
- **Admin** xem được toàn bộ học sinh qua `/api/admin/*`.

## 6. API tóm tắt

| Method | Endpoint | Ai gọi | Mô tả |
|---|---|---|---|
| POST | `/api/auth/register/student` | công khai | Đăng ký học sinh (trả về `join_code`) |
| POST | `/api/auth/login` | công khai | Đăng nhập, trả JWT |
| GET | `/api/auth/me` | đã đăng nhập | Thông tin token hiện tại |
| GET | `/api/student/me` | học sinh | Toàn bộ tiến độ/kỹ năng/phiên học của bản thân |
| PUT | `/api/student/me/profile` | học sinh | Cập nhật tên/nhân vật/giới tính |
| POST | `/api/student/me/attempt` | học sinh | Nộp kết quả 1 lần làm bài — thay kết quả lần trước (chỉ tính lần cuối) |
| POST | `/api/student/me/speak` | học sinh | Lưu sao luyện nói từng từ/câu (chỉ cộng khi tốt hơn) |
| GET | `/api/student/me/report` | học sinh | Báo cáo học tập (mục Phụ huynh trên máy của con) |
| PUT | `/api/student/me/progress` | học sinh | (Cũ) Lưu số sao 1 bài `{level_key, stars}` |
| POST | `/api/student/me/skill` | học sinh | Cộng dồn đúng/sai theo kỹ năng |
| POST | `/api/student/me/session` | học sinh | Cộng dồn thời gian học trong ngày (giây) |
| GET | `/api/admin/students` | admin | Toàn bộ học sinh + tổng sao |
| GET | `/api/admin/students/:id` | admin | Chi tiết 1 học sinh + danh sách phụ huynh |
| GET | `/api/admin/parents` | admin | Toàn bộ phụ huynh + số con |

Mọi route trừ `register`/`login` cần header: `Authorization: Bearer <token>`.

## 7. Chạy thử ở máy local (tuỳ chọn)

Chỉ test riêng backend:
```bash
npm install
DATABASE_URL="..." JWT_SECRET="..." npm start
```
rồi mở `public/index.html` trực tiếp trong trình duyệt và sửa tạm `API_BASE` thành
`http://localhost:4000/api` (đổi lại `/api` trước khi đẩy lên Vercel).

Muốn giả lập đúng như Vercel thật (frontend + API cùng domain) thì dùng:
```bash
npm install -g vercel
vercel dev
```

## Tính năng (đồng bộ từ Học Vui Lớp 2 / Lớp 3)

**Không cần chạy SQL thủ công** — khi deploy, backend tự thêm cột/bảng mới (`src/db.js` → `ensureSchema`):
`users.display_name`, `student_rewards.en_stickers`, bảng `app_settings`.

- **Sticker**: ảnh nằm trong `public/stickers/{nhan-vat,xe-co,cua-hang}/*.webp`. Món nào chưa có ảnh vẫn hiển thị emoji
  theo kiểu sticker cắt dán viền trắng.
- **Sticker Xe cộ** giờ được lưu vào database (`student_rewards.en_stickers`), và tự bù lại từ các bài English đã đạt sao.
- **Tài khoản**: Quản trị → Tài khoản → *Sửa* để đổi tên / email / đặt mật khẩu mới cho mọi tài khoản (kể cả admin).
  Mọi người cũng tự đổi được mật khẩu của mình (API `PUT /api/auth/me`).
- **Giọng đọc**: `GET /api/tts?v=<giọng>&t=<câu>` trả về mp3, CDN Vercel lưu 1 năm. Admin chọn 1 giọng nữ + 1 giọng nam
  ở Quản trị → Giọng đọc; học sinh chọn *Giọng cô* / *Giọng thầy*. Mất mạng → tự dùng giọng thiết bị / giọng thu sẵn.
  Biến môi trường tùy chọn: `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`, `GOOGLE_TTS_API_KEY` (xem `.env.example`).
- **Bảng xếp hạng cả lớp**: tab Thành tích → Hạng (học sinh), Góc phụ huynh, và Quản trị. Đã xóa tính năng "Thu mã điểm".

Chạy thử ở máy: `npm install` → tạo `.env` (DATABASE_URL, JWT_SECRET) → `npm start` → mở http://localhost:4000

- **Tốc độ**: mục Thành tích hiện ngay từ dữ liệu trên máy rồi cập nhật nền; dữ liệu Thành tích được tải trước khi máy rảnh;
  file giọng thu sẵn tải sau khi trang đã hiện; mỗi API Thành tích chỉ 1 truy vấn tới Neon.
- **Đổi mật khẩu**: dùng `PUT /api/auth/me` (thay cho `POST /api/auth/change-password` cũ).

## Giao diện & bài tập kiểu Duolingo

Lớp giao diện/bài tập kiểu Duolingo nằm trong `tools/duolingo/duolingo.js` và được chèn vào cuối `public/index.html`
(giữa hai dòng `<!--DUO:START-->` … `<!--DUO:END-->`). Sửa file nguồn rồi chạy lại để cập nhật:

```bash
python3 tools/duolingo/inject.py public/index.html
```

- **Giao diện**: thanh tiến độ xanh, `COMBO xN` (vàng từ x5), ô chọn, thanh phản hồi xanh/đỏ, nút bấm viết hoa giống Duolingo.
- **Dạng bài mới cho tiếng Anh** (tự trộn vào mỗi bài English, tối đa 3 câu/bài, thay một số câu trắc nghiệm):
  - *Nối cặp* (“Nhấn vào các cặp tương ứng”): từ ↔ nghĩa, nghe 🔊 ↔ hình, câu ↔ nghĩa. Sai tối đa 1 lần vẫn tính đúng.
  - *Gõ lại* (từ 1 trở lên, Lớp Lá không có vì bé chưa biết gõ): nhìn hình/nghĩa gõ từ tiếng Anh, hoặc nghe rồi gõ.
  - *Dịch câu* bằng các từ cho sẵn kèm từ gây nhiễu (từ lớp 1).
- **Làm lại câu sai**: hết bài, các câu làm sai (Toán, Chữ cái, English) được hỏi lại; câu nào vẫn sai thì sang vòng
  tiếp theo, đến khi đúng hết mới hiện kết quả. Sao/điểm/xu/thống kê chỉ tính theo **lần làm đầu tiên**; vòng ôn lại không
  cộng điểm. Không áp dụng cho Luyện đề thi và Luyện nói.

## Cập nhật 20/10/2026 — Toán tư duy, thẻ kiến thức, ôn tập thông minh

Lớp tính năng dùng chung cho cả 6 app Học Vui, nằm ở `tools/hocthem/` (nguồn trong `src/*.js`) và được chèn
vào `public/index.html` giữa `<!--HT:START-->` … `<!--HT:END-->`, ngay trước khối Duolingo. Sửa nguồn rồi chạy:

```bash
python3 tools/hocthem/inject.py public/index.html   # tự ghép src/*.js thành hocthem.js rồi chèn
node tools/hocthem/test/gen_test.js 500             # kiểm thử bộ sinh đề (giải lại đáp án độc lập)
```

- **🧩 Tab Toán tư duy**: 7 nhóm (Quy luật, Đếm và tổ hợp, Suy luận lô-gic, Sơ đồ đoạn thẳng, Tính ngược và thử chọn,
  Hình và không gian, Tính nhanh) — 21 bài, Lớp Lá có 6 bài riêng. Đề máy tự sinh theo lớp, mỗi bài 10 câu
  (4 cơ bản, 4 vận dụng, 2 nâng cao), có hình vẽ (sơ đồ đoạn thẳng, hình ghép ô vuông, khối lập phương…),
  dạng kéo số vào ô, gợi ý nhiều bước. Điểm lưu vào `progress` với `level_key = td_<số bài>`, tính vào điểm tích lũy.
- **⭐ Thử thách hôm nay**: 1 câu đố mỗi ngày, +4 xu nếu đúng ngay lần đầu.
- **📘 Thẻ kiến thức** cho Toán (theo nội dung câu hỏi) và Tư duy: mở từ trang chủ, khi xem gợi ý, hoặc khi làm sai.
- **💡 Gợi ý** khi làm bài Toán/Tư duy (xem gợi ý thì câu đó không được xu “đúng ngay lần đầu”).
- **⚑ Báo câu sai**: học sinh gửi, admin xem ở Quản trị → ⚑ Báo lỗi (bảng `question_reports`, tự tạo).
- **Ôn câu sai bằng câu cùng dạng nhưng đổi số** (bài Tư duy sinh câu mới; bài Toán lấy câu cùng kỹ năng trong ngân hàng đề).
- **🔁 Cần ôn lại**: bài làm dưới 80% được nhắc ôn sau 1 – 3 – 7 ngày, hiện trên trang chủ Toán và trang Tư duy.
- **Góc phụ huynh**: Nhận xét tuần, Dạng bài con hay sai (đã sửa/chưa sửa), mục tiêu phút mỗi ngày,
  🎁 Phần thưởng do bố mẹ đặt — con đổi bằng xu ở Thành tích → 🎁 Quà (cần học ≥ 3/7 ngày, bố mẹ xác nhận).
- **Bảng xếp hạng**: thêm “Tuần này” (điểm các bài làm trong tuần) và “Chăm chỉ” (số ngày học trong tháng, chuỗi ngày).
- API mới ở `src/routes/extra.js` (gắn `/api/x`): `POST /x/student/report`, `GET|PUT /x/student/gifts`,
  `GET /x/student/rank2`, `GET|PUT|DELETE /x/admin/reports`. Bảng/cột mới tự tạo khi chạy, **không cần chạy SQL tay**.
