# Conservative Filing Treatment V3 Audit Results

Date: 2026-06-29

## Scope

Manual audit of `data/review/conservative_filing_treatment_v3_audit_sample.csv`. This is a construct-validity gate only. No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims are made.

## Results

- Sample rows audited: 150
- Candidate-positive rows sampled: 100
- Candidate-negative rows sampled: 50
- Accepted conservative positives: 92
- Borderline broader-treatment-only rows: 0
- Rejected as not conservative treatment: 58
- Overall strict disagreements versus V3 candidate flag: 8 / 150 = 5.3%

## Candidate-Positive Precision

- Strict accepted positives among sampled V3 candidate positives: 92 / 100 = 92.0%
- Borderline among sampled V3 candidate positives: 0 / 100 = 0.0%
- Rejected sampled V3 candidate positives: 8 / 100 = 8.0%

## Candidate-Negative False Negatives

- Strict accepted positives among sampled V3 candidate negatives: 0 / 50 = 0.0%
- Borderline among sampled V3 candidate negatives: 0 / 50 = 0.0%
- Confirmed negatives: 50 / 50 = 100.0%

## Accepted Conservative Positives By Audit Subcategory

- affordable housing / homeownership access: 23
- consumer credit access: 16
- financial inclusion / underbanked / underserved: 32
- financial inclusion / underbanked / underserved; consumer credit access: 3
- insurance / benefits access: 6
- payments / money movement / SMB commerce access: 12

## Candidate Category Diagnostics

- FHLB membership/liquidity/required-program boilerplate: no_not_conservative_treatment=4
- V3 hard exclusion: CRA/regulatory/congressional policy background: no_not_conservative_treatment=1
- V3 hard exclusion: FHLB housing/affordable-housing boilerplate: no_not_conservative_treatment=4
- V3 hard exclusion: broader-only private/HNW/investor-access vehicle: no_not_conservative_treatment=4
- affordable housing / homeownership access: no_not_conservative_treatment=1, yes_conservative_treatment=23
- affordable-housing accounting/tax-credit/investment-book context: no_not_conservative_treatment=4
- consumer credit access: no_not_conservative_treatment=6, yes_conservative_treatment=16
- financial inclusion / underbanked / underserved: no_not_conservative_treatment=1, yes_conservative_treatment=32
- financial inclusion / underbanked / underserved; consumer credit access: yes_conservative_treatment=3
- fractional-share/share-mechanics context: no_not_conservative_treatment=3
- generic philanthropy/community context: no_not_conservative_treatment=3
- generic trading/infrastructure/geographic market-access context: no_not_conservative_treatment=3
- insurance / benefits access: yes_conservative_treatment=6
- issuer liquidity/funding/access-to-credit context: no_not_conservative_treatment=3
- market-access language lacks public-purpose/smaller-issuer beneficiary: no_not_conservative_treatment=3
- no V2 conservative positive rule satisfied: no_not_conservative_treatment=3
- no_raw_phrase_hits_in_extracted_sections: no_not_conservative_treatment=3
- non-financial access or barriers context: no_not_conservative_treatment=3
- payments / money movement / SMB commerce access: yes_conservative_treatment=12
- regulator/agency boilerplate without issuer access action: no_not_conservative_treatment=3
- retail/institutional-investor language is broader-sensitivity only: no_not_conservative_treatment=3
- risk-only or competitor-access context: no_not_conservative_treatment=3

## Main Failure Modes

- V3 residual false positives are limited and mostly come from CRA/regulatory-policy text that still contains access-to-credit wording.
- One sampled affordable-housing positive was accounting/performance context: gain on sale of affordable-housing residential mortgage loans.
- Candidate negatives showed no strict false negatives in this sample.

## Decision

V3 passes the pre-specified 90% candidate-positive precision gate in this audit. It is reasonable to proceed to construct a validated conservative filing-level treatment variable from V3, while preserving the audit result and documenting the remaining known leakage modes. Price, return, and benchmark work should still wait until the validated treatment file and treatment-construction checkpoint are created.

## Integrity Checks

- Raw `data/extracted/phrase_hits.csv` SHA256: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- V3 candidate file SHA256: `35732761204372a336815efa84e0df05ad6d2fb2399aa2aac8e092729a2b010e`
- V3 evidence file SHA256: `953ce22aabe32ed3ca089c60e0fbacd197ef4564da1fdface7f7c97486e177c0`
- Audited output: `data/review/conservative_filing_treatment_v3_audit_sample_audited_20260629.csv`

No prices fetched, no returns computed, no SEC requests made, and no empirical claims made.
