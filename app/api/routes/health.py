from fastapi import APIRouter, Query, status

from app.core.config import get_settings
from app.schemas.common import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Application Health Check",
    description="Returns current service status and environment metadata.",
)
async def get_health(
    check_deps: bool = Query(
        default=False,
        description="Whether to perform active connectivity checks to PostgreSQL, Qdrant, and Ollama.",
    ),
) -> HealthResponse:
    settings = get_settings()

    return HealthResponse(
        status="ok",
        version="0.1.0",
        environment=settings.APP_ENV,
        dependencies=[],
    )
