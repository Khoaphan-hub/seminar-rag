# Ghi chú thuyết trình 15 phút

Mỗi người phụ trách 4 slide và khoảng 5 phút. Có thể đổi cách chia theo thế mạnh nhưng mọi người cần nói và trả lời ít nhất một câu. Dùng file này cùng bộ slide Canva; không đọc toàn văn báo cáo lên slide.

## 1 — RAG có loại bỏ hallucination (60 giây, Người A)

Mở bằng câu hỏi: nếu đã cho LLM tài liệu đúng, vì sao câu trả lời vẫn có thể sai? Bài này kiểm tra hai bước: hệ thống lấy được bằng chứng gì và model sử dụng bằng chứng ra sao. Ba tiêu chí cần tách là retrieval, correctness và grounding. Không nói “RAG làm LLM luôn đúng”. Giới thiệu phạm vi: một corpus mở và 20 câu hỏi; kết luận chỉ ở phạm vi minh họa đó.

## 2 — Hai loại bộ nhớ (75 giây, Người A)

Parametric là kiến thức lưu trong trọng số, còn non-parametric là kho ngoài truy xuất lúc hỏi. Nhấn mạnh retriever vẫn có model với tham số; “non-parametric” không có nghĩa toàn hệ thống không học. Fine-tuning thay đổi trọng số, đưa toàn bộ tài liệu vào prompt dùng context trực tiếp, RAG có bước chọn tài liệu. Ba cách không loại trừ nhau. Paper Lewis vừa dùng RAG vừa huấn luyện query encoder và BART. Demo không huấn luyện lại model.

## 3 — Pipeline (75 giây, Người A)

Đi qua nhánh chuẩn bị dữ liệu một lần và nhánh xử lý câu hỏi mỗi lượt. Metadata trang và ID được giữ từ đầu. Lỗi PDF/table có thể lan sang retrieval; chunk nhỏ có thể tách điều kiện; chunk dài tăng nhiễu. Sau top-k, chỉ những đoạn tìm được vào prompt. Generator trong demo không tự tìm toàn kho. Nếu thiếu bằng chứng thì chỉ dẫn yêu cầu nói thiếu thông tin. Cuối cùng kiểm tra cả nội dung lẫn trích dẫn.

## 4 — Công thức (90 giây, Người A)

Giải thích x, y, z, k, eta, theta. Trong Sequence, một tài liệu cố định bên trong mỗi nhánh xác suất của cả câu; sau đó cộng các nhánh. Token đổi vị trí phép tổng vào từng bước sinh. Không nói mỗi token bắt buộc query lại database. Tính lần lượt 0,42 và 0,08 rồi cộng 0,50. Các số là giả định minh họa, không lấy từ Gemini, và xác suất chuỗi không phải xác suất sự thật. Demo ghép nhiều chunk vào prompt không thực hiện marginalization như paper.

## 5 — Corpus và license (60 giây, Người B)

Giới thiệu abess, bài JMLR 2022 có 7 trang, trong đó 4 trang nội dung chính. Giữ ba trang bibliography để corpus phản ánh tài liệu PDF thực và có các đoạn gây nhiễu. Giấy phép CC BY 4.0 của article được in trang 1; mã phần mềm có GPL-3 là đối tượng khác. Bộ 20 câu có reference và gold span để kiểm chứng. Các câu hỏi lịch sử phải trả lời theo 2022, không theo bản phần mềm hiện nay.

## 6 — Hai retriever (90 giây, Người B)

TF-IDF dùng từ/ngram có trọng số; MiniLM dùng vector ngữ nghĩa 384 chiều. Cả hai có thể dùng cosine, nên cosine không phải đặc điểm riêng của dense retrieval. Dùng chung chunk96/192 WordPiece token, overlap24, tránh vượt giới hạn256token MiniLM. 81/36chunk đủ nhỏ để tính cosine toàn bộ. Không so sánh khoảng cách Chroma mặc định với cosine; mã thí nghiệm quy định rõ vector chuẩn hóa. Kích thước này khác số ký tự500 trong prototype cũ.

