from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


class SourceCitation(BaseModel):
    """Source reference for RAG grounded answers."""

    source_type: Literal["document", "database", "hybrid"]
    document_name: str | None = None
    page_number: int | None = None
    table_name: str | None = None
    snippet: str | None = None


class ChatRequest(BaseModel):
    """Incoming user chat query."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="The natural language question from the user.",
        examples=["What is the company leave policy?", "Who are the top 5 customers by revenue?"],
    )
    conversation_id: str | None = Field(
        default=None,
        description="Optional conversation ID for multi-turn state tracking.",
    )


class ChatResponse(BaseModel):
    """Assistant chat response."""

    answer: str
    conversation_id: str
    route_used: Literal["rag", "sql", "hybrid", "direct"]
    sources: list[SourceCitation] = Field(default_factory=list)
    sql_query: str | None = Field(
        default=None,
        description="SQL query generated if route was SQL or Hybrid.",
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
