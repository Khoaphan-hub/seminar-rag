"""Export transparent, source-checked assistant annotations, not an independent LLM judge.

Labels below were assigned after reading every final response, reference and the relevant
retrieved context. They are intentionally editable for independent review by the team.
"""
import csv, hashlib, json, re
from collections import Counter
from .prepare import ROOT

# correctness: 1 complete core answer, .5 partial/qualified, 0 wrong or no answer.
CB = [
(.5,'Đúng mục tiêu chọn tập nhỏ, nhưng mô tả tìm qua mọi subset dễ đánh đồng với vét cạn; thiếu sự tối thiểu phù hợp.'),
(1,'Đúng C++, có giao diện Python/R.'),(1,'Đúng PyPI và CRAN.'),
(0,'Không trả lời splicing technique; chỉ nhắc lại best-subset selection.'),
(.5,'Có warm-start và OpenMP nhưng không có sparse matrix support; thêm mô tả thuật toán thay cho bộ ba trong paper.'),
(0,'R 3.5.0 sai; paper nêu R >=3.1.0.'),(1,'Đúng GitHub Actions.'),
(0,'Chỉ cho cận >90% và >80%, không nêu hai số coverage 97%/96% được hỏi.'),
(1,'Đúng cặp GPL-3 và CC BY 4.0; cụm or later không được xác nhận từ giấy phép nêu trong paper.'),
(.5,'Có normalization/standardization nhưng thiếu screening; chi tiết mean/variance không được paper này nêu.'),
(0,'abessVS sai; class cần trả lời là Metric.'),
(.5,'Đúng AIC, nhưng BIC thông thường không phải high dimensional BIC được nêu.'),
(0,'Không chỉ rõ subclass Algorithm và virtual interface; mô tả implementation khác với Architecture.'),
(0,'predict sai; bộ ba cần là print, coef, plot.'),(0,'AUC 0.99 và synthetic logistic sai; paper nêu khoảng 0.966.'),
(0,'100 test sets sai; cần 20.'),(1,'Đúng số phần tử/coefficients khác 0.'),
(.5,'Đúng phủ định bảo đảm phổ quát và NP-hard, nhưng không nêu chính xác high probability under linear model; thêm giả định/thuật toán ngoài paper.'),
(.5,'Phủ định tính phổ quát đúng nhưng không xác định cancer và baseline l1 theo reference.'),
(0,'500/1000 sai; cần 217/1413.')]

TF = {6:(0,'Từ chối vì context thiếu phiên bản; không phải đáp án sai do bịa.'),
9:(.5,'Đúng GPL-3, từ chối phần article license vì thiếu nguồn.'),
13:(0,'Nêu kế hoạch tương lai rồi từ chối cách mở rộng; context thiếu đoạn Algorithm.'),
19:(.5,'Nêu đúng phạm vi cancer nhưng không trả lời dứt khoát No; context thiếu các hàng abess đầy đủ để kiểm chứng mọi dataset.')}
EM = {2:(0,'Từ chối ngôn ngữ core khi context không chứa C++.'),
4:(0,'Từ chối vì không có đoạn splicing tương ứng.'),
5:(.5,'Có warm-start/OpenMP trong hình, thiếu sparse matrix support và thay bằng C++; đã tự nêu thiếu bằng chứng cho bộ ba.'),
9:(.5,'Đúng CC BY 4.0, từ chối GPL-3 vì context thiếu đoạn code license.'),
15:(0,'Từ chối AUC; nhầm việc bảng benchmark bị cắt với usage example. Đầu chunk vẫn có 0.9663829492654472 nhưng thiếu phần code liên kết rõ ràng.'),
19:(.5,'Giữ đúng phạm vi cancer, nhưng chỉ nói không đủ thông tin thay vì trả lời No rõ ràng.')}

def main():
    source=ROOT/'results/generation.jsonl'
    records=[json.loads(x) for x in source.read_text(encoding='utf-8').splitlines()]
    if len(records)!=60: raise ValueError('Expected exactly 60 final responses.')
    rows=[]
    for r in records:
        n=int(r['question_id'][1:]); cond=r['condition']
        score,note=CB[n-1] if cond=='closed_book' else (TF if cond=='tfidf' else EM).get(n,(1,'Đủ nội dung cốt lõi trong reference; đối chiếu nguồn và context.'))
        citations=re.findall(r'\bs\d+-p\d+-t\d+\b',r['answer'])
        invalid=sorted(set(citations)-set(r['retrieved_ids']))
        pure_abstain=(cond=='tfidf' and n in [6,13]) or (cond=='embedding' and n in [2,4,15])
        grounding='not_applicable' if cond=='closed_book' else 'supported'
        if pure_abstain:grounding='abstention'
        if cond=='embedding' and n==7:
            grounding='inference_from_URL';note+=' Đúng tên dịch vụ nhưng suy ra chức năng kiểm tra code từ URL /actions; context không có câu continuous integration.'
        if cond=='embedding' and n==15:
            grounding='uncertain_explanation';note+=' Giải thích lý do thiếu bằng chứng nhầm Figure 3 với phần bảng; không xem là một câu factual được hỗ trợ đầy đủ.'
        if cond=='embedding' and n==14:note+=' Nội dung đúng và có trong context, nhưng response bỏ citation.'
        if cond=='embedding' and n==3:note+=' URLs PyPI/CRAN là bằng chứng tương đương ngoài gold chọn ở trang 1; đây là hạn chế của selected-span recall.'
        rows.append({'question_id':r['question_id'],'condition':cond,'score':score,
            'fully_correct':int(score==1),'abstained_on_requested_answer':int(pure_abstain),
            'grounding_review':grounding,'citation_ids':';'.join(citations),'invalid_citation_ids':';'.join(invalid),
            'missing_citation_on_substantive_answer':int(cond!='closed_book' and not pure_abstain and not citations),
            'reviewer':'Codex-assisted source review; pending independent team verification',
            'answer_sha256':hashlib.sha256(r['answer'].encode()).hexdigest(),'rationale_vi':note})
    rows.sort(key=lambda r:(r['question_id'],r['condition']))
    with (ROOT/'results/answer_review.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    summaries=[]
    for c in ['closed_book','tfidf','embedding']:
        part=[r for r in rows if r['condition']==c]
        summaries.append({'condition':c,'n':20,'fully_correct':sum(r['fully_correct'] for r in part),
            'partial':sum(r['score']==.5 for r in part),'mean_score':sum(r['score'] for r in part)/20,
            'abstentions':sum(r['abstained_on_requested_answer'] for r in part),
            'invalid_citation_answers':sum(bool(r['invalid_citation_ids']) for r in part),
            'missing_citation_answers':sum(r['missing_citation_on_substantive_answer'] for r in part)})
    (ROOT/'results/answer_summary.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'assessment':'Assisted review, descriptive, not blind or independent human assessment.',
        'citation_warning':'ID existence and missing citations are structural checks, not automatic proof of semantic support.',
        'summaries':summaries},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summaries,indent=2))

if __name__=='__main__':main()
