"""
Complete FastAPI for the RAG Agent.
Run with: uvicorn agent_app.fasiapi:api --reload
"""

from dotenv import load_dotenv
from pathlib import Path

# Load .env file from agent_app directory
_agent_root = Path(__file__).resolve().parent
load_dotenv(_agent_root / ".env")

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
import os
import uuid

from agent_app.graph.graph_app import app as agent_graph
from agent_app.doc_process import store_pdf_to_faiss
from agent_app.llm.models import reload_retriever


# -----------------------------------------------------------------------------
# App Setup
# -----------------------------------------------------------------------------
api = FastAPI(
    title="Agent App API",
    description="RAG-powered Q&A agent with PDF retrieval and web search fallback",
    version="1.0.0",
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
VECTOR_STORE_PATH = "vector_store/faiss"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)


# -----------------------------------------------------------------------------
# Schemas
# -----------------------------------------------------------------------------
class RunResponse(BaseModel):
    answer: str
    thread_id: str


class HealthResponse(BaseModel):
    status: str
    vector_store_ready: bool


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@api.get("/", tags=["Root"])
def root():
    """Root endpoint with API info."""
    return {
        "message": "Agent App API",
        "docs": "/docs",
        "health": "/health",
        "run": "POST /run",
    }


@api.get("/health", response_model=HealthResponse, tags=["Health"])
def health():
    """Check API and vector store status."""
    from agent_app.llm.models import retriever
    return HealthResponse(
        status="ok",
        vector_store_ready=retriever is not None,
    )


@api.post("/run", response_model=RunResponse, tags=["Agent"])
def run_agent(
    question: str = Form(..., description="Your question"),
    document: UploadFile | None = File(None, description="Optional PDF to ingest before answering"),
    thread_id: str | None = Form(None, description="Optional thread ID for conversation continuity"),
):
    """
    Run the RAG agent on a question.

    - **question**: Required. The user's question.
    - **document**: Optional. PDF file to add to the vector store before answering.
    - **thread_id**: Optional. Stable ID for multi-turn conversations.

    Returns the agent's answer.
    """
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # 1. Handle PDF upload if provided
    if document is not None:
        if document.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        pdf_path = os.path.join(DATA_DIR, document.filename or "uploaded.pdf")

        try:
            with open(pdf_path, "wb") as f:
                f.write(document.file.read())

            store_pdf_to_faiss(
                pdf_path=pdf_path,
                vector_store_path=VECTOR_STORE_PATH,
            )
            reload_retriever()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    # 2. Run the agent
    tid = thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": tid}}
    inputs = {
        "messages": [HumanMessage(content=question.strip())],
    }

    try:
        # Stream to end and get final state
        final_state = None
        for output in agent_graph.stream(inputs, config=config):
            final_state = output

        if not final_state:
            raise HTTPException(status_code=500, detail="Agent produced no output")

        # Extract the last message (AI response) from the last node's output
        last_output = list(final_state.values())[0]
        messages = last_output.get("messages", [])
        if not messages:
            raise HTTPException(status_code=500, detail="Agent produced no response")

        answer = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1])
        return RunResponse(answer=answer, thread_id=tid)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
