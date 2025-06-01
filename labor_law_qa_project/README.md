# Labor Law QA Project (企业劳动法智能问答系统)

这是一个基于 RAG（检索增强生成）的中文劳动法智能问答系统，支持劳动合同、劳动争议等法律问题解答。系统支持多大模型后端（OpenAI, 智谱GLM-4, Moonshot等），可灵活切换，且本地构建知识库，支持中文向量化检索。

## ✨ 功能亮点
- ✅ 中文劳动法/合同领域智能问答
- ✅ 本地知识库构建（BGE-large-zh + FAISS向量数据库）
- ✅ 多大模型后端切换（GLM-4、Moonshot、OpenAI）
- ✅ Prompt模板可配置，支持业务定制
- ✅ 支持命令行交互/ Web API模式
- ✅ 支持API Key环境变量管理，安全合规

## 📦 安装依赖

```bash
pip install -r requirements.txt
