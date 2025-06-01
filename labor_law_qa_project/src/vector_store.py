# src/vector_store.py
import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim=None):
        self.index = None
        self.data = []
        self.dim = dim

    def add(self, embeddings, texts):
        if self.index is None:
            # 动态创建索引，确保维度正确
            d = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(d)
            self.dim = d
        self.index.add(embeddings)
        self.data.extend(texts)

    def search(self, query_embedding, top_k=3):
        if self.index is None:
            raise ValueError("FAISS index is not initialized.")
        D, I = self.index.search(query_embedding, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.data):
                results.append(self.data[idx])
        return results
