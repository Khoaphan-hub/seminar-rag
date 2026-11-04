"""Check that the refactor preserves the published lexical retrieval results."""
import json
import unittest
from pathlib import Path

from src.retrievers import create_retriever, top_chunks

ROOT = Path(__file__).resolve().parents[1]


class RetrieverChecks(unittest.TestCase):
    def test_tfidf_matches_recorded_rankings_and_scores(self):
        questions = json.loads((ROOT / 'data/questions.json').read_text(encoding='utf-8'))
        records = json.loads((ROOT / 'results/retrieval_details.json').read_text(encoding='utf-8'))
        for size in (96, 192):
            chunks = json.loads((ROOT / f'data/processed/chunks_{size}.json').read_text(encoding='utf-8'))
            retriever = create_retriever('tfidf', [c['text'] for c in chunks])
            scores = retriever.score([q['question'] for q in questions])
            for i, question in enumerate(questions):
                for k in (1, 3, 5):
                    expected = next(r['retrieved'] for r in records
                                    if r['method'] == 'tfidf' and r['chunk_tokens'] == size
                                    and r['question_id'] == question['id'] and r['k'] == k)
                    actual = top_chunks(chunks, scores[i], k)
                    self.assertEqual([c['id'] for c in actual], [c['id'] for c in expected])
                    for a, b in zip(actual, expected):
                        self.assertAlmostEqual(a['score'], b['score'], places=10)

    def test_ties_preserve_corpus_order_and_invalid_k_is_rejected(self):
        chunks = [{'id': 'first'}, {'id': 'second'}]
        self.assertEqual(top_chunks(chunks, [0., 0.], 1)[0]['id'], 'first')
        with self.assertRaises(ValueError):
            top_chunks(chunks, [0., 0.], 0)


if __name__ == '__main__':
    unittest.main()
