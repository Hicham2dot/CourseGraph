"""Calcul du score de recurrence par notion (frequence * recence)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NotionScore:
    notion: str
    chapter: str
    frequency: int
    recency_weight: float
    recurrence_score: float


def compute_recurrence_scores(
    mappings: list[dict],  # type: ignore[type-arg]
    course_name: str,
    decay_factor: float = 0.9,
) -> list[NotionScore]:
    """Calcule le score de récurrence pour chaque notion d'un cours sur l'ensemble des annales."""
    pass  # type: ignore[return-value]


def get_top_notions(course_name: str, top_k: int = 10) -> list[NotionScore]:
    """Retourne les k notions les plus récurrentes d'un cours."""
    pass  # type: ignore[return-value]
