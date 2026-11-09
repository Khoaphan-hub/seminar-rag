import hashlib, json, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class EvidenceChecks(unittest.TestCase):
    def test_generation_comparison_is_complete_and_bound_to_sources(self):
        source=ROOT/'results/generation.jsonl'
        rows=[json.loads(line) for line in source.read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(rows),60)
        expected={(f'Q{i:02}',c) for i in range(1,21) for c in ['closed_book','tfidf','embedding']}
        self.assertEqual({(r['question_id'],r['condition']) for r in rows},expected)
        details=json.loads((ROOT/'results/retrieval_details.json').read_text(encoding='utf-8'))
        retrieval={(r['question_id'],r['method']):r['retrieved'] for r in details if r['chunk_tokens']==192 and r['k']==3}
        common=rows[0]['prompt'].split('\n')[0]
        for row in rows:
            self.assertEqual(row['model'],'gemini-3.5-flash-lite')
            self.assertEqual(row['finish_reason'],'STOP')
            self.assertEqual(row['prompt'].split('\n')[0],common)
            self.assertEqual(row['prompt_sha256'],hashlib.sha256(row['prompt'].encode()).hexdigest())
            contexts=[] if row['condition']=='closed_book' else retrieval[(row['question_id'],row['condition'])]
            self.assertEqual(row['retrieved_ids'],[c['id'] for c in contexts])
            for chunk in contexts:
                self.assertIn(chunk['text'],row['prompt'])
        review=json.loads((ROOT/'results/answer_summary.json').read_text(encoding='utf-8'))
        self.assertEqual(review['generation_sha256'],hashlib.sha256(source.read_bytes()).hexdigest())

    def test_gold_quotes_exist_in_correct_pages(self):
        pages=json.loads((ROOT/'data/processed/pages.json').read_text(encoding='utf-8'))
        qs=json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))
        self.assertEqual(len(qs),20)
        for q in qs:
            for e in q['evidence']:
                self.assertIn(e['quote'],pages[e['page']-1]['text'],q['id'])

    def test_retrieval_nesting_and_recall_monotonicity(self):
        rows=json.loads((ROOT/'results/retrieval_details.json').read_text(encoding='utf-8'))
        self.assertEqual(len(rows),240)
        for r in rows:
            self.assertGreater(r['gold_chunk_count'],0)
            self.assertEqual(len(r['retrieved']),r['k'])
            self.assertEqual(len({x['id'] for x in r['retrieved']}),r['k'])
            self.assertTrue(0<=r['chunk_recall']<=1)
            if r['k']==1: continue
            prev=next(p for p in rows if p['method']==r['method'] and p['question_id']==r['question_id'] and p['chunk_tokens']==r['chunk_tokens'] and p['k']==(1 if r['k']==3 else 3))
            self.assertLessEqual(prev['chunk_recall'],r['chunk_recall'])
            self.assertEqual(prev['retrieved'],r['retrieved'][:prev['k']])

    def test_no_embedding_truncation(self):
        for size in [96,192]:
            chunks=json.loads((ROOT/f'data/processed/chunks_{size}.json').read_text(encoding='utf-8'))
            self.assertTrue(all(c['tokens']<=size and c['tokens']+2<=256 for c in chunks))

if __name__=='__main__': unittest.main()
