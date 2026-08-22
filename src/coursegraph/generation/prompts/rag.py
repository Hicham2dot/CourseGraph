"""Prompts pour le chat RAG sourcé."""

from __future__ import annotations

RAG_SYSTEM_PROMPT = """\
Tu es un assistant de révision. Tu réponds UNIQUEMENT à partir des extraits de cours fournis.
Si la réponse ne figure pas dans les extraits, réponds : « Je ne trouve pas cette information dans le corpus. »
Chaque affirmation doit être citée au format [Cours ch.<chapitre>, slide <page>].
"""

RAG_USER_TEMPLATE = """\
Extraits du corpus :
{context}

Question : {question}
"""


def build_rag_prompt(question: str, context_chunks: list[dict]) -> str:  # type: ignore[type-arg]
    """Construit le prompt RAG final à partir de la question et des chunks reranked."""
    parts: list[str] = []
    for chunk in context_chunks:
        label = f"[{chunk.get('doc_type', 'Cours')} ch.{chunk.get('chapter', '?')}, slide {chunk.get('page', '?')}]"
        parts.append(f"{label}\n{chunk['text']}")
    context = "\n\n---\n\n".join(parts)
    return RAG_SYSTEM_PROMPT + "\n" + RAG_USER_TEMPLATE.format(context=context, question=question)
