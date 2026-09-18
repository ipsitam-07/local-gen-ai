from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """Extracted metadata for an ingested document."""

    filename: str
    file_type: Literal["pdf", "docx", "txt", "md"]
    file_size_bytes: int
    chunk_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class DocumentIngestResponse(BaseModel):
    """Response returned after document ingestion."""

    document_id: str
    filename: str
    status: Literal["success", "processing", "failed"]
    chunks_created: int
    message: str


class DocumentListItem(BaseModel):
    """Summary item for listed documents."""

    document_id: str
    filename: str
    file_type: str
    file_size_bytes: int
    ingested_at: datetime


class DocumentListResponse(BaseModel):
    """List of all indexed documents in the assistant."""

    documents: list[DocumentListItem] = Field(default_factory=list)
    total_count: int = 0
