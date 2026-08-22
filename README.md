# CourseGraph

**Assistant de révision RAG ancré sur les supports de cours et les annales.**

> Chaque réponse citée `[Cours ch.3, slide 12]`. Zéro hallucination tolérée.

## Démarrage rapide

```bash
cp .env.example .env
make up        # démarre Qdrant + Ollama + API
make dev       # streamlit en local
```

## Stack

| Couche | Technologie |
|---|---|
| API | FastAPI + Pydantic v2 |
| Vecteurs | Qdrant (dense BGE-M3 + BM25) |
| Reranker | bge-reranker-v2-m3 |
| LLM | Mistral-7B-Instruct via Ollama |
| Vérification | DeBERTa-v3 NLI |
| Front | Streamlit |
| Export | genanki (Anki .apkg) |

## Commandes

```bash
make up       # docker compose up -d
make down     # docker compose down
make lint     # ruff + mypy
make test     # pytest
make eval     # pipeline d'évaluation RAGAS
make build    # build image Docker
```

## Corpus de démonstration

Le répertoire `data/sample_corpus/` contient uniquement des documents sous licence libre (MIT OpenCourseWare, France Université Numérique).  
**Ne jamais committer de PDF de cours ENSICAEN** (droits des enseignants).

## Structure

```
src/coursegraph/
├── api/          FastAPI routers + schemas
├── ingestion/    Parsing PDF, chunking, détection chapitres
├── retrieval/    Qdrant hybride + reranker
├── generation/   LLM, prompts, vérification NLI
├── study/        Mapping annale→chapitre, récurrence, quiz, maîtrise
└── export/       Export Anki
```

## Évaluation

Voir [docs/evaluation.md](docs/evaluation.md) et `eval/`.

```bash
make eval
```

## Licence

MIT — corpus de démonstration sous leurs licences respectives.
