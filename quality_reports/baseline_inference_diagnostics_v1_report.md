# Baseline Inference Diagnostics V1 Report

## Guardrails

- This checkpoint adds inference diagnostics to the baseline association estimates.
- No new regression specification was estimated.
- No causal claims were made.
- Non-significance is not interpreted as proof of no association.

## MDE And Interval Diagnostics

| Horizon | Estimate | SE | MDE rule-of-thumb | 90% CI | 95% CI | Treated clusters | Inference note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0093684377 | 0.0348082971 | 0.0974632319 | [-0.0478861160, 0.0666229914] | [-0.0588558246, 0.0775927001] | 44 | more_informative_null |
| 3 | 0.0404468895 | 0.1192755012 | 0.3339714034 | [-0.1557438513, 0.2366376303] | [-0.1933330928, 0.2742268719] | 24 | wide_interval_lower_power_long_horizon |
| 5 | 0.1911030375 | 0.3734258454 | 1.0455923671 | [-0.4231278187, 0.8053338937] | [-0.5408116195, 0.9230176946] | 19 | wide_interval_lower_power_long_horizon |

## Equivalence Framing

The 90% confidence interval is reported to support later TOST-style equivalence framing if an economically meaningful equivalence threshold is justified before interpretation. Checked thresholds are diagnostic only and are not a substitute for a pre-specified economics-based threshold.

| Horizon | 90% CI | Smallest checked delta satisfying equivalence |
| --- | --- | --- |
| 1 | [-0.0478861160, 0.0666229914] | 0.10 |
| 3 | [-0.1557438513, 0.2366376303] | 0.25 |
| 5 | [-0.4231278187, 0.8053338937] | none_up_to_0.50 |

## Missingness And Non-Computed Rows

| Non-computed status | Rows |
| --- | --- |
| not_computed_missing_issuer_return_inside_window | 26 |
| not_computed_raw_coverage_incomplete | 27 |

## Interpretation Boundary

The 1-year estimate is more informative than the long-horizon estimates because its cluster-robust standard error and MDE are much smaller. The 3-year and especially 5-year estimates should not receive the same epistemic weight as the 1-year estimate. The increasing point estimates across horizons should not be narrated as a trend because the standard errors widen substantially with horizon, consistent with long-horizon buy-and-hold return noise and skew.

## Outputs

- `data/analysis/baseline_inference_diagnostics_v1.csv`
- `data/analysis/baseline_table_footnotes_v1.csv`

## Input Integrity

- `baseline_year_fe_estimates_v1.csv` unchanged: yes
- `baseline_year_fe_model_diagnostics_v1.csv` unchanged: yes
- `regression_modeling_dataset_v1.csv` unchanged: yes
- `return_analysis_panel_v1.csv` unchanged: yes
- `return_winsorization_thresholds_v1.csv` unchanged: yes
