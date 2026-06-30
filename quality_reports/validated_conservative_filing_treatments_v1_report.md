# Validated Conservative Filing Treatments V1 Report

Generated from V3 candidate layer and CHECKPOINT_22 audit on 2026-06-29.

## Guardrails

- This stage constructs a validated text-treatment dataset only.
- No prices were fetched.
- No returns were computed.
- No benchmark data were loaded.
- No SEC requests were made.
- No empirical performance claims were made.

## Validation Basis

- Source candidate layer: `data/treatments/conservative_filing_treatment_candidates_v3.csv`.
- Source evidence layer: `data/treatments/conservative_filing_treatment_evidence_v3.csv`.
- Manual audit checkpoint: `CHECKPOINT_22_CONSERVATIVE_FILING_TREATMENT_V3_AUDIT.md`.
- Candidate-positive precision estimate: 92.0%.
- Candidate-negative false-negative estimate: 0.0%.

## Treatment Counts

- Filing rows in treatment panel: 5,954
- Validated conservative treated filings: 182
- Untreated/control filings: 5,772
- Validated evidence rows retained for treated filings: 330

## Treated Filings By Filing Year

| Filing year | Treated filings |
| --- | --- |
| 2015 | 12 |
| 2016 | 9 |
| 2017 | 13 |
| 2018 | 18 |
| 2019 | 14 |
| 2020 | 15 |
| 2021 | 15 |
| 2022 | 19 |
| 2023 | 26 |
| 2024 | 23 |
| 2025 | 18 |

## Treated Filings By Primary Narrative Subcategory

| Primary narrative subcategory | Treated filings |
| --- | --- |
| financial inclusion / underbanked / underserved | 91 |
| consumer credit access | 39 |
| affordable housing / homeownership access | 33 |
| payments / money movement / SMB commerce access | 13 |
| insurance / benefits access | 6 |

## Top Treated Firms

| Firm | Treated filings |
| --- | --- |
| CBSH (CIK0000022356) | 11 |
| PGC (CIK0001050743) | 11 |
| LSAK (CIK0001041514) | 10 |
| RM (CIK0001519401) | 10 |
| PYPL (CIK0001633917) | 8 |
| EEFT (CIK0001029199) | 7 |
| CUBB (CIK0001488813) | 7 |
| GPN (CIK0001123360) | 6 |
| MA (CIK0001141391) | 6 |
| RF (CIK0001281761) | 6 |
| ATLC (CIK0001464343) | 6 |
| CASH (CIK0000907471) | 5 |
| LC (CIK0001409970) | 5 |
| NBTB (CIK0000790359) | 4 |
| CATY (CIK0000861842) | 4 |
| FBP (CIK0001057706) | 4 |
| ARES (CIK0001176948) | 4 |
| OPRT (CIK0001538716) | 4 |
| VCTR (CIK0001570827) | 4 |
| OPFI (CIK0001818502) | 4 |
| STBA (CIK0000719220) | 3 |
| UVE (CIK0000891166) | 3 |
| CFFN (CIK0001490906) | 3 |
| ENVA (CIK0001529864) | 3 |
| UPST (CIK0001647639) | 3 |

## Calendar Window Observability For Treated Filings

These are date-maturity flags only, not return availability checks.

| 1Y matured | 3Y matured | 5Y matured | Treated filings |
| --- | --- | --- | --- |
| no | no | no | 2 |
| yes | no | no | 41 |
| yes | yes | no | 45 |
| yes | yes | yes | 94 |

## Residual Construct-Validity Risk Flags

| Residual risk flag | Treated filings |
| --- | --- |
| no | 136 |
| yes | 46 |

## Input Integrity

- `conservative_filing_treatment_candidates_v3.csv` before: `35732761204372a336815efa84e0df05ad6d2fb2399aa2aac8e092729a2b010e`
- `conservative_filing_treatment_candidates_v3.csv` after: `35732761204372a336815efa84e0df05ad6d2fb2399aa2aac8e092729a2b010e`
- `conservative_filing_treatment_candidates_v3.csv` unchanged: yes
- `conservative_filing_treatment_evidence_v3.csv` before: `953ce22aabe32ed3ca089c60e0fbacd197ef4564da1fdface7f7c97486e177c0`
- `conservative_filing_treatment_evidence_v3.csv` after: `953ce22aabe32ed3ca089c60e0fbacd197ef4564da1fdface7f7c97486e177c0`
- `conservative_filing_treatment_evidence_v3.csv` unchanged: yes
- `conservative_filing_treatment_v3_audit_sample_audited_20260629.csv` before: `2cc97e2685280e4dd04771968f6d08a47f63805026cf8aa5b72875f2f54de084`
- `conservative_filing_treatment_v3_audit_sample_audited_20260629.csv` after: `2cc97e2685280e4dd04771968f6d08a47f63805026cf8aa5b72875f2f54de084`
- `conservative_filing_treatment_v3_audit_sample_audited_20260629.csv` unchanged: yes
- `filing_index.csv` before: `1396bd2909f1020a9d50cef996b079f865c15c4daef5f7d0660e3262d04a476d`
- `filing_index.csv` after: `1396bd2909f1020a9d50cef996b079f865c15c4daef5f7d0660e3262d04a476d`
- `filing_index.csv` unchanged: yes
- `firm_universe.csv` before: `3eaaf45d0fd487a2c405ffc11f8972670dfc0440e3cbb5b171bf9e6905539d2a`
- `firm_universe.csv` after: `3eaaf45d0fd487a2c405ffc11f8972670dfc0440e3cbb5b171bf9e6905539d2a`
- `firm_universe.csv` unchanged: yes
- `phrase_hits.csv` before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- `phrase_hits.csv` after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- `phrase_hits.csv` unchanged: yes

## Next Gate

The next methodological step is linking/security-return preparation. That step should first audit ticker/CIK/security identifiers, delisting and corporate-action handling, benchmark definitions, and return-window status codes. SEC requests, if needed, should wait until that stage and must use a valid SEC user-agent.
