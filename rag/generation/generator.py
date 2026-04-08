from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class RAGGenerator:
    def __init__(self):
        # 답변 생성을 위한 모델 설정 (속도가 빠른 gpt-4o-mini 추천)
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # AI에게 부여할 역할과 답변 지침(Prompt) 설정
        self.template = """
        당신은 대한민국 정부의 '2026년 민생 체감 정책' 전문 상담사입니다.
        반드시 아래 제공된 [Context]의 내용만을 바탕으로 질문에 답변하세요.
        답변할 수 있는 근거가 없으면 "관련 정책 내용을 찾을 수 없습니다"라고 답하세요.
        
        [Context]
        {context}
        
        질문: {question}
        
        답변:
        """
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.parser = StrOutputParser()

    def generate_answer(self, question, context_docs):
        # 검색된 문서들을 하나의 텍스트로 합치기
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        # 체인 생성 및 실행
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({"context": context_text, "question": question})