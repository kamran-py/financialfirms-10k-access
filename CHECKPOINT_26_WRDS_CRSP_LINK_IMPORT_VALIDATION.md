# CHECKPOINT 26: WRDS CRSP Link Import Validation

## Completed

- Imported WRDS CRSP/Compustat link output.
- Reconciled raw WRDS rows against the original 5,954 filing events.
- Resolved one CRSP PERMNO per event only when exactly one active ordinary common-share PERMNO survived the pre-specified rule.
- Flagged unresolved, non-common-share, no-PERMNO, and ambiguous link cases.
- Created a linked return-window request scaffold for the next WRDS daily-return pull.
- Validation decision: `passed_with_crsp_source_coverage_limit`.
- Did not fetch prices, compute returns, load benchmarks, make SEC requests, or make empirical claims.

## Files Created

- `scripts/import_validate_wrds_crsp_links_v1.py`
- `data/linking/wrds_crsp_link_resolved_v1.csv`
- `data/returns/wrds_crsp_return_windows_linked_request_v1.csv`
- `quality_reports/wrds_crsp_link_import_validation_v1_report.md`
- `CHECKPOINT_26_WRDS_CRSP_LINK_IMPORT_VALIDATION.md`

## Counts

- Original filing events: 5,954
- Raw WRDS output rows: 5,089
- Resolved common-share PERMNO events: 4,259
- Multiple-share-class ambiguous events: 0
- No WRDS link row events: 251
- Non-common-share events: 585
- No-PERMNO events: 238
- Ready mature return-window rows: 8,291
- Ready treated 1-year windows: 138
- Ready treated 3-year windows: 93
- Ready treated 5-year windows: 63

## Next

Use `data/returns/wrds_crsp_return_windows_linked_request_v1.csv` to request CRSP daily returns only for rows with `post_link_return_window_status == ready_for_wrds_daily_return_request`. Validate raw return coverage before computing any 1-, 3-, or 5-year outcomes.
