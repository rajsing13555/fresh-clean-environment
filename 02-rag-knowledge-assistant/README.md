# 📚 RAG-based Enterprise Knowledge Assistant

A Retrieval-Augmented Generation (RAG) system that ingests a company's
internal documents (policies, wikis, reports) and answers employee
questions using **only** that grounded content — not model guesses.

## Why this matters through 2030
RAG is the core pattern behind almost every internal enterprise AI
assistant today, because companies need AI answers grounded in their
own private, changing data — not frozen training data. As long as
companies want to keep data secure and answers accurate, RAG stays relevant.

## Features
- **Document Ingestion** – chunk and index `.txt`/`.md` documents
- **Vector Store** – lightweight local embedding-based retrieval
  (swap in Pinecone/Weaviate/pgvector for production)
- **RAG Query Engine** – retrieves top-k relevant chunks, then asks
  Claude to answer strictly from that context (with citations)
- **CLI Chat Interface** – ask questions interactively

## Tech Stack
- Python 3.10+
- `anthropic` SDK for generation
- `scikit-learn` (TF-IDF, 100% offline, no model downloads) for retrieval
- `numpy` for scoring

> The retrieval layer is deliberately offline/dependency-light so the
> project runs immediately after `pip install`, with zero external
> downloads or internet dependency. For higher-quality semantic search,
> swap in `sentence-transformers` embeddings or a hosted vector DB
> (Pinecone/Weaviate/pgvector) — see Roadmap below.

## Project Structure
```
02-rag-knowledge-assistant/
├── docs/                 # sample company documents
├── rag/
│   ├── __init__.py
│   ├── ingest.py
│   ├── vector_store.py
│   └── query_engine.py
├── main.py
├── requirements.txt
└── README.md
```

## Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key-here"
python main.py
```

## Roadmap / How to extend
- [ ] Swap TF-IDF for `sentence-transformers` embeddings for better semantic recall
- [ ] Swap local vector store for Pinecone/Weaviate/pgvector at scale
- [ ] Add PDF/DOCX ingestion (not just .txt/.md)
- [ ] Add a web UI (Streamlit/FastAPI) for employees
- [ ] Add access-control so users only retrieve docs they're permitted to see
- [ ] Add answer citations pointing back to the source document

## License
MIT
