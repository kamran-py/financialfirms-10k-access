# Full Corpus V2 Spot-Check Sample Plan

Generated at: 2026-06-29T19:34:13.632867+00:00

## Scope And Guardrails

- Prepared a 150-row post-scale spot-check sample from `data/classified/phrase_hits_classified_v2.csv`.
- This stage validates full-corpus classification quality only.
- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.
- Raw `phrase_hits.csv` and classified `phrase_hits_classified_v2.csv` were not modified.
- Script version: `prepare_full_corpus_classification_spotcheck_v1`.
- Deterministic seed: `20260629`.

## Input Integrity

- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes
- Classified `phrase_hits_classified_v2.csv` SHA256 before: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- Classified `phrase_hits_classified_v2.csv` SHA256 after: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- Classified file unchanged: yes

## Full Corpus Counts

- Full classified rows: 9400
- Full-corpus true-positive rows: 7414
- Full-corpus true-positive filings: 2520

## Sample Counts

- Spot-check sample size: 150
- Sampled full-corpus positives: 100
- Sampled full-corpus non-positives: 50
- Sampled high-risk phrase rows: 121
- Sampled high-risk phrase rows labeled true positive: 73
- Sampled rows from top true-positive firms: 46

## Sample Label Distribution Before Spot Check

| Final label V2 | Rows |
| --- | --- |
| true_positive_access_expansion | 100 |
| operational_access_or_platform_language | 14 |
| false_positive | 13 |
| risk_disclosure_only | 12 |
| customer_access_unrelated_to_finance | 7 |
| ambiguous | 2 |
| generic_marketing | 2 |

## Sample Section Coverage

| Section | Rows |
| --- | --- |
| Item 1 Business | 72 |
| Item 7 MD&A | 43 |
| Item 1A Risk Factors | 35 |

## Sample Filing-Year Coverage

| Filing year | Rows |
| --- | --- |
| 2022 | 24 |
| 2023 | 18 |
| 2024 | 17 |
| 2015 | 16 |
| 2021 | 14 |
| 2020 | 12 |
| 2025 | 12 |
| 2016 | 11 |
| 2017 | 9 |
| 2019 | 9 |
| 2018 | 8 |

## Sample High-Risk Phrase Coverage

| Phrase | Rows |
| --- | --- |
| affordable housing | 39 |
| access to credit | 17 |
| market access | 11 |
| institutional quality | 8 |
| access to markets | 7 |
| fractional share | 7 |
| institutional caliber | 7 |
| institutional-grade | 7 |
| lower barriers | 6 |
| capital markets access | 3 |
| eliminate barriers | 3 |
| reduced barriers | 3 |
| institutional level | 2 |
| reduce barriers | 1 |

## Sample Category Coverage

| Category | Rows |
| --- | --- |
| homeownership access | 39 |
| institutional-grade access for individuals | 24 |
| retail access to investing | 22 |
| broader market participation | 21 |
| expanded access to credit | 19 |
| lower barriers / level playing field | 13 |
| underserved / underbanked / unbanked | 10 |
| financial inclusion | 2 |

## Planned Audit Fields

- `spotcheck_label`
- `spotcheck_confidence`
- `spotcheck_notes`
- `spotcheck_disagreement_flag`

## Audit Instructions

- Use only the excerpt and `classification_guidelines_v3.md`.
- Do not use returns, prices, later news, outside firm knowledge, or external events.
- Set `spotcheck_disagreement_flag = yes` only when `spotcheck_label` differs from `final_label_v2`.
- Keep notes concise and specific.
