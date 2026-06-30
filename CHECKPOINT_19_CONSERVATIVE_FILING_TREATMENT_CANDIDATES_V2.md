# CHECKPOINT 19: Conservative Filing Treatment Candidates V2

Generated at: 2026-06-29

## Completed

- Revised filing-level candidate construction after the CHECKPOINT_18 audit failure.
- Encoded stricter exclusions for FHLB boilerplate, regulator/agency language, generic market access, affordable-housing accounting, and broader-only retail/institutional investor language.
- Built V2 filing-level candidate flags and evidence rows from local extracted text.
- Prepared a fresh V2 audit sample and audit plan.
- Did not fetch prices, compute returns, make SEC requests, modify raw text artifacts, or make empirical performance claims.

## Files Created

- `config/conservative_filing_treatment_rules_v2.md`
- `scripts/build_conservative_filing_treatments_v2.py`
- `data/treatments/conservative_filing_treatment_candidates_v2.csv`
- `data/treatments/conservative_filing_treatment_evidence_v2.csv`
- `quality_reports/conservative_filing_treatment_candidates_v2_report.md`
- `data/review/conservative_filing_treatment_v2_audit_sample.csv`
- `quality_reports/conservative_filing_treatment_v2_audit_plan.md`
- `CHECKPOINT_19_CONSERVATIVE_FILING_TREATMENT_CANDIDATES_V2.md`

## Counts

- Filings considered: 5,954
- V2 candidate-positive filings: 256
- V2 candidate-negative filings: 5,698
- V2 evidence rows: 485
- V2 audit sample rows: 150
- V2 audit sample positives: 100
- V2 audit sample negatives: 50

## Candidate Positives By Filing Year

| Filing year | Candidate filings |
| --- | --- |
| 2015 | 15 |
| 2016 | 11 |
| 2017 | 16 |
| 2018 | 21 |
| 2019 | 18 |
| 2020 | 19 |
| 2021 | 18 |
| 2022 | 24 |
| 2023 | 40 |
| 2024 | 38 |
| 2025 | 36 |

## Evidence By Narrative Subcategory

| Narrative subcategory | Evidence rows |
| --- | --- |
| financial inclusion / underbanked / underserved | 276 |
| consumer credit access | 95 |
| affordable housing / homeownership access | 69 |
| payments / money movement / SMB commerce access | 39 |
| insurance / benefits access | 6 |

## Excluded High-Risk Phrase Families

| High-risk phrase family | Excluded raw-hit rows |
| --- | --- |
| affordable housing / homeownership access | 2271 |
| risk-section access language | 2044 |
| CRA/regulatory language | 1071 |
| access to credit | 850 |
| market access / access to markets / capital markets access | 701 |
| fractional share | 631 |
| institutional quality / institutional grade | 165 |
| lower/reduce/remove/eliminate barriers | 123 |

## Integrity

- Raw `data/extracted/phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `data/extracted/phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw phrase hits unchanged: yes
- Full-corpus V2 hit labels unchanged: yes
- Tiered V1 labels unchanged: yes

## Next Gate

Manually audit `data/review/conservative_filing_treatment_v2_audit_sample.csv`. Do not construct final treatment variables or fetch prices until the V2 audit passes the pre-specified precision gate.
