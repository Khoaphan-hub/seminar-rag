"""Dense retrieval: MiniLM embeddings and exact cosine similarity."""
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'


class EmbeddingRetriever:
    def __init__(self, texts, model=None, offline=False):
        self.model = model if model is not None else SentenceTransformer(
            MODEL_NAME, local_files_only=offline, device='cpu')
        self.model.eval()
        self.vectors = self.model.encode(texts, normalize_embeddings=True)

    def score(self, questions):
        return self.model.encode(questions, normalize_embeddings=True) @ self.vectors.T
