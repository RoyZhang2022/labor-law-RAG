from transformers import AutoTokenizer, AutoModel
import torch

from config import EMBEDDING_MODEL

class Embedder:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
        self.model = AutoModel.from_pretrained(EMBEDDING_MODEL)

    def embed(self, text):
        tokens = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            embedding = self.model(**tokens).last_hidden_state.mean(dim=1).squeeze()
        return embedding.numpy()