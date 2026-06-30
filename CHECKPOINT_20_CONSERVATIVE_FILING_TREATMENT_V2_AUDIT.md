# CHECKPOINT 20 - Conservative Filing Treatment V2 Audit

Date: 2026-06-29

Completed manual audit of the 150-row V2 filing-level treatment sample.

## Created

- `data/review/conservative_filing_treatment_v2_audit_sample_audited_20260629.csv`
- `quality_reports/conservative_filing_treatment_v2_audit_results_20260629.md`
- `CHECKPOINT_20_CONSERVATIVE_FILING_TREATMENT_V2_AUDIT.md`

## Key Results

- Sample rows audited: 150
- Candidate-positive precision under strict conservative treatment: 70 / 100 = 70.0%
- Candidate-negative strict false-negative rate: 0 / 50 = 0.0%
- Borderline rows retained but excluded from conservative treatment: 9
- Overall strict disagreements versus V2 candidate flag: 30 / 150 = 20.0%

## Decision

Do not construct final treatment variables from V2 candidates yet. V2 improved over V1 but did not pass the 90% precision gate. Revise candidate construction again with hard exclusions for FHLB/affordable-housing boilerplate, generic CRE affordable-housing loan categories, regulatory CRA-rule text, and broader-only access language.

## Guardrails Honored

- No prices fetched.
- No returns computed.
- No SEC requests made.
- No empirical performance claims made.
- Raw phrase hits and V2 candidate/evidence files were not modified.
