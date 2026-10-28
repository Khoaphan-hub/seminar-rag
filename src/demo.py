"""Interactive retrieval inspection without API charges; use --question to ask once."""
import argparse
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from .experiment import load
from .generate import build_prompt

def main():
    p=argparse.ArgumentParser();p.add_argument('--method',choices=['tfidf','embedding'],default='tfidf');p.add_argument('--k',type=int,default=3);p.add_argument('--size',type=int,choices=[96,192],default=192);p.add_argument('--question');p.add_argument('--prompt',action='store_true');args=p.parse_args()
    chunks=load(f'data/processed/chunks_{args.size}.json');texts=[c['text'] for c in chunks]
    if args.method=='tfidf':
        model=TfidfVectorizer(stop_words='english',ngram_range=(1,2));vectors=model.fit_transform(texts)
    else:
        model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2');vectors=model.encode(texts,normalize_embeddings=True)
    while True:
        q=args.question or input('Question (exit to quit): ').strip()
        if q.lower()=='exit':break
        scores=(model.transform([q])@vectors.T).toarray()[0] if args.method=='tfidf' else model.encode([q],normalize_embeddings=True)[0]@vectors.T
        found=[dict(chunks[i],score=float(scores[i])) for i in np.argsort(-scores,kind='stable')[:max(1,args.k)]]
        for c in found:print(f"\n[{c['id']}] page {c['page']} cosine={c['score']:.4f}\n{c['text']}")
        if args.prompt:print('\nPROMPT\n'+build_prompt(q,found))
        if args.question:break

if __name__=='__main__':main()
