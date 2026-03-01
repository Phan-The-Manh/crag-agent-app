"""
Request schemas for API endpoints.
"""
from pydantic import BaseModel, Field


class RunRequest(BaseModel):
    """Request model for running the agent (future JSON body support)."""
    
    question: str = Field(..., description="The user's question", min_length=1)
    thread_id: str | None = Field(None, description="Optional thread ID for conversation continuity")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is automatic prompt design?",
                "thread_id": "user-123"
            }
        }
