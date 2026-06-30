# CHECKPOINT 28: WRDS CRSP Window Returns

## Status

Completed WRDS CRSP window-return computation V1.

## Created

- `scripts/compute_wrds_crsp_window_returns_v1.py`
- `data/returns/wrds_crsp_window_returns_v1.csv`
- `quality_reports/wrds_crsp_window_return_computation_v1_report.md`
- `CHECKPOINT_28_WRDS_CRSP_WINDOW_RETURNS.md`

## Validation

- Coverage input rows: 8,291
- Output return-window rows: 8,291
- Computed rows: 8,238
- Non-computed rows retained: 53
- Computed treated rows: 294
- Raw WRDS daily issuer returns file unchanged.
- Raw WRDS market benchmark file unchanged.
- Coverage input file unchanged.

## Guardrails

- No prices fetched.
- No SEC requests made.
- No regressions or event-study estimates run.
- No empirical performance or causal claims made.
