"""Mapping automatique exercice d'annale → chapitre(s) du cours."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExerciseMapping:
    exercise_id: str
    exercise_text: str
    top_chapters: list[tuple[str, float]]  # [(chapter_title, score), ...]
    top_chapter: str
    confidence: float


async def map_exercise_to_chapters(
    exercise_text: str,
    course_name: str,
    top_k: int = 3,
) -> ExerciseMapping:
    """Mappe un exercice au(x) chapitre(s) du cours par retrieval + vote pondéré."""
    pass  # type: ignore[return-value]


async def map_all_exercises(
    annale_doc_id: str,
    course_name: str,
) -> list[ExerciseMapping]:
    """Mappe tous les exercices d'une annale aux chapitres du cours correspondant."""
    pass  # type: ignore[return-value]
