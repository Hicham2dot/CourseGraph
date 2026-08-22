# CLAUDE.md — Conventions CourseGraph

Ce fichier décrit les conventions du projet pour les sessions Claude Code.

## Contexte

CourseGraph est un assistant de révision RAG (Python 3.11) composé de :
- Une API FastAPI (`src/coursegraph/api/`)
- Un pipeline LangGraph (`src/coursegraph/retrieval/`, `generation/`)
- Une base vectorielle Qdrant (dense BGE-M3 + BM25 sparse)
- Un LLM Mistral-7B via Ollama
- Un front Streamlit (`app/`)

## Conventions de code

- **Python 3.11**, typage strict (`from __future__ import annotations`)
- Toutes les fonctions publiques ont une **signature typée complète** et une docstring une ligne
- Pas de commentaires sauf pour les contraintes non-évidentes
- Pas de logique dans les `__init__.py` — ils réexportent uniquement
- Les constantes de configuration passent **toujours** par `config.py` (pydantic-settings), jamais en dur
- Style : **ruff** (lint + format), **mypy** strict — `make lint` doit passer avant tout commit
- Tests : **pytest**, fixtures dans `tests/conftest.py`, pas de mocks DB sauf unitaires isolés

## Structure des modules

```
src/coursegraph/
├── config.py          Settings (pydantic-settings), lit .env
├── api/               FastAPI : main.py + routers/ + schemas/
├── ingestion/         PDF→chunks→Qdrant
├── retrieval/         Hybride dense+BM25, reranker, vector_store
├── generation/        LLM, prompts/, verifier NLI
├── study/             mapping, recurrence, quiz, mastery
└── export/            anki.py
```

## Commandes fréquentes

```bash
make up       # docker compose up -d (Qdrant + Ollama + API)
make lint     # ruff check . && mypy src/
make test     # pytest -v
make eval     # python eval/run_eval.py
```

## Règles métier importantes

1. **Abstention** : si le score NLI < `NLI_THRESHOLD`, retourner une abstention explicite, jamais halluciner
2. **Citations** : chaque chunk retourné doit porter `{doc_type, chapter, page}` dans le payload Qdrant
3. **Mapping annale→chapitre** : dans `study/mapping.py`, vote pondéré sur top-k chunks du corpus cours
4. **Score de récurrence** : `study/recurrence.py`, fréquence × récence, mis à jour à chaque ingestion d'annale

## Variables d'environnement

Toutes définies dans `.env.example`. La classe `Settings` dans `config.py` est la source de vérité.

## Docker

- `docker-compose.yml` orchestre : `qdrant` (6333), `ollama` (11434), `api` (8000)
- L'image `api` se build depuis `src/` avec le `pyproject.toml` comme base
- `make up` = `docker compose up -d --build`

## Ne jamais

- Committer de PDF de cours dans le repo (droits enseignants)
- Hardcoder des URLs ou modèles — tout passe par `Settings`
- Merger sans que `make lint && make test` passent
