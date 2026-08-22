"""Client Ollama pour la génération de texte (streaming et batch)."""

from __future__ import annotations

from collections.abc import AsyncIterator


async def generate(
    prompt: str,
    ollama_url: str,
    model: str,
    temperature: float = 0.1,
) -> str:
    """Génère une réponse complète via l'API Ollama."""
    pass  # type: ignore[return-value]


async def generate_stream(
    prompt: str,
    ollama_url: str,
    model: str,
    temperature: float = 0.1,
) -> AsyncIterator[str]:
    """Génère une réponse en streaming token par token."""
    pass  # type: ignore[return-value]
    yield ""
