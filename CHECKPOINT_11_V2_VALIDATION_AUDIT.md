# CHECKPOINT 11: V2 Validation Audit

Generated at: 2026-06-29T01:57:50.8630654-04:00

## Completed

- Created `scripts/prepare_v2_validation_sample.py`.
- Created a targeted 100-row V2 Codex-assisted validation sample.
- Validated all 100 sampled rows using excerpts and `config/classification_guidelines_v3.md`.
- Wrote the audited validation sample and validation audit results report.
- Preserved manual calibration labels and prior manual audit labels.
- Preserved raw phrase hits unchanged.

## Explicit Non-Actions

- No prices fetched.
- No returns computed.
- No return analysis run.
- No SEC requests made.
- No empirical performance claims made.
- No classification scaled to all 9,400 raw hits.
- No modification of `data/extracted/phrase_hits.csv`.

## Files Created Or Modified

- Created `scripts/prepare_v2_validation_sample.py`
- Created `data/review/v2_codex_assisted_validation_sample.csv`
- Created `quality_reports/v2_validation_sample_plan.md`
- Created `data/review/v2_codex_assisted_validation_sample_audited.csv`
- Created `quality_reports/v2_validation_audit_results.md`
- Created `CHECKPOINT_11_V2_VALIDATION_AUDIT.md`

## Validation Row Counts

- Eligible V2 Codex-assisted rows: 330
- Validation sample rows: 100
- Sampled V2 true positives: 75
- Sampled V2 non-positives: 25
- Manual calibration rows included: 0
- Prior manual audit rows included: 0
- Rows with all validation fields filled: 100
- Raw `data/extracted/phrase_hits.csv` SHA256 remained `BA511BF32939B78C7D15B6518C7FBA78CEE3E7E6357B49BFEF21F90D18288054`

## Validation Precision Result

- Total disagreements: 0 / 100 (0.0%)
- True-positive precision among sampled V2 true positives: 75 / 75 (100.0%)
- False-negative rate among sampled V2 non-positives: 0 / 25 (0.0%)

## Disagreement Summary

- No disagreements were recorded in the targeted validation sample.
- Label counts before validation matched label counts after validation.
- The validation sample included all 10 categories, 31 phrases, 11 filing years, 3 sections, and 76 firms.

## Scale Recommendation

Recommend scaling classification to all 9,400 raw hits under the decision rule:

- Sampled V2 true-positive precision was at least 85%.
- False negatives among sampled V2 non-positives were not above 20%.

Scaling should retain high-risk phrase flags and should produce a post-scale quality report before any treatment variables are used in return analysis.

## Remaining Classification Risks

- High-risk phrases still require flags and spot checks: `affordable housing`, `access to credit`, market-access phrases, institutional-quality phrases, `fractional share`, and barrier-reduction phrases.
- Full-corpus scaling may expose phrase contexts not represented in the 600-row review sample.
- Post-scale validation should audit low-confidence positives, high-risk phrase positives, and unusual firm/section concentrations.
- Treatment construction is still not final until the full-corpus classified output is reviewed and approved.

## Guardrail Reminder

Returns, prices, benchmark outcomes, and empirical performance analysis remain off-limits until treatment classification is finalized and approved.
