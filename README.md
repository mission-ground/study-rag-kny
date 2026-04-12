# RAG Study

본 프로젝트는 단순히 결과물을 만드는 것이 아니라, 
Retrieval-Augmented Generation(RAG) 구조를 학습하고 실험하기 위한 프로젝트입니다.  
문서 처리, 임베딩 생성, 벡터 검색, LLM 응답 생성까지의 전체 RAG 파이프라인을 구현하고 다양한 실험을 진행합니다.

---

## Tech Stack

* **Language:** Python 3.10+
* **Framework:** LangChain, FastAPI
* **Vector DB:** FAISS, ChromaDB
* **LLM & Embedding:** OpenAI (`gpt-4o-mini`, `text-embedding-3-small`)
* **PDF Processing:** pdfplumber

---

## Learning Objectives

1.  **Fundamental RAG:** 외부 라이브러리에 의존하기보다 데이터 추출, 청킹, 임베딩의 흐름을 직접 제어하며 원리를 파악
2.  **Framework Evolution:** 순수 Python 코드에서 시작하여 점진적으로 **LangChain**과 같은 프롬프트 오케스트레이션 도구를 도입하며 생산성 변화를 체감
3.  **Data Versatility:** 2026 민생 정책 가이드를 시작으로, 다양한 도메인의 데이터를 주입하여 검색 품질(Retrieval Quality)을 실험

---

## Learning Steps

### Phase 1: Bare-metal RAG (Current)
* **Target:** 프레임워크 없이 핵심 로직 직접 구현
* **Focus:** `pdfplumber`를 이용한 로우 레벨 텍스트 추출, `FAISS` 바이너리 파일 직접 관리 및 로드
* **Goal:** 벡터 데이터와 메타데이터가 로컬 파일 시스템에서 어떻게 상호작용하는지 이해

### Phase 2: Framework Integration (Next)
* **Target:** **LangChain** 도입 및 고도화
* **Focus:** `Chains`, `LCEL(LangChain Expression Language)`을 활용한 코드 간소화
* **Goal:** 복잡해지는 파이프라인을 프레임워크로 관리하는 방법 학습

### Phase 3: Advanced Optimization
* **Target:** 검색 및 답변 품질 튜닝
* **Focus:** 다양한 청킹 전략(Semantic Chunking), 하이브리드 검색, 답변 평가 지표 도입

---

## Project Structure

```
study-rag-kny/
├── core/                       # 공통 설정 및 환경 설정
│   └── config.py               # API 키, 경로, 모델 설정 등
│
├── rag/                        # RAG(Retrieval-Augmented Generation) 핵심 로직
│   │
│   ├── embeddings/             # 문서를 벡터로 변환하는 임베딩 모듈
│   │   └── embedder.py
│   │
│   ├── vectorstores/           # 단계 3: 벡터 데이터베이스 관리
│   │   └── faiss/              # FAISS 인덱스 생성 및 로드
│   │       └── vector_store.py
│   │
│   ├── ingestion/              # 단계 1-2: 데이터 추출 및 전처리
│   │   ├── chunker.py          # 문서를 chunk 단위로 분할
│   │   └── index_builder.py    # 벡터 인덱스 생성
│   │
│   ├── retrieval/              # 사용자 질문과 관련된 문서 검색
│   │   └── retriever.py
│   │
│   └── generation/             # 단계 4: RAG 기반 답변 생성
│       └── generator.py        # Prompt Engineering 및 LLM 연동
│
├── data/                       # RAG 실험에 사용하는 데이터
│   ├── raw/                    # 원본 문서
│   ├── processed/              # 전처리된 텍스트 데이터
│   └── chunks/                 # chunk 단위로 분리된 데이터
│
├── scripts/                    # 데이터 처리 및 인덱스 생성 스크립트
│   ├── ingest_data.py          # 문서 수집 및 데이터 전처리 테스트
│   ├── build_index.py          # 벡터 인덱스 생성 실행
│   └── test_retrieval.py       # 검색 품질 테스트
│
├── requirements.txt            # Python 의존성 패키지 목록
└── README.md                   # 프로젝트 설명
```

---


## Workflow
1.  **Ingestion:** `pdfplumber`를 이용해 PDF에서 텍스트를 추출합니다.
2.  **Chunking:** 문맥 보존을 위해 `chunk_size: 1000`, `overlap: 100` 규칙으로 텍스트를 분할합니다.
3.  **Embedding & Indexing:** OpenAI 임베딩을 통해 텍스트를 벡터화하고 `FAISS` 로컬 인덱스에 저장합니다.
4.  **Retrieval:** 사용자 질문과 가장 유사한 상위 3개의 청크를 검색합니다.
5.  **Generation:** 검색된 문맥(Context)을 바탕으로 GPT-4o-mini가 최종 답변을 생성합니다.

---


## How to Run

### 1. 환경 설정
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### 2. API 키 설정
루트 디렉토리에 `.env` 파일을 생성합니다.
```text
OPENAI_API_KEY=sk-your-key-here
```

### 3. 인덱스 생성 및 실행
```bash
# 벡터 데이터베이스 구축
python scripts/build_index.py

# 통합 챗봇 실행
python main.py
```

---

## Experiments & Records
* **청킹 전략:** 초기 800자에서 문맥 보존을 위해 1000자로 확장 (총 66개 청크 생성)
* **검색 검증:** `test_retrieval.py`를 통해 부처별 정책 내용이 중복 구간(`overlap`)을 통해 잘 연결되는지 확인 완료
* **프롬프트 지침:** 상담사 페르소나를 부여하고 반드시 제공된 컨텍스트 내에서만 답변하도록 제한(Hallucination 방지)
