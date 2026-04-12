import faiss
import numpy as np
import pickle
import os
from typing import Any

class ManualVectorStore:
    """
    LangChain 프레임워크 없이 FAISS 라이브러리를 직접 제어하는 벡터 스토어 클래스입니다.
    """
    def __init__(self, dimension: int = 1536):
        # IndexFlatL2: 유클리드 거리를 기반으로 하는 가장 기본적인 FAISS 인덱스
        self.index: Any = faiss.IndexFlatL2(dimension)
        # 벡터와 1:1로 매핑될 실제 텍스트 조각들을 저장하는 리스트
        self.chunks = []

    def add_vectors_with_text(self, vectors: list, texts: list):
        """
        임베딩 벡터와 그에 대응하는 원문 텍스트를 인덱스에 저장합니다.
        """
        if len(vectors) != len(texts):
            raise ValueError("벡터와 텍스트의 개수가 일치하지 않습니다.")

        # FAISS는 float32 타입의 numpy 배열을 입력으로 받습니다.
        vector_np = np.array(vectors).astype('float32')
        
        # 1. FAISS 인덱스에 벡터 추가
        self.index.add(vector_np)
        # 2. 검색 시 꺼내올 원문 텍스트를 별도 리스트에 순서대로 보관
        self.chunks.extend(texts)

    def search_similar_chunks(self, query_vector: list, k: int = 3):
        """
        쿼리 벡터와 가장 유사한 상위 k개의 텍스트 조각을 찾아 반환합니다.
        """
        query_np = np.array([query_vector]).astype('float32')
        
        # distances: 유사도 거리(값이 작을수록 유사), indices: 인덱스 번호
        distances, indices = self.index.search(query_np, k)
        
        results = []
        for idx in indices[0]:
            if idx != -1: # 검색 결과가 있는 경우만 추가
                results.append(self.chunks[idx])
        return results

    def save_to_local(self, folder_path: str):
        """
        인덱스(수학적 지도)와 메타데이터(텍스트)를 로컬 파일로 영구 저장합니다.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 1. 벡터 데이터(Index) 저장
        faiss.write_index(self.index, os.path.join(folder_path, "index.faiss"))
        # 2. 텍스트 데이터(Metadata) 저장 - 파이썬 객체 직렬화(Pickle) 사용
        with open(os.path.join(folder_path, "index.pkl"), "wb") as f:
            pickle.dump(self.chunks, f)

    def load_from_local(self, folder_path: str):
        """
        로컬에 저장된 faiss 및 pkl 파일을 로드하여 메모리에 올립니다.
        """
        index_file = os.path.join(folder_path, "index.faiss")
        pkl_file = os.path.join(folder_path, "index.pkl")

        if not os.path.exists(index_file) or not os.path.exists(pkl_file):
            raise FileNotFoundError("인덱스 파일을 찾을 수 없습니다.")

        self.index = faiss.read_index(index_file)
        with open(pkl_file, "rb") as f:
            self.chunks = pickle.load(f)