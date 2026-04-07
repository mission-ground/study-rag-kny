from rag.ingestion.extractors import extract_text_from_pdf
from rag.ingestion.chunker import get_chunks
import os

def run_ingestion():
    raw_pdf_path = "data/raw/2026_policy.pdf"
    output_path = "data/processed/2026_policy_raw.txt"
    
    print(f"작업 시작: {raw_pdf_path} 추출 중...")
    
    # 1. PDF 텍스트 추출
    raw_text = extract_text_from_pdf(raw_pdf_path)
    
    # 2. 결과 저장 (나중에 눈으로 확인하기 위해 txt로 저장)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(raw_text)
        
    print(f"완료! 추출된 텍스트가 {output_path}에 저장되었습니다.")

    # 3. 청킹
    chunks = get_chunks(raw_text)
    
    print(f"총 {len(chunks)}개의 청크로 분할되었습니다.")

    # 4. 모든 청크를 각각 파일로 저장 (학습 및 확인용)
    chunks_dir = "data/chunks/"
    os.makedirs(chunks_dir, exist_ok=True)
    
    # 기존에 있던 청크 파일 삭제
    for f in os.listdir(chunks_dir):
        os.remove(os.path.join(chunks_dir, f))

    for i, chunk in enumerate(chunks):
        chunk_path = f"{chunks_dir}chunk_{i+1:03d}.txt" # chunk_001.txt 형식
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk)
            
    print(f"완료! {len(chunks)}개의 청크 파일이 {chunks_dir}에 생성되었습니다.")

if __name__ == "__main__":
    run_ingestion()