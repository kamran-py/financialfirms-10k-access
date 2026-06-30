# V2 Validation Audit Results

Generated at: 2026-06-29T05:56:56.991287+00:00

## Scope

- Manually validated the 100-row V2 Codex-assisted validation sample using excerpts and `classification_guidelines_v3.md` only.
- No prices, returns, outcome data, SEC requests, later news, outside firm knowledge, litigation, bankruptcies, acquisitions, or external events were used.
- Raw `phrase_hits.csv` was not modified.

## Validation Counts

- Eligible V2 Codex-assisted rows: 330
- Validation sample size: 100
- Sampled V2 true positives: 75
- Sampled V2 non-positives: 25
- Validation fields filled: 100
- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes

## Label Counts Before Validation

| V2 final label | Rows |
| --- | --- |
| true_positive_access_expansion | 75 |
| operational_access_or_platform_language | 12 |
| false_positive | 5 |
| generic_marketing | 4 |
| risk_disclosure_only | 2 |
| ambiguous | 1 |
| customer_access_unrelated_to_finance | 1 |

## Label Counts After Validation

| Validation label | Rows |
| --- | --- |
| true_positive_access_expansion | 75 |
| operational_access_or_platform_language | 12 |
| false_positive | 5 |
| generic_marketing | 4 |
| risk_disclosure_only | 2 |
| ambiguous | 1 |
| customer_access_unrelated_to_finance | 1 |

## Agreement Metrics

- Total disagreements: 0 / 100 (0.0%)
- True-positive precision among sampled V2 true positives: 75 / 75 (100.0%)
- False-negative rate among sampled V2 non-positives: 0 / 25 (0.0%)

## Disagreement Counts By Phrase

- None

## Disagreement Counts By Category

- None

## Scale Decision

- Recommend scaling classification to all 9,400 raw hits, with high-risk phrase flags retained and post-scale spot checks.

## Specific Remaining Rule Refinements

- Keep high-risk flags for `affordable housing`, `access to credit`, market-access phrases, and institutional-quality phrases during full-corpus scaling.
- After scaling, run a post-scale spot check of high-risk phrases and any low-confidence positives.
- Preserve validation source fields so treatment construction remains auditable.

## Guardrail Reminder

Treatment construction is not finalized until validation results are accepted. Returns remain off-limits until treatment classification is finalized.
