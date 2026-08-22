"""Abstraction Qdrant : création de collection, indexation et recherche hybride."""

from __future__ import annotations

import uuid

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    Fusion,
    FusionQuery,
    MatchValue,
    PointStruct,
    Prefetch,
    SparseVector,
    SparseVectorParams,
    VectorParams,
)

from coursegraph.config import get_settings
from coursegraph.ingestion.chunking import Chunk

DENSE_DIM = 1024        # dimension BGE-M3
DENSE_NAME = "dense"
SPARSE_NAME = "sparse"
BATCH_SIZE = 64         # nombre de points par appel upsert

# Singleton client — créé une seule fois, partagé entre les appels
_client: AsyncQdrantClient | None = None


def _get_client() -> AsyncQdrantClient:
    """Retourne le client Qdrant singleton."""
    global _client
    if _client is None:
        _client = AsyncQdrantClient(url=get_settings().qdrant_url)
    return _client


def _point_id(chunk_id: str) -> str:
    """Convertit un chunk_id en UUID Qdrant stable (UUID v5)."""
    return str(uuid.uuid5(uuid.NAMESPACE_OID, chunk_id))


async def _ensure_collection(client: AsyncQdrantClient, collection: str) -> None:
    """Crée la collection avec vecteurs dense + sparse si elle n'existe pas encore."""
    if not await client.collection_exists(collection):
        await client.create_collection(
            collection_name=collection,
            vectors_config={
                DENSE_NAME: VectorParams(size=DENSE_DIM, distance=Distance.COSINE),
            },
            sparse_vectors_config={
                SPARSE_NAME: SparseVectorParams(),
            },
        )


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------


async def upsert_chunks(chunks: list[Chunk], collection: str) -> int:
    """Indexe une liste de chunks dans Qdrant. Retourne le nombre de points upsertés.

    Pour chaque chunk :
      1. Calcule l'embedding dense BGE-M3 (1024 floats, cosine)
      2. Calcule le vecteur sparse TF/lexical
      3. Upsert en batches de BATCH_SIZE
    """
    if not chunks:
        return 0

    from coursegraph.retrieval.hybrid import embed_dense, embed_sparse

    settings = get_settings()
    client = _get_client()
    await _ensure_collection(client, collection)

    points: list[PointStruct] = []

    for chunk in chunks:
        dense_vec = await embed_dense(chunk.text, settings.embed_model)
        sparse_vec = embed_sparse(chunk.text)

        points.append(
            PointStruct(
                id=_point_id(chunk.chunk_id),
                vector={
                    DENSE_NAME: dense_vec,
                    SPARSE_NAME: SparseVector(
                        indices=list(sparse_vec.keys()),
                        values=list(sparse_vec.values()),
                    ),
                },
                payload={
                    "chunk_id": chunk.chunk_id,
                    "doc_id": chunk.doc_id,
                    "doc_type": chunk.doc_type,
                    "course_name": chunk.course_name,
                    "chapter": chunk.chapter,
                    "page": chunk.page,
                    "text": chunk.text,
                    "token_count": chunk.token_count,
                },
            )
        )

    for i in range(0, len(points), BATCH_SIZE):
        await client.upsert(
            collection_name=collection,
            points=points[i : i + BATCH_SIZE],
        )

    return len(points)


async def search(
    query_dense: list[float],
    query_sparse: dict[int, float],
    collection: str,
    top_k: int = 20,
    filters: dict | None = None,  # type: ignore[type-arg]
) -> list[dict]:  # type: ignore[type-arg]
    """Recherche hybride RRF (dense + sparse) dans Qdrant avec filtres optionnels.

    Qdrant applique RRF nativement via deux Prefetch (dense, sparse) fusionnés
    en FusionQuery(RRF). Les filtres sur le payload permettent de restreindre
    la recherche à un cours ou un type de document spécifique.

    Exemple de filtres : {"course_name": "Algo S3", "doc_type": "cours"}
    """
    client = _get_client()

    qdrant_filter: Filter | None = None
    if filters:
        qdrant_filter = Filter(
            must=[
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filters.items()
            ]
        )

    results = await client.query_points(
        collection_name=collection,
        prefetch=[
            Prefetch(
                query=query_dense,
                using=DENSE_NAME,
                limit=top_k,
                filter=qdrant_filter,
            ),
            Prefetch(
                query=SparseVector(
                    indices=list(query_sparse.keys()),
                    values=list(query_sparse.values()),
                ),
                using=SPARSE_NAME,
                limit=top_k,
                filter=qdrant_filter,
            ),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=top_k,
        with_payload=True,
    )

    return [{"score": pt.score, **pt.payload} for pt in results.points]


async def delete_document(doc_id: str, collection: str) -> int:
    """Supprime tous les points d'un document de la collection. Retourne 0 (Qdrant ne compte pas)."""
    client = _get_client()
    await client.delete(
        collection_name=collection,
        points_selector=Filter(
            must=[FieldCondition(key="doc_id", match=MatchValue(value=doc_id))]
        ),
    )
    return 0
