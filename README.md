# RAG Project

문서에서 사용자의 질문과 관련된 내용을 검색하고,
검색 결과를 기반으로 답변을 생성하는 RAG 시스템 구현 프로젝트입니다.

## Features

- TXT, PDF, CSV 문서 로딩
- 웹페이지 URL의 텍스트 추출
- Sentence Transformer를 이용한 문서 및 질문 임베딩
- FAISS를 이용한 Top-K 유사 문서 검색
- 유사도 임계값을 이용한 검색 결과 필터링
- 임베딩 캐시 저장 및 재사용
- Ollama 로컬 LLM을 이용한 답변 생성
- 검색 결과의 출처와 원문 위치 표시

## Supported Input Types

| Input type | Chunking method |
|---|---|
| TXT | 빈 줄로 구분된 문단 단위 |
| PDF | 페이지 단위 |
| CSV | 행 단위 |
| URL | 제목, 문단, 목록 HTML 요소 단위 |

PDF와 CSV는 각각 페이지 번호와 원본 행 번호를 메타데이터로 저장하며,
검색 결과와 함께 원문 위치를 표시합니다.

## RAG Pipeline

```text
Document or URL
        ↓
Document Loader
        ↓
Text Chunks
        ↓
Sentence Transformer
        ↓
Embedding Cache
        ↓
FAISS Similarity Search
        ↓
Similarity Filtering
        ↓
Prompt Construction
        ↓
Ollama Local LLM
        ↓
Generated Answer
```

## Project Structure

```text
RagProject/
├── data/
│   ├── test.txt
│   ├── test.pdf
│   └── test.csv
├── src/
│   ├── document_loader.py
│   ├── embedder.py
│   ├── embedding_cache.py
│   ├── generator.py
│   ├── main.py
│   ├── prompt_builder.py
│   ├── retriever.py
│   └── test_llm.py
├── .gitignore
├── README.md
└── requirements.txt
```

### Main Components

- `document_loader.py`: TXT, PDF, CSV 및 URL에서 텍스트와 메타데이터 추출
- `embedder.py`: 문서와 질문을 임베딩 벡터로 변환
- `embedding_cache.py`: 생성된 문서 임베딩 저장 및 재사용
- `retriever.py`: FAISS를 이용한 유사 문서 검색
- `prompt_builder.py`: 검색 결과를 바탕으로 LLM 프롬프트 구성
- `generator.py`: Ollama 로컬 LLM을 이용한 답변 생성
- `main.py`: 전체 RAG 파이프라인 실행