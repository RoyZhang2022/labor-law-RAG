import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.data = []

    def add(self, embeddings, texts):
        self.index.add(embeddings)
        self.data.extend(texts)

    def search(self, query_embedding, top_k=3):
        D, I = self.index.search(query_embedding, top_k)
        return [self.data[i] for i in I[0]]