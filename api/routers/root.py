"""
Root router for basic API information.
"""
from fastapi import APIRouter

from agent_app.api.schemas.responses import RootResponse


router = APIRouter(tags=["Root"])


@router.get("/", response_model=RootResponse)
def root():
    """Root endpoint with API information."""
    return RootResponse(
        message="Agent App API",
        docs="/docs",
        health="/health",
        run="POST /run",
    )
