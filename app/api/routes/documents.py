from fastapi import APIRouter, UploadFile, status

from app.core.exceptions import NotImplementedFeatureError
from app.schemas.documents import DocumentIngestResponse, DocumentListResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "/ingest",
    response_model=DocumentIngestResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Ingest a Document",
    description="Uploads and indexes a PDF, DOCX, TXT, or MD document into Qdrant.",
)
async def ingest_document(file: UploadFile) -> DocumentIngestResponse:
    raise NotImplementedFeatureError(
        feature_name="Document Ingestion Pipeline",
        planned_milestone="Day 3+",
    )


@router.get(
    "",
    response_model=DocumentListResponse,
    summary="List Ingested Documents",
    description="Retrieves a list of all documents currently indexed in the vector store.",
)
async def list_documents() -> DocumentListResponse:
    raise NotImplementedFeatureError(
        feature_name="Document Retrieval and Listing",
        planned_milestone="Day 3+",
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Delete a Document",
    description="Removes a document and its embeddings from the vector store.",
)
async def delete_document(document_id: str) -> dict[str, str]:
    raise NotImplementedFeatureError(
        feature_name="Document Deletion",
        planned_milestone="Day 3+",
    )
