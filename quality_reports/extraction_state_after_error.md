# Extraction State After Error

Generated at: 2026-06-29

## Scope

This recovery check inspected only:

- `data/extracted/filing_sections.csv`
- `quality_reports/section_extraction_report.md`
- `CHECKPOINT_04_EXTRACTION.md`
- `scripts/extract_sections.py`
- `data/metadata/filing_index.csv`
- `data/metadata/download_attempts.csv`

No full extraction rerun, phrase matching, price fetching, SEC requests, or research checks were performed.

## Recovery Findings

1. `data/extracted/filing_sections.csv` exists: yes.
2. Row count of `filing_sections.csv`: 17,862 section rows.
3. Expected filing-section rows:
   - Baseline from downloaded-success filings: 5,953 downloaded filings x 3 sections = 17,859 rows.
   - Metadata/extraction scope shows 5,954 10-K filing rows in `filing_index.csv`, so scoped expected output is 5,954 x 3 = 17,862 rows.
   - `download_attempts.csv` shows 5,953 `DOWNLOADED` rows and 1 `HTTP_FAILURE` row. The extraction output includes 3 `SOURCE_FILE_UNAVAILABLE` rows for the unavailable filing, which reconciles the 17,862 total.
4. Counts by `section_name`:
   - Item 1 Business: 5,954
   - Item 1A Risk Factors: 5,954
   - Item 7 MD&A: 5,954
5. Counts by `extraction_status`:
   - OK: 16,450
   - SUSPICIOUSLY_SHORT: 552
   - SECTION_NOT_FOUND: 536
   - LIKELY_TOC_ONLY: 321
   - SOURCE_FILE_UNAVAILABLE: 3
6. Counts by `filing_year`:
   - 2015: 1,353
   - 2016: 1,380
   - 2017: 1,416
   - 2018: 1,464
   - 2019: 1,521
   - 2020: 1,578
   - 2021: 1,671
   - 2022: 1,800
   - 2023: 1,848
   - 2024: 1,887
   - 2025: 1,944
7. Unique `accession_number` count in `filing_sections.csv`: 5,954.
8. `CHECKPOINT_04_EXTRACTION.md` exists: yes.
9. `quality_reports/section_extraction_report.md` exists: yes.
10. Extraction state: complete for the 5,954-row metadata extraction scope, not empty, not partial by row count, and not apparently corrupted. It is not complete in the sense of every section successfully extracted, because 1,412 rows have non-OK extraction statuses.
11. Safest next command:

```powershell
Get-Content -LiteralPath 'quality_reports/extraction_state_after_error.md'
```

## Integrity Notes

- Parsed `filing_sections.csv` successfully with no malformed rows detected.
- `section_extraction_report.md` reports 17,862 section output rows and the same 5,954 found 10-K filing-row scope.
- `CHECKPOINT_04_EXTRACTION.md` exists and records the extraction checkpoint generated on 2026-06-27.
