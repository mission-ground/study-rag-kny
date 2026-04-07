import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

class FAISSVectorStore:
    def __init__(self):
        # 한국어 성능이 좋은 OpenAI의 최신 임베딩 모델 사용
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = None

    def create_index(self, chunks):
        """텍스트 청크 리스트를 받아 벡터 인덱스 생성"""
        print(f"{len(chunks)}개의 청크로 벡터 인덱스를 생성합니다...")
        self.vector_store = FAISS.from_texts(chunks, self.embeddings)
        return self.vector_store

    def save_index(self, folder_path):
        """생성된 인덱스를 로컬 파일로 저장"""
        if self.vector_store:
            self.vector_store.save_local(folder_path)
            print(f"인덱스가 {folder_path}에 저장되었습니다.")

    def load_index(self, folder_path):
        """저장된 인덱스 파일 불러오기"""
        self.vector_store = FAISS.load_local(
            folder_path, self.embeddings, allow_dangerous_deserialization=True
        )
        return self.vector_store