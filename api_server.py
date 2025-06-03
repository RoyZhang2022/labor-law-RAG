from fastapi import FastAPI
from pydantic import BaseModel
from src.qa_pipeline import QAPipeline
import os
import time

app = FastAPI()

qa_pipeline = QAPipeline()

# 加载知识库
def load_documents(filepath):
    documents = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                documents.append(line)
    return documents

start_time = time.time()
project_root = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(project_root, 'data', 'documents.txt')
documents = load_documents(file_path)
qa_pipeline.build_knowledge_base(documents)
print(f"QA系统启动完成，耗时 {time.time() - start_time:.2f} 秒")

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

