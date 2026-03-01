"""
Dependency injection functions for FastAPI routes.
"""
from typing import Annotated
from fastapi import Depends

from agent_app.services.agent_service import AgentService
from agent_app.services.document_service import DocumentService


# Service instances (singleton pattern)
_agent_service_instance = None
_document_service_instance = None


def get_agent_service() -> AgentService:
    """
    Dependency that provides the AgentService instance.
    
    Returns:
        AgentService instance
    """
    global _agent_service_instance
    if _agent_service_instance is None:
        _agent_service_instance = AgentService()
    return _agent_service_instance


def get_document_service() -> DocumentService:
    """
    Dependency that provides the DocumentService instance.
    
    Returns:
        DocumentService instance
    """
    global _document_service_instance
    if _document_service_instance is None:
        _document_service_instance = DocumentService()
    return _document_service_instance


# Type aliases for dependency injection
AgentServiceDep = Annotated[AgentService, Depends(get_agent_service)]
DocumentServiceDep = Annotated[DocumentService, Depends(get_document_service)]
