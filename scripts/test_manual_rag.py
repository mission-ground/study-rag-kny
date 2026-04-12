import os
from rag.embeddings.manual_embedder import ManualEmbedder
from rag.vectorstores.faiss.manual_store import ManualVectorStore

def test_manual_pipeline():
    # 1. 초기화
    embedder = ManualEmbedder()
    vector_store = ManualVectorStore()
    save_path = "data/manual_index"

    # 2. 샘플 데이터 준비 (테스트용)
    test_chunks = [
        "2026년 청년 도약 계좌는 만 19세부터 34세까지 가입 가능합니다.",
        "K-패스는 월 15회 이상 이용 시 대중교통 비용을 환급해주는 제도입니다.",
        "육아휴직 급여가 2026년부터 월 최대 250만원으로 인상되었습니다."
    ]

    print("--- [1] 임베딩 및 인덱스 생성 시작 ---")
    # 랭체인 없이 직접 벡터 추출
    vectors = embedder.embed_documents(test_chunks)
    
    # 벡터와 텍스트를 수동으로 매핑하여 저장
    vector_store.add_vectors_with_text(vectors, test_chunks)
    
    # 로컬에 파일(faiss, pkl) 저장
    vector_store.save_to_local(save_path)
    print(f"인덱스 저장 완료: {save_path}")

    print("\n--- [2] 인덱스 로드 및 검색 테스트 ---")
    # 새로운 스토어 객체를 생성하여 저장된 파일 불러오기
    new_store = ManualVectorStore()
    new_store.load_from_local(save_path)

    # 사용자 질문
    query = "지하철 요금 환급받으려면 어떻게 해야 해?"
    print(f"질문: {query}")

    # 질문 임베딩 -> 검색
    query_vector = embedder.embed_text(query)
    results = new_store.search_similar_chunks(query_vector, k=1)

    print(f"검색 결과: {results[0] if results else '결과 없음'}")

if __name__ == "__main__":
    test_manual_pipeline()