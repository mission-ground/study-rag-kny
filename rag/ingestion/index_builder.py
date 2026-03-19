import fitz  # PyMuPDF
import re
import unicodedata
import os
from rag.ingestion.chunker import Chunker

class IndexBuilder:
    def __init__(self):
        # PDF 파일들이 모여있는 경로
        self.raw_data_path = "data/raw/pdf/"
        self.chunker = Chunker()

    def load_and_chunk(self):
        """1. 추출 -> 2. 전처리 -> 3. 청킹 과정을 하나로 연결"""
        all_chunks = []
        
        # 폴더 내의 모든 PDF 파일을 찾아서 반복
        for filename in os.listdir(self.raw_data_path):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(self.raw_data_path, filename)
                print(f"🔍 {filename} 분석 시작...")
                
                # [STEP 1] PDF 열기 및 텍스트 추출
                doc = fitz.open(pdf_path)
                
                for page_num, page in enumerate(doc):
                    raw_text = page.get_text()
                    
                    if not raw_text.strip():
                        continue
                        
                    # [STEP 2] 전처리 (Cleaning)
                    # 유니코드 정규화 및 불필요한 공백/줄바꿈 제거
                    text = unicodedata.normalize("NFC", raw_text)
                    text = re.sub(r'\s+', ' ', text).strip()
                    
                    # [STEP 3] 청킹 (Chunking)
                    # split(text, page_number) 함수 호출
                    # 이 함수는 [{text:..., page:..., chunk:...}, ...] 형태의 리스트를 반환함
                    page_chunks = self.chunker.split(text, page_num + 1)
                    
                    # 각 청크에 어떤 파일에서 왔는지 정보(source)를 추가로 기록
                    for c in page_chunks:
                        c["source"] = filename
                    
                    # 전체 리스트에 합치기
                    all_chunks.extend(page_chunks)
                
                doc.close()
                
        print(f"✅ 총 {len(all_chunks)}개의 데이터 조각(Chunk) 생성 완료!")
        return all_chunks