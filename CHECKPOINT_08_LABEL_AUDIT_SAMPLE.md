# CHECKPOINT 08: Codex-Assisted Label Audit Sample

Generated at: 2026-06-29T01:28:50.7088724-04:00

## Completed

- Created a deterministic audit-sample preparation script.
- Created a 150-row audit sample from Codex-assisted rows only.
- Wrote an audit plan report with counts, rationale, and specific risks to check.
- Preserved manual calibration rows outside the audit sample.
- Preserved raw phrase hits unchanged.

## Explicit Non-Actions

- No prices fetched.
- No return analysis run.
- No SEC requests made.
- No empirical performance claims made.
- No raw files modified.
- No classification scaled to all 9,400 hits.
- No outcome data loaded.

## Files Created

- `scripts/prepare_label_audit_sample.py`
- `data/review/codex_assisted_label_audit_sample.csv`
- `quality_reports/codex_assisted_label_audit_plan.md`
- `CHECKPOINT_08_LABEL_AUDIT_SAMPLE.md`

## Acceptance Checks

- Eligible Codex-assisted rows: 480
- Audit sample rows: 150
- True-positive audit rows: 100
- Non-true-positive audit rows: 50
- Manual calibration rows included: 0
- Rows with `label_source == codex_assisted`: 150
- Rows with blank audit fields: 150
- Raw `data/extracted/phrase_hits.csv` SHA256 remained `BA511BF32939B78C7D15B6518C7FBA78CEE3E7E6357B49BFEF21F90D18288054`

## Audit Sample Coverage

- Categories represented: 10
- Phrases represented: 60
- Filing years represented: 11
- Sections represented: 3
- Firms represented: 89

## Label Counts In Audit Sample

- `true_positive_access_expansion`: 100
- `generic_marketing`: 23
- `operational_access_or_platform_language`: 14
- `risk_disclosure_only`: 5
- `false_positive`: 4
- `ambiguous`: 4

## Main Risks To Audit

- Over-calling `true_positive_access_expansion` when the excerpt lacks an external beneficiary.
- Over-calling `true_positive_access_expansion` when the excerpt lacks a financial-access mechanism.
- `affordable housing` in tax-credit, partnership, accounting, portfolio, or commitments-table context.
- `market access`, `access to markets`, and `capital markets access` in issuer financing, regulatory, competitive, risk, or operational contexts.
- `fractional share` in stock split, merger, issuance, or cash-in-lieu mechanics.
- `institutional quality`, `institutional-grade`, and related phrases in real-estate quality, platform, infrastructure, or internal capability contexts.
- Item 1A `access to credit` language about issuer liquidity or funding rather than external borrowers or customers.
- Regulatory or CRA language that lists compliance objectives without issuer action benefiting external financial users.

## Treatment Status

Treatment construction is not finalized. The current audit sample is only a pre-scaling validation step for Codex-assisted text labels. Future treatment variables must remain auditable to `hit_id`, accession number, section, phrase, excerpt, label, confidence, and label source.

## Next Recommended Stage

Manually audit `data/review/codex_assisted_label_audit_sample.csv` using `config/classification_guidelines_v2.md`, fill the blank audit columns, and summarize disagreement rates overall and by phrase/category. Do not scale classification or load return outcomes until audit quality is reviewed.
