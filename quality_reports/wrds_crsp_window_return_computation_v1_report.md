# WRDS CRSP Window Return Computation V1 Report

## Guardrails

- Returns were computed only for rows marked `raw_coverage_ready_for_return_computation`.
- Rows without raw coverage were retained with explicit non-computed statuses.
- Issuer returns use compounded `ret_with_delisting` from the WRDS raw daily file.
- Primary benchmark-adjusted return is issuer compounded return minus compounded CRSP `vwretd`.
- No regressions, hypothesis tests, causal claims, or performance conclusions were made.

## Inputs

- `data/returns/wrds_crsp_return_window_raw_coverage_v1.csv`
- `data/returns/wrds_crsp_daily_returns_raw_v1.csv`
- `data/returns/wrds_crsp_market_benchmark_raw_v1.csv`

## Output

- `data/returns/wrds_crsp_window_returns_v1.csv`

## Source File Counts

- Coverage input rows: 8,291
- Issuer daily rows indexed: 1,105,019
- Issuer unique PERMNOs indexed: 520
- Issuer duplicate PERMNO-date rows skipped: 0
- Issuer rows with blank/non-numeric `ret_with_delisting`: 3,162
- Benchmark rows indexed: 2,493
- Benchmark duplicate date rows skipped: 0

## Return Computation Status Counts

| Return computation status | Window rows |
| --- | --- |
| computed | 8,238 |
| not_computed_missing_issuer_return_inside_window | 26 |
| not_computed_raw_coverage_incomplete | 27 |

## Return Computation Reason Counts

| Return computation reason | Window rows |
| --- | --- |
| at_least_one_issuer_trading_day_has_blank_or_non_numeric_return | 26 |
| issuer_and_benchmark_returns_compounded_successfully | 8,238 |
| issuer_end_trading_date_unavailable_within_buffer | 27 |

## Return Computation By Horizon

| Horizon years | Return computation status | Window rows |
| --- | --- | --- |
| 1 | computed | 3718 |
| 1 | not_computed_missing_issuer_return_inside_window | 7 |
| 1 | not_computed_raw_coverage_incomplete | 7 |
| 3 | computed | 2698 |
| 3 | not_computed_missing_issuer_return_inside_window | 10 |
| 3 | not_computed_raw_coverage_incomplete | 10 |
| 5 | computed | 1822 |
| 5 | not_computed_missing_issuer_return_inside_window | 9 |
| 5 | not_computed_raw_coverage_incomplete | 10 |

## Treated Return Computation By Horizon

| Horizon years | Return computation status | Treated window rows |
| --- | --- | --- |
| 1 | computed | 138 |
| 3 | computed | 93 |
| 5 | computed | 63 |

## Computed Row Counts

- Computed window rows: 8,238
- Computed treated window rows: 294

## Input Integrity

- `wrds_crsp_return_window_raw_coverage_v1.csv` before: `23280f8db2b19e371bc33a217f146b29932a39b4fa867ea775bff613bc26e4fc`
- `wrds_crsp_return_window_raw_coverage_v1.csv` after: `23280f8db2b19e371bc33a217f146b29932a39b4fa867ea775bff613bc26e4fc`
- `wrds_crsp_return_window_raw_coverage_v1.csv` unchanged: yes
- `wrds_crsp_daily_returns_raw_v1.csv` before: `651959cca9c8f22f489f46a8af01c2a2fd2012a296bf81f22e28070946e35f20`
- `wrds_crsp_daily_returns_raw_v1.csv` after: `651959cca9c8f22f489f46a8af01c2a2fd2012a296bf81f22e28070946e35f20`
- `wrds_crsp_daily_returns_raw_v1.csv` unchanged: yes
- `wrds_crsp_market_benchmark_raw_v1.csv` before: `60d00aea3224d9b3818a328caf3fc4974c78725efef7236649492d33e4382b92`
- `wrds_crsp_market_benchmark_raw_v1.csv` after: `60d00aea3224d9b3818a328caf3fc4974c78725efef7236649492d33e4382b92`
- `wrds_crsp_market_benchmark_raw_v1.csv` unchanged: yes
