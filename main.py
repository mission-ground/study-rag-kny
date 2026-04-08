import os
import sys
from rag.vectorstores.faiss.vector_store import FAISSVectorStore
from rag.generation.generator import RAGGenerator

def main():
    # 1. 초기화 (인덱스 로드 및 생성기 준비)
    vs = FAISSVectorStore()
    vector_db = vs.load_index("rag/vectorstores/faiss/index")
    generator = RAGGenerator()
    
    print("=== 2026 민생 정책 Q&A 서비스 (종료: q) ===")
    
    while True:
        query = input("\n질문: ")
        if query.lower() == 'q': break
        
        # 2. 검색 (Retrieval)
        docs = vector_db.similarity_search(query, k=3)
        
        # 3. 답변 생성 (Generation)
        answer = generator.generate_answer(query, docs)
        
        print(f"\nAI 답변: {answer}")

if __name__ == "__main__":
    main()