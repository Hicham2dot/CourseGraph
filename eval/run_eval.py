"""Pipeline d'évaluation RAGAS + métriques maison sur le goldset."""

from __future__ import annotations

import json
from pathlib import Path

GOLDSET_PATH = Path(__file__).parent / "goldset.jsonl"
RESULTS_DIR = Path(__file__).parent / "results"


def load_goldset(path: Path = GOLDSET_PATH) -> list[dict]:  # type: ignore[type-arg]
    """Charge le goldset JSONL."""
    if not path.exists() or path.stat().st_size == 0:
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def evaluate_retrieval(goldset: list[dict], top_k: int = 5) -> dict[str, float]:  # type: ignore[type-arg]
    """Calcule Recall@k et MRR sur le goldset."""
    pass  # type: ignore[return-value]


def evaluate_faithfulness(goldset: list[dict]) -> dict[str, float]:  # type: ignore[type-arg]
    """Calcule faithfulness (RAGAS) et taux de citations invalides."""
    pass  # type: ignore[return-value]


def evaluate_abstention(goldset: list[dict]) -> dict[str, float]:  # type: ignore[type-arg]
    """Calcule taux de faux positifs/négatifs d'abstention sur questions hors-corpus."""
    pass  # type: ignore[return-value]


def evaluate_mapping(goldset: list[dict]) -> dict[str, float]:  # type: ignore[type-arg]
    """Calcule accuracy top-1/top-3 du mapping annale→chapitre."""
    pass  # type: ignore[return-value]


def main() -> None:
    """Lance l'évaluation complète et sauvegarde les résultats."""
    goldset = load_goldset()
    if not goldset:
        print("Goldset vide — créer eval/goldset.jsonl avant d'évaluer.")
        return

    RESULTS_DIR.mkdir(exist_ok=True)

    results = {
        "retrieval": evaluate_retrieval(goldset),
        "faithfulness": evaluate_faithfulness(goldset),
        "abstention": evaluate_abstention(goldset),
        "mapping": evaluate_mapping(goldset),
    }

    import datetime

    output = RESULTS_DIR / f"eval_{datetime.datetime.now():%Y%m%d_%H%M%S}.json"
    output.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Résultats sauvegardés dans {output}")


if __name__ == "__main__":
    main()
