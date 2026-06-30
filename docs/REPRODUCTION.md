# Reproduction Notes

This repository is designed to document the workflow and publish code, checkpoints, and aggregate results. It does not publish raw or licensed data.

## Requirements

- Python 3.
- SEC EDGAR access with a compliant user-agent.
- WRDS/CRSP access for security links and return data.

## High-Level Pipeline

1. Build firm universe and filing index.
2. Download 10-K filings from SEC EDGAR.
3. Extract Item 1, Item 1A, and Item 7.
4. Run phrase matching.
5. Classify and audit candidate access-oriented disclosure language.
6. Construct validated conservative filing-level treatment.
7. Prepare WRDS/CRSP linking and return-window request files.
8. Import WRDS/CRSP links and daily return data.
9. Compute return windows and benchmark-adjusted outcomes.
10. Build analysis panel.
11. Run baseline year fixed-effect association models.
12. Add power, attrition, bootstrap, and equivalence diagnostics.

## Data Not Included

The following are intentionally excluded from Git:

- Raw SEC filing files.
- Extracted section-level text.
- Raw phrase-hit tables.
- Manual review samples.
- WRDS/CRSP raw link and return data.
- Row-level return-analysis panels.

Aggregate tables under `data/analysis/` are included only where they do not expose licensed row-level data.

## Current Result Reproduction

The published aggregate outputs can be checked against:

- `quality_reports/baseline_year_fe_estimation_v1_report.md`
- `quality_reports/baseline_inference_diagnostics_v1_report.md`
- `quality_reports/baseline_finalization_diagnostics_v1_report.md`
- `methodology/baseline_table_appendix_draft_v1.md`

Full reproduction from raw data requires private/local regeneration of excluded files.
