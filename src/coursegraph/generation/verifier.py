"""Vérification d'ancrage par NLI (DeBERTa-v3) et seuil d'abstention."""

from __future__ import annotations


def compute_faithfulness(answer: str, contexts: list[str], model_name: str) -> float:
    """Calcule le score de fidélité NLI de la réponse par rapport aux contextes."""
    pass  # type: ignore[return-value]


def should_abstain(faithfulness_score: float, threshold: float) -> bool:
    """Retourne True si le score est trop bas pour répondre."""
    pass  # type: ignore[return-value]


def check_citation_validity(answer: str, chunks: list[dict]) -> dict[str, bool]:  # type: ignore[type-arg]
    """Vérifie que chaque citation [Cours ch.X, slide Y] pointe vers un chunk existant."""
    pass  # type: ignore[return-value]
