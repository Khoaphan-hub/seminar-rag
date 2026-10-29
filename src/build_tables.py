import json
from .prepare import ROOT

rows=json.loads((ROOT/'results/retrieval_summary.json').read_text(encoding='utf-8'))
s=r'\begin{table}[h]\centering\small'+'\n'+r'\begin{tabular}{lrrrrr}\toprule'+'\n'
s+=r'Method & Tokens & k & Recall@k & Evidence & All \\ \midrule'+'\n'
for r in rows:
    s+=f"{r['method']} & {r['chunk_tokens']} & {r['k']} & {r['chunk_recall']:.3f} & {r['evidence_recall']:.3f} & {r['all_evidence']:.3f} "+'\\\\\n'
s+=r'\bottomrule\end{tabular}'+'\n'+r'\caption{Measured results on 20 questions. Recall: macro chunk Recall@k; Evidence: evidence recall; All: fraction of questions with every gold span covered. Source: project code and data.}\end{table}'
(ROOT/'report/retrieval_table.tex').write_text(s,encoding='utf-8')
