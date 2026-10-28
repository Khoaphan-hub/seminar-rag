# Nội dung cuối cùng của slide Canva

Bản trích văn bản ngày 28/10/2026 sau khi lưu các sửa đổi đã duyệt. Phần hình/biểu đồ xem trong [Canva](https://canva.link/abw5shp7wrkofnm). Ghi chú thuyết trình ở `speaker_notes.md`.

RAG có loại bỏ hallucination?
Câu hỏi nghiên cứu • CS420 S07 — RAG và kiểm chứng bằng chứng
RAG có thể truy xuất đúng tài liệu — nhưng câu trả lời có đúng, có căn cứ và có thể kiểm chứng không?

Kiểm chứng bằng chứng là lớp bảo vệ sau sinh: đối chiếu từng claim với nguồn, metadata và phạm vi hỗ trợ thực sự.
RETRIEVALTruy xuất
CORRECTNESSĐộ chính xác
GROUNDINGCăn cứ
Lewis et al., NeurIPS 2020; Schneider 2024, DOI 10.1007/s10462-024-10916-x
Parametric memory ↔ Non-parametric memory

Trọng số mô hình (weights)Học mẫu, tri thức nén; cập nhật bằng huấn luyện.

Kho dữ liệu ngoài (external datastore)Có thể cập nhật, truy vết và trích dẫn.

PHƯƠNG PHÁP
TRI THỨC
CẬP NHẬT / DẪN NGUỒN
Fine-tuning
Trong weights
Tốn huấn luyện / khó trích dẫn
RAG
Datastore + weights
Nhanh / có evidence metadata
Toàn bộ tài liệu trong prompt
Context window
Đơn giản / dễ quá dài
Fine-tuning và RAG có thể kết hợp: một bên điều chỉnh hành vi, một bên cung cấp bằng chứng cập nhật.
Lewis et al., NeurIPS 2020; MiniLM model card
Từ PDF đến kiểm chứng: lỗi có thể xuất hiện ở mọi bước
Một pipeline tốt không chỉ sinh câu trả lời — nó lưu ID, trang và đường đi của bằng chứng.
PDFchuẩn hóa + chunk
Top-kTF-IDF / embedding
Promptcontext + ID + trang
Geminitrả lời
Kiểm chứngtừng claim

OCR / chunk sai

Truy xuất nhầm

Thiếu context

Suy diễn vượt nguồn

Citation ≠ support
Zhu et al., JMLR 2022; Gemini model documentation
RAG-Sequence và RAG-Token

RAG-SEQUENCE
p(y|x) ≈ Σ_z pη(z|x) · pθ(y|x,z)
Một tài liệu z được dùng cho toàn bộ chuỗi đầu ra.

RAG-TOKEN
p(y|x) ≈ ∏ᵢ Σ_z pη(z|x) · pθ(yᵢ|x,z,y<ᵢ)
Marginalization theo tài liệu được thực hiện ở từng token.
0,6 × 0,7 + 0,4 × 0,2 = 0,50
Ví dụ dùng số giả định. Đây là xác suất sinh, không phải xác suất trả lời đúng. Nối context không tái lập marginalization.
Lewis et al., NeurIPS 2020
Corpus abess — nhỏ, rõ nguồn, có gold

7
trang
4 trang nội dung3 trang tham khảo
20 câu tiếng Anhcó đáp án và gold tham chiếu

LICENSE
Bài báo: CC BY 4.0Code: GPL-3 — khác license bài báo

jmlr.org/papers/v23/21-1060.html
Zhu et al., JMLR 2022
TF-IDF hay MiniLM? Cùng cosine, khác biểu diễn

TF-IDF
Unigram + bigramVector thưa, khớp từ trực tiếpExact search

MiniLM-L6-v2
Embedding 384 chiềuVector dày, tương đồng ngữ nghĩaExact search

THIẾT LẬP CHUNG
Chunk 96 / 192 token  •  overlap 24  •  k = 1 / 3 / 5
81 chunks (96)  →  36 chunks (192)
Zhu et al., JMLR 2022; MiniLM model card
Recall@k đo khả năng tìm thấy evidence

Recall@k = | relevant ∩ top-k | / | relevant |

MACRO
Trung bình Recall@k trên 20 câu hỏi.

EVIDENCE RECALL
Evidence recall: tỷ lệ đoạn gold tìm được.All-evidence: tỷ lệ câu tìm đủ mọi đoạn gold.
Gold không exhaustive ⇒ recall truy xuất không đồng nghĩa answer accuracy.
Phương pháp nhóm • src/experiment.py • Gold là các đoạn tham chiếu đã chọn
Chunk 192: TF-IDF dẫn trước ở mọi k

k=1     0,450 / 0,400k=3     0,800 / 0,600k=5     0,900 / 0,725
Kết quả trên bộ 20 câu; không thể suy rộng cho corpus lớn hoặc miền khác.
Thí nghiệm nhóm • results/retrieval_summary.csv • n = 20
Q08: khi context và metadata cùng đúng

Câu hỏi về coverage của Python và R
s192-p2-t336  •  trang 2
97%
Python
96%
R

Gemini trả lời đúng 97% và 96%, dẫn đúng ID chunk; metadata trỏ đến trang 2.
Context mang con số; metadata giúp câu trả lời có thể truy vết.
Gemini model documentation; Zhu et al., JMLR 2022
60 responses: RAG cải thiện mạnh, chưa hoàn hảo
20 câu × 3 nhánh  •  temperature = 0  •  paper metadata  •  RAG 192 token, k=3

Closed-book
5/20 đầy đủ · 6/20 một phần
TF-IDF
16/20 đầy đủ · 2/20 một phần
MiniLM
14/20 đầy đủ · 3/20 một phần
Gemini 3.5 Flash-Lite. Đánh giá có AI hỗ trợ; chưa phải human evaluation độc lập.
Thí nghiệm nhóm • results/answer_review.csv • Chấm có AI hỗ trợ
Bốn lỗi thật — bốn kiểu thất bại khác nhau

Q06
TF-IDF
Thiếu version → từ chối trả lời

Q13
TF-IDF
Lấy kết luận, bỏ sót đoạn subclass Algorithm

Q14
MiniLM
Đúng print/coef/plot, thiếu citation

Q09
Cả hai
Thiếu một license; citation chưa chắc support
Bài học: retrieval đúng chưa đủ; câu trả lời phải đủ, đúng và được evidence hỗ trợ trực tiếp.
Thí nghiệm nhóm • results/generation.jsonl và answer_review.csv
RAG giảm rủi ro — không xóa hallucination
Kết luận
Mỗi claim cần một đường dẫn bằng chứng có thể tái lập.

GIỚI HẠN
20 câu · 1 paper · 1 embedding nhỏ · gold thiếu · 1 lượt model

01  Kiểm tra từng claim
02  Ghi version / hash
03  Rebuild + regression test
Disclosure: Codex hỗ trợ biên soạn và chấm điểm; Gemini là model thử nghiệm.
Lewis 2020; Schneider 2024; Zhu 2022; MiniLM model card
