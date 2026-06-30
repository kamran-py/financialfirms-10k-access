# CHECKPOINT 04: Section Extraction

Generated at: 2026-06-27T22:19:59.883760+00:00

## Completed

- Implemented local-only section extraction for downloaded 10-K filings.
- Extracted sections: Item 1 Business, Item 1A Risk Factors, Item 7 MD&A.
- Wrote structured section rows with required metadata and full section text.
- Wrote quality report with success by section/year, shortest sections, and missing section lists.

## Explicit Non-Actions

- No phrase matching.
- No classification.
- No price fetching.
- No research claims.
- No SEC requests.
- No raw filing overwrites.

## Inputs

- Filing index rows: 9060
- Found 10-K filing rows: 5954

## Outputs

- `data\extracted\filing_sections.csv`
- `quality_reports\section_extraction_report.md`
- `CHECKPOINT_04_EXTRACTION.md`

## OK Counts By Section

- Item 1 Business: 5643/5954
- Item 1A Risk Factors: 5391/5954
- Item 7 MD&A: 5416/5954

## Status Counts

- LIKELY_TOC_ONLY: 321
- OK: 16450
- SECTION_NOT_FOUND: 536
- SOURCE_FILE_UNAVAILABLE: 3
- SUSPICIOUSLY_SHORT: 552

## Known Limitation

The extractor uses standard-library HTML parsing and regex item boundaries. Shortest, missing, suspiciously short, suspiciously long, and table-of-contents-only cases require audit before phrase matching.

## Next Recommended Prompt

Audit `quality_reports/section_extraction_report.md`, especially missing sections and the 25 shortest sections for each type. If acceptable, proceed to implement raw phrase matching on `data/extracted/filing_sections.csv`; otherwise refine extraction rules first.
