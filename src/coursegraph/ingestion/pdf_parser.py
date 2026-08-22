"""Parsing de PDF avec PyMuPDF — extrait texte, spans, positions et métadonnées."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz  # PyMuPDF


@dataclass
class PageContent:
    page_number: int
    text: str
    spans: list[dict]  # type: ignore[type-arg]
    images: list[dict]  # type: ignore[type-arg]


@dataclass
class ParsedDocument:
    path: Path
    doc_type: str
    course_name: str
    year: int | None
    pages: list[PageContent]
    n_pages: int


def parse_pdf(
    path: Path,
    doc_type: str,
    course_name: str,
    year: int | None = None,
) -> ParsedDocument:
    """Parse un PDF et retourne son contenu structuré page par page."""
    doc = fitz.open(str(path))
    pages: list[PageContent] = []

    for page_idx in range(len(doc)):
        page = doc[page_idx]

        # get_text("dict") expose les blocs, lignes et spans avec leurs attributs
        raw = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)

        spans: list[dict] = []  # type: ignore[type-arg]
        for block in raw.get("blocks", []):
            if block.get("type") != 0:  # 0 = text, 1 = image
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if not span["text"].strip():
                        continue
                    spans.append(
                        {
                            "text": span["text"],
                            "font": span["font"],
                            "size": round(span["size"], 2),
                            # flags : bit 4 (16) = gras, bit 1 (2) = italique
                            "flags": span["flags"],
                            "bbox": span["bbox"],  # (x0, y0, x1, y1)
                        }
                    )

        images: list[dict] = [  # type: ignore[type-arg]
            {"xref": img[0], "width": img[2], "height": img[3]}
            for img in page.get_images(full=False)
        ]

        pages.append(
            PageContent(
                page_number=page_idx + 1,
                text=page.get_text("text").strip(),
                spans=spans,
                images=images,
            )
        )

    doc.close()
    return ParsedDocument(
        path=path,
        doc_type=doc_type,
        course_name=course_name,
        year=year,
        pages=pages,
        n_pages=len(pages),
    )
