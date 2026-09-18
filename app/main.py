from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, documents, health
from app.core.config import get_settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    unhandled_exception_handler,
)
from app.core.logging import get_logger, setup_logging

# Initialize logging on import
setup_logging()
logger = get_logger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown lifecycle events."""
    settings = get_settings()
    logger.info("Starting up %s in [%s] mode...", settings.APP_NAME, settings.APP_ENV)
    yield
    logger.info("Shutting down %s...", settings.APP_NAME)


def create_app() -> FastAPI:
    """Application factory for FastAPI instance."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        description="Local GenAI Data Assistant: RAG over documents and Text-to-SQL over PostgreSQL.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Secure CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.DEBUG else ["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register global exception handlers
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Register routers
    app.include_router(health.router)
    app.include_router(chat.router, prefix="/api/v1")
    app.include_router(documents.router, prefix="/api/v1")

    return app


app = create_app()
