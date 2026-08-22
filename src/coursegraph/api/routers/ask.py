"""Router /ask — chat RAG avec citations."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from coursegraph.api.schemas.ask import AskRequest, AskResponse

router = APIRouter()


@router.post("/", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    """Répond à une question en citant les sources du corpus, ou s'abstient."""
    pass  # type: ignore[return-value]


@router.post("/stream")
async def ask_stream(request: AskRequest) -> StreamingResponse:
    """Version streaming SSE de /ask."""
    pass  # type: ignore[return-value]
