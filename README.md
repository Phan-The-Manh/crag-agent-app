# Agent App – Conversational RAG API

A production-ready **FastAPI** service that exposes a **Conversational Retrieval-Augmented Generation (cRAG)** agent.

The system ingests PDFs into a **FAISS vector store**, retrieves relevant chunks using **OpenAI embeddings**, and uses a **graph-based agent** to produce context-aware, multi-turn answers.

---

# CRAG Architecture

## Mermaid
```mermaid
graph LR
    %% Node Definitions
    I([<b>Input</b>])
    R{<b>Retrieve ?</b>}
    RET[[<b>Retriever</b>]]
    G1[[<b>Grader</b>]]
    S{<b>Sufficient</b>}
    WS[[<b>Web search</b>]]
    G2[[<b>Grader</b>]]
    A([<b>Answer</b>])

    %% Flow
    I --> R
    R -- Yes --> RET
    RET --> G1
    G1 --> S
    S -- Yes --> A
    S -- No --> WS
    WS --> G2
    G2 --> A
    R -- No --> A
```

## Features

- **FastAPI HTTP API** with Swagger docs (`/docs`)
- **PDF ingestion** into FAISS vector store
- **Conversational RAG (cRAG)** with `thread_id`
- **Graph-based agent flow**
- **OpenAI LLM and embeddings**
- **CORS enabled** for frontend use

---


