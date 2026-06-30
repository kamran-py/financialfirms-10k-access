# Conservative Filing Treatment V2 Audit Plan

## Purpose

This plan defines the next validation gate for V2 filing-level conservative candidates. The audit tests construct validity only and must not inspect prices, returns, benchmarks, news, or future outcomes.

## Sample Design

- Total sampled filings: 150
- Candidate-positive sampled filings: 100
- Candidate-negative sampled filings: 50
- Full V2 candidate-positive universe: 256
- The sample is deterministic and stratified across filing years, narrative subcategories or no-candidate reasons, sections, and firms.

## Audit Labels

- `yes_conservative_treatment`: excerpt satisfies external beneficiary, direct financial-access mechanism, and issuer attribution.
- `no_not_conservative_treatment`: excerpt fails the conservative standard.
- `borderline_broader_treatment_only`: access-related but not strict enough for the conservative main treatment.

## Validation Gate

- Candidate-positive precision must be at least 90% before V2 candidates can become conservative treatment variables.
- Candidate-negative false negatives should be documented and preferably remain below 15-20%.
- Borderline rows do not count as conservative positives.

## Sample Count By Candidate Flag

| Candidate flag | Sampled filings |
| --- | --- |
| yes | 100 |
| no | 50 |

## Sample Count By Filing Year

| Filing year | Sampled filings |
| --- | --- |
| 2015 | 24 |
| 2016 | 21 |
| 2017 | 24 |
| 2018 | 24 |
| 2019 | 10 |
| 2020 | 9 |
| 2021 | 9 |
| 2022 | 7 |
| 2023 | 8 |
| 2024 | 7 |
| 2025 | 7 |

## Sample Count By Subcategory Or Reason

| Subcategory or reason | Sampled filings |
| --- | --- |
| affordable housing / homeownership access | 33 |
| financial inclusion / underbanked / underserved | 29 |
| consumer credit access | 21 |
| payments / money movement / SMB commerce access | 10 |
| insurance / benefits access | 6 |
| FHLB membership/liquidity/required-program boilerplate | 4 |
| affordable-housing accounting/tax-credit/investment-book context | 4 |
| fractional-share/share-mechanics context | 4 |
| generic philanthropy/community context | 4 |
| generic trading/infrastructure/geographic market-access context | 4 |
| issuer liquidity/funding/access-to-credit context | 4 |
| market-access language lacks public-purpose/smaller-issuer beneficiary | 4 |
| no V2 conservative positive rule satisfied | 4 |
| no_raw_phrase_hits_in_extracted_sections | 4 |
| non-financial access or barriers context | 4 |
| regulator/agency boilerplate without issuer access action | 4 |
| retail/institutional-investor language is broader-sensitivity only | 3 |
| risk-only or competitor-access context | 3 |
| financial inclusion / underbanked / underserved; consumer credit access | 1 |

No prices, returns, SEC requests, or empirical claims are part of this audit.
