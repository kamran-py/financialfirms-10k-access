# V2 Codex-Assisted Validation Sample Plan

Generated at: 2026-06-29T05:54:27.486230+00:00

## Scope

- Prepared a targeted validation sample from V2 Codex-assisted labels only.
- Excluded manual calibration and prior manual audit rows.
- Did not fetch prices, compute returns, make SEC requests, make empirical claims, scale classification to all 9,400 raw hits, or modify raw files.
- Script version: `prepare_v2_validation_sample_v1`.
- Deterministic seed: 20260629

## Guardrail Warning

Treatment construction is not finalized. This sample validates the text-treatment classifier only.

## Eligibility And Sample Size

- Eligible V2 Codex-assisted rows: 330
- Eligible V2 true-positive rows: 235
- Eligible V2 non-positive rows: 95
- Validation sample rows: 100
- Target / actual V2 positives: 75 / 75
- Target / actual V2 non-positives: 25 / 25
- High-risk phrase rows selected: 64
- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged by this stage: yes

## Counts By V2 Final Label

| V2 final label | Rows |
| --- | --- |
| true_positive_access_expansion | 75 |
| operational_access_or_platform_language | 12 |
| false_positive | 5 |
| generic_marketing | 4 |
| risk_disclosure_only | 2 |
| ambiguous | 1 |
| customer_access_unrelated_to_finance | 1 |

## Counts By Category

| Category | Rows |
| --- | --- |
| homeownership access | 32 |
| expanded access to credit | 15 |
| underserved / underbanked / unbanked | 15 |
| lower barriers / level playing field | 11 |
| retail access to investing | 11 |
| broader market participation | 6 |
| democratized access | 4 |
| affordable financial products | 2 |
| financial inclusion | 2 |
| institutional-grade access for individuals | 2 |

## Counts By Phrase

| Phrase | Rows |
| --- | --- |
| affordable housing | 31 |
| access to credit | 11 |
| fractional share | 5 |
| lower barriers | 3 |
| reduced barriers | 3 |
| access to investing | 2 |
| access to markets | 2 |
| affordable financial services | 2 |
| capital markets access | 2 |
| credit access | 2 |
| democratizing access | 2 |
| democratizing financial services | 2 |
| expand access to credit | 2 |
| financial inclusion | 2 |
| individual investors | 2 |
| institutional quality | 2 |
| level playing field | 2 |
| market access | 2 |
| reduce barriers | 2 |
| retail investors | 2 |
| unbanked | 2 |
| underbanked | 2 |
| underbanked consumers | 2 |
| underserved | 2 |
| underserved communities | 2 |
| underserved consumers | 2 |
| expanding homeownership | 1 |
| removing barriers | 1 |
| unbanked consumers | 1 |
| unbanked populations | 1 |
| underserved populations | 1 |

## Counts By Section

| Section | Rows |
| --- | --- |
| Item 1 Business | 53 |
| Item 7 MD&A | 26 |
| Item 1A Risk Factors | 21 |

## Counts By Filing Year

| Filing year | Rows |
| --- | --- |
| 2015 | 1 |
| 2016 | 10 |
| 2017 | 7 |
| 2018 | 10 |
| 2019 | 3 |
| 2020 | 9 |
| 2021 | 9 |
| 2022 | 10 |
| 2023 | 13 |
| 2024 | 14 |
| 2025 | 14 |

## Counts By High-Risk Phrase

| High-risk phrase | Rows |
| --- | --- |
| affordable housing | 31 |
| access to credit | 11 |
| fractional share | 5 |
| lower barriers | 3 |
| reduced barriers | 3 |
| access to markets | 2 |
| capital markets access | 2 |
| institutional quality | 2 |
| market access | 2 |
| reduce barriers | 2 |
| removing barriers | 1 |

## Validation Instructions

- Fill `validation_label`, `validation_confidence`, `validation_notes`, and `validation_disagreement_flag` using only the excerpt and `config/classification_guidelines_v3.md`.
- Set `validation_disagreement_flag` to `yes` when `validation_label` differs from `final_label_v2`; otherwise set it to `no`.
- Do not use returns, prices, later news, outside firm knowledge, litigation, bankruptcies, acquisitions, or external events.
- Keep notes concise but specific.
