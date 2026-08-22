"""Router /ingest — upload et indexation de documents PDF."""

from __future__ import annotations

from fastapi import APIRouter, File, Form, UploadFile

from coursegraph.api.schemas.ingest import IngestResponse

router = APIRouter()


@router.post("/", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),  # noqa: B008
    doc_type: str = Form(..., description="cours | annale | correction"),
    course_name: str = Form(...),
    year: int | None = Form(None),
) -> IngestResponse:
    """Ingère un PDF, le découpe en chunks, détecte les chapitres et indexe dans Qdrant."""
    pass  # type: ignore[return-value]
