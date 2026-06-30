# CHECKPOINT 21: Conservative Filing Treatment Candidates V3

Generated at: 2026-06-29

## Completed

- Revised V2 after CHECKPOINT_20 audit failure.
- Added hard exclusions for FHLB/housing boilerplate, CRE property lists, CRA/regulatory-policy background, infrastructure democratization, and broad mission language.
- Built V3 filing-level candidate flags, evidence rows, report, and audit sample.
- Did not fetch prices, compute returns, make SEC requests, modify raw text artifacts, or make empirical performance claims.

## Files Created

- `config/conservative_filing_treatment_rules_v3.md`
- `scripts/build_conservative_filing_treatments_v3.py`
- `data/treatments/conservative_filing_treatment_candidates_v3.csv`
- `data/treatments/conservative_filing_treatment_evidence_v3.csv`
- `quality_reports/conservative_filing_treatment_candidates_v3_report.md`
- `data/review/conservative_filing_treatment_v3_audit_sample.csv`
- `quality_reports/conservative_filing_treatment_v3_audit_plan.md`
- `CHECKPOINT_21_CONSERVATIVE_FILING_TREATMENT_CANDIDATES_V3.md`

## Counts

- Filings considered: 5,954
- V3 candidate-positive filings: 182
- V3 candidate-negative filings: 5,772
- V3 evidence rows: 330
- V3 audit sample rows: 150
- V3 audit sample positives: 100
- V3 audit sample negatives: 50

## Candidate Positives By Filing Year

| Filing year | Candidate filings |
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

## Evidence By Narrative Subcategory

| Narrative subcategory | Evidence rows |
| --- | --- |
| financial inclusion / underbanked / underserved | 187 |
| consumer credit access | 69 |
| affordable housing / homeownership access | 42 |
| payments / money movement / SMB commerce access | 26 |
| insurance / benefits access | 6 |

## Excluded High-Risk Phrase Families

| High-risk phrase family | Excluded raw-hit rows |
| --- | --- |
| affordable housing / homeownership access | 2300 |
| risk-section access language | 2056 |
| CRA/regulatory language | 1096 |
| access to credit | 876 |
| market access / access to markets / capital markets access | 701 |
| fractional share | 631 |
| institutional quality / institutional grade | 165 |
| lower/reduce/remove/eliminate barriers | 123 |

## Integrity

- Raw phrase hits unchanged: yes
- Full-corpus V2 hit labels unchanged: yes
- Tiered V1 labels unchanged: yes

## Next Gate

Manually audit `data/review/conservative_filing_treatment_v3_audit_sample.csv`. Do not construct final treatment variables or fetch prices until V3 passes the pre-specified precision gate.
