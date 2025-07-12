from fastapi import FastAPI
from pydantic import BaseModel
from src.qa_pipeline import QAPipeline
import os
import time

app = FastAPI()

qa_pipeline = QAPipeline()

def load_documents(filepath):
    documents = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                documents.append(line)
    return documents

@app.on_event("startup")
async def startup_event():
    print("📚 Loading documents and building knowledge base...")
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, 'data', 'documents.txt')
    documents = load_documents(file_path)
    qa_pipeline.build_knowledge_base(documents)
    print("✅ QA system ready.")

class QueryRequest(BaseModel):
    question: str

@app.post("/qa/")
async def get_answer(request: QueryRequest):
    answer = qa_pipeline.answer(request.question)
    return {
        "question": request.question,
        "answer": answer
    }

@app.get("/")
async def health_check():
    return {"status": "ok"}
