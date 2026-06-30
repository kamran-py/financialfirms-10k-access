# WRDS CRSP Raw Return Import Validation V1 Report

## Guardrails

- Raw WRDS daily issuer returns were imported and validated for coverage only.
- Raw CRSP market benchmark rows were imported and validated for coverage only.
- No 1-year, 3-year, or 5-year issuer returns were computed.
- No benchmark-adjusted returns were computed.
- No regressions, tests, or empirical performance claims were made.

## Inputs

- `data/returns/wrds_crsp_return_windows_linked_request_v1.csv`
- `data/returns/wrds_crsp_daily_returns_raw_v1.csv`
- `data/returns/wrds_crsp_market_benchmark_raw_v1.csv`
- `quality_reports/wrds_crsp_return_pull_manifest_v1.txt`

## Output

- `data/returns/wrds_crsp_return_window_raw_coverage_v1.csv`

## Manifest Reconciliation

| Metric | Manifest count | Local count | Matches |
| --- | --- | --- | --- |
| Ready windows | 8291 | 8291 | True |
| Unique PERMNOs | 520 | 520 | True |
| Daily return rows | 1105019 | 1105019 | True |
| Benchmark rows | 2493 | 2493 | True |

## Raw File Counts

- Ready return-window rows checked: 8,291
- Daily issuer rows: 1,105,019
- Daily issuer duplicate PERMNO-date rows: 0
- Unique PERMNOs in request: 520
- Unique PERMNOs in raw daily file: 520
- Requested PERMNOs missing from raw daily file: 0
- Delisting-return rows reported in manifest: 520
- Raw daily rows with nonblank `dlret`: 9
- Benchmark rows: 2,493
- Benchmark duplicate date rows: 0

## Raw Coverage Status Counts

| Coverage status | Window rows |
| --- | --- |
| raw_coverage_incomplete | 27 |
| raw_coverage_ready_for_return_computation | 8264 |

## Raw Coverage Reason Counts

| Coverage reason | Window rows |
| --- | --- |
| issuer_and_benchmark_raw_rows_available | 8264 |
| issuer_end_trading_date_unavailable_within_buffer | 27 |

## Coverage By Horizon

| Horizon years | Coverage status | Window rows |
| --- | --- | --- |
| 1 | raw_coverage_incomplete | 7 |
| 1 | raw_coverage_ready_for_return_computation | 3725 |
| 3 | raw_coverage_incomplete | 10 |
| 3 | raw_coverage_ready_for_return_computation | 2708 |
| 5 | raw_coverage_incomplete | 10 |
| 5 | raw_coverage_ready_for_return_computation | 1831 |

## Treated Coverage By Horizon

| Horizon years | Coverage status | Treated window rows |
| --- | --- | --- |
| 1 | raw_coverage_ready_for_return_computation | 138 |
| 3 | raw_coverage_ready_for_return_computation | 93 |
| 5 | raw_coverage_ready_for_return_computation | 63 |

## Benchmark Missingness

| Benchmark field | Missing rows |
| --- | --- |

## Input Integrity

- `wrds_crsp_daily_returns_raw_v1.csv` before: `651959cca9c8f22f489f46a8af01c2a2fd2012a296bf81f22e28070946e35f20`
- `wrds_crsp_daily_returns_raw_v1.csv` after: `651959cca9c8f22f489f46a8af01c2a2fd2012a296bf81f22e28070946e35f20`
- `wrds_crsp_daily_returns_raw_v1.csv` unchanged: yes
- `wrds_crsp_market_benchmark_raw_v1.csv` before: `60d00aea3224d9b3818a328caf3fc4974c78725efef7236649492d33e4382b92`
- `wrds_crsp_market_benchmark_raw_v1.csv` after: `60d00aea3224d9b3818a328caf3fc4974c78725efef7236649492d33e4382b92`
- `wrds_crsp_market_benchmark_raw_v1.csv` unchanged: yes
- `wrds_crsp_return_pull_manifest_v1.txt` before: `33a427a6fc7dbeaa3e30f1c4c4f646b6c530b33c4685b0c4886c48b615b28808`
- `wrds_crsp_return_pull_manifest_v1.txt` after: `33a427a6fc7dbeaa3e30f1c4c4f646b6c530b33c4685b0c4886c48b615b28808`
- `wrds_crsp_return_pull_manifest_v1.txt` unchanged: yes
- `wrds_crsp_return_windows_linked_request_v1.csv` before: `89e09381aa13c051aa32b884de7800b0a60d1dc1ebb2e4dc3cadff3a0322ee09`
- `wrds_crsp_return_windows_linked_request_v1.csv` after: `89e09381aa13c051aa32b884de7800b0a60d1dc1ebb2e4dc3cadff3a0322ee09`
- `wrds_crsp_return_windows_linked_request_v1.csv` unchanged: yes