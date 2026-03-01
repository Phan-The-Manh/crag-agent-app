"""
Agent router for running the RAG agent.
"""
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from agent_app.api.dependencies import AgentServiceDep, DocumentServiceDep
from agent_app.api.schemas.responses import RunResponse


router = APIRouter(tags=["Agent"], prefix="/agent")


@router.post("/run", response_model=RunResponse)
def run_agent(
    question: str = Form(..., description="Your question"),
    document: UploadFile | None = File(None, description="Optional PDF to ingest before answering"),
    thread_id: str | None = Form(None, description="Optional thread ID for conversation continuity"),
    agent_service: AgentServiceDep = None,
    document_service: DocumentServiceDep = None,
):
    """
    Run the RAG agent on a question.
    
    - **question**: Required. The user's question.
    - **document**: Optional. PDF file to add to the vector store before answering.
    - **thread_id**: Optional. Stable ID for multi-turn conversations.
    
    Returns the agent's answer.
    """
    # Validate question
    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Handle PDF upload if provided
    if document is not None:
        document_service.process_pdf(document)
    
    # Generate or use provided thread_id
    tid = thread_id or str(uuid.uuid4())
    
    # Run the agent
    answer = agent_service.run_agent(question.strip(), tid)
    
    return RunResponse(answer=answer, thread_id=tid)
