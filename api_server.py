import threading
from fastapi import FastAPI
from pydantic import BaseModel
from src.qa_pipeline import QAPipeline
import os
import time

app = FastAPI()
qa_pipeline = QAPipeline()

def build_kb():
    print("📚 Loading documents and building knowledge base...")
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, 'data', 'documents.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        documents = [line.strip() for line in f if line.strip()]
    qa_pipeline.build_knowledge_base(documents)
    print("✅ QA system ready.")

@app.on_event("startup")
async def startup_event():
    threading.Thread(target=build_kb, daemon=True).start()

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
