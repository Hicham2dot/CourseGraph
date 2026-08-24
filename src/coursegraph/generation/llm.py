"""Client Groq pour la génération de texte (batch et streaming)."""

from __future__ import annotations

from collections.abc import AsyncIterator

from groq import AsyncGroq


def _client(api_key: str) -> AsyncGroq:
    """Retourne un client Groq initialisé avec la clé fournie."""
    return AsyncGroq(api_key=api_key)


async def generate(
    prompt: str,
    api_key: str,
    model: str,
    temperature: float = 0.1,
) -> str:
    """Génère une réponse complète via l'API Groq."""
    client = _client(api_key)
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        stream=False,
    )
    return response.choices[0].message.content or ""


async def generate_stream(
    prompt: str,
    api_key: str,
    model: str,
    temperature: float = 0.1,
) -> AsyncIterator[str]:
    """Génère une réponse en streaming token par token via Groq."""
    client = _client(api_key)
    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        stream=True,
    )
    async for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            yield token
