"""Reranking cross-encoder bge-reranker-v2-m3."""

from __future__ import annotations

from sentence_transformers import CrossEncoder

_rerank_models: dict[str, CrossEncoder] = {}


def _get_model(model_name: str) -> CrossEncoder:
    """Retourne le cross-encoder en cache, le charge si nécessaire."""
    if model_name not in _rerank_models:
        _rerank_models[model_name] = CrossEncoder(model_name)
    return _rerank_models[model_name]


def rerank(
    query: str,
    candidates: list[dict],  # type: ignore[type-arg]
    model_name: str,
    top_k: int = 5,
) -> list[dict]:  # type: ignore[type-arg]
    """Reclasse les candidats par pertinence croisée question/passage."""
    if not candidates:
        return []
    model = _get_model(model_name)
    pairs = [[query, c["text"]] for c in candidates]
    scores = model.predict(pairs)
    ranked = sorted(zip(candidates, scores, strict=True), key=lambda x: x[1], reverse=True)
    return [{**c, "rerank_score": float(s)} for c, s in ranked[:top_k]]
