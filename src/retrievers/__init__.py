"""Interchangeable lexical and dense retrieval for the shared RAG pipeline."""
import numpy as np


def create_retriever(method, texts, **kwargs):
    if method == 'tfidf':
        from .tfidf import TfidfRetriever
        return TfidfRetriever(texts)
    if method == 'embedding':
        from .embedding import EmbeddingRetriever
        return EmbeddingRetriever(texts, **kwargs)
    raise ValueError(f'Unknown retrieval method: {method}')


def top_chunks(chunks, scores, k):
    if k < 1:
        raise ValueError('k must be at least 1')
    return [dict(chunks[i], score=float(scores[i]))
            for i in np.argsort(-np.asarray(scores), kind='stable')[:k]]
