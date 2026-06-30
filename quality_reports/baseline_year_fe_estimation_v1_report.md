# Baseline Year-FE Estimation V1 Report

## Guardrails

- This checkpoint runs only the pre-specified baseline association models.
- Estimates are conditional associations, not causal effects.
- No claim is made that disclosure language caused later stock returns.
- No additional controls were introduced after viewing results.
- The upstream modeling dataset was preserved unchanged.

## Model

Separate models were estimated for each horizon:

```text
outcome_primary_excess_vwretd_winsor_p01_p99 = alpha + beta * treatment_main + filing_year_fixed_effects + error
```

- Standard errors are clustered by issuer.
- P-values and confidence intervals use a normal approximation to the cluster-robust t-statistic.
- Outcome is winsorized excess return versus CRSP value-weighted market return with dividends.

## Treatment Coefficients

| Horizon | Estimate | Cluster SE | t-stat | p-value | 95% CI low | 95% CI high | N | Clusters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0093684377 | 0.0348082971 | 0.2691438108 | 0.7878190177 | -0.0588558246 | 0.0775927001 | 3718 | 516 |
| 3 | 0.0404468895 | 0.1192755012 | 0.3391047544 | 0.7345308169 | -0.1933330928 | 0.2742268719 | 2698 | 450 |
| 5 | 0.1911030375 | 0.3734258454 | 0.5117563229 | 0.6088215621 | -0.5408116195 | 0.9230176946 | 1822 | 400 |

## Model Diagnostics

| Horizon | Rows | Treated | Controls | Issuers | Years | Rank | K | R-squared |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3718 | 138 | 3580 | 516 | 2015,2016,2017,2018,2019,2020,2021,2022,2023 | 10 | 10 | 0.1081883375 |
| 3 | 2698 | 93 | 2605 | 450 | 2015,2016,2017,2018,2019,2020,2021 | 8 | 8 | 0.0880839255 |
| 5 | 1822 | 63 | 1759 | 400 | 2015,2016,2017,2018,2019 | 6 | 6 | 0.0289515095 |

## Interpretation Boundary

These estimates describe whether validated conservative access-expansion filings are associated with different later benchmark-adjusted returns within filing-year cells. They do not identify a causal effect of the narrative, management policy, or any access-expansion action.

## Outputs

- `data/analysis/baseline_year_fe_estimates_v1.csv`
- `data/analysis/baseline_year_fe_model_diagnostics_v1.csv`

## Input Integrity

- `regression_modeling_dataset_v1.csv` before: `e11ae8cf2f706f7988217c2a57b123338919500766fd9705d98ffdd9899cce83`
- `regression_modeling_dataset_v1.csv` after: `e11ae8cf2f706f7988217c2a57b123338919500766fd9705d98ffdd9899cce83`
- `regression_modeling_dataset_v1.csv` unchanged: yes
