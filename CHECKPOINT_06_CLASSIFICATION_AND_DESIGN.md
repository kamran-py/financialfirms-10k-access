# CHECKPOINT 06: Classification Framework And Research Design

Generated at: 2026-06-29T01:03:25.3095995-04:00

## Completed

- Created manual classification guidelines for raw phrase-hit validation.
- Implemented a deterministic stratified review-sample preparation script.
- Generated a 600-row manual review sample from 9,400 raw phrase hits.
- Generated a blank review template with the required review columns.
- Prepared a classification prep quality report.
- Pre-specified econometric design before return collection.
- Pre-specified a pre-analysis plan before return collection.

## Explicit Non-Actions

- No prices fetched.
- No return analysis run.
- No SEC requests made.
- No empirical claims made.
- No automatic classification of every hit as true positive.
- No overwrite of `data/extracted/phrase_hits.csv`.

## Inputs

- `research_plan.md`
- `methodology_notes.md`
- `schema.sql`
- `CHECKPOINT_05_PHRASE_MATCHING.md`
- `quality_reports/phrase_hit_report.md`
- `config/access_phrases.csv`
- `data/extracted/phrase_hits.csv`
- `data/extracted/filing_sections.csv`

## Outputs

- `config/classification_guidelines.md`
- `scripts/prepare_review_sample.py`
- `data/review/phrase_hit_review_sample.csv`
- `data/review/phrase_hit_review_template.csv`
- `methodology/econometric_design.md`
- `methodology/pre_analysis_plan.md`
- `quality_reports/classification_prep_report.md`
- `CHECKPOINT_06_CLASSIFICATION_AND_DESIGN.md`

## Review Sample

- Raw hits available for review: 9,400
- Review sample rows: 600
- Review sample stratification targets: phrase category, phrase, filing year, section, and firm
- Human review columns: `human_label`, `reviewer_notes`, `confidence`
- Company names populated from local `config/firm_universe.csv` where available

## Classification Labels

- `true_positive_access_expansion`
- `generic_marketing`
- `risk_disclosure_only`
- `customer_access_unrelated_to_finance`
- `operational_access_or_platform_language`
- `ambiguous`
- `false_positive`

## Design Guardrails

- Raw phrase hits are not interpreted evidence.
- Classified labels must be stored as a separate layer that preserves raw hit IDs.
- Return windows are right-censored as of 2026-06-29 unless their target dates are observable by that date.
- No conclusion should use the word `causes` unless a separately justified identification strategy has been approved.

## Next Recommended Prompt

Manually review `data/review/phrase_hit_review_sample.csv` using `config/classification_guidelines.md`, then create a locked classified-hit table with reviewer metadata and agreement/adjudication fields. Do not fetch or analyze returns until classification validation is complete and the return-data source is approved.
