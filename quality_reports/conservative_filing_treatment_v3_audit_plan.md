# Conservative Filing Treatment V3 Audit Plan

## Purpose

This plan defines the next validation gate for V3 filing-level conservative candidates. The audit tests construct validity only and must not inspect prices, returns, benchmarks, news, or future outcomes.

## Sample Design

- Total sampled filings: 150
- Candidate-positive sampled filings: 100
- Candidate-negative sampled filings: 50
- Full V3 candidate-positive universe: 182
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
| 2015 | 25 |
| 2016 | 23 |
| 2017 | 26 |
| 2018 | 16 |
| 2019 | 8 |
| 2020 | 8 |
| 2021 | 10 |
| 2022 | 8 |
| 2023 | 9 |
| 2024 | 8 |
| 2025 | 9 |

## Sample Count By Subcategory Or Reason

| Subcategory or reason | Sampled filings |
| --- | --- |
| financial inclusion / underbanked / underserved | 33 |
| affordable housing / homeownership access | 24 |
| consumer credit access | 22 |
| payments / money movement / SMB commerce access | 12 |
| insurance / benefits access | 6 |
| FHLB membership/liquidity/required-program boilerplate | 4 |
| V3 hard exclusion: FHLB housing/affordable-housing boilerplate | 4 |
| V3 hard exclusion: broader-only private/HNW/investor-access vehicle | 4 |
| affordable-housing accounting/tax-credit/investment-book context | 4 |
| financial inclusion / underbanked / underserved; consumer credit access | 3 |
| fractional-share/share-mechanics context | 3 |
| generic philanthropy/community context | 3 |
| generic trading/infrastructure/geographic market-access context | 3 |
| issuer liquidity/funding/access-to-credit context | 3 |
| market-access language lacks public-purpose/smaller-issuer beneficiary | 3 |
| no V2 conservative positive rule satisfied | 3 |
| no_raw_phrase_hits_in_extracted_sections | 3 |
| non-financial access or barriers context | 3 |
| regulator/agency boilerplate without issuer access action | 3 |
| retail/institutional-investor language is broader-sensitivity only | 3 |
| risk-only or competitor-access context | 3 |
| V3 hard exclusion: CRA/regulatory/congressional policy background | 1 |

No prices, returns, SEC requests, or empirical claims are part of this audit.
