# Baseline Finalization Diagnostics V1 Report

## Guardrails

- This checkpoint adds attrition, wild-cluster-bootstrap, and equivalence diagnostics.
- It does not change the baseline economic specification.
- No causal claims are made.
- Equivalence rows are diagnostics unless the threshold is explicitly approved as economically meaningful.

## Treated Attrition Status By Horizon

| Horizon | Treatment | Attrition status | Event-window rows | Issuer clusters |
| --- | --- | --- | --- | --- |
| 1 | 1 | analysis_ready | 138 | 44 |
| 1 | 1 | calendar_right_censored_not_mature | 2 | 2 |
| 1 | 1 | post_link_crsp_return_window_exceeds_available_daily_coverage | 23 | 23 |
| 1 | 1 | security_link_crsp_source_coverage_unavailable_after_2024_12_31 | 16 | 16 |
| 1 | 1 | security_link_non_common_share_code | 3 | 1 |
| 3 | 1 | analysis_ready | 93 | 24 |
| 3 | 1 | calendar_right_censored_not_mature | 43 | 26 |
| 3 | 1 | post_link_crsp_return_window_exceeds_available_daily_coverage | 43 | 29 |
| 3 | 1 | security_link_non_common_share_code | 3 | 1 |
| 5 | 1 | analysis_ready | 63 | 19 |
| 5 | 1 | calendar_right_censored_not_mature | 88 | 41 |
| 5 | 1 | post_link_crsp_return_window_exceeds_available_daily_coverage | 28 | 17 |
| 5 | 1 | security_link_non_common_share_code | 3 | 1 |

## Treated Horizon-Transition Attrition

| Transition | Treatment | Target-horizon status | Event rows | Issuer clusters |
| --- | --- | --- | --- | --- |
| 1->3 | 1 | analysis_ready | 93 | 24 |
| 1->3 | 1 | calendar_right_censored_not_mature | 2 | 2 |
| 1->3 | 1 | post_link_crsp_return_window_exceeds_available_daily_coverage | 43 | 29 |
| 1->5 | 1 | analysis_ready | 63 | 19 |
| 1->5 | 1 | calendar_right_censored_not_mature | 47 | 32 |
| 1->5 | 1 | post_link_crsp_return_window_exceeds_available_daily_coverage | 28 | 17 |
| 3->5 | 1 | analysis_ready | 63 | 19 |
| 3->5 | 1 | calendar_right_censored_not_mature | 2 | 2 |
| 3->5 | 1 | post_link_crsp_return_window_exceeds_available_daily_coverage | 28 | 17 |

## Wild Cluster Bootstrap

| Horizon | Estimate | CR1 SE | CR1 t | Bootstrap p | Bootstrap 95% CI | Clusters |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.0093684377 | 0.0348082971 | 0.2691438108 | 0.7780000000 | [-0.0636936640, 0.0791195454] | 516 |
| 3 | 0.0404468895 | 0.1192755012 | 0.3391047544 | 0.7650000000 | [-0.1979461271, 0.2850455216] | 450 |
| 5 | 0.1911030375 | 0.3734258454 | 0.5117563229 | 0.8140000000 | [-0.4379887210, 0.8591617856] | 400 |

## Equivalence Diagnostics

| Horizon | Threshold | Delta | 90% CI | Passes interval rule |
| --- | --- | --- | --- | --- |
| 1 | absolute_10pp | 0.1000000000 | [-0.0478861160, 0.0666229914] | yes |
| 1 | absolute_15pp | 0.1500000000 | [-0.0478861160, 0.0666229914] | yes |
| 1 | absolute_25pp | 0.2500000000 | [-0.0478861160, 0.0666229914] | yes |
| 3 | absolute_10pp | 0.1000000000 | [-0.1557438513, 0.2366376303] | no |
| 3 | absolute_15pp | 0.1500000000 | [-0.1557438513, 0.2366376303] | no |
| 3 | absolute_25pp | 0.2500000000 | [-0.1557438513, 0.2366376303] | yes |
| 5 | absolute_10pp | 0.1000000000 | [-0.4231278187, 0.8053338937] | no |
| 5 | absolute_15pp | 0.1500000000 | [-0.4231278187, 0.8053338937] | no |
| 5 | absolute_25pp | 0.2500000000 | [-0.4231278187, 0.8053338937] | no |

## Interpretation Boundary

Differential attrition is now summarized from the full scaffold rather than inferred from the final model sample. Current files distinguish calendar right-censoring, CRSP/security-link limitations, CRSP daily-coverage limits, and return-computation failures, but they do not yet classify acquisition versus bankruptcy versus other delisting causes. A separate CRSP delist-code or corporate-action checkpoint would be needed before making exit-mode claims.

## Outputs

- `data/analysis/baseline_differential_attrition_v1.csv`
- `data/analysis/baseline_horizon_transition_attrition_v1.csv`
- `data/analysis/baseline_wild_cluster_bootstrap_v1.csv`
- `data/analysis/baseline_equivalence_diagnostics_v1.csv`

## Input Integrity

- `baseline_year_fe_estimates_v1.csv` unchanged: yes
- `regression_modeling_dataset_v1.csv` unchanged: yes
- `return_analysis_panel_v1.csv` unchanged: yes
- `return_window_scaffold_v1.csv` unchanged: yes
- `wrds_crsp_link_resolved_v1.csv` unchanged: yes
- `wrds_crsp_return_windows_linked_request_v1.csv` unchanged: yes
