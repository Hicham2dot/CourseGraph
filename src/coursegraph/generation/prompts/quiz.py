"""Prompts pour la génération de QCM et de fiches de révision."""

from __future__ import annotations

QCM_SYSTEM_PROMPT = """\
Tu es un enseignant. Génère un QCM à partir UNIQUEMENT des extraits fournis.
Chaque question doit avoir 4 options (A-D), une seule correcte, avec une explication sourcée.
Format JSON strict : {"questions": [{"question": "...", "options": {...}, "answer": "A", "explanation": "...", "source": "..."}]}
"""

FICHE_SYSTEM_PROMPT = """\
Tu es un enseignant. Génère une fiche de révision synthétique à partir UNIQUEMENT des extraits fournis.
Structure : titre du chapitre, notions clés (avec citations), formules importantes, points à retenir.
"""


def build_quiz_prompt(chapter: str, context_chunks: list[dict], n_questions: int = 5) -> str:  # type: ignore[type-arg]
    """Construit le prompt de génération de QCM pour un chapitre."""
    pass  # type: ignore[return-value]


def build_fiche_prompt(chapter: str, context_chunks: list[dict]) -> str:  # type: ignore[type-arg]
    """Construit le prompt de génération de fiche de révision."""
    pass  # type: ignore[return-value]
