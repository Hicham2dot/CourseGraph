"""Découpage sémantique des pages en chunks indexables avec overlap."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from coursegraph.ingestion.chapter_detect import assign_chapter_to_page, detect_chapters
from coursegraph.ingestion.pdf_parser import ParsedDocument

# Coupe sur les fins de phrase (point, !, ?) suivies d'une espace
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    doc_type: str
    course_name: str
    chapter: str
    page: int
    text: str
    token_count: int


# ---------------------------------------------------------------------------
# Helpers privés
# ---------------------------------------------------------------------------


def _doc_id(document: ParsedDocument) -> str:
    """ID stable basé sur le cours, le type et le chemin du fichier."""
    raw = f"{document.course_name}:{document.doc_type}:{document.path}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]


def _estimate_tokens(text: str) -> int:
    """Estimation rapide : ~1.3 tokens/mot (tokenizer BERT-style)."""
    return max(1, int(len(text.split()) * 1.3))


def _split_sentences(text: str) -> list[str]:
    """Découpe un texte en phrases en conservant la ponctuation de fin."""
    return [s.strip() for s in _SENTENCE_END.split(text) if s.strip()]


def _chunk_sentences(
    sentences: list[str],
    max_tokens: int,
    overlap: int,
    chunk_id_prefix: str,
    start_idx: int,
    doc_id: str,
    doc_type: str,
    course_name: str,
    chapter: str,
    page: int,
) -> list[Chunk]:
    """Regroupe les phrases en chunks de ≤ max_tokens avec recouvrement."""
    chunks: list[Chunk] = []
    window: list[str] = []
    window_tokens = 0

    def _emit() -> None:
        if not window:
            return
        idx = start_idx + len(chunks)
        chunks.append(
            Chunk(
                chunk_id=f"{chunk_id_prefix}_{idx:05d}",
                doc_id=doc_id,
                doc_type=doc_type,
                course_name=course_name,
                chapter=chapter,
                page=page,
                text=" ".join(window),
                token_count=window_tokens,
            )
        )

    for sentence in sentences:
        s_tokens = _estimate_tokens(sentence)

        if window_tokens + s_tokens > max_tokens and window:
            _emit()

            # Recouvrement : on conserve les dernières phrases jusqu'à `overlap` tokens
            overlap_sents: list[str] = []
            overlap_tokens = 0
            for s in reversed(window):
                t = _estimate_tokens(s)
                if overlap_tokens + t > overlap:
                    break
                overlap_sents.insert(0, s)
                overlap_tokens += t

            window = [*overlap_sents, sentence]
            window_tokens = overlap_tokens + s_tokens
        else:
            window.append(sentence)
            window_tokens += s_tokens

    _emit()
    return chunks


# ---------------------------------------------------------------------------
# API publique
# ---------------------------------------------------------------------------


def chunk_document(
    document: ParsedDocument,
    max_tokens: int = 512,
    overlap: int = 64,
) -> list[Chunk]:
    """Découpe un document parsé en chunks avec overlap, assignés à leur chapitre."""
    chapter_map = detect_chapters(document)
    doc_id = _doc_id(document)
    chunks: list[Chunk] = []

    for page in document.pages:
        text = page.text.strip()
        if not text:
            continue

        chapter = assign_chapter_to_page(page.page_number, chapter_map)
        page_tokens = _estimate_tokens(text)

        if page_tokens <= max_tokens:
            # La page entière tient dans un seul chunk
            chunks.append(
                Chunk(
                    chunk_id=f"{doc_id}_{len(chunks):05d}",
                    doc_id=doc_id,
                    doc_type=document.doc_type,
                    course_name=document.course_name,
                    chapter=chapter,
                    page=page.page_number,
                    text=text,
                    token_count=page_tokens,
                )
            )
        else:
            # Page dense : on découpe en sous-chunks par phrase
            sentences = _split_sentences(text)
            page_chunks = _chunk_sentences(
                sentences,
                max_tokens,
                overlap,
                chunk_id_prefix=doc_id,
                start_idx=len(chunks),
                doc_id=doc_id,
                doc_type=document.doc_type,
                course_name=document.course_name,
                chapter=chapter,
                page=page.page_number,
            )
            chunks.extend(page_chunks)

    return chunks
