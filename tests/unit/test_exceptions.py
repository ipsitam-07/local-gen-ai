from fastapi import status

from app.core.exceptions import (
    AppException,
    DocumentValidationError,
    NotImplementedFeatureError,
    ServiceUnavailableException,
)


def test_app_exception_defaults() -> None:
    exc = AppException(message="Something failed")
    assert exc.message == "Something failed"
    assert exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.details == {}


def test_service_unavailable_exception() -> None:
    exc = ServiceUnavailableException(service_name="qdrant", reason="Connection refused")
    assert exc.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert exc.details["service"] == "qdrant"


def test_not_implemented_feature_error() -> None:
    exc = NotImplementedFeatureError(feature_name="text_to_sql")
    assert exc.status_code == status.HTTP_501_NOT_IMPLEMENTED
    assert exc.details["planned_milestone"] == "Day 3+"


def test_document_validation_error() -> None:
    exc = DocumentValidationError(filename="malicious.exe", reason="Unsupported extension")
    assert exc.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.details["filename"] == "malicious.exe"
