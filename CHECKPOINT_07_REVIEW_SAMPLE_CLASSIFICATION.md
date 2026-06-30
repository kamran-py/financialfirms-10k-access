# CHECKPOINT 07: Review Sample Classification

Generated at: 2026-06-29T01:23:26.2794711-04:00

## Completed

- Imported the 120-row manually labeled calibration subset.
- Created v2 classification guidance incorporating calibration lessons.
- Implemented a text-only review-sample classifier.
- Classified the 600-row review sample with manual labels preserved separately from Codex-assisted labels.
- Wrote a quality report for label distributions, high-risk phrases, ambiguous cases, and future treatment-variable construction.

## Explicit Non-Actions

- No prices fetched.
- No returns computed.
- No return analysis run.
- No SEC requests made.
- No empirical performance claims made.
- No later stock returns, later news, litigation, bankruptcies, acquisitions, or external firm events used for classification.
- No modification of `data/extracted/phrase_hits.csv`.

## Files Created Or Modified

- Created `data/review/manual_calibration_labels_20260629.csv`
- Created `config/classification_guidelines_v2.md`
- Created `scripts/classify_review_sample.py`
- Created `data/review/phrase_hit_review_sample_classified_v1.csv`
- Created `quality_reports/review_sample_classification_report.md`
- Created `CHECKPOINT_07_REVIEW_SAMPLE_CLASSIFICATION.md`

## Row Counts

- Raw phrase hits available in `data/extracted/phrase_hits.csv`: 9,400
- Review sample rows: 600
- Manual calibration rows imported: 120
- Codex-assisted rows classified: 480
- Classified sample rows written: 600
- Rows missing `final_label`, `final_confidence`, or `label_source`: 0
- Manual calibration mismatches against imported labels: 0

## Label Distribution

- `true_positive_access_expansion`: 365
- `operational_access_or_platform_language`: 83
- `false_positive`: 52
- `generic_marketing`: 44
- `risk_disclosure_only`: 42
- `ambiguous`: 8
- `customer_access_unrelated_to_finance`: 6

## Strongest True-Positive Categories

- `retail access to investing`: 83 true positives / 112 rows
- `underserved / underbanked / unbanked`: 81 true positives / 85 rows
- `homeownership access`: 56 true positives / 96 rows
- `expanded access to credit`: 47 true positives / 65 rows
- `democratized access`: 32 true positives / 43 rows

These are validation-sample text labels only. They are not return treatments until classification quality is reviewed and filing-level construction rules are approved.

## Noisiest Phrases And Categories

Noisiest phrases by negative/noise-label rate among phrases with at least 3 sampled rows:

- `capital markets access`: 4/4 negative or noise labels
- `institutional grade`: 4/4 negative or noise labels
- `broader participation`: 3/3 negative or noise labels
- `reducing barriers`: 3/3 negative or noise labels
- `market access`: 25/27 negative or noise labels
- `level playing field`: 8/9 negative or noise labels
- `institutional quality`: 13/15 negative or noise labels
- `fractional share`: 27/32 negative or noise labels
- `access to markets`: 8/10 negative or noise labels
- `lower barriers`: 6/8 negative or noise labels

Noisiest categories by negative/noise-label rate:

- `broader market participation`: 40/44 negative or noise labels
- `institutional-grade access for individuals`: 26/39 negative or noise labels
- `lower barriers / level playing field`: 25/53 negative or noise labels
- `homeownership access`: 40/96 negative or noise labels
- `retail access to investing`: 29/112 negative or noise labels

## Unresolved Classification Risks

- Codex-assisted labels are rule-based text classifications and need human quality review before downstream use.
- The 120-row manual calibration subset may not cover all phrases, issuers, sections, and edge cases.
- `affordable housing`, `market access`, `fractional share`, `institutional quality`, and `institutional-grade` remain high-risk and should be flagged or manually reviewed before primary treatment construction.
- Risk-factor language can contain both issuer-risk and customer-access language; Item 1A positives should be audited carefully.
- Regulatory and CRA language can be substantive, operational, or table/accounting context; label quality should be checked before aggregation.
- The review sample validates sampled hits only. It does not validate all 9,400 raw hits.

## Recommended Next Stage

Review `quality_reports/review_sample_classification_report.md` and audit a targeted set of high-risk phrase/category cases. If label quality is acceptable, create a locked classified-hit table with reviewer metadata, classification version, source, confidence, and audit notes. Then define filing-level validated text variables from `final_label == true_positive_access_expansion`, preserving `hit_id`, accession number, section, phrase, excerpt, label, confidence, and label source.

Return analysis is still not allowed until classification quality is reviewed and approved, security/price data sources are approved, and return-window construction is implemented with explicit missingness and right-censoring reason codes.
