# Tiered Classification Audit Plan

Generated at: 2026-06-29T20:10:05.331475+00:00

## Scope And Guardrails

- Prepared a post-tiered classification audit sample from `data/classified/phrase_hits_tiered_v1.csv`.
- Did not modify `data/extracted/phrase_hits.csv`.
- Did not modify `data/classified/phrase_hits_tiered_v1.csv`.
- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.
- This sample validates text-treatment candidates only.

## File Integrity

- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes
- Tiered classified SHA256 before: `c647e1d0acc4498d40426388e8f7046b664e7fee6eca3ffc817ddb50707159df`
- Tiered classified SHA256 after: `c647e1d0acc4498d40426388e8f7046b664e7fee6eca3ffc817ddb50707159df`
- Tiered classified file unchanged: yes

## Full-Corpus Counts

- Total tiered classified rows: 9400
| Tiered label | Rows |
| --- | ---: |
| excluded_non_treatment | 5812 |
| tier_3_exploratory | 1571 |
| tier_2_broader_validated | 1292 |
| tier_1_conservative | 725 |

## Audit Sample Design

- Total target sample size: 150 rows.
- Target label split: 75 Tier 1, 50 Tier 2, 25 excluded.
- Deterministic sampling seed: 1601.
- Oversampling priorities: high-risk phrase flags and families, high-count firms, all sections where feasible, filing years 2015-2025, and high-count narrative subcategories.
- Tier 3 rows are not sampled directly in this audit because the requested validation design focuses on Tier 1, Tier 2, and excluded false negatives.

## Sample Counts

- Audit sample rows: 150
| Tiered label | Sample rows |
| --- | ---: |
| tier_1_conservative | 75 |
| tier_2_broader_validated | 50 |
| excluded_non_treatment | 25 |

## High-Risk Coverage

| High-risk flag | Sample rows |
| --- | ---: |
| yes | 131 |
| no | 19 |

| High-risk phrase family | Sample rows |
| --- | ---: |
| risk-section access language | 39 |
| CRA/regulatory language | 25 |
| none | 19 |
| CRA/regulatory language; risk-section access language | 18 |
| affordable housing | 13 |
| access to credit | 8 |
| market access / access to markets / capital markets access; risk-section access language | 5 |
| market access / access to markets / capital markets access | 4 |
| fractional share | 4 |
| access to credit; risk-section access language | 3 |
| lower/reduce/remove/eliminate barriers | 3 |
| institutional quality / institutional-grade / institutional caliber / institutional level | 3 |
| affordable housing; risk-section access language | 2 |
| fractional share; risk-section access language | 2 |
| lower/reduce/remove/eliminate barriers; risk-section access language | 1 |
| institutional quality / institutional-grade / institutional caliber / institutional level; risk-section access language | 1 |

## Coverage By Section

| Section | Sample rows |
| --- | ---: |
| Item 1A Risk Factors | 79 |
| Item 1 Business | 52 |
| Item 7 MD&A | 19 |

## Coverage By Filing Year

| Filing year | Sample rows |
| --- | ---: |
| 2025 | 22 |
| 2022 | 19 |
| 2023 | 15 |
| 2017 | 14 |
| 2024 | 14 |
| 2019 | 12 |
| 2018 | 12 |
| 2016 | 12 |
| 2021 | 11 |
| 2020 | 10 |
| 2015 | 9 |

## Coverage By Narrative Subcategory

| Narrative subcategory | Sample rows |
| --- | ---: |
| financial inclusion / underbanked / underserved | 56 |
| consumer credit access | 28 |
| excluded / non-treatment | 25 |
| affordable housing / homeownership access | 14 |
| retail investing / brokerage democratization | 12 |
| smaller-issuer capital-market access | 7 |
| payments / money movement / SMB commerce access | 2 |
| generic/other access-expansion | 2 |
| private-market or alternative-investment access | 2 |
| fee / cost / minimum-reduction framing | 1 |
| insurance / benefits access | 1 |

## Top Sample Phrases

| Phrase | Sample rows |
| --- | ---: |
| affordable housing | 15 |
| unbanked | 14 |
| underserved communities | 13 |
| underserved markets | 12 |
| retail investors | 12 |
| access to credit | 11 |
| underserved borrowers | 11 |
| market access | 9 |
| financial inclusion | 9 |
| underbanked | 7 |
| fractional share | 6 |
| individual investors | 6 |
| expand access to credit | 5 |
| underserved | 3 |
| underserved consumers | 2 |
| institutional-grade | 2 |
| democratize finance | 1 |
| affordable homeownership | 1 |
| democratizing finance | 1 |
| reduced barriers | 1 |
| institutional quality | 1 |
| democratized access | 1 |
| affordable financial services | 1 |
| removing barriers | 1 |
| promote financial inclusion | 1 |

