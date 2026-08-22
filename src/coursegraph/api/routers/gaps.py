"""Router /gaps — lacunes et plan de révision priorisé."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/{course_name}")
async def get_gaps(course_name: str, session_id: str) -> dict:  # type: ignore[type-arg]
    """Retourne le radar de maîtrise par chapitre et le plan de révision priorisé."""
    pass  # type: ignore[return-value]
