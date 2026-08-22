# Architecture CourseGraph

## Vue d'ensemble

```
┌───────────────────────────────────────────────────────────────┐
│  FRONT · Streamlit                                            │
│  Upload cours+annales · Chat sourcé · Quiz · Radar de maîtrise│
└───────────────────────────┬───────────────────────────────────┘
                            │ HTTP / SSE
┌───────────────────────────▼───────────────────────────────────┐
│  API · FastAPI (Python 3.11)                                  │
│  /ingest  /ask  /quiz  /gaps  /recurrence  /export/anki  /eval│
└───────────────────────────┬───────────────────────────────────┘
                            │
        ┌───────────────────▼────────────────────┐
        │  PIPELINE RAG (LangGraph)              │
        │  question → réécriture → retrieval     │
        │  hybride → rerank → génération sourcée │
        │  → vérification NLI → réponse|abstention│
        └───────────┬────────────────────┬───────┘
                    │                    │
   ┌────────────────▼──────────┐ ┌───────▼────────────────┐
   │  INDEX · Qdrant           │ │  LLM · Ollama          │
   │  dense BGE-M3 + BM25      │ │  Mistral-7B-Instruct   │
   │  payload: cours/ch/page   │ └────────────────────────┘
   └────────────────┬──────────┘
                    │           ┌────────────────────────┐
   ┌────────────────▼──────────┐│  NLI · DeBERTa-v3     │
   │  INGESTION                ││  vérif. d'ancrage      │
   │  PDF → PyMuPDF            │└────────────────────────┘
   │  → chunk sémantique       │
   │  → détection chapitres    │ ┌────────────────────────┐
   │  → embeddings             │ │  SQLite                │
   └───────────────────────────┘ │  sessions, réponses,   │
                                 │  scores de maîtrise    │
   ┌───────────────────────────┐ └────────────────────────┘
   │  MOTEUR MAPPING           │
   │  annale → chapitre        │
   │  + score de récurrence    │
   └───────────────────────────┘
```

## Flux de données

### Ingestion

1. Upload PDF (cours / annale / correction)
2. `pdf_parser.py` → `ParsedDocument` (pages + spans)
3. `chapter_detect.py` → mapping `{page: chapitre}`
4. `chunking.py` → `List[Chunk]` (max 512 tokens, overlap 64)
5. `hybrid.py:embed_dense` + `embed_sparse` → vecteurs BGE-M3
6. `vector_store.py:upsert_chunks` → Qdrant

### Chat RAG

1. Question utilisateur
2. `hybrid.py:rewrite_query` → question réécrite (HyDE/reformulation)
3. `hybrid.py:embed_dense` + `embed_sparse` → vecteurs requête
4. `vector_store.py:search` → top-20 chunks (RRF dense+BM25)
5. `reranker.py:rerank` → top-5 chunks (bge-reranker-v2-m3)
6. `prompts/rag.py:build_rag_prompt` → prompt avec contexte
7. `llm.py:generate` → réponse avec citations
8. `verifier.py:compute_faithfulness` → score NLI
9. Si score < seuil → abstention ; sinon → réponse

### Mapping annale → chapitre

1. Segmenter l'annale en exercices
2. Pour chaque exercice : retrieval top-k dans le corpus cours
3. Vote pondéré par score sur les chapitres des chunks retournés
4. Résultat : `ExerciseMapping` avec top-3 chapitres et scores

## Décisions d'architecture

Voir [adr/](adr/) pour les Architecture Decision Records.

## Technologies

| Couche | Choix | Raison |
|---|---|---|
| API | FastAPI + Pydantic v2 | |
| Orchestration | LangGraph | |
| Vecteurs | Qdrant | |
| Embeddings | BAAI/bge-m3 | |
| Reranker | bge-reranker-v2-m3 | |
| LLM | Mistral-7B via Ollama | |
| NLI | DeBERTa-v3-base | |
| Parsing | PyMuPDF | |
| État | SQLite + SQLModel | |
| Export | genanki | |
| Front | Streamlit | |

## Contraintes

- Fonctionne sans GPU (Mistral-7B Q4 via Ollama CPU)
- Stack 100% open source, zéro coût d'API
- `make up` suffit à démarrer l'environnement complet
