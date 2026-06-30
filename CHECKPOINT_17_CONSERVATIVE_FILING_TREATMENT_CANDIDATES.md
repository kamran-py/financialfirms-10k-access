# CHECKPOINT 17: Conservative Filing Treatment Candidates

Generated at: 2026-06-29

## Completed

- Created conservative filing-level treatment rules.
- Built filing-level candidate flags from raw extracted phrase hits and extracted filing sections.
- Built candidate evidence table preserving hit-level excerpts.
- Wrote candidate construction report.
- Prepared filing-level audit sample and audit plan for the next validation gate.
- Did not fetch prices, compute returns, make SEC requests, modify raw phrase hits, or make empirical performance claims.
- Did not use V2 full-corpus labels or tiered V1 hit-level labels as treatment variables.

## Files Created

- `config/conservative_filing_treatment_rules_v1.md`
- `scripts/build_conservative_filing_treatments_v1.py`
- `data/treatments/conservative_filing_treatment_candidates_v1.csv`
- `data/treatments/conservative_filing_treatment_evidence_v1.csv`
- `quality_reports/conservative_filing_treatment_candidates_v1_report.md`
- `data/review/conservative_filing_treatment_audit_sample.csv`
- `quality_reports/conservative_filing_treatment_audit_plan.md`
- `CHECKPOINT_17_CONSERVATIVE_FILING_TREATMENT_CANDIDATES.md`

## Source File Integrity

- Raw `data/extracted/phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `data/extracted/phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes
- V2 classified SHA256 before: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- V2 classified SHA256 after: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- V2 classified file unchanged: yes
- Tiered V1 SHA256 before: `c647e1d0acc4498d40426388e8f7046b664e7fee6eca3ffc817ddb50707159df`
- Tiered V1 SHA256 after: `c647e1d0acc4498d40426388e8f7046b664e7fee6eca3ffc817ddb50707159df`
- Tiered V1 file unchanged: yes

## Candidate Filing Counts

- Total filings considered: 5,954
- Conservative candidate-positive filings: 928
- Candidate-negative filings: 5,026

## Evidence Counts

- Candidate evidence rows: 2,012

Candidate positives by filing year:

| Filing year | Candidate filings |
| --- | --- |
| 2015 | 52 |
| 2016 | 56 |
| 2017 | 60 |
| 2018 | 63 |
| 2019 | 62 |
| 2020 | 64 |
| 2021 | 80 |
| 2022 | 108 |
| 2023 | 134 |
| 2024 | 131 |
| 2025 | 118 |

Candidate evidence by narrative subcategory:

| Narrative subcategory | Evidence rows |
| --- | --- |
| financial inclusion / underbanked / underserved | 630 |
| consumer credit access | 559 |
| affordable housing / homeownership access | 415 |
| insurance / benefits access | 193 |
| smaller-issuer capital-market access | 94 |
| payments / money movement / SMB commerce access | 73 |
| private-market or alternative-investment access | 31 |
| retail investing / brokerage democratization | 14 |
| generic/other access-expansion | 3 |

## Audit Sample Counts

- Total audit sample filings: 150
- Candidate-positive audit rows: 100
- Candidate-negative audit rows: 50

## Main Exclusion Rules

- Exclude fractional-share stock mechanics.
- Exclude institutional-quality/platform language unless explicitly tied to retail or individual investor access.
- Exclude generic market access unless smaller issuers or external clients are beneficiaries.
- Exclude issuer liquidity, issuer funding, issuer access to credit, FHLB advances, and issuer credit-rating contexts.
- Exclude affordable-housing accounting, tax-credit, partnership, portfolio, investment-income, sale, and commitments-table context.
- Exclude generic barriers language in AI, HR, healthcare, sports, regulation, competition, and internal operations.
- Exclude generic ESG, mission, platform, API, infrastructure, or operational language without explicit end-user financial access.

Excluded high-risk phrase families from raw hits:

| High-risk phrase family | Excluded raw-hit rows |
| --- | --- |
| affordable housing / homeownership access | 1926 |
| risk-section access language | 1795 |
| CRA/regulatory language | 1052 |
| access to credit | 826 |
| fractional share | 631 |
| market access / access to markets / capital markets access | 602 |
| institutional quality / institutional grade | 150 |
| lower/reduce/remove/eliminate barriers | 119 |

## Remaining Construct-Validity Risks

- Conservative filing-level candidates may still include regulatory or risk-section text that names a beneficiary and mechanism but is not issuer-specific action.
- Affordable-housing language remains difficult where community, development, program-definition, financing, and tax-credit language are adjacent.
- Retail-investor and fractional-investing language can still mix product access with stock mechanics or risk disclosure.
- Filing-level aggregation means one qualifying excerpt marks the filing as a candidate; manual audit must verify whether the evidence is strong enough for treatment construction.
- Company names are blank because the requested construction inputs do not include `company_name`; identifiers are preserved through firm_id, ticker, CIK, accession, and filing date.

## Guardrail Reminder

Returns, prices, benchmark outcomes, SEC requests, and empirical performance analysis remain off-limits until filing-level treatment candidates pass audit. These outputs are candidate construction artifacts only and are not final treatment variables.
