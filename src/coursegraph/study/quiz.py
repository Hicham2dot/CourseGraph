"""Génération et gestion des sessions de QCM."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class QuizQuestion:
    question_id: str
    question: str
    options: dict[str, str]  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer: str
    explanation: str
    source: str
    chapter: str


@dataclass
class QuizSession:
    session_id: str
    course_name: str
    questions: list[QuizQuestion]


async def generate_quiz_for_chapter(
    course_name: str,
    chapter: str,
    n_questions: int = 5,
) -> QuizSession:
    """Génère un QCM pour un chapitre donné, ancré dans le corpus."""
    pass  # type: ignore[return-value]


def score_quiz_submission(
    session: QuizSession,
    answers: dict[str, str],
) -> dict[str, float]:  # type: ignore[type-arg]
    """Score une soumission et retourne le résultat par chapitre."""
    pass  # type: ignore[return-value]
