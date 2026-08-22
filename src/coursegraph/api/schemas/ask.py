"""Schémas de chat RAG."""

from __future__ import annotations

from pydantic import BaseModel


class Source(BaseModel):
    doc_type: str
    course_name: str
    chapter: str
    page: int
    score: float
    excerpt: str


class AskRequest(BaseModel):
    question: str
    course_name: str | None = None
    session_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]
    abstained: bool
    faithfulness_score: float | None = None
