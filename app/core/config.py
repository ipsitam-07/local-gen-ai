from typing import Literal
from functools import lru_cache
from pathlib import Path
from typing import Dict

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8"
    )

    #Application settings
    APP_NAME: str = "Local GenAI Data Assistant"
    APP_ENV: Literal["development", "production", "testing"] = "development"
    DEBUG: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    #PostgreSQL settings
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "genai_data"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres_password"

    # PostgreSQL (Read-Only User for future SQL Agent)
    POSTGRES_RO_USER: str = "genai_reader"
    POSTGRES_RO_PASSWORD: str = "reader_password"

    # Qdrant Vector Store
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_GRPC_PORT: int = 6334
    QDRANT_COLLECTION_NAME: str = "documents"
    
    # Ollama Local LLM
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text"
    OLLAMA_TIMEOUT_SECONDS: int = 60

    # Storage Paths
    DOCUMENTS_DIR: str = "data/documents"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL using psycopg v3 driver."""
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    @computed_field  # type: ignore[prop-decorator]
    @property
    def ro_database_url(self) -> str:
        """Construct read-only PostgreSQL connection URL for future SQL Agent."""
        return (
            f"postgresql+psycopg://{self.POSTGRES_RO_USER}:{self.POSTGRES_RO_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    @computed_field  # type: ignore[prop-decorator]
    @property
    def documents_path(self) -> Path:
        """Return resolved Path object for documents directory."""
        return Path(self.DOCUMENTS_DIR).resolve()

        
@lru_cache
def get_settings() -> Settings:
    """Cached singleton instance of application settings."""
    return Settings()