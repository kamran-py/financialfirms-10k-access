# CHECKPOINT 33: Baseline Finalization Diagnostics

## Status

Completed differential attrition, wild cluster bootstrap, and equivalence diagnostics.

## Created

- `scripts/run_baseline_finalization_diagnostics_v1.py`
- `data/analysis/baseline_differential_attrition_v1.csv`
- `data/analysis/baseline_horizon_transition_attrition_v1.csv`
- `data/analysis/baseline_wild_cluster_bootstrap_v1.csv`
- `data/analysis/baseline_equivalence_diagnostics_v1.csv`
- `quality_reports/baseline_finalization_diagnostics_v1_report.md`
- `CHECKPOINT_33_BASELINE_FINALIZATION_DIAGNOSTICS.md`

## Validation

- Scaffold event-window rows processed: 17,862
- Wild bootstrap replications requested per horizon: 999
- Upstream scaffold, link, linked-request, return-panel, modeling, and estimate files unchanged.

## Guardrails

- No new economic specification introduced.
- No causal claims made.
- Exit-mode claims remain blocked until delist/acquisition reasons are separately classified.
