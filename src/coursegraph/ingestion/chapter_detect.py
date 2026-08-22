"""Détection automatique des chapitres dans un PDF de cours par analyse des spans."""

from __future__ import annotations

import re
import statistics

from coursegraph.ingestion.pdf_parser import ParsedDocument

# Motifs courants de titres de chapitres (français et anglais)
_CHAPTER_RE = re.compile(
    r"""
    ^(
        (?:chapitre|chapter|partie|part|section|module|cours)\s+\d+   # "Chapitre 3"
        | \d+(?:\.\d+)*\s+\w{3,}                                       # "3.1 Introduction"
        | [IVX]+[.\s]+\w{3,}                                           # "III. Algorithmes"
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)


def detect_chapters(document: ParsedDocument) -> dict[int, str]:
    """Retourne un mapping {page_number: chapter_title} pour un cours.

    Stratégie : un span est un titre de chapitre s'il est significativement
    plus grand que la médiane des tailles de fonte (seuil x1.25) OU s'il
    correspond à un motif de titre connu, ET qu'il est court et commence en majuscule.
    """
    # Collecte toutes les tailles de fonte du document
    all_sizes = [
        span["size"]
        for page in document.pages
        for span in page.spans
        if span["text"].strip()
    ]

    if not all_sizes:
        return {1: document.course_name}

    median_size = statistics.median(all_sizes)
    heading_threshold = median_size * 1.25  # 25 % plus grand = probable titre

    chapter_map: dict[int, str] = {}

    for page in document.pages:
        for span in page.spans:
            text = span["text"].strip()

            # Filtres rapides : longueur et présence de contenu
            if not text or len(text) < 3 or len(text) > 120:
                continue

            size = span["size"]
            is_bold = bool(span["flags"] & 16)  # bit 4 = gras dans PyMuPDF
            is_large = size >= heading_threshold
            starts_upper = text[0].isupper()
            no_trailing_dot = not text.endswith(".")
            is_short = len(text) <= 80

            matches_pattern = bool(_CHAPTER_RE.match(text))
            looks_like_title = starts_upper and is_short and no_trailing_dot

            is_heading = (
                matches_pattern
                or (is_large and looks_like_title)
                or (is_bold and is_large and starts_upper)
            )

            if is_heading and page.page_number not in chapter_map:
                chapter_map[page.page_number] = text
                break  # un seul titre retenu par page

    return chapter_map if chapter_map else {1: document.course_name}


def assign_chapter_to_page(page_number: int, chapter_map: dict[int, str]) -> str:
    """Retourne le titre du chapitre auquel appartient une page donnée.

    Sélectionne la dernière entrée du chapter_map dont la page est <= page_number.
    """
    if not chapter_map:
        return "Document"

    preceding = [p for p in sorted(chapter_map) if p <= page_number]
    if not preceding:
        # La page est avant le premier titre détecté : on prend le premier chapitre
        return chapter_map[min(chapter_map)]

    return chapter_map[preceding[-1]]
