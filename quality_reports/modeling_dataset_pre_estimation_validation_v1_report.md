# Modeling Dataset Pre-Estimation Validation V1 Report

## Guardrails

- This step built modeling inputs and locked the first model specification.
- No regressions, event-study estimates, p-values, or empirical claims were produced.
- The upstream analysis panel was preserved unchanged.

## Inputs

- `data/analysis/return_analysis_panel_v1.csv`

## Outputs

- `data/analysis/regression_modeling_dataset_v1.csv`
- `data/analysis/model_sample_support_v1.csv`
- `methodology/model_specification_v1.md`

## Reconciliation

- Analysis panel rows read: 8,291
- Regression modeling rows written: 8,238
- Non-analysis-ready rows excluded from modeling dataset: 53

## Required Field Checks

| Field issue | Rows |
| --- | --- |
| none | 0 |

## Horizon Support

| Horizon years | Rows | Treated rows | Control rows | Unique issuers | Treated issuers | Within-issuer variation issuers |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3718 | 138 | 3580 | 516 | 44 | 37 |
| 3 | 2698 | 93 | 2605 | 450 | 24 | 17 |
| 5 | 1822 | 63 | 1759 | 400 | 19 | 10 |

## Treated Filing-Year Support

| Filing year | Horizon years | Treated rows |
| --- | --- | --- |
| 2015 | 1 | 11 |
| 2015 | 3 | 11 |
| 2015 | 5 | 11 |
| 2016 | 1 | 9 |
| 2016 | 3 | 9 |
| 2016 | 5 | 9 |
| 2017 | 1 | 12 |
| 2017 | 3 | 12 |
| 2017 | 5 | 12 |
| 2018 | 1 | 17 |
| 2018 | 3 | 17 |
| 2018 | 5 | 17 |
| 2019 | 1 | 14 |
| 2019 | 3 | 14 |
| 2019 | 5 | 14 |
| 2020 | 1 | 15 |
| 2020 | 3 | 15 |
| 2021 | 1 | 15 |
| 2021 | 3 | 15 |
| 2022 | 1 | 19 |
| 2023 | 1 | 26 |

## Input Integrity

- `return_analysis_panel_v1.csv` before: `0c33513e0be39571bc693b5f4f01db97f6fb1d2fcb0441f128b1d9440f382a83`
- `return_analysis_panel_v1.csv` after: `0c33513e0be39571bc693b5f4f01db97f6fb1d2fcb0441f128b1d9440f382a83`
- `return_analysis_panel_v1.csv` unchanged: yes
