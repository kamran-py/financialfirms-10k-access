# CHECKPOINT 31: Baseline Year-FE Estimation

## Status

Completed baseline filing-year fixed-effect association models.

## Created

- `scripts/run_baseline_year_fe_models_v1.py`
- `data/analysis/baseline_year_fe_estimates_v1.csv`
- `data/analysis/baseline_year_fe_model_diagnostics_v1.csv`
- `quality_reports/baseline_year_fe_estimation_v1_report.md`
- `CHECKPOINT_31_BASELINE_YEAR_FE_ESTIMATION.md`

## Validation

- Horizons estimated: 1, 3, 5
- Treatment coefficient rows: 3
- Upstream modeling dataset unchanged: yes

## Guardrails

- Baseline estimates are association-only.
- No causal claims made.
- No post-result controls added.
- Firm fixed effects, raw-return sensitivity, and alternative benchmarks remain future robustness checkpoints.
