"""Vérification d'ancrage par NLI (DeBERTa-v3) et seuil d'abstention."""

from __future__ import annotations

import re

from sentence_transformers import CrossEncoder

_nli_models: dict[str, CrossEncoder] = {}

# cross-encoder/nli-deberta-v3-base : labels [contradiction=0, neutral=1, entailment=2]
_ENTAILMENT_IDX = 2

_CITATION_RE = re.compile(r"\[([^\]]+ch[^\]]+slide\s*\d+[^\]]*)\]", re.IGNORECASE)


def _get_nli_model(model_name: str) -> CrossEncoder:
    """Retourne le modèle NLI en cache, le charge si nécessaire."""
    if model_name not in _nli_models:
        _nli_models[model_name] = CrossEncoder(model_name, num_labels=3)
    return _nli_models[model_name]


def compute_faithfulness(answer: str, contexts: list[str], model_name: str) -> float:
    """Calcule le score de fidélité NLI de la réponse par rapport aux contextes.

    Stratégie : score = max(entailment) sur tous les contextes.
    premise = contexte, hypothesis = réponse générée.
    """
    if not contexts or not answer.strip():
        return 0.0
    model = _get_nli_model(model_name)
    pairs = [[ctx, answer] for ctx in contexts]
    scores = model.predict(pairs, apply_softmax=True)
    return float(max(s[_ENTAILMENT_IDX] for s in scores))


def should_abstain(faithfulness_score: float, threshold: float) -> bool:
    """Retourne True si le score est trop bas pour répondre."""
    return faithfulness_score < threshold


def check_citation_validity(answer: str, chunks: list[dict]) -> dict[str, bool]:  # type: ignore[type-arg]
    """Vérifie que chaque citation [ch.X, slide Y] pointe vers un chunk existant."""
    valid_refs = {
        (str(c.get("chapter", "")), str(c.get("page", "")))
        for c in chunks
    }
    result: dict[str, bool] = {}
    for citation in _CITATION_RE.findall(answer):
        page_match = re.search(r"slide\s*(\d+)", citation, re.IGNORECASE)
        page = page_match.group(1) if page_match else ""
        result[citation] = any(page == ref_page for _, ref_page in valid_refs)
    return result
