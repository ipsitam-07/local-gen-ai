from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base exception for all domain-specific application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class ServiceUnavailableException(AppException):
    """Raised when an external dependency (PostgreSQL, Qdrant, Ollama) is unreachable."""

    def __init__(self, service_name: str, reason: str = "Service unreachable") -> None:
        super().__init__(
            message=f"External dependency '{service_name}' is currently unavailable: {reason}",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"service": service_name, "reason": reason},
        )


class DocumentValidationError(AppException):
    """Raised when an uploaded document fails format, corruption, or size validation."""

    def __init__(self, filename: str, reason: str) -> None:
        super().__init__(
            message=f"Validation failed for document '{filename}': {reason}",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"filename": filename, "reason": reason},
        )


class EntityNotFoundError(AppException):
    """Raised when a requested resource (document, order, customer) does not exist."""

    def __init__(self, entity_type: str, entity_id: str | int) -> None:
        super().__init__(
            message=f"{entity_type} with identifier '{entity_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"entity_type": entity_type, "entity_id": str(entity_id)},
        )


class NotImplementedFeatureError(AppException):
    """Raised for endpoints planned for future milestones (Day 3+)."""

    def __init__(self, feature_name: str, planned_milestone: str = "Day 3+") -> None:
        super().__init__(
            message=f"Feature '{feature_name}' is not yet implemented.",
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            details={
                "feature": feature_name,
                "planned_milestone": planned_milestone,
                "status": "planned",
            },
        )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Global handler for all domain AppException subclasses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "status_code": exc.status_code,
                "details": exc.details,
                "path": request.url.path,
            }
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected Python errors to prevent stack trace leakage."""
    import logging

    logger = logging.getLogger("app.core.unhandled")
    logger.exception("Unhandled server error encountered while processing request: %s", exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "An unexpected internal server error occurred. Please consult server logs.",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "path": request.url.path,
            }
        },
    )
