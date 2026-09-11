"""Lightweight local vector store using TF-IDF + cosine similarity.

Deliberately dependency-light and 100% offline: no model downloads,
no internet connection required, works the moment you `pip install`.
For higher-quality semantic search at scale, swap this for
sentence-transformers embeddings or a hosted vector DB (Pinecone,
Weaviate, pgvector) — see README for how.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class VectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.chunks: list[dict] = []
        self.matrix = None

    def build(self, chunks: list[dict]):
        self.chunks = chunks
        texts = [c["text"] for c in chunks]
        self.matrix = self.vectorizer.fit_transform(texts)
        print(f"[VectorStore] Indexed {len(chunks)} chunks (TF-IDF).")

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if self.matrix is None:
            raise RuntimeError("Call build() before search().")
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.matrix).flatten()
        top_idx = np.argsort(scores)[::-1][:top_k]
        return [
            {**self.chunks[i], "score": float(scores[i])}
            for i in top_idx
        ]
