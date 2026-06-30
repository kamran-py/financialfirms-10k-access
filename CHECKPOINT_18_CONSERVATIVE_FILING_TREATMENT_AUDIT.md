# CHECKPOINT 18 - Conservative Filing Treatment Audit

Date: 2026-06-29

Completed manual audit of the 150-row conservative filing-level treatment sample from CHECKPOINT_17.

## Created

- `data/review/conservative_filing_treatment_audit_sample_audited_20260629.csv`
- `quality_reports/conservative_filing_treatment_audit_results_20260629.md`
- `CHECKPOINT_18_CONSERVATIVE_FILING_TREATMENT_AUDIT.md`

## Key Results

- Sample rows audited: 150
- Candidate-positive precision under strict conservative treatment: 42 / 100 = 42.0%
- Candidate-negative strict false-negative rate: 3 / 50 = 6.0%
- Borderline rows retained but excluded from conservative treatment: 5
- Overall strict disagreements versus candidate flag: 61 / 150 = 40.7%

## Decision

Do not construct final treatment variables from `conservative_filing_treatment_candidates_v1.csv` yet. The filing-level approach is directionally better, but the candidate-positive precision is below the pre-specified 90% threshold. Revise filing-level rules to remove regulatory/FHLB/agency boilerplate and split conservative positives from broader sensitivity-only cases, then re-audit before any price, return, or benchmark work.

## Guardrails Honored

- No prices fetched.
- No returns computed.
- No SEC requests made.
- No empirical performance claims made.
- Raw phrase hits and candidate/evidence files were not modified.
