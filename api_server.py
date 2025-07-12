import threading
from fastapi import FastAPI
from pydantic import BaseModel
from src.qa_pipeline import QAPipeline
import os
import time

app = FastAPI()
qa_pipeline = QAPipeline()

def build_kb():
    print("🟡 Starting knowledge base setup...")

    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, 'data', 'documents.txt')
    print(f"📁 Loading documents from {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        documents = [line.strip() for line in f if line.strip()]
    print(f"📄 Loaded {len(documents)} documents")

    try:
        qa_pipeline.build_knowledge_base(documents)
        print("✅ Knowledge base built successfully.")
        qa_pipeline.ready = True
    except Exception as e:
        print(f"❌ Failed to build knowledge base: {e}")
        qa_pipeline.ready = False

@app.on_event("startup")
async def startup_event():
    threading.Thread(target=build_kb, daemon=True).start()

class QueryRequest(BaseModel):
    question: str

@app.post("/qa/")
async def get_answer(request: QueryRequest):
    if not getattr(qa_pipeline, "ready", False):
        return {"error": "QA system is still loading. Try again in a few seconds."}
    answer = qa_pipeline.answer(request.question)
    return {
        "question": request.question,
        "answer": answer
    }
	
@app.get("/")
async def health_check():
    return {"status": "ok"}
