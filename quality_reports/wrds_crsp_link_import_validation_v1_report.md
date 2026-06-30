# WRDS CRSP Link Import Validation V1 Report

## Guardrails

- Raw WRDS link output was preserved unchanged.
- No prices were fetched.
- No returns were computed.
- No benchmark data were loaded.
- No SEC requests were made.
- No empirical performance claims were made.

## Inputs

- `data/linking/wrds_crsp_link_input_v1.csv`
- `data/linking/wrds_crsp_link_output_v1.csv`
- `data/returns/wrds_crsp_return_windows_request_v1.csv`
- `methodology/market_data_source_plan.md`

## Outputs

- `data/linking/wrds_crsp_link_resolved_v1.csv`
- `data/returns/wrds_crsp_return_windows_linked_request_v1.csv`

## Resolution Rule

A filing event is marked `resolved_common_share_permno` only when the WRDS CIK-GVKEY-CCM link and CRSP stock-name filters leave exactly one active ordinary common-share PERMNO at the filing date. Ordinary common shares require `shrcd in (10, 11)`. If multiple eligible PERMNOs survive, the filing is marked `multiple_share_class_ambiguous` rather than force-resolved.

## WRDS/CRSP Coverage Limit

WRDS diagnostics supplied from the project notebook on 2026-06-29 show `crsp.stocknames` max `nameenddt` = `2024-12-31` and `crsp.dsf` max `date` = `2024-12-31`. Return-window rows whose target calendar end date exceeds this coverage date are not marked ready for daily-return requests.

## Reconciliation Counts

- Original filing events: 5,954
- Raw WRDS output rows: 5,089
- Raw WRDS unique event IDs: 5,089
- Resolved output rows: 5,954
- Raw rows with unknown event IDs: 0
- Validation decision: `passed_with_crsp_source_coverage_limit`
- Validation warning: WRDS diagnostics supplied on 2026-06-29 show `crsp.stocknames` and `crsp.dsf` both end on 2024-12-31. Filing years after that date are source-coverage limited, not silently dropped.

## Raw WRDS Link Status Counts

| Raw link status | Rows |
| --- | --- |
| candidate_link | 4259 |
| no_permno_link | 238 |
| non_common_share_code | 585 |
| permno_without_active_name_at_event_date | 7 |

## Final Security Link Status Counts

| Security link status | Filing events |
| --- | --- |
| crsp_source_coverage_unavailable_after_2024_12_31 | 614 |
| no_permno_link | 238 |
| no_wrds_link_row | 251 |
| non_common_share_code | 585 |
| permno_without_active_name_at_event_date | 7 |
| resolved_common_share_permno | 4259 |

## Link Confidence Counts

| Link confidence | Filing events |
| --- | --- |
| failed | 1695 |
| high | 4259 |

## Treatment Balance By Link Status

| Security link status | Treated filings | Untreated/control filings |
| --- | --- | --- |
| crsp_source_coverage_unavailable_after_2024_12_31 | 18 | 596 |
| no_permno_link | 0 | 238 |
| no_wrds_link_row | 0 | 251 |
| non_common_share_code | 3 | 582 |
| permno_without_active_name_at_event_date | 0 | 7 |
| resolved_common_share_permno | 161 | 4098 |

## Ready Mature Return Windows By Horizon

| Horizon years | Ready windows |
| --- | --- |
| 1 | 3732 |
| 3 | 2718 |
| 5 | 1841 |

## Ready Treated Mature Return Windows By Horizon

| Horizon years | Ready treated windows |
| --- | --- |
| 1 | 138 |
| 3 | 93 |
| 5 | 63 |

## Link Status By Filing Year

| Filing year | Security link status | Filing events |
| --- | --- | --- |
| 2015 | no_permno_link | 18 |
| 2015 | no_wrds_link_row | 39 |
| 2015 | non_common_share_code | 51 |
| 2015 | resolved_common_share_permno | 343 |
| 2016 | no_permno_link | 18 |
| 2016 | no_wrds_link_row | 31 |
| 2016 | non_common_share_code | 52 |
| 2016 | resolved_common_share_permno | 359 |
| 2017 | no_permno_link | 19 |
| 2017 | no_wrds_link_row | 33 |
| 2017 | non_common_share_code | 56 |
| 2017 | resolved_common_share_permno | 364 |
| 2018 | no_permno_link | 21 |
| 2018 | no_wrds_link_row | 29 |
| 2018 | non_common_share_code | 62 |
| 2018 | resolved_common_share_permno | 376 |
| 2019 | no_permno_link | 21 |
| 2019 | no_wrds_link_row | 28 |
| 2019 | non_common_share_code | 59 |
| 2019 | resolved_common_share_permno | 399 |
| 2020 | no_permno_link | 21 |
| 2020 | no_wrds_link_row | 21 |
| 2020 | non_common_share_code | 57 |
| 2020 | resolved_common_share_permno | 427 |
| 2021 | no_permno_link | 21 |
| 2021 | no_wrds_link_row | 29 |
| 2021 | non_common_share_code | 57 |
| 2021 | resolved_common_share_permno | 450 |
| 2022 | no_permno_link | 22 |
| 2022 | no_wrds_link_row | 16 |
| 2022 | non_common_share_code | 63 |
| 2022 | resolved_common_share_permno | 499 |
| 2023 | no_permno_link | 24 |
| 2023 | no_wrds_link_row | 14 |
| 2023 | non_common_share_code | 63 |
| 2023 | resolved_common_share_permno | 515 |
| 2024 | no_permno_link | 26 |
| 2024 | no_wrds_link_row | 11 |
| 2024 | non_common_share_code | 65 |
| 2024 | resolved_common_share_permno | 527 |
| 2025 | crsp_source_coverage_unavailable_after_2024_12_31 | 614 |
| 2025 | no_permno_link | 27 |
| 2025 | permno_without_active_name_at_event_date | 7 |

## Input Integrity

- `market_data_source_plan.md` before: `394d68aab59ca75434d89d1d1d02e2d226e98ffdd0af602270fd79fb25c49c5f`
- `market_data_source_plan.md` after: `394d68aab59ca75434d89d1d1d02e2d226e98ffdd0af602270fd79fb25c49c5f`
- `market_data_source_plan.md` unchanged: yes
- `wrds_crsp_link_input_v1.csv` before: `34c214e2f0240c7c89085aa9a0394cfc982745552e685e21b8fd0f554bd2ab5b`
- `wrds_crsp_link_input_v1.csv` after: `34c214e2f0240c7c89085aa9a0394cfc982745552e685e21b8fd0f554bd2ab5b`
- `wrds_crsp_link_input_v1.csv` unchanged: yes
- `wrds_crsp_link_output_v1.csv` before: `0c8abcfd2863691c0494deaa506a122edef74bddeeb8a04b084696d56b14666b`
- `wrds_crsp_link_output_v1.csv` after: `0c8abcfd2863691c0494deaa506a122edef74bddeeb8a04b084696d56b14666b`
- `wrds_crsp_link_output_v1.csv` unchanged: yes
- `wrds_crsp_return_windows_request_v1.csv` before: `d5fc7481be07ca546dc128e63d879947bacb8521e8b3ea7ef1c64e8a744323a5`
- `wrds_crsp_return_windows_request_v1.csv` after: `d5fc7481be07ca546dc128e63d879947bacb8521e8b3ea7ef1c64e8a744323a5`
- `wrds_crsp_return_windows_request_v1.csv` unchanged: yes