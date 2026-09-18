from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class DependencyStatus(BaseModel):
    """Status of an external service dependency (PostgreSQL, Qdrant, Ollama)."""

    name: str
    status: Literal["healthy", "unhealthy", "unreachable", "not_checked"]
    details: dict[str, Any] = Field(default_factory=dict)
    latency_ms: float | None = None


class HealthResponse(BaseModel):
    """Application health status response."""

    status: Literal["ok", "degraded", "error"]
    version: str = "0.1.0"
    environment: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    dependencies: list[DependencyStatus] = Field(default_factory=list)


class ErrorDetail(BaseModel):
    """Standardized error payload schema."""

    message: str
    status_code: int
    details: dict[str, Any] = Field(default_factory=dict)
    path: str | None = None


class ErrorResponse(BaseModel):
    """Top-level error response model."""

    error: ErrorDetail
