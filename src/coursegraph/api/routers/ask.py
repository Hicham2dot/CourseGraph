"""Router /ask — chat RAG avec citations et vérification NLI."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from coursegraph.api.schemas.ask import AskRequest, AskResponse, Source
from coursegraph.config import get_settings
from coursegraph.generation.llm import generate, generate_stream
from coursegraph.generation.prompts.rag import build_rag_prompt
from coursegraph.generation.verifier import compute_faithfulness, should_abstain
from coursegraph.retrieval.hybrid import embed_dense, embed_sparse
from coursegraph.retrieval.reranker import rerank
from coursegraph.retrieval.vector_store import search

router = APIRouter()

_ABSTENTION_MSG = "Je ne trouve pas cette information dans le corpus."


async def _retrieve_and_rerank(question: str, course_name: str | None) -> list[dict]:  # type: ignore[type-arg]
    """Recherche hybride Qdrant + reranking cross-encoder."""
    settings = get_settings()
    query_dense = await embed_dense(question, settings.embed_model)
    query_sparse = embed_sparse(question)
    filters = {"course_name": course_name} if course_name else None
    candidates = await search(
        query_dense, query_sparse,
        settings.qdrant_collection,
        top_k=settings.retrieval_top_k,
        filters=filters,
    )
    return rerank(question, candidates, settings.rerank_model, top_k=settings.rerank_top_k)


def _build_sources(chunks: list[dict]) -> list[Source]:  # type: ignore[type-arg]
    """Convertit les chunks reranked en objets Source."""
    return [
        Source(
            doc_type=c.get("doc_type", ""),
            course_name=c.get("course_name", ""),
            chapter=c.get("chapter", ""),
            page=c.get("page", 0),
            score=float(c.get("rerank_score", c.get("score", 0.0))),
            excerpt=c.get("text", "")[:300],
        )
        for c in chunks
    ]


@router.post("/", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    """Répond à une question en citant les sources du corpus, ou s'abstient."""
    settings = get_settings()

    ranked = await _retrieve_and_rerank(request.question, request.course_name)
    if not ranked:
        return AskResponse(
            answer=_ABSTENTION_MSG, sources=[], abstained=True, faithfulness_score=0.0
        )

    prompt = build_rag_prompt(request.question, ranked)
    answer = await generate(prompt, settings.groq_api_key, settings.groq_model)

    contexts = [c["text"] for c in ranked]
    faith = compute_faithfulness(answer, contexts, settings.nli_model)
    abstained = should_abstain(faith, settings.nli_threshold)

    return AskResponse(
        answer=_ABSTENTION_MSG if abstained else answer,
        sources=_build_sources(ranked),
        abstained=abstained,
        faithfulness_score=faith,
    )


@router.post("/stream")
async def ask_stream(request: AskRequest) -> StreamingResponse:
    """Version streaming SSE de /ask — tokens envoyés au fur et à mesure."""
    settings = get_settings()

    ranked = await _retrieve_and_rerank(request.question, request.course_name)

    async def event_gen() -> AsyncIterator[str]:
        if not ranked:
            yield f"data: {json.dumps({'token': _ABSTENTION_MSG})}\n\n"
            yield "data: [DONE]\n\n"
            return
        prompt = build_rag_prompt(request.question, ranked)
        async for token in generate_stream(prompt, settings.groq_api_key, settings.groq_model):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")
