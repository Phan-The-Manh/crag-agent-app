"""
Health check router.
"""
from fastapi import APIRouter

from agent_app.api.schemas.responses import HealthResponse
from agent_app.llm.models import retriever


router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health():
    """
    Check API and vector store status.
    
    Returns:
        HealthResponse with status and vector store readiness
    """
    return HealthResponse(
        status="ok",
        vector_store_ready=retriever is not None,
    )
