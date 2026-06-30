# CHECKPOINT 30: Modeling Dataset And Specification

## Status

Completed regression-modeling dataset construction and pre-estimation model specification.

## Created

- `scripts/prepare_modeling_specification_v1.py`
- `data/analysis/regression_modeling_dataset_v1.csv`
- `data/analysis/model_sample_support_v1.csv`
- `methodology/model_specification_v1.md`
- `quality_reports/modeling_dataset_pre_estimation_validation_v1_report.md`
- `CHECKPOINT_30_MODELING_DATASET_AND_SPEC.md`

## Validation

- Modeling rows: 8,238
- Non-analysis-ready rows excluded: 53
- Required field issue types: 0
- Upstream analysis panel unchanged: yes

## Guardrails

- No regressions run.
- No event-study estimates run.
- No p-values, coefficients, or empirical claims produced.
- Controls beyond filing-year fixed effects remain blocked until a separate point-in-time control-import checkpoint.
