import numpy as np
from src.embedder import Embedder
from src.vector_store import VectorStore
from src.retriever import Retriever
from src.llm_client import LLMClient
from src.prompt_loader import load_prompt_template
from config import VECTOR_DIM, TOP_K

class QAPipeline:
    def __init__(self):
        self.embedder = Embedder()
        self.store = VectorStore(dim=VECTOR_DIM)
        self.retriever = Retriever()
        self.llm = LLMClient()
        self.prompt_template = load_prompt_template()

    def build_knowledge_base(self, documents):
        chunks = []
        for doc in documents:
            chunks.extend(self.retriever.split_text(doc))
        embeddings = [self.embedder.embed(chunk) for chunk in chunks]
        self.store.add(np.vstack(embeddings), chunks)

    def answer(self, user_question):
        query_embedding = self.embedder.embed(user_question).reshape(1, -1)
        relevant_chunks = self.store.search(query_embedding, top_k=TOP_K)
        context = "\n".join(relevant_chunks)

        prompt = self.prompt_template.format(context=context, user_question=user_question)
        return self.llm.generate(prompt)