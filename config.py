"""
Configuration settings for the application.
"""
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Settings
    app_title: str = "Agent App API"
    app_description: str = "RAG-powered Q&A agent with PDF retrieval and web search fallback"
    app_version: str = "1.0.0"
    
    # CORS Settings
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    # Directory Settings
    data_dir: str = "data"
    vector_store_path: str = "vector_store/faiss"
    
    # OpenAI Settings (from environment)
    openai_api_key: Optional[str] = None
    
    @property
    def data_dir_path(self) -> Path:
        """Get data directory as Path object."""
        return Path(self.data_dir)
    
    @property
    def vector_store_path_obj(self) -> Path:
        """Get vector store path as Path object."""
        return Path(self.vector_store_path)


# Global settings instance
settings = Settings()
