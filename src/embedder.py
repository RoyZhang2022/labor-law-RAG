# src/embedder.py
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import os

class Embedder:
    def __init__(self):
        # 获取当前工程根目录
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 拼接成绝对路径，适配 Windows/Linux
		
		# comment for web deployment
        #model_dir = os.path.join(project_root, 'm3e-base')
        #self.tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
        #self.model = AutoModel.from_pretrained(model_dir, trust_remote_code=True)

        model_name = "moka-ai/m3e-base"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True)

    def embed(self, text):
        if isinstance(text, list):
            tokens = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        else:
            tokens = self.tokenizer([text], padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            embeddings = self.model(**tokens).last_hidden_state.mean(dim=1)

        return embeddings.squeeze().cpu().numpy()

    def embed_batch(self, texts, batch_size=8):
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            tokens = self.tokenizer(batch, padding=True, truncation=True, return_tensors='pt')
            with torch.no_grad():
                outputs = self.model(**tokens).last_hidden_state.mean(dim=1)
                all_embeddings.append(outputs.cpu().numpy())
        return np.vstack(all_embeddings)
