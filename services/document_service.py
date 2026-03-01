"""
Document service for handling PDF processing and vector store management.
"""
import os
from pathlib import Path
from fastapi import HTTPException, UploadFile

from agent_app.doc_process import store_pdf_to_faiss
from agent_app.llm.models import reload_retriever
from agent_app.config import settings


class DocumentService:
    """Service for managing document processing."""
    
    def __init__(self):
        """Initialize the document service and ensure directories exist."""
        self.data_dir = settings.data_dir_path
        self.vector_store_path = settings.vector_store_path_obj
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
    
    def process_pdf(self, document: UploadFile) -> str:
        """
        Process a PDF file and add it to the vector store.
        
        Args:
            document: The uploaded PDF file
            
        Returns:
            The path where the PDF was saved
            
        Raises:
            HTTPException: If the file is not a PDF or processing fails
        """
        # Validate file type
        if document.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )
        
        # Save the uploaded file
        pdf_path = self.data_dir / (document.filename or "uploaded.pdf")
        
        try:
            with open(pdf_path, "wb") as f:
                f.write(document.file.read())
            
            # Process and store in FAISS
            store_pdf_to_faiss(
                pdf_path=str(pdf_path),
                vector_store_path=str(self.vector_store_path),
            )
            
            # Reload the retriever to include new documents
            reload_retriever()
            
            return str(pdf_path)
            
        except Exception as e:
            # Clean up the file if processing failed
            if pdf_path.exists():
                pdf_path.unlink()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process PDF: {str(e)}"
            )
