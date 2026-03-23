# Agent App – Conversational RAG API

A production-ready **FastAPI** service that exposes a **Conversational Retrieval-Augmented Generation (cRAG)** agent.

The system ingests PDFs into a **FAISS vector store**, retrieves relevant chunks using **OpenAI embeddings**, and uses a **graph-based agent** to produce context-aware, multi-turn answers.

---

## CRAG Architecture

```mermaid
graph LR
    %% Node Definitions
    I([<b>Input</b>])
    R{<b>Retrieve ?</b>}
    RET[[<b>Retriever</b>]]
    G1[[<b>Grader</b>]]
    S{<b>Sufficient</b>}
    WS[[<b>Web search</b>]]
    A([<b>Answer</b>])

    %% Flow
    I --> R
    R -- Yes --> RET
    RET --> G1
    G1 --> S
    S -- Yes --> A
    S -- No --> WS
    WS --> A
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

## Limitations

- **Simple architecture** (baseline cRAG; limited advanced routing/verification)
- **Single document** focus (best for **simple queries** grounded in one uploaded PDF)
- **Not optimized** for **multi-document** reasoning, **complex/multi-hop** questions, or heavy **production-scale** workloads


