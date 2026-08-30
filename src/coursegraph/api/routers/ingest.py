"""Router /ingest — upload et indexation de documents PDF."""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from coursegraph.api.schemas.ingest import IngestResponse
from coursegraph.config import get_settings
from coursegraph.ingestion.chunking import chunk_document, compute_doc_id
from coursegraph.ingestion.pdf_parser import parse_pdf
from coursegraph.retrieval.vector_store import upsert_chunks

router = APIRouter()

_VALID_DOC_TYPES = {"cours", "annale", "correction"}


@router.post("/", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),  # noqa: B008
    doc_type: str = Form(..., description="cours | annale | correction"),
    course_name: str = Form(...),
    year: int | None = Form(None),
) -> IngestResponse:
    """Ingère un PDF, le découpe en chunks, détecte les chapitres et indexe dans Qdrant."""
    if doc_type not in _VALID_DOC_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"doc_type invalide : {doc_type!r} (attendu : {sorted(_VALID_DOC_TYPES)})",
        )

    settings = get_settings()
    contents = await file.read()

    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp.flush()
        document = parse_pdf(Path(tmp.name), doc_type, course_name, year)

    chunks = chunk_document(document)
    doc_id = compute_doc_id(document)
    n_indexed = await upsert_chunks(chunks, settings.qdrant_collection)
    chapters = sorted({chunk.chapter for chunk in chunks})

    return IngestResponse(
        doc_id=doc_id,
        doc_type=doc_type,
        course_name=course_name,
        n_chunks=n_indexed,
        chapters=chapters,
        message=f"{n_indexed} chunks indexés depuis {file.filename!r}",
    )
