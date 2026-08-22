"""Génération de fichiers Anki (.apkg) via genanki."""

from __future__ import annotations

from pathlib import Path

from coursegraph.study.quiz import QuizQuestion


def create_anki_deck(
    course_name: str,
    questions: list[QuizQuestion],
    output_path: Path,
) -> Path:
    """Crée un deck Anki à partir des questions de QCM et retourne le chemin du .apkg."""
    pass  # type: ignore[return-value]


def flashcard_from_chunk(chunk_text: str, source: str) -> tuple[str, str]:
    """Crée une paire (recto, verso) de flashcard à partir d'un chunk de cours."""
    pass  # type: ignore[return-value]
