# CHECKPOINT 22 - Conservative Filing Treatment V3 Audit

Date: 2026-06-29

Completed manual audit of the 150-row V3 filing-level treatment sample.

## Created

- `data/review/conservative_filing_treatment_v3_audit_sample_audited_20260629.csv`
- `quality_reports/conservative_filing_treatment_v3_audit_results_20260629.md`
- `CHECKPOINT_22_CONSERVATIVE_FILING_TREATMENT_V3_AUDIT.md`

## Key Results

- Sample rows audited: 150
- Candidate-positive precision under strict conservative treatment: 92 / 100 = 92.0%
- Candidate-negative strict false-negative rate: 0 / 50 = 0.0%
- Borderline rows retained but excluded from conservative treatment: 0
- Overall strict disagreements versus V3 candidate flag: 8 / 150 = 5.3%

## Decision

V3 passes the 90% conservative precision gate. Proceed next to construct the validated conservative filing-level treatment dataset from V3, carrying audit notes and known residual false-positive categories forward. Do not fetch prices or compute returns until the validated treatment dataset has its own checkpoint.

## Guardrails Honored

- No prices fetched.
- No returns computed.
- No SEC requests made.
- No empirical performance claims made.
- Raw phrase hits and V3 candidate/evidence files were not modified.
