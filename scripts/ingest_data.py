from rag.ingestion.extractors import extract_text_from_pdf
import os

def run_ingestion():
    raw_pdf_path = "data/raw/2026_policy.pdf"
    output_path = "data/processed/2026_policy_raw.txt"
    
    print(f"작업 시작: {raw_pdf_path} 추출 중...")
    
    # 1. PDF 텍스트 추출
    extracted_text = extract_text_from_pdf(raw_pdf_path)
    
    # 2. 결과 저장 (나중에 눈으로 확인하기 위해 txt로 저장)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
        
    print(f"완료! 추출된 텍스트가 {output_path}에 저장되었습니다.")

if __name__ == "__main__":
    run_ingestion()