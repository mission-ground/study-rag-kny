import os
import sys

# 루트 경로 추가 (기존 scripts 문제 해결 방식 적용)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

from rag.ingestion.extractors import extract_text_from_pdf
from rag.ingestion.chunker import get_chunks
from rag.vectorstores.faiss.vector_store import FAISSVectorStore

def run_build_index():
    raw_pdf_path = "data/raw/pdf/2026_policy.pdf"
    index_save_path = "rag/vectorstores/faiss/index"

    # 1. 데이터 추출 및 청킹
    raw_text = extract_text_from_pdf(raw_pdf_path)
    chunks = get_chunks(raw_text)

    # 2. 벡터 스토어 생성 및 저장
    vs = FAISSVectorStore()
    vs.create_index(chunks)
    vs.save_index(index_save_path)

if __name__ == "__main__":
    run_build_index()