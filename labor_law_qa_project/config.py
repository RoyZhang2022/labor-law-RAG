import os

LLM_BACKEND = os.getenv("LLM_BACKEND", "glm4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
GLM4_API_KEY = os.getenv("GLM4_API_KEY")
GLM4_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
MOONSHOT_API_URL = "https://api.moonshot.cn/v1/chat/completions"
EMBEDDING_MODEL = "BAAI/bge-large-zh"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
TOP_K = 3
VECTOR_DIM = 1024