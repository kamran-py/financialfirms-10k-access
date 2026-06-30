# CHECKPOINT 09 - Label Audit Results

## Files Created

- `data\review\codex_assisted_label_audit_sample_audited_20260629.csv`
- `quality_reports\codex_assisted_label_audit_results.md`

## Counts

- Audit rows: 150
- Label disagreements: 64
- Audited true-positive precision: 67/100 (67.0%)
- Audited non-positive rows relabeled positive: 15/50 (30.0%)
- Raw phrase hits unchanged: yes

## Guardrails

- No prices fetched.
- No SEC requests made.
- No return outcomes loaded or computed.
- No empirical performance claims made.
- Classification has not been scaled to all 9,400 raw hits.

## Next Recommended Stage

Revise the classification rules/script using audit disagreements, then rerun the 600-row review sample classification and compare audit precision before scaling to all raw hits.
