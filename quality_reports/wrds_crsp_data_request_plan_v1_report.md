# WRDS CRSP Data Request Plan V1 Report

## Guardrails

- No WRDS connection was opened.
- No prices were fetched.
- No returns were computed.
- No benchmark data were loaded.
- No SEC requests were made.
- No empirical performance claims were made.

## Source Decision

Primary source: WRDS CRSP with Compustat/CRSP linking. FactSet remains a fallback/cross-check source.

## Files Created

- `methodology/market_data_source_plan.md`
- `sql/wrds_crsp_linking_query_v1.sql`
- `sql/wrds_crsp_daily_returns_query_v1.sql`
- `sql/wrds_crsp_market_benchmark_query_v1.sql`
- `data/linking/wrds_crsp_link_input_v1.csv`
- `data/returns/wrds_crsp_return_windows_request_v1.csv`

## Request Counts

- Filing events for WRDS linking: 5,954
- Mature filing-window rows requesting returns after link resolution: 13,945
- Treated filing events: 182
- Untreated/control filing events: 5,772

## Mature Window Requests By Horizon

| Horizon years | Mature window requests |
| --- | --- |
| 1 | 5901 |
| 3 | 4627 |
| 5 | 3417 |

## Treated Mature Window Requests By Horizon

| Horizon years | Treated mature window requests |
| --- | --- |
| 1 | 180 |
| 3 | 139 |
| 5 | 94 |

## Filing Events By Event Year

| Event year | Filing events |
| --- | --- |
| 2015 | 451 |
| 2016 | 460 |
| 2017 | 472 |
| 2018 | 488 |
| 2019 | 507 |
| 2020 | 526 |
| 2021 | 557 |
| 2022 | 600 |
| 2023 | 616 |
| 2024 | 629 |
| 2025 | 648 |

## Export / Import Contract

- Export WRDS link results to `data/linking/wrds_crsp_link_output_v1.csv`.
- Export WRDS daily security returns to `data/returns/wrds_crsp_daily_returns_raw_v1.csv`.
- Export WRDS market benchmark returns to `data/returns/wrds_crsp_market_benchmark_raw_v1.csv`.
- Do not compute returns until these files are imported, validated, and status counts are reported.

## Input Integrity

- `filing_security_link_scaffold_v1.csv` before: `b65c5f615b99844cee9de2f43fcdf5fbd658efbad577c38d33d11c898e9bfe6a`
- `filing_security_link_scaffold_v1.csv` after: `b65c5f615b99844cee9de2f43fcdf5fbd658efbad577c38d33d11c898e9bfe6a`
- `filing_security_link_scaffold_v1.csv` unchanged: yes
- `market_data_source_plan.md` before: `394d68aab59ca75434d89d1d1d02e2d226e98ffdd0af602270fd79fb25c49c5f`
- `market_data_source_plan.md` after: `394d68aab59ca75434d89d1d1d02e2d226e98ffdd0af602270fd79fb25c49c5f`
- `market_data_source_plan.md` unchanged: yes
- `return_window_scaffold_v1.csv` before: `7fd90e72dfd30fc38c4f781e05a7871a2a1a1eb5ffcc9bddc03c929375f43b7d`
- `return_window_scaffold_v1.csv` after: `7fd90e72dfd30fc38c4f781e05a7871a2a1a1eb5ffcc9bddc03c929375f43b7d`
- `return_window_scaffold_v1.csv` unchanged: yes