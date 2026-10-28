# Quy ước đánh giá

## Retrieval

Q01–Q20 là 20 câu hỏi có đáp án trong paper. Viết câu hỏi, đáp án và gold evidence trước khi chạy xếp hạng. Không đưa đáp án hay câu hỏi vào corpus. Khung 2 phương pháp × 2 kích thước × 3 giá trị k được áp dụng đồng nhất.

Gold evidence là một hoặc nhiều khoảng ký tự trong bản text chuẩn hóa, được xác minh bằng phép so khớp chính xác. Một chunk relevant theo nhãn này nếu chứa trọn ít nhất một khoảng bằng chứng. Recall@k = số chunk relevant trong top-k / tổng số chunk relevant. Báo cáo lấy trung bình theo câu hỏi. Số lượng relevant có thể đổi theo chunk size, vì vậy báo cáo thêm các chỉ số ở cấp bằng chứng:

- Hit@k: có lấy được trọn ít nhất một đoạn bằng chứng không.
- Evidence recall@k: tỷ lệ các đoạn bằng chứng tham chiếu được phủ đầy đủ bởi hợp các chunk trong top-k.
- All-evidence@k: có phủ đủ toàn bộ đoạn bằng chứng cần cho câu hỏi không.

Gold là tập bằng chứng được chọn, không phải toàn bộ các diễn đạt tương đương. Ví dụ thông tin PyPI/CRAN xuất hiện cả trang 1 lẫn trang 2; việc không lấy đúng đoạn đã gán nhãn không luôn đồng nghĩa thiếu thông tin. Vì vậy đánh giá câu trả lời phải đọc cả context thật sự và PDF, không suy ra nhãn đúng/sai từ Recall. Overlap cũng tạo nhiều chunk chứa cùng một fact và có thể làm chunk recall thấp dù đã đủ bằng chứng. Bộ nhãn lưu nguyên để tái lập, không sửa theo phương pháp có kết quả tốt hơn.

## Generation

Ba điều kiện: không context, context TF-IDF, context embedding. Cùng 20 câu hỏi, cùng model và temperature. Mọi điều kiện đều nhận tên bài, Jin Zhu et al., năm 2022 và JMLR 23, 1–7 để không phạt baseline vì thiếu nhận diện paper. Hai RAG cùng chunk=192, k=3, prompt giống nhau ngoài các đoạn context. Prompt closed-book cho phép dùng kiến thức sẵn có và yêu cầu nói không biết khi không chắc, không giả vờ đã tra nguồn. Mỗi lượt là hội thoại độc lập; xoay thứ tự ba điều kiện theo câu. `generation_pilot.jsonl` là lượt thử trước khi thêm metadata nhận diện paper, bị loại khỏi kết quả chính.

Chấm mỗi câu trên ba trục tách biệt:

1. **Correctness**: 1 nếu trả lời đầy đủ đúng các ý cốt lõi trong reference; 0.5 nếu chỉ có một phần ý cần thiết, diễn đạt còn quá rộng hoặc thêm giải thích thiếu chính xác nhưng vẫn thể hiện phần trọng tâm; 0 nếu dữ kiện đích sai (chẳng hạn phiên bản, con số, tên class), không trả lời hoặc từ chối. Đây là rubric có phán đoán; xem lý do từng mẫu trong `answer_review.csv`. Từ chối có thể an toàn nhưng không phải đáp án đúng cho câu vốn có đáp án.
2. **Groundedness** (hai nhánh RAG): mọi khẳng định thực tế có được context đã đưa vào hỗ trợ không. Kiến thức đúng nhưng ngoài context vẫn là vượt bằng chứng. Từ chối hoàn toàn ghi `abstain`, không cộng như một câu factual đúng.
3. **Citation support** (hai nhánh RAG): ID được dẫn có tồn tại trong prompt và đúng chunk có hỗ trợ nhận định được gắn trích dẫn không. Chỉ kiểm tra regex không đủ để chứng minh support.

Người chấm phải ghi lý do cho nhãn, đọc response và context thực. Điểm có AI hỗ trợ không được gọi là đánh giá con người độc lập. Không lấy độ giống từ với reference làm tiêu chí correctness duy nhất.

## Phân loại lỗi

- Missing retrieval: không có đủ thông tin cần trong top-k.
- Incorrect retrieval: các đoạn trả về nói về nội dung khác, gần từ khóa nhưng không trả lời câu hỏi.
- Irrelevant citation: câu trả lời dẫn một chunk không chứng minh nội dung.
- Beyond evidence: bổ sung một thông tin không có trong context, kể cả khi thông tin đó đúng trong toàn PDF.

Một mẫu có thể thuộc nhiều nhóm. Trường hợp tạo có chủ đích để minh họa phải ghi rõ là tình huống giả lập, không được đếm như lỗi model thực đo.
