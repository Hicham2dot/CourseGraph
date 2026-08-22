"""Reranking cross-encoder bge-reranker-v2-m3."""

from __future__ import annotations


def rerank(
    query: str,
    candidates: list[dict],  # type: ignore[type-arg]
    model_name: str,
    top_k: int = 5,
) -> list[dict]:  # type: ignore[type-arg]
    """Reclasse les candidats par pertinence croisée question/passage."""
    pass  # type: ignore[return-value]