## Label Coverage Diagnostics

### High-Risk Family By Label

- CRA/regulatory language: tier_1_conservative=15, tier_2_broader_validated=7, excluded_non_treatment=3
- CRA/regulatory language; risk-section access language: tier_1_conservative=4, tier_2_broader_validated=5, excluded_non_treatment=9
- access to credit: tier_1_conservative=6, tier_2_broader_validated=1, excluded_non_treatment=1
- access to credit; risk-section access language: tier_1_conservative=1, tier_2_broader_validated=1, excluded_non_treatment=1
- affordable housing: tier_1_conservative=5, tier_2_broader_validated=7, excluded_non_treatment=1
- affordable housing; risk-section access language: tier_1_conservative=1, excluded_non_treatment=1
- fractional share: tier_1_conservative=2, tier_2_broader_validated=1, excluded_non_treatment=1
- fractional share; risk-section access language: tier_2_broader_validated=1, excluded_non_treatment=1
- institutional quality / institutional-grade / institutional caliber / institutional level: tier_2_broader_validated=2, excluded_non_treatment=1
- institutional quality / institutional-grade / institutional caliber / institutional level; risk-section access language: excluded_non_treatment=1
- lower/reduce/remove/eliminate barriers: tier_2_broader_validated=2, excluded_non_treatment=1
- lower/reduce/remove/eliminate barriers; risk-section access language: excluded_non_treatment=1
- market access / access to markets / capital markets access: tier_1_conservative=2, tier_2_broader_validated=1, excluded_non_treatment=1
- market access / access to markets / capital markets access; risk-section access language: tier_2_broader_validated=4, excluded_non_treatment=1
- none: tier_1_conservative=10, tier_2_broader_validated=9
- risk-section access language: tier_1_conservative=29, tier_2_broader_validated=9, excluded_non_treatment=1

### Section By Label

- Item 1 Business: tier_1_conservative=31, tier_2_broader_validated=17, excluded_non_treatment=4
- Item 1A Risk Factors: tier_1_conservative=36, tier_2_broader_validated=24, excluded_non_treatment=19
- Item 7 MD&A: tier_1_conservative=8, tier_2_broader_validated=9, excluded_non_treatment=2

### Filing Year By Label

- 2015: tier_1_conservative=6, tier_2_broader_validated=2, excluded_non_treatment=1
- 2016: tier_1_conservative=8, tier_2_broader_validated=2, excluded_non_treatment=2
- 2017: tier_1_conservative=9, tier_2_broader_validated=3, excluded_non_treatment=2
- 2018: tier_1_conservative=6, tier_2_broader_validated=4, excluded_non_treatment=2
- 2019: tier_1_conservative=5, tier_2_broader_validated=3, excluded_non_treatment=4
- 2020: tier_1_conservative=5, tier_2_broader_validated=3, excluded_non_treatment=2
- 2021: tier_1_conservative=4, tier_2_broader_validated=5, excluded_non_treatment=2
- 2022: tier_1_conservative=11, tier_2_broader_validated=6, excluded_non_treatment=2
- 2023: tier_1_conservative=5, tier_2_broader_validated=7, excluded_non_treatment=3
- 2024: tier_1_conservative=6, tier_2_broader_validated=5, excluded_non_treatment=3
- 2025: tier_1_conservative=10, tier_2_broader_validated=10, excluded_non_treatment=2

## Manual Audit Instructions

Fill `audit_tiered_label`, `audit_confidence`, `audit_narrative_subcategory`, `audit_notes`, and `audit_disagreement_flag` using only the excerpt and tiered classification guidelines.

Allowed `audit_tiered_label` values:

- `tier_1_conservative`
- `tier_2_broader_validated`
- `tier_3_exploratory`
- `excluded_non_treatment`

`audit_disagreement_flag` must be `yes` when the audit label differs from the original `tiered_label`, otherwise `no`.

## Decision Rules For Results Report

- Tier 1 may proceed to main treatment-candidate construction only if sampled Tier 1 precision is at least 90%.
- Tier 2 may proceed to broader/sensitivity treatment-candidate construction only if sampled Tier 2 precision is at least 80%.
- If excluded false-negative rate exceeds 20%, revise the classifier before treatment construction.
- If Tier 1 precision is below 90%, revise the classifier before treatment construction.
