import json
from .prepare import ROOT

rows=json.loads((ROOT/'results/retrieval_summary.json').read_text(encoding='utf-8'))
s=r'\begin{table}[h]\centering\small'+'\n'+r'\begin{tabular}{lrrrrr}\toprule'+'\n'
s+=r'Method & Token & k & Recall & Evidence & All \\ \midrule'+'\n'
for r in rows:
    s+=f"{r['method']} & {r['chunk_tokens']} & {r['k']} & {r['chunk_recall']:.3f} & {r['evidence_recall']:.3f} & {r['all_evidence']:.3f} "+'\\\\\n'
s+=r'\bottomrule\end{tabular}'+'\n'+r'\caption{Kết quả thực đo trên 20 câu hỏi. Recall: macro chunk Recall@k; Evidence: evidence recall; All: tỷ lệ lấy đủ gold. Nguồn: mã và dữ liệu của nhóm.}\end{table}'
(ROOT/'report/retrieval_table.tex').write_text(s,encoding='utf-8')