## 7 — Metrics (75 giây, Người B)

Recall@k là tỷ lệ chunk relevant tìm lại được, macro trên20câu. Một câu có hai fact, tìm được một thì hit=1 nhưng evidence recall=0,5 và all-evidence=0. Overlap và gold chưa đầy đủ gây khác biệt giữa các chỉ số. Q03 có PyPI/CRAN ở nhiều trang nên có thể trả lời đúng mà không trúng span đã chọn. Accuracy/đúng nội dung của generator cần chấm riêng, không đọc từ recall.

## 8 — Kết quả retrieval (75 giây, Người B)

Tập trung dòng192token,k3: Recall0,80 TF-IDF và0,60 MiniLM. Với k5 thành0,90 và0,725. TF-IDF tốt ở bộ này có thể vì nhiều thuật ngữ/API trùng câu hỏi. Chưa tách được tác động câu hỏi, model, corpus để kết luận nguyên nhân. Có câu dense tốt hơn, như Q06 vàQ13. Tăng k tăng recall trên top-k lồng nhau nhưng không chứng minh generation tốt hơn vì chưa thử sinh ở mọik.

## 9 — Ví dụ end-to-end (75 giây, Người C)

Đọc Q08 và cho xem chunk trang2 chứa coverage. Nêu đúng top3, không chọn lọc bỏ các đoạn gây nhiễu sau khi đã chạy. Response thực Gemini trả97%choPython,96%choR và dẫn s192-p2-t336. Kiểm tra ba thứ: hai số, thứ tự và nguồn. Có thể mở results/generation.jsonl khi demo để xem toàn prompt. Không cần gọi API live trước lớp nếu quota/mạng không ổn.

## 10 — So sánh generation (90 giây, Người C)

60response chính thức, cùng metadata nhận diện paper cho baseline để so sánh công bằng. Cả hai RAG192token,k3 cùng modelGemini3.5Flash-Lite. Số đúng đầy đủ5/20,16/20,14/20. Đúng một phần6,2,3. Nhãn có AI hỗ trợ, nhóm phải kiểm tra độc lập. Ví dụQ16: baseline100 testsets sai, hai RAG20 đúng. Không dùng các số này để xếp hạng Gemini chung hoặc tuyên bố giảm hallucination một tỷ lệ phổ quát.

## 11 — Lỗi và citations (75 giây, Người C)

Q06lexical thiếu version; Q13lexical lấy phần kết luận; Q09mỗi nhánh RAG chỉ trả được mộtlicense. Q14dense đúng ba hàm nhưng khôngcitation. Phân biệt missing, incorrect retrieval, irrelevant citation và beyond evidence. Trong lượt chính thức không quan sát IDtrích dẫn không tồn tại, nhưng vẫn cần kiểm tra nghĩa; không có lỗi ID không đồng nghĩa mọiclaim được chứng minh. Case citation sai được tự tạo trong báo cáo phải gọi rõ “giả lập”, không gán cho Gemini.

## 12 — Kết luận (60 giây, Người C)

Trả lời câu hỏi mở đầu: tài liệu ngoài giúp tra cứu và kiểm chứng, nhưng không bảo đảm hết hallucination. Đề xuất giữ hash/version, lập lại index, regression test và kiểm chứng từngclaim. Nhắc giới hạn20câu,1paper,1embedding nhỏ,goldchưa đầy đủ,1lượtmodel. Mời hỏi đáp. Chia câu hỏi để cả ba thành viên đều trả lời ít nhất một câu trong5phút.

Tổng dự kiến 15 phút. Nếu nói chậm, rút phần so sánh nền tảng và giữ nguyên thời gian ví dụ, bảng kết quả, lỗi.
