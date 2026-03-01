"""
Main entry point for the restructured Agent App API.

Run with:
    uvicorn main:app --reload
    
Or from project root:
    uvicorn agent_app.main:app --reload
"""

from dotenv import load_dotenv
from pathlib import Path

# Load .env file from agent_app directory
_agent_root = Path(__file__).resolve().parent
load_dotenv(_agent_root / ".env")

from agent_app.api.main import app

# This allows running with: uvicorn main:app
__all__ = ["app"]
