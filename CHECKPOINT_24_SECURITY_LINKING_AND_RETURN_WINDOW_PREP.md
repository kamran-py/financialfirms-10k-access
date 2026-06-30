# CHECKPOINT 24: Security Linking And Return Window Prep

Generated at: 2026-06-29

## Completed

- Created firm-level security link candidates.
- Created filing-level security link scaffold.
- Created filing-window scaffold for 1-year, 3-year, and 5-year horizons.
- Preserved treatment status and event dates from the validated treatment dataset.
- Marked all security links as pending price identifier assignment.
- Marked right-censored windows separately from mature-but-pending windows.
- Did not fetch prices, compute returns, load benchmarks, make SEC requests, or make empirical claims.

## Files Created

- `scripts/prepare_security_linking_and_return_windows_v1.py`
- `data/linking/security_link_candidates_v1.csv`
- `data/linking/filing_security_link_scaffold_v1.csv`
- `data/returns/return_window_scaffold_v1.csv`
- `quality_reports/security_linking_and_return_window_prep_v1_report.md`
- `CHECKPOINT_24_SECURITY_LINKING_AND_RETURN_WINDOW_PREP.md`

## Counts

- Unique firm link candidates: 655
- Filing link rows: 5,954
- Return-window scaffold rows: 17,862
- Treated filing rows: 182
- Untreated/control filing rows: 5,772

## Guardrails

- No prices fetched.
- No returns computed.
- No benchmarks loaded.
- No SEC requests made.
- No empirical performance claims made.

## Next

Choose and document the market/security data source before assigning final price identifiers or computing returns.
