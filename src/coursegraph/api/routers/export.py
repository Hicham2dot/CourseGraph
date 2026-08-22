"""Router /export — export Anki (.apkg)."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/anki/{course_name}")
async def export_anki(course_name: str, session_id: str | None = None) -> FileResponse:
    """Génère et télécharge un deck Anki (.apkg) pour un cours."""
    pass  # type: ignore[return-value]
