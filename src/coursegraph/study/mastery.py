"""Radar de maîtrise par chapitre et plan de révision priorisé."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChapterMastery:
    chapter: str
    mastery_score: float      # [0, 1]
    recurrence_score: float   # [0, 1]
    priority_score: float     # recurrence * (1 - mastery)
    n_attempts: int


def compute_mastery(
    session_id: str,
    course_name: str,
) -> list[ChapterMastery]:
    """Calcule le score de maîtrise par chapitre à partir des réponses de l'utilisateur."""
    pass  # type: ignore[return-value]


def build_revision_plan(mastery: list[ChapterMastery]) -> list[ChapterMastery]:
    """Trie les chapitres par priorite decroissante (recurrence * (1 - maitrise))."""
    pass  # type: ignore[return-value]


def update_mastery_from_quiz(
    session_id: str,
    chapter: str,
    score: float,
) -> None:
    """Met à jour le score de maîtrise en base après une session de quiz."""
    pass
