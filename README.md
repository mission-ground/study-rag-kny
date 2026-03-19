# RAG Lab

Retrieval-Augmented Generation(RAG) 구조를 학습하고 실험하기 위한 프로젝트입니다.  
문서 처리, 임베딩 생성, 벡터 검색, LLM 응답 생성까지의 전체 RAG 파이프라인을 구현하고 다양한 실험을 진행합니다.

---

## Project Structure

api  
FastAPI 기반 사용자 질의 인터페이스

core  
프로젝트 설정 및 공통 구성

rag  
RAG 파이프라인 핵심 로직

data  
문서 데이터 및 전처리 결과

scripts  
데이터 ingestion 및 인덱스 생성 스크립트

docs  
실험 기록 및 참고 자료

---

## RAG Pipeline

전체 처리 흐름

Document  
↓  
Chunking  
↓  
Embedding  
↓  
Vector Store  
↓  
Retriever  
↓  
LLM Generator  
↓  
Response

---

## Directory Details

rag/

embeddings  
문서 임베딩 생성

vectorstores  
벡터 데이터베이스 관리 (FAISS 등)

ingestion  
문서 로딩 및 chunk 생성

retrieval  
벡터 검색 기반 문서 retrieval

generation  
LLM 기반 답변 생성

---

## Data Structure

data/

raw  
원본 문서

processed  
전처리된 텍스트

chunks  
chunk 단위 데이터

---

## Tech Stack

Python  
FastAPI  
FAISS  
LLM / Embedding Model

---

## Purpose

- RAG 구조 학습
- 문서 기반 질의응답 시스템 이해
- 검색 + 생성 기반 LLM 아키텍처 실험

---

## Project Structure

```
rag-lab/
├── api/                    # FastAPI 기반 사용자 질의 API
│   └── routes/
│       └── chat.py         # 질문 요청을 받아 RAG 파이프라인 호출
│
├── core/                   # 공통 설정 및 환경 설정
│   └── config.py           # API 키, 경로, 모델 설정 등
│
├── rag/                    # RAG(Retrieval-Augmented Generation) 핵심 로직
│   ├── rag_pipeline.py     # 전체 RAG 파이프라인 오케스트레이션
│   │
│   ├── embeddings/         # 문서를 벡터로 변환하는 임베딩 모듈
│   │   └── embedder.py
│   │
│   ├── vectorstores/       # 벡터 데이터베이스 관리
│   │   └── faiss/
│   │       └── vector_store.py
│   │
│   ├── ingestion/          # 문서 수집 및 전처리
│   │   ├── chunker.py      # 문서를 chunk 단위로 분할
│   │   └── index_builder.py# 벡터 인덱스 생성
│   │
│   ├── retrieval/          # 사용자 질문과 관련된 문서 검색
│   │   └── retriever.py
│   │
│   └── generation/         # 검색된 문서를 기반으로 LLM 답변 생성
│       └── generator.py
│
├── data/                   # RAG 실험에 사용하는 데이터
│   ├── raw/                # 원본 문서
│   │   └── pdf/
│   │
│   ├── processed/          # 전처리된 텍스트 데이터
│   │   └── text/
│   │
│   └── chunks/             # chunk 단위로 분리된 데이터
│
├── scripts/                # 데이터 처리 및 인덱스 생성 스크립트
│   ├── ingest_data.py      # 문서 수집 및 전처리 실행
│   └── build_index.py      # 벡터 인덱스 생성 실행
│
├── docs/                   # 실험 기록, 참고 자료
│
├── requirements.txt        # Python 의존성 패키지 목록
└── README.md               # 프로젝트 설명
```