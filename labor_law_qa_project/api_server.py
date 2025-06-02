# api_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.qa_pipeline import QAPipeline
import os

app = FastAPI()

qa_pipeline = QAPipeline()

# ⚡⚡⚡ 从文件加载知识库文档
def load_documents(filepath):
    documents = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # 非空行
                documents.append(line)
    return documents

# 获取当前项目路径，兼容Win/Linux
project_root = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(project_root, 'data', 'documents.txt')

# 加载并构建向量知识库
documents = load_documents(file_path)
qa_pipeline.build_knowledge_base(documents)

# 请求结构
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

