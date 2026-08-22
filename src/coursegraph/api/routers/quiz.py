"""Router /quiz — génération et soumission de QCM."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/generate")
async def generate_quiz(course_name: str, chapter: str | None = None, n_questions: int = 5) -> dict:  # type: ignore[type-arg]
    """Génère un QCM ancré dans le corpus pour un cours (et optionnellement un chapitre)."""
    pass  # type: ignore[return-value]


@router.post("/submit")
async def submit_quiz(session_id: str, answers: dict[str, str]) -> dict:  # type: ignore[type-arg]
    """Enregistre les réponses et met à jour le radar de maîtrise."""
    pass  # type: ignore[return-value]
