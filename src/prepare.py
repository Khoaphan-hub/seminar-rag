"""Extract the openly licensed PDF without inserting reference answers into the corpus."""
import json, re, unicodedata, hashlib
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]

def normalize(text):
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    return re.sub(r'\s+', ' ', text).strip()

def main():
    source = ROOT / 'data/sources/abess_2022.pdf'
    pages = [{'page': i+1, 'text': normalize(p.extract_text()), 'source': source.name}
             for i, p in enumerate(PdfReader(source).pages)]
    out = ROOT / 'data/processed'
    out.mkdir(parents=True, exist_ok=True)
    (out/'pages.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
    manifest = {'title':'abess: A Fast Best-Subset Selection Library in Python and R',
        'authors':'Jin Zhu, Xueqin Wang, Liyuan Hu, Junhao Huang, Kangkang Jiang, Yanhang Zhang, Shiyun Lin, Junxian Zhu',
        'year':2022,'url':'https://jmlr.org/papers/v23/21-1060.html',
        'download_url':'https://jmlr.org/papers/volume23/21-1060/21-1060.pdf',
        'license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/',
        'license_evidence':'Copyright and license statement on PDF page 1',
        'sha256':hashlib.sha256(source.read_bytes()).hexdigest(), 'pages':len(pages),
        'transformations':'PDF text extraction, NFKC normalization, line-end dehyphenation, whitespace collapse. All 7 pages included; pages 5-7 contain acknowledgments/references. Tables are not manually rewritten.'}
    (ROOT/'data/sources/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Prepared',len(pages),'pages')

if __name__ == '__main__': main()
