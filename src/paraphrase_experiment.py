"""Exploratory paired query-paraphrase study; no generation API calls."""
import json, hashlib
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from .experiment import covers, evidence_spans
from .retrievers import create_retriever, top_chunks
from .prepare import ROOT

def main():
    read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
    original=read('data/questions.json'); paraphrases=read('data/questions_paraphrased.json')
    assert len(original)==len(paraphrases)==20
    for a,b in zip(original,paraphrases):
        assert a['id']==b['id'] and a['answer']==b['answer'] and a['evidence']==b['evidence']
        assert a['question']==b['original_question']
    pages=read('data/processed/pages.json')
    model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2',local_files_only=True,device='cpu')
    details=[]; summary=[]
    for size in [96,192]:
        chunks=read(f'data/processed/chunks_{size}.json')
        for method in ['tfidf','embedding']:
            retriever=create_retriever(method,[c['text'] for c in chunks],model=model)
            for variant,qs in [('original',original),('paraphrased',paraphrases)]:
                scores=retriever.score([q['question'] for q in qs])
                for k in [1,3,5]:
                    batch=[]
                    for q,ss in zip(qs,scores):
                        spans=evidence_spans(q,pages); selected=top_chunks(chunks,ss,k)
                        relevant={c['id'] for c in chunks if any(covers([c],s) for s in spans)}
                        support=[covers(selected,s) for s in spans]
                        row=dict(question_id=q['id'],variant=variant,method=method,chunk_tokens=size,k=k,
                            chunk_recall=len(relevant & {c['id'] for c in selected})/len(relevant),
                            evidence_recall=sum(support)/len(support),all_evidence=int(all(support)),hit=int(any(support)),retrieved=selected)
                        batch.append(row)
                    details.extend(batch)
                    summary.append(dict(variant=variant,method=method,chunk_tokens=size,k=k,**{m:float(np.mean([r[m] for r in batch])) for m in ['chunk_recall','evidence_recall','all_evidence','hit']}))
    for name,value in [('details',details),('summary',summary)]:
        (ROOT/f'results/paraphrase_{name}.json').write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps([r for r in summary if r['chunk_tokens']==192 and r['k']==3],indent=2))
if __name__=='__main__':main()
