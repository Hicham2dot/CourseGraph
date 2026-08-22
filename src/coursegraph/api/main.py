"""Point d'entrée FastAPI — monte tous les routers."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from coursegraph.api.routers import ask, export, gaps, ingest, quiz, recurrence

app = FastAPI(
    title="CourseGraph API",
    version="0.1.0",
    description="Assistant de révision RAG ancré sur les supports de cours et les annales.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/ingest", tags=["ingestion"])
app.include_router(ask.router, prefix="/ask", tags=["rag"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(gaps.router, prefix="/gaps", tags=["gaps"])
app.include_router(recurrence.router, prefix="/recurrence", tags=["recurrence"])
app.include_router(export.router, prefix="/export", tags=["export"])


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Healthcheck utilisé par Docker et le Makefile."""
    return {"status": "ok"}


@app.get("/", tags=["meta"])
async def root() -> dict[str, str]:
    """Redirection vers la doc."""
    return {"docs": "/docs", "redoc": "/redoc"}
