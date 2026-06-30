# Conservative Filing Treatment V2 Audit Results

Date: 2026-06-29

## Scope

Manual audit of `data/review/conservative_filing_treatment_v2_audit_sample.csv`. This is a construct-validity gate only. No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims are made.

## Results

- Sample rows audited: 150
- Candidate-positive rows sampled: 100
- Candidate-negative rows sampled: 50
- Accepted conservative positives: 70
- Borderline broader-treatment-only rows: 9
- Rejected as not conservative treatment: 71
- Overall strict disagreements versus V2 candidate flag: 30 / 150 = 20.0%

## Candidate-Positive Precision

- Strict accepted positives among sampled V2 candidate positives: 70 / 100 = 70.0%
- Borderline among sampled V2 candidate positives: 6 / 100 = 6.0%
- Rejected sampled V2 candidate positives: 24 / 100 = 24.0%

## Candidate-Negative False Negatives

- Strict accepted positives among sampled V2 candidate negatives: 0 / 50 = 0.0%
- Borderline among sampled V2 candidate negatives: 3 / 50 = 6.0%
- Confirmed negatives: 47 / 50 = 94.0%

## Accepted Conservative Positives By Audit Subcategory

- affordable housing / homeownership access: 17
- consumer credit access: 16
- financial inclusion / underbanked / underserved: 24
- financial inclusion / underbanked / underserved; consumer credit access: 1
- insurance / benefits access: 6
- payments / money movement / SMB commerce access: 6

## Candidate Category Diagnostics

- FHLB membership/liquidity/required-program boilerplate: no_not_conservative_treatment=4
- affordable housing / homeownership access: no_not_conservative_treatment=16, yes_conservative_treatment=17
- affordable-housing accounting/tax-credit/investment-book context: no_not_conservative_treatment=4
- consumer credit access: no_not_conservative_treatment=5, yes_conservative_treatment=16
- financial inclusion / underbanked / underserved: borderline_broader_treatment_only=3, no_not_conservative_treatment=2, yes_conservative_treatment=24
- financial inclusion / underbanked / underserved; consumer credit access: yes_conservative_treatment=1
- fractional-share/share-mechanics context: no_not_conservative_treatment=4
- generic philanthropy/community context: no_not_conservative_treatment=4
- generic trading/infrastructure/geographic market-access context: no_not_conservative_treatment=4
- insurance / benefits access: yes_conservative_treatment=6
- issuer liquidity/funding/access-to-credit context: no_not_conservative_treatment=4
- market-access language lacks public-purpose/smaller-issuer beneficiary: no_not_conservative_treatment=4
- no V2 conservative positive rule satisfied: borderline_broader_treatment_only=1, no_not_conservative_treatment=3
- no_raw_phrase_hits_in_extracted_sections: no_not_conservative_treatment=4
- non-financial access or barriers context: borderline_broader_treatment_only=2, no_not_conservative_treatment=2
- payments / money movement / SMB commerce access: borderline_broader_treatment_only=3, no_not_conservative_treatment=1, yes_conservative_treatment=6
- regulator/agency boilerplate without issuer access action: no_not_conservative_treatment=4
- retail/institutional-investor language is broader-sensitivity only: no_not_conservative_treatment=3
- risk-only or competitor-access context: no_not_conservative_treatment=3

## Main Failure Modes

- FHLB membership and FHLB required affordable-housing-program language still leaked into sampled positives.
- Generic commercial-real-estate loan categories that include affordable housing are not access-expansion narratives.
- Regulatory/CRA-rule language still leaked into positives when the issuer did not itself describe a product or program.
- Card-issuing technology, private-access vehicles, and broad financial-inclusion mission language are better treated as broader sensitivity candidates unless direct end-user access is explicit.

## Decision

V2 is materially cleaner than V1 but still fails the pre-specified 90% candidate-positive precision gate. Do not construct final treatment variables or fetch price/return data yet. A V3 rule pass should mostly target affordable-housing/FHLB exclusions, regulatory CRA-rule leakage, and infrastructure/broader-access borderline cases.

## Integrity Checks

- Raw `data/extracted/phrase_hits.csv` SHA256: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- V2 candidate file SHA256: `42d875eb89014b51aecdeb2493208365920ab1a22cc3988addf3a1709c49d018`
- V2 evidence file SHA256: `bb88f166237c4fbfbaa7ecbc7a69db4b2b133dcf84f0897318cf9ccdefcb2e74`
- Audited output: `data/review/conservative_filing_treatment_v2_audit_sample_audited_20260629.csv`

No prices fetched, no returns computed, no SEC requests made, and no empirical claims made.
