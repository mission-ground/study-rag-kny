import os
import sys

# 루트 경로 추가
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from rag.vectorstores.faiss.vector_store import FAISSVectorStore

def run_test():
    index_path = "rag/vectorstores/faiss/index"
    
    # 1. 벡터 스토어 로드
    vs = FAISSVectorStore()
    vector_db = vs.load_index(index_path) # 반환값을 변수에 담기
    
    # 2. 테스트 질문 던지기
    print("=== 정책 검색 테스트 모드 (종료: q 입력) ===")
    while True:
        query = input("\n질문을 입력하세요: ")
        if query.lower() == 'q':
            break
    
        # 관련성 높은 상위 3개 조각 검색
        # search_local 같은 메서드가 없다면 vs.vector_store.similarity_search 사용
        # 3. 검색 (None 체크 추가)
        if vector_db:
            docs = vector_db.similarity_search(query, k=3)
            for i, doc in enumerate(docs):
                print(f"[★검색 결과 {i+1}] {doc.page_content[:200]}...") 
        else:
            print("인덱스를 불러오지 못했습니다. 경로를 확인하세요.")

if __name__ == "__main__":
    run_test()