"""Interactive retrieval inspection without API charges; use --question to ask once."""
import argparse
import sys
import json
from pathlib import Path
from .retrievers import create_retriever, top_chunks
from .generate import build_prompt

def main():
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser();p.add_argument('--method',choices=['tfidf','embedding'],default='tfidf');p.add_argument('--k',type=int,default=3);p.add_argument('--size',type=int,choices=[96,192],default=192);p.add_argument('--question');p.add_argument('--prompt',action='store_true');args=p.parse_args()
    if args.k<1:p.error('--k must be at least 1')
    root=Path(__file__).resolve().parents[1]
    chunks=json.loads((root/f'data/processed/chunks_{args.size}.json').read_text(encoding='utf-8'))
    retriever=create_retriever(args.method,[c['text'] for c in chunks])
    while True:
        q=args.question or input('Question (exit to quit): ').strip()
        if q.lower()=='exit':break
        found=top_chunks(chunks,retriever.score([q])[0],args.k)
        for c in found:print(f"\n[{c['id']}] page {c['page']} cosine={c['score']:.4f}\n{c['text']}")
        if args.prompt:print('\nPROMPT\n'+build_prompt(q,found))
        if args.question:break

if __name__=='__main__':main()
