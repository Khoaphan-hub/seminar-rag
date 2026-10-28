# Kịch bản và phân công

Thay Người A/B/C bằng tên nhóm khi đã thống nhất. Đây là đề xuất phân công, chưa xác nhận tên người trình bày.

| Người | Slide | Thời gian | Việc cần kiểm tra |
|---|---|---|---|
| A | 1–4 | 5 phút | Câu hỏi nghiên cứu, hai loại memory, pipeline, paper và công thức |
| B | 5–8 | 5 phút | Corpus/license, hai retriever, metrics, bảng kết quả |
| C | 9–12 | 5 phút | Ví dụ generation, lỗi, verification, kết luận |

Mỗi người cần trả lời ít nhất một câu trong 5 phút hỏi đáp. Tập chạy demo trước và mở sẵn nhật ký đã lưu khi API miễn phí không khả dụng tại lớp.

# Câu hỏi phản biện và ý trả lời

1. **RAG có loại bỏ hallucination không?** Không có bảo đảm. Lỗi có thể do nguồn, retrieval, prompt, generation hoặc citation. Thí nghiệm nhỏ chỉ minh họa các cơ chế, không đo được toàn bộ các dạng hallucination.
2. **Vì sao TF-IDF tốt hơn MiniLM ở bộ thử này?** Các câu hỏi có nhiều tên API và thuật ngữ trùng paper; MiniLM nhỏ và không được fine-tune cho corpus. Đây là diễn giải hợp lý, chưa phải kết luận nhân quả. Muốn kiểm chứng phải có bộ paraphrase độc lập và thêm model.
3. **TF-IDF cũng dùng cosine à?** Có. Vector TF-IDF thưa và embedding đặc đều có thể so bằng cosine; khác nhau ở cách biểu diễn.
4. **Tại sao chunk theo token?** Để kiểm soát đầu vào embedding 256 token; 96/192 cộng token đặc biệt đều không bị cắt. Token ở đây theo tokenizer MiniLM, không phải số ký tự hay token tính phí Gemini.
5. **Recall@k có phải accuracy không?** Không. Recall đo truy xuất theo tập relevant. Accuracy đo nội dung câu trả lời. Còn groundedness đo sự hỗ trợ của context.
6. **Nếu tăng k có luôn tốt hơn?** Retrieval recall không giảm khi top-k lồng nhau, nhưng generation có thể bị nhiễu và tốn context hơn. Thí nghiệm sinh chỉ cố định k=3 nên chưa kết luận về ảnh hưởng k lên generation.
7. **Vì sao RAG-Sequence khác việc nối ba chunk vào prompt?** RAG-Sequence trong paper cộng xác suất của toàn chuỗi theo các tài liệu tiềm ẩn; demo chỉ nối context rồi gọi API. Không có truy cập xác suất chuỗi để tái hiện phép marginalization.
8. **RAG-Token có tìm kiếm lại ở mỗi token không?** Công thức cho phép tài liệu tiềm ẩn thay đổi theo token trong tập top-k đã truy xuất. Không có nghĩa bắt buộc chạy lại tìm kiếm mỗi token.
9. **RAG có thể fine-tune không?** Có. Paper gốc huấn luyện query encoder và generator; giữ document encoder/index cố định. Demo dùng retriever và generator sẵn có.
10. **Non-parametric có nghĩa retriever không có tham số?** Không. Kho kiến thức ngoài trọng số là non-parametric memory; query/document encoder vẫn có tham số học được.
11. **Vì sao giấy phép paper khác thư viện?** CC BY 4.0 cho bài abess; GPL-3 cho source code abess. Corpus là bài nghiên cứu, không phải mã thư viện.
12. **Có data leakage không?** Không đưa câu hỏi/reference vào index. Tuy nhiên paper công khai có thể đã ở dữ liệu huấn luyện LLM; không kiểm soát được. Vì vậy closed-book là baseline thực dụng, không phải phép đo kiến thức hoàn toàn chưa thấy.
13. **Gold có đầy đủ không?** Chỉ gán một tập đoạn bằng chứng tham chiếu. Các đoạn tương đương có thể bị bỏ sót; ghi nhận đây là hạn chế và đọc context thủ công khi chấm generation.
14. **Tại sao không dùng Chroma cũ?** Corpus chỉ vài chục chunk, tìm toàn bộ bằng tích vô hướng chuẩn hóa là đủ và dễ kiểm tra cosine. Không đánh đồng distance mặc định của vectorstore cũ với cosine.
15. **Cập nhật tài liệu ra sao?** Lưu version/hash; phát hiện file đổi; trích xuất/chunk/index lại; chạy regression set; kiểm tra citation còn trỏ đúng trang/đoạn. Với câu hỏi lịch sử phải giữ snapshot 2022.
16. **Ví dụ số RAG-Sequence lấy từ model không?** Không. Là số giả định phục vụ giải thích phương trình; log API không trả các xác suất điều kiện đó.
17. **Ai chấm câu trả lời?** Có AI hỗ trợ đối chiếu trực tiếp nguồn; chưa có đánh giá mù bởi nhiều người. Các thành viên cần kiểm tra lại nhãn trước khi nộp.
18. **Có thể nói model không có hallucination nếu 20/20 đúng?** Không. Chỉ nói không quan sát lỗi theo rubric trên 20 mẫu ở lần chạy này; không chứng minh bảo đảm cho câu hỏi khác.
