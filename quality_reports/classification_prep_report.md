# Classification Preparation Report

Generated at: 2026-06-29T05:01:02.980419+00:00

## Scope

- Prepared a manual review sample from raw phrase hits.
- Did not classify hits, fetch prices, make SEC requests, run return analysis, or make empirical claims.
- Raw phrase hits remain unchanged in `data/extracted/phrase_hits.csv`.
- Script version: `prepare_review_sample_v1`.

## Warning

No return outcomes have been loaded yet. Raw phrase hits and review samples are text-validation artifacts only.

## Raw Hits Available For Review

- Raw phrase hits available: 9400
- Proposed initial review sample size: 600
- Requested sample size parameter: 600
- Deterministic sample seed: 20260629
- Firm-level soft cap before fallback fill: 12
- Company-name source: config\firm_universe.csv

## Recommended Initial Sample Size And Tradeoffs

The recommended initial sample is 600 raw hits. This is large enough to cover all phrase categories, common phrases, years, sections, and a broad firm set, while remaining practical for manual review. A smaller sample near 300 would be faster but would provide weak coverage of rare phrases and section/year combinations. A larger sample near 1,000 would improve phrase-level precision but should usually wait until reviewers calibrate on the first batch.

## Stratification Method

- Assigned stable `hit_id` values from raw phrase-hit row order without modifying the raw file.
- Selected deterministic coverage passes by phrase, category, filing year, section, and firm.
- Applied a firm-level cap during the main selection passes to reduce concentration in frequent issuers.
- Filled remaining slots deterministically from the remaining raw hits.

## Proposed Review Sample Counts By Category

| Category | Sample count |
| --- | --- |
| retail access to investing | 112 |
| homeownership access | 96 |
| underserved / underbanked / unbanked | 85 |
| expanded access to credit | 65 |
| lower barriers / level playing field | 53 |
| broader market participation | 44 |
| democratized access | 43 |
| institutional-grade access for individuals | 39 |
| financial inclusion | 37 |
| affordable financial products | 26 |

## Proposed Review Sample Counts By Year

| Filing year | Sample count |
| --- | --- |
| 2015 | 20 |
| 2016 | 36 |
| 2017 | 43 |
| 2018 | 41 |
| 2019 | 46 |
| 2020 | 50 |
| 2021 | 51 |
| 2022 | 66 |
| 2023 | 79 |
| 2024 | 84 |
| 2025 | 84 |

## Proposed Review Sample Counts By Section

| Section | Sample count |
| --- | --- |
| Item 1 Business | 332 |
| Item 1A Risk Factors | 139 |
| Item 7 MD&A | 129 |

## Likely High-False-Positive Categories

| Category | Raw hits | High-risk phrases | Medium-risk phrases | Low-risk phrases |
| --- | --- | --- | --- | --- |
| institutional-grade access for individuals | 165 | 6 | 0 | 2 |
| broader market participation | 707 | 3 | 6 | 0 |
| retail access to investing | 3119 | 3 | 4 | 0 |
| homeownership access | 2346 | 1 | 6 | 2 |
| underserved / underbanked / unbanked | 1595 | 1 | 5 | 6 |

## Top Sampled Phrases

| Phrase | Sample count |
| --- | --- |
| affordable housing | 82 |
| retail investors | 37 |
| underserved | 34 |
| financial inclusion | 32 |
| fractional share | 32 |
| access to credit | 30 |
| individual investors | 28 |
| market access | 27 |
| affordable financial services | 16 |
| institutional quality | 15 |
| institutional-grade | 13 |
| expand access to credit | 11 |
| access to markets | 10 |
| credit access | 10 |
| underserved consumers | 10 |
| access to investment | 9 |
| democratize finance | 9 |
| level playing field | 9 |
| democratize access | 8 |
| democratizing access | 8 |
| democratizing financial services | 8 |
| lower barriers | 8 |
| removing barriers | 8 |
| underbanked | 8 |
| affordable loans | 7 |

## Top Sampled Firms

| Firm ID | Sample count |
| --- | --- |
| CIK0001041514 | 12 |
| CIK0001404912 | 12 |
| CIK0001409970 | 12 |
| CIK0001538716 | 12 |
| CIK0001633917 | 12 |
| CIK0001783879 | 12 |
| CIK0001128361 | 11 |
| CIK0001141391 | 11 |
| CIK0001820302 | 10 |
| CIK0001289419 | 9 |
| CIK0001497770 | 9 |
| CIK0001529864 | 9 |
| CIK0000907471 | 8 |
| CIK0001403161 | 8 |
| CIK0001818502 | 8 |
| CIK0000880631 | 6 |
| CIK0001069157 | 6 |
| CIK0001393818 | 6 |
| CIK0001775734 | 6 |
| CIK0000005272 | 5 |
| CIK0001278021 | 5 |
| CIK0001281761 | 5 |
| CIK0001381197 | 5 |
| CIK0001408198 | 5 |
| CIK0001467760 | 5 |

## Recommended Next Stage

Review `data/review/phrase_hit_review_sample.csv` under `config/classification_guidelines.md`. After reviewer calibration, create a locked classified-hit table that preserves raw hit IDs, human labels, confidence, reviewer metadata, and audit notes. Only after that should return data be loaded and merged under the pre-analysis plan.

## Output Files

- `data\review\phrase_hit_review_sample.csv`
- `data\review\phrase_hit_review_template.csv`
- `quality_reports\classification_prep_report.md`
