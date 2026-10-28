# CS420 S07 — Retrieval-Augmented Generation

Seminar tiếng Việt về truy xuất tài liệu và kiểm chứng câu trả lời. Bộ thử nghiệm tiếng Anh dùng bài **abess: A Fast Best-Subset Selection Library in Python and R**, Zhu et al. (2022), 7 trang, **CC BY 4.0**.

## Thành phần

**Báo cáo đã biên dịch:** [PDF 9 trang (8 trang nội dung + 1 trang tham khảo)](report/main.pdf). **Slide chỉnh sửa trên Canva:** https://canva.link/abw5shp7wrkofnm

- `report/main.tex`: báo cáo LaTeX, biên dịch bằng XeLaTeX.
- `slides/`: nội dung slide, ghi chú thuyết trình và liên kết Canva.
- `data/questions.json`: 20 câu hỏi, đáp án tham chiếu, trang và đoạn bằng chứng.
- `data/sources/`: PDF nguồn, giấy phép và mã kiểm tra SHA-256.
- `src/`: chuẩn bị dữ liệu, truy xuất TF-IDF/embedding và sinh câu trả lời Gemini.
- `results/`: kết quả thực đo và nhật ký từng câu; không phải kết quả chép từ paper.
- `docs/`: phương pháp đánh giá, câu hỏi phản biện, phân công và checklist.
- `RAG/`: mã dự án ban đầu của nhóm, làm cơ sở cho cách dùng MiniLM/Gemini. Pipeline đánh giá chuẩn ở `src/`.

## Chạy lại

Python 3.11 trở lên. Tạo môi trường riêng:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.prepare
.\.venv\Scripts\python.exe -m src.experiment
```

Lần đầu embedding sẽ tải `sentence-transformers/all-MiniLM-L6-v2`. Nếu đã có cache, thêm `--offline` vào lệnh cuối. Máy đang chuẩn bị bài có thể dùng `RAG\.venv\Scripts\python.exe` thay cho `.venv\Scripts\python.exe`.

Hai phương pháp dùng cùng chunk 96/192 **WordPiece token**, overlap 24, cosine similarity, k=1/3/5. Tìm chính xác trên toàn bộ chunk, không dùng chỉ mục xấp xỉ. Điểm cosine càng cao càng tương đồng; không được đọc nó như xác suất câu trả lời đúng.

## Gemini

Tạo `.env` theo `.env.example`, đặt key miễn phí của chính bạn. Nếu `.env` ở gốc không có, chương trình dùng `RAG/.env`. Key không được ghi vào kết quả hay Git.

```powershell
.\.venv\Scripts\python.exe -m src.generate --limit 60 --delay 10
```

Mỗi câu có ba lượt độc lập: closed-book, TF-IDF RAG, embedding RAG. Cấu hình RAG cố định trước khi xem kết quả: 192 token, k=3. Mỗi lượt có temperature=0, tối đa 2048 output token. Chương trình ghi từng kết quả vào JSONL, bỏ qua lượt đã thành công khi chạy lại, và dừng nếu có lỗi API/quota. `--limit` giới hạn lượt mới, không phải số câu hỏi. Không tự chuyển sang gói trả phí.

Không sửa model giữa một phép so sánh. Model thí nghiệm: `gemini-3.5-flash-lite`; 3.8 bị timeout và 2.5 Flash-Lite bị Google từ chối cho người dùng mới. Không coi các lần lỗi là câu trả lời sai.

## Biên dịch báo cáo

```powershell
cd report
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Dùng XeLaTeX với Times New Roman. Khi dùng Overleaf/Linux chưa có font này, đổi sang font hỗ trợ tiếng Việt như TeX Gyre Termes. Kết quả thực nghiệm được đưa vào `report/retrieval_table.tex` và `report/generation_results.tex`.

## Cộng tác

Repo private: https://github.com/Khoaphan-hub/seminar-rag

Chủ repo thêm thành viên ở **Settings → Collaborators → Add people**. Mỗi bạn tạo nhánh riêng, ví dụ `report-review`, `slides-review`, `evaluation-review`, rồi mở pull request để ghép bài. Chỉ một người cập nhật số liệu sinh tự động mỗi lần. Trước khi nộp, ba thành viên cần đọc lại đáp án và tự luyện trình bày/hỏi đáp.

Không commit `.env`, môi trường Python, model weights, vectorstore hoặc dữ liệu cá nhân. PDF đề và hai paper giáo viên cung cấp vẫn giữ tại máy; repo lưu thông tin trích dẫn thay vì tự cấp lại giấy phép cho các tài liệu đó.

## Giới hạn

Đã hoàn tất 240 cấu hình truy xuất theo câu hỏi (20 × 2 phương pháp × 2 kích thước × 3 giá trị k) và 60 câu trả lời Gemini chính thức. Chấm có AI hỗ trợ cho thấy số câu trả lời đầy đủ lần lượt là 5/20 (closed-book), 16/20 (TF-IDF) và 14/20 (MiniLM); nhóm cần kiểm tra độc lập nhãn trong `results/answer_review.csv`. `generation_pilot.jsonl` là lượt thử ban đầu, đã loại khỏi kết quả vì prompt baseline chưa có cùng metadata nhận diện paper.

20 câu hỏi do người chuẩn bị chủ động thiết kế, một paper, một embedding nhỏ, một lần sinh mỗi điều kiện. Gold là tập đoạn tham chiếu đã chọn, không bao quát mọi diễn đạt tương đương trong paper. Các tỷ lệ truy xuất không phải accuracy của LLM. Không suy rộng kết quả thành thứ hạng chung giữa TF-IDF và embedding.

Xem `THIRD_PARTY_NOTICES.md` và `docs/AI_DISCLOSURE.md` để biết nguồn và việc sử dụng AI.
