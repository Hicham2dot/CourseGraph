"""Fusion RRF, réécriture de requête et calcul des embeddings dense + sparse."""

from __future__ import annotations

import asyncio
import re
from collections import Counter

import numpy as np
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Singleton pour le modèle dense (chargement au premier appel)
# ---------------------------------------------------------------------------

_dense_models: dict[str, SentenceTransformer] = {}


def _get_dense_model(model_name: str) -> SentenceTransformer:
    """Retourne le modèle sentence-transformers en cache, le charge si nécessaire."""
    if model_name not in _dense_models:
        _dense_models[model_name] = SentenceTransformer(model_name)
    return _dense_models[model_name]


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------


async def embed_dense(text: str, model_name: str) -> list[float]:
    """Calcule l'embedding dense BGE-M3 d'un texte (exécuté dans un thread pool)."""
    model = _get_dense_model(model_name)
    loop = asyncio.get_running_loop()
    # SentenceTransformer.encode est synchrone et CPU-bound → executor pour ne pas bloquer l'event loop
    vec: np.ndarray = await loop.run_in_executor(
        None,
        lambda: model.encode(text, normalize_embeddings=True),
    )
    return vec.tolist()


def embed_sparse(text: str) -> dict[int, float]:
    """Vecteur sparse TF normalisé par feature hashing sur 2^20 dimensions.

    Approximation BM25 légère. Remplacer par FlagEmbedding BGE-M3 sparse
    (lexical_weights) pour la production afin d'obtenir de vraies pondérations lexicales.
    """
    tokens = re.findall(r"\b\w+\b", text.lower())
    if not tokens:
        return {}
    freq = Counter(tokens)
    n = len(tokens)
    # Feature hashing : hash(terme) & 0xFFFFF → indice dans [0, 1 048 575]
    # TF normalisé par le nombre total de tokens
    return {hash(term) & 0xFFFFF: count / n for term, count in freq.items()}


# ---------------------------------------------------------------------------
# Fusion RRF (utilisée en fallback si Qdrant ne gère pas la fusion lui-même)
# ---------------------------------------------------------------------------


def reciprocal_rank_fusion(
    dense_results: list[dict],  # type: ignore[type-arg]
    sparse_results: list[dict],  # type: ignore[type-arg]
    k: int = 60,
) -> list[dict]:  # type: ignore[type-arg]
    """Fusionne deux listes de résultats par Reciprocal Rank Fusion.

    score_RRF(d) = sum_r [ 1 / (k + rank_r(d)) ]
    où r parcourt les listes dense et sparse.
    """
    scores: dict[str, float] = {}
    payloads: dict[str, dict] = {}  # type: ignore[type-arg]

    for rank, result in enumerate(dense_results):
        doc_id = result["chunk_id"]
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        payloads[doc_id] = result

    for rank, result in enumerate(sparse_results):
        doc_id = result["chunk_id"]
        scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        payloads.setdefault(doc_id, result)

    return [
        {**payloads[doc_id], "score": score}
        for doc_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)
    ]


# ---------------------------------------------------------------------------
# Réécriture de requête (stub — implémenté en Semaine 2)
# ---------------------------------------------------------------------------


async def rewrite_query(question: str, ollama_url: str, model: str) -> str:
    """Réécrit la question pour améliorer le recall (HyDE ou reformulation)."""
    pass  # type: ignore[return-value]
