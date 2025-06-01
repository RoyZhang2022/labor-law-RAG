# src/embedder.py
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class Embedder:
    def __init__(self):
        model_name_or_path = 'moka-ai/m3e-base'  # HuggingFace模型名字
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name_or_path, trust_remote_code=True)

    def embed(self, text):
        if isinstance(text, list):
            tokens = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        else:
            tokens = self.tokenizer([text], padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            embeddings = self.model(**tokens).last_hidden_state.mean(dim=1)

        return embeddings.squeeze().cpu().numpy()
