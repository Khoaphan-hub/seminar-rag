# Đối chiếu yêu cầu S07

| Yêu cầu | Vị trí |
|---|---|
| Parametric/non-parametric; RAG vs fine-tuning/toàn prompt | report/main.tex, phần Background |
| Pipeline và lỗi mỗi stage | Background, phân tích lỗi |
| Corpus5–10trang có nguồn phù hợp | data/sources/abess_2022.pdf,7trang,CCBY4.0 |
| 15–20câu có reference và nguồn | data/questions.json,20câu |
| Retrieval và >=2chunksize hoặc2k | src/experiment.py,2methods×2sizes×3k |
| Bảng Recall@k | results/retrieval_summary.csv,report/retrieval_table.tex |
| Có/khôngretrieval cùngcâu | results/generation.jsonl,60response chính thức |
| Định nghĩa mọi ký hiệu/giả định/ví dụ số | report/main.tex,Method |
| Ví dụ question→chunks→answer/citation | Q08 trong report và slide9 |
| >=3failure | Q06,Q13,Q09; thêmQ14,Q15 ở generation |
| Verification và cập nhật nguồn | report/phần kiểm chứng và kết luận |
| Paper Required,so sánhSequence/Token | report/Background vàMethod |
| Báo cáo tiếngViệt,A4,6–10trang nội dung | report/main.tex vàPDF đãbiên dịch |
| 8–12slide nội dung,15phút | bộCanva12slide vàslides/speaker_notes.md |
| Q&A5phút,mỗingườitrảlời>=1câu | docs/PRESENTATION_AND_QA.md |
| Tríchnguồn dữliệu,hình,bảng,phươngtrình,AI | bibliography,caption,THIRD_PARTY_NOTICES,AI_DISCLOSURE |

## Nhóm cần hoàn tất trước khi nộp

- Điền tên/MSSV thành viên nếu lớp yêu cầu; hiện chưa có thông tin này.
- Kiểm tra độc lập nhãn trong answer_review.csv, đặc biệt các mẫu điểm0,5 và inference_from_URL.
- Tập đủ15phút và chia phần hỏiđáp để cả3người đều thamgia.
- Xác nhận hạn nộp,kênh nộp,tênfile theo thông báo riêng của cô; PDFđề không ghi ngày cụ thể.
- Repo/private vàCanva cần chủ sở hữu mời đúng các bạn cùngnhóm. Không gửi APIkey khi mời cộngtác.
