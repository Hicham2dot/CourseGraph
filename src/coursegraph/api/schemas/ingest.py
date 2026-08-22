"""Schémas d'ingestion."""

from __future__ import annotations

from pydantic import BaseModel


class IngestResponse(BaseModel):
    doc_id: str
    doc_type: str
    course_name: str
    n_chunks: int
    chapters: list[str]
    message: str
