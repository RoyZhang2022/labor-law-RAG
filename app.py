import logging
from src.qa_pipeline import QAPipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("初始化QA系统...")
    documents = []
    with open('data/documents.txt', 'r', encoding='utf-8') as f:
        documents = f.read().split("\n\n")

    qa = QAPipeline()
    qa.build_knowledge_base(documents)

    while True:
        user_question = input("\n请输入您的劳动法问题 (输入exit退出): ")
        if user_question.lower() == "exit":
            break
        try:
            answer = qa.answer(user_question)
            print(f"\n【智能问答回复】\n{answer}")
        except Exception as e:
            logger.error("生成回答失败", exc_info=True)

if __name__ == "__main__":
    main()