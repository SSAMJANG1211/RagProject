# RAG Project

문서에서 사용자의 질문과 관련된 내용을 검색하고,
검색 결과를 기반으로 답변을 생성하는 RAG 시스템입니다.

## Initial Goal

- 텍스트 문서를 문단 단위로 분할
- Sentence Transformer를 이용한 임베딩 생성
- 질문과 관련된 문단 Top-K 검색
- 검색 결과 출력

## Project Structure

```text
rag-project/
├── data/
├── src/
├── README.md
└── requirements.txt
```

## Current Features

- Load text documents
- Generate sentence embeddings
- Retrieve Top-K documents using cosine similarity
- Similarity threshold filtering