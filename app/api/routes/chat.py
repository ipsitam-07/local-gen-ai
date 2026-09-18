from fastapi import APIRouter

from app.core.exceptions import NotImplementedFeatureError
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "",
    response_model=ChatResponse,
    summary="Chat with Documents & Data",
    description="Submits a natural-language query to the assistant.",
)
async def chat(request: ChatRequest) -> ChatResponse:
    raise NotImplementedFeatureError(
        feature_name="Natural Language Assistant (RAG & Text-to-SQL)",
        planned_milestone="Day 3+",
    )
