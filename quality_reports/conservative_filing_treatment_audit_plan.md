# Conservative Filing Treatment Audit Plan

## Purpose

This plan defines the manual audit for conservative filing-level treatment candidates. The audit validates whether filing-level evidence supports candidate access-expansion treatment status under `config/conservative_filing_treatment_rules_v1.md`.

## Guardrails

- Audit only the filing-level candidate evidence and representative raw-hit excerpts.
- Do not inspect prices, returns, benchmarks, or future outcomes.
- Do not make SEC requests.
- Do not treat candidate flags as final treatment variables before audit.

## Sample Design

- Total sampled filings: 150
- Candidate-positive sampled filings: 100
- Candidate-negative sampled filings: 50
- The sample is deterministic and oversamples high-risk evidence, borderline single-evidence filings, and negative filings with raw high-risk phrase hits.
- The sample is round-robin stratified across filing years, narrative subcategories or no-candidate reasons, sections where available, and firms through deterministic accession ordering.

## Audit Fields

- `audit_candidate_flag`: yes/no.
- `audit_confidence`: high/medium/low.
- `audit_subcategory`: primary validated subcategory or excluded/non-treatment.
- `audit_notes`: concise rationale based only on filing text excerpts.
- `audit_disagreement_flag`: yes/no compared with constructed candidate flag.

## Sample Count By Candidate Flag

| Candidate flag | Sampled filings |
| --- | --- |
| yes | 100 |
| no | 50 |

## Sample Count By Filing Year

| Filing year | Sampled filings |
| --- | --- |
| 2015 | 34 |
| 2016 | 32 |
| 2017 | 23 |
| 2018 | 16 |
| 2019 | 14 |
| 2020 | 14 |
| 2021 | 15 |
| 2022 | 2 |

## Sample Count By Subcategory Or Reason

| Subcategory or reason | Sampled filings |
| --- | --- |
| affordable housing / homeownership access | 20 |
| financial inclusion / underbanked / underserved | 18 |
| smaller-issuer capital-market access | 15 |
| insurance / benefits access | 14 |
| payments / money movement / SMB commerce access | 12 |
| consumer credit access | 11 |
| consumer credit access; affordable housing / homeownership access | 3 |
| financial inclusion / underbanked / underserved; affordable housing / homeownership access | 3 |
| FHLB/issuer-liquidity context | 3 |
| affordable-housing accounting/tax-credit/portfolio context | 3 |
| fractional-share stock mechanics | 3 |
| generic affordable-housing philanthropy/community context | 3 |
| generic non-end-user barriers context | 3 |
| generic or issuer market-access context | 3 |
| generic regulatory/agency context without issuer action | 3 |
| high-risk raw phrase did not pass conservative positive rule: CRA/regulatory language | 3 |
| high-risk raw phrase did not pass conservative positive rule: access to credit | 3 |
| financial inclusion / underbanked / underserved; consumer credit access | 2 |
| private-market or alternative-investment access | 2 |
| high-risk raw phrase did not pass conservative positive rule: affordable housing / homeownership access | 2 |
| high-risk raw phrase did not pass conservative positive rule: lower/reduce/remove/eliminate barriers | 2 |
| high-risk raw phrase did not pass conservative positive rule: market access / access to markets / capital markets access | 2 |
| high-risk raw phrase did not pass conservative positive rule: risk-section access language | 2 |
| institutional-quality/platform context without retail access | 2 |
| issuer liquidity/funding/access-to-credit context | 2 |
| no_raw_phrase_hits_in_extracted_sections | 2 |
| non-financial underserved/access context | 2 |
| platform/API/infrastructure without explicit end-user financial access | 2 |
| raw hit did not satisfy conservative positive rule | 2 |
| risk-only or competitor access language | 2 |

## Validation Gate

The candidate layer should not be used for return analysis unless the manual audit demonstrates acceptable precision under the conservative treatment definition and documents false negatives among sampled candidate-negative filings.

Full candidate universe size: 5,954 filings.
