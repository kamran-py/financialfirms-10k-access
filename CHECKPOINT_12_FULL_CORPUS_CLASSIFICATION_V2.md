# CHECKPOINT 12: Full Corpus Classification V2

Generated at: 2026-06-29T15:29:01.0336345-04:00

## Completed

- Created `scripts/classify_all_phrase_hits_v2.py`.
- Classified all rows in `data/extracted/phrase_hits.csv`.
- Wrote `data/classified/phrase_hits_classified_v2.csv`.
- Wrote `quality_reports/full_corpus_classification_v2_report.md`.
- Preserved all raw phrase-hit fields in the classified output.
- Added required V2 classification fields:
  - `final_label_v2`
  - `final_confidence_v2`
  - `label_source_v2`
  - `classifier_version`
  - `high_risk_phrase_flag`
  - `classification_notes_v2`
- Set `classifier_version` to `classification_guidelines_v3` for all classified rows.
- Preserved manual calibration, manual audit, and V2 validation-audit labels as source artifacts where their derived row-number `hit_id` matched the full corpus.
- Flagged known noisy high-risk phrases in `high_risk_phrase_flag`.

## Explicit Non-Actions

- No prices fetched.
- No returns computed.
- No return analysis run.
- No benchmark outcomes loaded.
- No SEC requests made.
- No empirical performance claims made.
- No modification of `data/extracted/phrase_hits.csv`.
- No downstream treatment-variable construction beyond hit-level treatment-candidate classification.

## Files Created

- `scripts/classify_all_phrase_hits_v2.py`
- `data/classified/phrase_hits_classified_v2.csv`
- `quality_reports/full_corpus_classification_v2_report.md`
- `CHECKPOINT_12_FULL_CORPUS_CLASSIFICATION_V2.md`

## Validation Counts

- Total classified rows: 9,400
- Expected raw-hit count from prior checkpoint: 9,400
- Rows with blank `final_label_v2`, `final_confidence_v2`, or `classifier_version`: 0
- Classifier-version mismatches: 0
- True-positive count: 7,414
- True-positive filings count: 2,520
- High-risk phrase rows: 4,484
- High-risk true-positive rows: 2,738
- High-risk positive rate: 61.1%

## Label Distribution

| Final label V2 | Rows |
| --- | --- |
| true_positive_access_expansion | 7,414 |
| false_positive | 662 |
| risk_disclosure_only | 548 |
| operational_access_or_platform_language | 514 |
| customer_access_unrelated_to_finance | 179 |
| ambiguous | 54 |
| generic_marketing | 29 |

## Label Source Distribution

| Label source V2 | Rows |
| --- | --- |
| codex_assisted_full_corpus_v2 | 8,800 |
| codex_assisted_v2 | 230 |
| manual_audit | 150 |
| manual_calibration | 120 |
| v2_validation_audit | 100 |

## File Integrity

- Raw `data/extracted/phrase_hits.csv` SHA256 before classification: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `data/extracted/phrase_hits.csv` SHA256 after classification: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes
- Classified output SHA256: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`

## Quality Report Coverage

`quality_reports/full_corpus_classification_v2_report.md` includes:

- Total classified rows.
- Label distribution.
- True-positive count.
- True-positive filings count.
- Label distribution by category.
- Label distribution by phrase.
- Label distribution by section.
- Label distribution by filing year.
- High-risk phrase counts and positive rates.
- Top firms by classified true-positive count.
- Top phrases driving true positives.
- Recommended post-scale spot checks.
- Warning that no return outcomes have been loaded.

## Post-Scale Review Risks

- `affordable housing` is the largest true-positive phrase driver and remains a high-risk phrase requiring spot checks.
- Risk-section positives should be spot-checked before filing-level treatment construction.
- Firms with high classified true-positive counts should be reviewed for repeated boilerplate and section-extraction artifacts.
- Low- and medium-confidence positives should be sampled before labels are used in any downstream treatment variables.

## Guardrail Reminder

These outputs are treatment-candidate construction only. No return outcomes, prices, benchmark returns, or empirical performance data have been loaded. Return analysis remains off-limits until treatment classification is reviewed and approved.
