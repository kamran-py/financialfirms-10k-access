# Return Outlier and Winsorization Policy V1

This policy is defined before regression or event-study estimation.

## Raw Outcomes

- Raw computed returns are preserved unchanged in `data/analysis/return_analysis_panel_v1.csv`.
- The primary raw outcome for market-adjusted performance is `excess_return_vs_vwretd`.
- `issuer_raw_return_compounded` is retained as an unadjusted descriptive outcome.

## Winsorized Outcomes

- Winsorization is applied only to analysis-ready computed rows.
- Thresholds are calculated separately within each return horizon: 1-year, 3-year, and 5-year.
- Thresholds use the pooled treated and control sample within each horizon, not treatment-specific thresholds.
- The default analysis-ready winsorized variables cap each outcome at the 1st and 99th percentiles within horizon.
- Winsorized variables are suffixed `_winsor_p01_p99_by_horizon`.
- Raw variables remain available for sensitivity checks and are not overwritten.

## Guardrails

- This policy does not imply that any return is erroneous.
- Outlier-tail files are diagnostic aids, not exclusion rules.
- Any later alternative threshold must be documented as a robustness specification, not selected after viewing results.
