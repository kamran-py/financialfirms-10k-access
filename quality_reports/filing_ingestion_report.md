# Filing Ingestion Report

Generated at: 2026-06-27T20:37:27.849876+00:00

## Scope

- Filing form: exact `10-K`.
- Filing years: 2015-2025 based on SEC filing date.
- SEC endpoints: `data.sec.gov/submissions` and `www.sec.gov/Archives`.
- SEC fair-access limit: scripts reject rates above 10 requests/second.

## Filing Index Counts

- Firms represented in index: 823
- Firm-year rows with no 10-K found or metadata issue: 3106
- 10-K filing rows found: 5954

## Found 10-K Filings By Filing Year

- 2015: 451
- 2016: 460
- 2017: 472
- 2018: 488
- 2019: 507
- 2020: 526
- 2021: 557
- 2022: 600
- 2023: 616
- 2024: 629
- 2025: 648

## Missing Or Metadata Reasons

- NO_FILING_FOUND: 3106

## Metadata Status Counts

- DOWNLOADED: 691
- SKIPPED_DUPLICATE: 8369

## Download Attempt Status Counts

- DOWNLOADED: 5953
- HTTP_FAILURE: 1

## Download Error Reasons

- URL_ERROR: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond: 1

## Required Distinctions

- No filing found: 3106
- CIK missing: 0
- HTTP failure: 1
- Malformed metadata: 0
- Skipped duplicate: 0

## Output Files

- `data\metadata\filing_index.csv`
- `data\metadata\download_attempts.csv`

Every firm-year appears either as a discovered filing row or as an explicit missing row with a reason.
