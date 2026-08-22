"""Router /recurrence — score de récurrence par notion."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/{course_name}")
async def get_recurrence(course_name: str) -> dict:  # type: ignore[type-arg]
    """Retourne le tableau de recurrence des notions (frequence * recence) pour un cours."""
    pass  # type: ignore[return-value]
