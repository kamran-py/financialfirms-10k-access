# Codex-Assisted Label Audit Plan

Generated at: 2026-06-29T05:28:15.668133+00:00

## Scope

- Prepared a manual audit sample from Codex-assisted review-sample labels only.
- Excluded all manual calibration rows.
- Did not fetch prices, run return analysis, make SEC requests, load outcome data, modify raw files, or scale classification to all 9,400 hits.
- Script version: `prepare_label_audit_sample_v1`.
- Deterministic sample seed: 20260629

## Guardrail Warning

Treatment construction is not finalized yet. This audit sample is a pre-scaling validation step for the text-treatment variable only.

## Eligible Rows And Sample Size

- Eligible Codex-assisted rows: 480
- Eligible Codex-assisted true-positive rows: 315
- Eligible Codex-assisted non-true-positive rows: 165
- Audit sample size: 150
- Audit true-positive target / actual: 100 / 100
- Audit non-true-positive target / actual: 50 / 50
- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged by this stage: yes

## Counts By Final Label

| Final label | Audit rows |
| --- | --- |
| true_positive_access_expansion | 100 |
| generic_marketing | 23 |
| operational_access_or_platform_language | 14 |
| risk_disclosure_only | 5 |
| ambiguous | 4 |
| false_positive | 4 |

## Counts By Category

| Category | Audit rows |
| --- | --- |
| expanded access to credit | 25 |
| underserved / underbanked / unbanked | 22 |
| lower barriers / level playing field | 19 |
| democratized access | 16 |
| institutional-grade access for individuals | 16 |
| homeownership access | 15 |
| retail access to investing | 14 |
| broader market participation | 10 |
| affordable financial products | 8 |
| financial inclusion | 5 |

## Counts By Phrase

| Phrase | Audit rows |
| --- | --- |
| affordable financial services | 6 |
| access to credit | 5 |
| affordable housing | 5 |
| credit access | 5 |
| institutional caliber | 5 |
| access to markets | 4 |
| affordable credit | 4 |
| democratizing access | 4 |
| fractional share | 4 |
| institutional quality | 4 |
| access to affordable credit | 3 |
| democratize access | 3 |
| democratize finance | 3 |
| expand access to credit | 3 |
| expanding access to credit | 3 |
| institutional-grade | 3 |
| remove barriers | 3 |
| access to affordable housing | 2 |
| access to homeownership | 2 |
| access to housing | 2 |
| access to investing | 2 |
| access to investment | 2 |
| affordable homeownership | 2 |
| affordable loans | 2 |
| broader participation | 2 |
| capital markets access | 2 |
| democratize financial services | 2 |
| democratizing financial services | 2 |
| eliminate barriers | 2 |
| eliminating barriers | 2 |
| expanded access to credit | 2 |
| expanding homeownership | 2 |
| financial inclusion | 2 |
| inclusive financial system | 2 |
| individual investors | 2 |
| institutional grade | 2 |
| institutional level | 2 |
| level playing field | 2 |
| lower barriers | 2 |
| market access | 2 |
| reduce barriers | 2 |
| reduced barriers | 2 |
| reducing barriers | 2 |
| removing barriers | 2 |
| retail access | 2 |
| retail investors | 2 |
| unbanked | 2 |
| unbanked consumers | 2 |
| unbanked populations | 2 |
| underbanked | 2 |
| underbanked consumers | 2 |
| underserved | 2 |
| underserved borrowers | 2 |
| underserved communities | 2 |
| underserved consumers | 2 |
| underserved markets | 2 |
| underserved populations | 2 |
| democratized access | 1 |
| democratizing finance | 1 |
| promote financial inclusion | 1 |

## Counts By Section

| Section | Audit rows |
| --- | --- |
| Item 1 Business | 91 |
| Item 1A Risk Factors | 32 |
| Item 7 MD&A | 27 |

## Counts By Filing Year

| Filing year | Audit rows |
| --- | --- |
| 2015 | 6 |
| 2016 | 7 |
| 2017 | 6 |
| 2018 | 5 |
| 2019 | 11 |
| 2020 | 12 |
| 2021 | 10 |
| 2022 | 21 |
| 2023 | 22 |
| 2024 | 24 |
| 2025 | 26 |

## Why This Audit Sample Is Sufficient Before Scaling

- The sample audits 150 of 480 Codex-assisted rows, or 31.25% of the Codex-assisted review-sample labels.
- It deliberately oversamples `true_positive_access_expansion` rows, where the main risk is over-calling positives that would later become treatment observations.
- The 50 non-positive rows provide checks for false negatives, label-boundary errors, and confusion among risk, operational, marketing, ambiguous, and false-positive labels.
- Stratification across category, phrase, filing year, section, and firm gives coverage of common wording families and known high-risk phrases before any full-corpus scaling.
- This is sufficient as a pre-scaling validation gate, not as final evidence that the full 9,400-hit corpus is correctly classified.

## Specific Risks To Check

- Over-calling true positives where the excerpt lacks an external beneficiary.
- Over-calling true positives where the excerpt lacks a financial-access mechanism.
- `affordable housing` in tax-credit, partnership, accounting, portfolio, or commitments-table context.
- `market access`, `access to markets`, and `capital markets access` in issuer financing, regulatory, competitive, risk, or operational contexts.
- `fractional share` in stock split, merger, issuance, or cash-in-lieu mechanics.
- `institutional quality`, `institutional-grade`, and related phrases in real-estate quality, platform, infrastructure, or internal capability contexts.
- `access to credit` in Item 1A or liquidity-risk language about issuer funding rather than consumers, borrowers, customers, LMI communities, or underserved groups.
- Regulatory or CRA language that lists compliance objectives without issuer action benefiting external financial users.
- Codex-assisted confidence values that look too high for short, noisy, or ambiguous excerpts.

## Audit Instructions

- Fill `audit_label`, `audit_confidence`, `audit_notes`, and `audit_disagreement_flag` only after manual review.
- Set `audit_disagreement_flag` to `yes` when audit label or confidence materially differs from the Codex-assisted/final label.
- Do not use returns, prices, later news, litigation, bankruptcies, acquisitions, or external firm events during audit.
- Do not construct treatment variables until audit results are reviewed.
