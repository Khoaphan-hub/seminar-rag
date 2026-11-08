"""Export transparent, source-checked assistant annotations, not an independent LLM judge.

Labels below were assigned after reading every final response, reference and the relevant
retrieved context. They are intentionally editable for independent review by the team.
"""
import csv, hashlib, json, re
from collections import Counter
from .prepare import ROOT

# correctness: 1 complete core answer, .5 partial/qualified, 0 wrong or no answer.
CB = [
(.5,'Identifies the goal of choosing a small subset, but searching all subsets can suggest exhaustive enumeration; the minimal adequate subset is not clearly stated.'),
(1,'Correctly identifies C++ with Python/R interfaces.'),(1,'Correctly identifies PyPI and CRAN.'),
(0,'Does not identify the splicing technique; repeats best-subset selection.'),
(.5,"Includes warm starts and OpenMP but omits sparse matrix support; substitutes algorithm details for the paper's three features."),
(0,'R 3.5.0 is incorrect; the paper specifies R >=3.1.0.'),(1,'Correctly identifies GitHub Actions.'),
(0,'Only gives bounds above 90% and 80%, omitting the requested 97%/96% coverage values.'),
(1,"Correctly pairs GPL-3 and CC BY 4.0; the added phrase 'or later' is not established by the paper's license statement."),
(.5,'Includes normalization/standardization but omits screening; mean/variance details are not stated in this paper.'),
(0,'abessVS is incorrect; the required class is Metric.'),
(.5,'AIC is correct, but ordinary BIC is not the specified high-dimensional BIC.'),
(0,'Does not identify subclassing Algorithm and its virtual interface; the implementation description differs from the Architecture section.'),
(0,'predict is incorrect; the required trio is print, coef, plot.'),(0,'AUC 0.99 and the synthetic logistic example are incorrect; the paper reports about 0.966.'),
(0,'100 test sets is incorrect; the answer is 20.'),(1,'Correctly identifies the number of nonzero elements/coefficients.'),
(.5,'Correctly rejects a universal guarantee and identifies NP-hardness, but omits the precise high-probability linear-model scope and adds assumptions/algorithms beyond the paper.'),
(.5,'Correctly rejects universality but does not identify the cancer setting and l1 baseline in the reference.'),
(0,'500/1000 is incorrect; the answer is 217/1413.')]

TF = {6:(0,'Abstains because the context lacks version requirements; this is not a fabricated wrong value.'),
9:(.5,'Correctly gives GPL-3 and abstains on the article license because supporting evidence is absent.'),
13:(0,'Mentions future plans, then abstains on extension; the context lacks the Algorithm passage.'),
19:(.5,'Identifies the cancer-specific scope but does not answer No explicitly; the context lacks complete abess rows needed to verify every dataset.')}
EM = {2:(0,'Abstains on the core language because C++ is absent from the context.'),
4:(0,'Abstains because the splicing passage is absent.'),
5:(.5,'Identifies warm starts/OpenMP in the figure, omits sparse matrix support, and substitutes C++; explicitly notes insufficient evidence for the full trio.'),
9:(.5,'Correctly gives CC BY 4.0 and abstains on GPL-3 because the code-license passage is missing.'),
15:(0,'Abstains on AUC and confuses the truncated benchmark table with the usage example. The chunk still begins with 0.9663829492654472, but lacks a clear connection to the preceding code.'),
19:(.5,'Preserves the cancer-specific scope but states insufficient information instead of explicitly answering No.')}

def main():
    source=ROOT/'results/generation.jsonl'
    records=[json.loads(x) for x in source.read_text(encoding='utf-8').splitlines()]
    if len(records)!=60: raise ValueError('Expected exactly 60 final responses.')
    rows=[]
    for r in records:
        n=int(r['question_id'][1:]); cond=r['condition']
        score,note=CB[n-1] if cond=='closed_book' else (TF if cond=='tfidf' else EM).get(n,(1,'Includes the core reference content; checked against the source and supplied context.'))
        citations=re.findall(r'\bs\d+-p\d+-t\d+\b',r['answer'])
        invalid=sorted(set(citations)-set(r['retrieved_ids']))
        pure_abstain=(cond=='tfidf' and n in [6,13]) or (cond=='embedding' and n in [2,4,15])
        grounding='not_applicable' if cond=='closed_book' else 'supported'
        if pure_abstain:grounding='abstention'
        if cond=='embedding' and n==7:
            grounding='inference_from_URL';note+=' The service name is correct, but its code-checking role is inferred from an /actions URL; the context lacks an explicit continuous-integration statement.'
        if cond=='embedding' and n==15:
            grounding='uncertain_explanation';note+=' The explanation for insufficient evidence confuses Figure 3 with the table; it is not treated as a fully supported factual answer.'
        if cond=='embedding' and n==14:note+=' The content is correct and present in the context, but the response omits a citation.'
        if cond=='embedding' and n==3:note+=' PyPI/CRAN URLs provide equivalent evidence outside the selected page-1 gold; this illustrates a limitation of selected-span recall.'
        rows.append({'question_id':r['question_id'],'condition':cond,'score':score,
            'fully_correct':int(score==1),'abstained_on_requested_answer':int(pure_abstain),
            'grounding_review':grounding,'citation_ids':';'.join(citations),'invalid_citation_ids':';'.join(invalid),
            'missing_citation_on_substantive_answer':int(cond!='closed_book' and not pure_abstain and not citations),
            'reviewer':'Codex-assisted source review; read and accepted by Phan Anh Khoa (24125059)',
            'answer_sha256':hashlib.sha256(r['answer'].encode()).hexdigest(),'rationale_en':note})
    rows.sort(key=lambda r:(r['question_id'],r['condition']))
    with (ROOT/'results/answer_review.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    summaries=[]
    for c in ['closed_book','tfidf','embedding']:
        part=[r for r in rows if r['condition']==c]
        summaries.append({'condition':c,'n':20,'fully_correct':sum(r['fully_correct'] for r in part),
            'partial':sum(r['score']==.5 for r in part),
            'incorrect':sum(r['score']==0 and not r['abstained_on_requested_answer'] for r in part),'mean_score':sum(r['score'] for r in part)/20,
            'abstentions':sum(r['abstained_on_requested_answer'] for r in part),
            'invalid_citation_answers':sum(bool(r['invalid_citation_ids']) for r in part),
            'missing_citation_answers':sum(r['missing_citation_on_substantive_answer'] for r in part)})
    (ROOT/'results/answer_summary.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'assessment':'Codex-assisted review, read and accepted by Phan Anh Khoa (24125059); not blind or independent multi-rater assessment.',
        'review_acceptance':{'reviewer':'Phan Anh Khoa','student_id':'24125059','status':'read_and_accepted','score_changes_requested':False,'basis':'Explicit confirmation in project conversation','separate_review_by_second_member_confirmed':False},
        'citation_warning':'ID existence and missing citations are structural checks, not automatic proof of semantic support.',
        'summaries':summaries},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summaries,indent=2))

if __name__=='__main__':main()
