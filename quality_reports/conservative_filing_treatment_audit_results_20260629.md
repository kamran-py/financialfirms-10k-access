# Conservative Filing Treatment Audit Results

Date: 2026-06-29

## Scope

Manual audit of `data/review/conservative_filing_treatment_audit_sample.csv` from CHECKPOINT_17. This is a construct-validity audit only. No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims are made.

## Audit Rule

A filing is accepted for the conservative treatment only when the excerpt supports both: (1) an external beneficiary and (2) a direct financial-access mechanism attributable to the issuer's filing narrative. Borderline rows are retained for possible broader sensitivity analysis but are not accepted for the conservative main treatment.

## Results

- Sample rows audited: 150
- Candidate-positive rows sampled: 100
- Candidate-negative rows sampled: 50
- Accepted conservative positives: 45
- Borderline broader-treatment-only rows: 5
- Rejected as not conservative treatment: 100
- Overall strict disagreements versus candidate flag: 61 / 150 = 40.7%

## Candidate-Positive Precision

- Strict accepted positives among sampled candidate positives: 42 / 100 = 42.0%
- Borderline among sampled candidate positives: 2 / 100 = 2.0%
- Rejected candidate positives: 56 / 100 = 56.0%

## Candidate-Negative False Negatives

- Strict accepted positives among sampled candidate negatives: 3 / 50 = 6.0%
- Borderline among sampled candidate negatives: 3 / 50 = 6.0%
- Confirmed negatives: 44 / 50 = 88.0%

## Accepted Conservative Positives By Audit Subcategory

- affordable housing / homeownership access: 7
- consumer credit access: 9
- consumer credit access; affordable housing / homeownership access: 3
- financial inclusion / underbanked / underserved: 1
- financial inclusion / underbanked / underserved; affordable housing / homeownership access: 1
- financial inclusion / underbanked / underserved; consumer credit access: 2
- insurance / benefits access: 6
- payments / money movement / SMB commerce access: 13
- private-market or alternative-investment access: 1
- smaller-issuer capital-market access: 2

## Candidate Category Diagnostics

- affordable housing / homeownership access: no_not_conservative_treatment=13, yes_conservative_treatment=7
- candidate-negative: borderline_broader_treatment_only=3, no_not_conservative_treatment=44, yes_conservative_treatment=3
- consumer credit access: borderline_broader_treatment_only=1, no_not_conservative_treatment=1, yes_conservative_treatment=9
- consumer credit access; affordable housing / homeownership access: yes_conservative_treatment=3
- financial inclusion / underbanked / underserved: no_not_conservative_treatment=17, yes_conservative_treatment=1
- financial inclusion / underbanked / underserved; affordable housing / homeownership access: no_not_conservative_treatment=2, yes_conservative_treatment=1
- financial inclusion / underbanked / underserved; consumer credit access: yes_conservative_treatment=2
- insurance / benefits access: no_not_conservative_treatment=8, yes_conservative_treatment=6
- payments / money movement / SMB commerce access: yes_conservative_treatment=12
- private-market or alternative-investment access: borderline_broader_treatment_only=1, yes_conservative_treatment=1
- smaller-issuer capital-market access: no_not_conservative_treatment=15


## Main Failure Modes

- FHLB membership/liquidity and required affordable-housing-program language often looks like housing access but is regulatory or institutional background rather than issuer access-oriented disclosure signal.
- CFPB/FIO/agency language often describes regulator authority, not management action by the filing firm.
- Generic `market access` often means trading infrastructure, issuer geographic expansion, competitor scale, or capital resources rather than beneficiary access.
- Low-income housing partnerships are mixed: rows were accepted only when the excerpt says the partnerships supply funds for construction/operation of affordable housing for lower-income beneficiaries.
- A small number of candidate-negative rows appear to be missed conservative positives, especially municipal-bond market access for public-purpose issuers and underserved SMB capital/service access.

## Decision

Do not scale these candidate flags into final treatment variables yet. Candidate-positive precision is below the 90% threshold for a conservative main treatment. The filing-level approach is still better than hit-level classification, but the candidate rules need another revision focused on excluding regulatory/FHLB/agency boilerplate and separating conservative positives from broader sensitivity-only cases.

## Integrity Checks

- Raw `data/extracted/phrase_hits.csv` SHA256: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Candidate file `data/treatments/conservative_filing_treatment_candidates_v1.csv` SHA256: `15ff2c7b510d9bcf15e82a34bc3fc905cd1ae09421c4a4f7422d53287575d27a`
- Evidence file `data/treatments/conservative_filing_treatment_evidence_v1.csv` SHA256: `f32a2f35f7acacc95bf77f5ad01695e653b43af506e7235c04a8bf297a86e6f8`
- Audited output: `data/review/conservative_filing_treatment_audit_sample_audited_20260629.csv`

No prices fetched, no returns computed, no SEC requests made, and no empirical claims made.
