import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ManualEmbedder:
    """
    LangChain 없이 OpenAI API를 직접 호출하여 텍스트를 벡터로 변환하는 클래스입니다.
    """
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def embed_text(self, text: str) -> list:
        """
        단일 문장을 벡터(List[float])로 변환합니다. (주로 사용자 질문 검색용)
        """
        # API 호출: 랭체인 내부에서 실행되는 실제 로직
        response = self.client.embeddings.create(
            input=[text.replace("\n", " ")], # 줄바꿈 제거는 임베딩 품질에 도움이 됩니다.
            model=self.model
        )
        # response.data[0].embedding에 1536개의 숫자가 들어있습니다.
        return response.data[0].embedding

    def embed_documents(self, texts: list) -> list:
        """
        여러 개의 문서 조각(Chunks)을 한꺼번에 벡터화합니다.
        """
        # 리스트 형태의 텍스트를 한 번에 전달하여 API 호출 횟수를 줄입니다.
        response = self.client.embeddings.create(
            input=[t.replace("\n", " ") for t in texts],
            model=self.model
        )
        
        # 각 텍스트에 대응하는 벡터값들만 추출하여 리스트로 반환
        return [item.embedding for item in response.data]