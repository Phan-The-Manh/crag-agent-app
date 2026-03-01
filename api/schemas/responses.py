"""
Response schemas for API endpoints.
"""
from pydantic import BaseModel, Field


class RunResponse(BaseModel):
    """Response model for agent execution."""
    
    answer: str = Field(..., description="The agent's answer")
    thread_id: str = Field(..., description="Thread ID for conversation continuity")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Automatic prompt design is a technique for...",
                "thread_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="API status")
    vector_store_ready: bool = Field(..., description="Whether vector store is loaded")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "vector_store_ready": True
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    detail: str = Field(..., description="Error message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Question cannot be empty"
            }
        }


class RootResponse(BaseModel):
    """Response model for root endpoint."""
    
    message: str
    docs: str
    health: str
    run: str
