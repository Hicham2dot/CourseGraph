"""Paramètres globaux lus depuis .env via pydantic-settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "coursegraph"

    # Ollama / LLM
    ollama_url: str = "http://localhost:11434"
    llm_model: str = "mistral:7b-instruct"
    embed_model: str = "BAAI/bge-m3"
    rerank_model: str = "BAAI/bge-reranker-v2-m3"

    # NLI
    nli_model: str = "cross-encoder/nli-deberta-v3-base"
    nli_threshold: float = 0.5

    # RAG
    retrieval_top_k: int = 20
    rerank_top_k: int = 5
    abstention_threshold: float = 0.3

    # Database
    database_url: str = "sqlite:///./coursegraph.db"

    # Logging
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Retourne l'instance singleton des paramètres."""
    return Settings()
