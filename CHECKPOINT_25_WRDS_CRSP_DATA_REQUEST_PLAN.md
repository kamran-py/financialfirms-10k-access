# CHECKPOINT 25: WRDS CRSP Data Request Plan

## Completed

- Documented WRDS/CRSP as the primary market/security data source.
- Created WRDS link input file.
- Created mature return-window request file.
- Created WRDS SQL templates for linking, daily returns, and market benchmark pulls.
- Did not connect to WRDS, fetch prices, compute returns, load benchmarks, make SEC requests, or make empirical claims.

## Files Created

- `methodology/market_data_source_plan.md`
- `sql/wrds_crsp_linking_query_v1.sql`
- `sql/wrds_crsp_daily_returns_query_v1.sql`
- `sql/wrds_crsp_market_benchmark_query_v1.sql`
- `scripts/prepare_wrds_crsp_inputs_v1.py`
- `data/linking/wrds_crsp_link_input_v1.csv`
- `data/returns/wrds_crsp_return_windows_request_v1.csv`
- `quality_reports/wrds_crsp_data_request_plan_v1_report.md`
- `CHECKPOINT_25_WRDS_CRSP_DATA_REQUEST_PLAN.md`

## Counts

- Filing events for WRDS linking: 5,954
- Mature return-window requests: 13,945
- Treated mature 1-year windows: 180
- Treated mature 3-year windows: 139
- Treated mature 5-year windows: 94

## Next

Run the WRDS linking query using `data/linking/wrds_crsp_link_input_v1.csv`, export the link output, and import/validate it before pulling daily returns.
