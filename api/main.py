"""
FastAPI application factory and setup.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent_app.config import settings
from agent_app.api.routers import root, health, agent

from dotenv import load_dotenv
from pathlib import Path

# Load .env file from agent_app directory
_agent_root = Path(__file__).resolve().parent
load_dotenv(_agent_root / ".env")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    print(f"🚀 Starting {settings.app_title} v{settings.app_version}")
    
    # Ensure directories exist
    settings.data_dir_path.mkdir(exist_ok=True)
    settings.vector_store_path_obj.mkdir(parents=True, exist_ok=True)
    
    yield
    
    # Shutdown
    print(f"👋 Shutting down {settings.app_title}")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
        lifespan=lifespan,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Register routers
    app.include_router(root.router)
    app.include_router(health.router)
    app.include_router(agent.router)
    
    return app


# Create the application instance
app = create_app()
