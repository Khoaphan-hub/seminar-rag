import json
from .prepare import ROOT

rows=json.loads((ROOT/'results/retrieval_summary.json').read_text(encoding='utf-8'))
s=r'\begin{table}[h]\centering\small'+'\n'+r'\begin{tabular}{lrrrrrr}\toprule'+'\n'
s+=r'Method & Tokens & k & Hit & Recall@k & Evidence & All \\ \midrule'+'\n'
for r in rows:
    s+=f"{r['method']} & {r['chunk_tokens']} & {r['k']} & {r['hit']:.3f} & {r['chunk_recall']:.3f} & {r['evidence_recall']:.3f} & {r['all_evidence']:.3f} "+'\\\\\n'
s+=r'\bottomrule\end{tabular}'+'\n'+r'\caption{Results on 20 questions. Hit/All: fraction of questions with at least one/every gold span covered; Recall@k: macro chunk recall; Evidence: evidence recall. Source: project data.}\end{table}'
(ROOT/'report/retrieval_table.tex').write_text(s,encoding='utf-8')
