# CHECKPOINT 10: Review Sample Classification V2

Generated at: 2026-06-29T01:47:46.0485075-04:00

## Completed

- Created revised classification guidance in `config/classification_guidelines_v3.md`.
- Implemented `scripts/classify_review_sample_v2.py`.
- Reclassified the 600-row review sample while preserving v1 labels for comparison.
- Preserved 120 manual calibration labels exactly.
- Preserved 150 manual audit labels exactly.
- Reclassified only rows without manual calibration or manual audit labels.
- Wrote the v2 classified sample and v1-versus-v2 quality report.

## Explicit Non-Actions

- No prices fetched.
- No returns computed.
- No return analysis run.
- No SEC requests made.
- No empirical performance claims made.
- No classification scaled to all 9,400 raw hits.
- No modification of `data/extracted/phrase_hits.csv`.

## Files Created Or Modified

- Created `config/classification_guidelines_v3.md`
- Created `scripts/classify_review_sample_v2.py`
- Created `data/review/phrase_hit_review_sample_classified_v2.csv`
- Created `quality_reports/review_sample_classification_v2_report.md`
- Created `CHECKPOINT_10_REVIEW_SAMPLE_CLASSIFICATION_V2.md`

## Row Counts

- Total review sample rows: 600
- Manual calibration rows: 120
- Manual audit rows: 150
- Codex-assisted v2 rows: 330
- Rows missing `final_label_v2`, `final_confidence_v2`, or `label_source_v2`: 0
- Manual calibration label mismatches: 0
- Manual audit label mismatches: 0
- Raw `data/extracted/phrase_hits.csv` SHA256 remained `BA511BF32939B78C7D15B6518C7FBA78CEE3E7E6357B49BFEF21F90D18288054`

## V2 Label Distribution

- `true_positive_access_expansion`: 367
- `operational_access_or_platform_language`: 95
- `false_positive`: 61
- `risk_disclosure_only`: 46
- `customer_access_unrelated_to_finance`: 15
- `generic_marketing`: 13
- `ambiguous`: 3

## V1 To V2 Change Summary

- Rows changed from v1 to v2: 134

Largest transitions:

- `operational_access_or_platform_language` -> `true_positive_access_expansion`: 31
- `true_positive_access_expansion` -> `operational_access_or_platform_language`: 30
- `true_positive_access_expansion` -> `false_positive`: 14
- `generic_marketing` -> `true_positive_access_expansion`: 13
- `generic_marketing` -> `operational_access_or_platform_language`: 12
- `generic_marketing` -> `customer_access_unrelated_to_finance`: 7
- `false_positive` -> `true_positive_access_expansion`: 6
- `ambiguous` -> `true_positive_access_expansion`: 5
- `true_positive_access_expansion` -> `risk_disclosure_only`: 4
- `true_positive_access_expansion` -> `generic_marketing`: 3

Categories with the most changed rows:

- `homeownership access`: 36
- `institutional-grade access for individuals`: 19
- `lower barriers / level playing field`: 19
- `democratized access`: 18
- `affordable financial products`: 10
- `expanded access to credit`: 10
- `retail access to investing`: 10

## Remaining Classification Risks

- V2 still uses Codex-assisted labels for 330 rows without direct manual calibration or audit labels.
- Institutional-quality and platform-capability language remains high-risk when excerpts mention real estate/property quality, custodian quality, API quality, platform quality, advisor analytics, or internal infrastructure.
- Market-access phrases remain high-risk unless external beneficiaries are explicit.
- Affordable-housing language remains sensitive to tax-credit, partnership, portfolio, investment-income, commitments-table, and accounting context.
- CRA/regulatory language remains difficult where issuer action and external beneficiary are implied rather than explicit.
- Explicit financial-access mission language can still be under-called if either beneficiary or mechanism is too implicit in the excerpt.

## Audit Recommendation

Another smaller audit is recommended before full-corpus scaling. The next audit should target 75-100 rows, oversampling:

- Rows changed from v1 to v2.
- Institutional/platform/market-access phrases.
- Affordable-housing rows.
- CRA/regulatory rows.
- Newly positive explicit mission-language rows.
- Rows with `codex_assisted_v2` source and medium or low confidence.

## Guardrail Reminder

Treatment construction is not finalized. Returns, prices, benchmark outcomes, and empirical performance analysis remain off-limits until post-revision classification quality is checked and approved.
