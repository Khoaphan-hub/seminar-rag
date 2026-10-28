"""Paired retrieval experiment with immutable source-span evidence and exact cosine search."""
import argparse, csv, hashlib, json, platform, time
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from .prepare import ROOT

def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def save(path, obj):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def chunks_for(pages, tokenizer, size, overlap=24):
    chunks=[]
    for p in pages:
        offsets=tokenizer(p['text'],add_special_tokens=False,return_offsets_mapping=True)['offset_mapping']
        for start in range(0,len(offsets),size-overlap):
            end=min(start+size,len(offsets)); a,b=offsets[start][0],offsets[end-1][1]
            chunks.append({'id':f"s{size}-p{p['page']}-t{start}",'page':p['page'],'start':a,'end':b,'text':p['text'][a:b],'tokens':end-start,'source':p['source']})
            if end==len(offsets): break
    return chunks

def evidence_spans(q,pages):
    spans=[]
    for e in q['evidence']:
        text=pages[e['page']-1]['text']; a=text.find(e['quote'])
        if a<0: raise ValueError(f"Missing gold evidence {q['id']}: {e}")
        spans.append((e['page'],a,a+len(e['quote'])))
    return spans

def covers(chunks,span):
    p,a,b=span; cursor=a
    for c in sorted((x for x in chunks if x['page']==p),key=lambda x:x['start']):
        if c['start']<=cursor<c['end']: cursor=c['end']
        if cursor>=b:return True
    return False

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--offline',action='store_true'); args=parser.parse_args()
    pages=load('data/processed/pages.json'); qs=load('data/questions.json')
    gold={q['id']:evidence_spans(q,pages) for q in qs}
    model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2',local_files_only=args.offline,device='cpu')
    model.eval(); query_emb=model.encode([q['question'] for q in qs],normalize_embeddings=True)
    rows=[]; details=[]
    for size in [96,192]:
        chunks=chunks_for(pages,model.tokenizer,size)
        assert max(c['tokens'] for c in chunks)+2<=model.max_seq_length
        save(f'data/processed/chunks_{size}.json',chunks)
        texts=[c['text'] for c in chunks]
        tf=TfidfVectorizer(lowercase=True,stop_words='english',ngram_range=(1,2),norm='l2',smooth_idf=True)
        matrix=tf.fit_transform(texts)
        sims={'tfidf':(tf.transform([q['question'] for q in qs])@matrix.T).toarray(),
              'embedding':query_emb@model.encode(texts,normalize_embeddings=True).T}
        for method,scores in sims.items():
            for k in [1,3,5]:
                stats=[]
                for qi,q in enumerate(qs):
                    ix=np.argsort(-scores[qi],kind='stable')[:k]
                    retrieved=[dict(chunks[i],score=float(scores[qi,i])) for i in ix]
                    spans=gold[q['id']]
                    support=[covers(retrieved,s) for s in spans]
                    relevant={c['id'] for c in chunks if any(covers([c],s) for s in spans)}
                    found={c['id'] for c in retrieved}&relevant
                    entry={'question_id':q['id'],'method':method,'chunk_tokens':size,'k':k,
                        'hit':int(any(support)),'evidence_recall':sum(support)/len(support),
                        'all_evidence':int(all(support)),
                        'chunk_recall':len(found)/len(relevant) if relevant else 0,
                        'gold_chunk_count':len(relevant),'retrieved':retrieved}
                    details.append(entry);stats.append(entry)
                rows.append({'method':method,'chunk_tokens':size,'overlap_tokens':24,'k':k,'chunks':len(chunks),'questions':len(qs),
                    **{s:float(np.mean([e[s] for e in stats])) for s in ['hit','chunk_recall','evidence_recall','all_evidence']}})
    save('results/retrieval_details.json',details);save('results/retrieval_summary.json',rows)
    with (ROOT/'results/retrieval_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    import importlib.metadata as md
    save('results/run_manifest.json',{'python':platform.python_version(),'packages':{p:md.version(p) for p in ['numpy','scikit-learn','sentence-transformers','pypdf','torch','transformers']},
        'model':'sentence-transformers/all-MiniLM-L6-v2','embedding_dim':int(query_emb.shape[1]),'max_seq_length':model.max_seq_length,
        'similarity':'cosine on L2-normalized vectors; exact exhaustive search',
        'question_sha256':hashlib.sha256((ROOT/'data/questions.json').read_bytes()).hexdigest(),
        'generation_config_preselected':{'chunk_tokens':192,'k':3,'reason':'Fixed before inspecting retrieval results; balance context and cost.'},
        'limitations':['20 manually authored English questions, one paper','No train/test tuning split; descriptive demonstration only','Gold evidence is a selected reference set, not exhaustive semantic relevance judgments','PDF tables retained as extracted text','Chunk recall penalizes redundant overlapping relevant chunks; evidence recall also reported']})
    for r in rows: print(r)

if __name__=='__main__':main()
