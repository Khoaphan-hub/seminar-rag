"""Lexical retrieval: TF-IDF vectors and exact cosine similarity."""
from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfRetriever:
    def __init__(self, texts):
        self.vectorizer = TfidfVectorizer(
            lowercase=True, stop_words='english', ngram_range=(1, 2),
            norm='l2', smooth_idf=True)
        self.vectors = self.vectorizer.fit_transform(texts)

    def score(self, questions):
        return (self.vectorizer.transform(questions) @ self.vectors.T).toarray()
