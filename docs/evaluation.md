# Évaluation CourseGraph

## Goldset

Fichier : `eval/goldset.jsonl`

Format d'une entrée :

```jsonc
{
  "id": "q001",
  "question": "...",
  "expected_answer": "...",
  "relevant_chunks": ["chunk_id_1", "chunk_id_2"],
  "chapter": "Chapitre 3 — Arbres",
  "type": "rag",            // "rag" | "abstention" | "mapping"
  "in_corpus": true
}
```

Objectif : 60–80 entrées sur 2 cours (semi-automatique + validation manuelle).

## Métriques Retrieval

Évaluées sur les entrées `type == "rag"`.

| Config | Recall@5 | MRR | Latence p95 |
|---|---|---|---|
| Dense seul | | | |
| + BM25 (RRF) | | | |
| + Reranker | | | |
| + Filtres payload | | | |

## Métriques Génération

| Métrique | Description | Valeur |
|---|---|---|
| Faithfulness (RAGAS) | Proportion d'affirmations ancrées dans les contextes | |
| Citations invalides | % de références `[ch.X, slide Y]` pointant vers une page inexistante | |
| Taux abstention correcte | Sur 20 questions hors-corpus : vrais positifs d'abstention | |

## Métriques Mapping

Évaluées sur 40 exercices annotés manuellement.

| Métrique | Valeur |
|---|---|
| Accuracy top-1 | |
| Accuracy top-3 | |

## Ablation Study

| Config retirée | Recall@5 delta | Faithfulness delta | Notes |
|---|---|---|---|
| Sans réécriture | | | |
| Sans reranker | | | |
| Sans NLI | | | |
| Sans filtres payload | | | |

## Retours utilisateurs

5 testeurs, 30 min chacun.

| Critère | Score moyen /10 | Commentaires |
|---|---|---|
| Utilité perçue | | |
| Fiabilité des sources | | |
| Temps de révision économisé (estimé) | | |
| Erreurs signalées | | |

## Lancer l'évaluation

```bash
make eval
# → eval/results/eval_YYYYMMDD_HHMMSS.json
```
