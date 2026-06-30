# CHECKPOINT 16: Tiered Classification Audit

Generated at: 2026-06-29T16:18:00-04:00

## Completed

- Created a deterministic post-tiered audit sampler.
- Created the requested 150-row audit sample.
- Manually audited all sampled rows using only the excerpt and tiered classification guidelines.
- Wrote the audited sample.
- Wrote the audit plan and audit results report.
- Preserved `data/extracted/phrase_hits.csv` unchanged.
- Preserved `data/classified/phrase_hits_tiered_v1.csv` unchanged.
- Did not fetch prices, compute returns, make SEC requests, construct treatment variables, or make empirical performance claims.

## Files Created

- `scripts/prepare_tiered_classification_audit_sample.py`
- `data/review/tiered_classification_audit_sample.csv`
- `quality_reports/tiered_classification_audit_plan.md`
- `data/review/tiered_classification_audit_sample_audited.csv`
- `quality_reports/tiered_classification_audit_results.md`
- `CHECKPOINT_16_TIERED_CLASSIFICATION_AUDIT.md`

## Source File Integrity

- Raw `data/extracted/phrase_hits.csv` SHA256: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Tiered classified `data/classified/phrase_hits_tiered_v1.csv` SHA256: `c647e1d0acc4498d40426388e8f7046b664e7fee6eca3ffc817ddb50707159df`
- Raw file unchanged: yes
- Tiered classified file unchanged: yes

## Full-Corpus Row Counts

- Total tiered classified rows: 9,400
- Full-corpus Tier 1 rows: 725
- Full-corpus Tier 2 rows: 1,292
- Full-corpus Tier 3 rows: 1,571
- Full-corpus excluded rows: 5,812

## Audit Sample Row Counts

- Audit sample rows: 150
- Sampled Tier 1 rows: 75
- Sampled Tier 2 rows: 50
- Sampled excluded rows: 25
- Rows with blank audit fields in audited file: 0

## Audit Label Counts

| Audit label | Rows |
| --- | ---: |
| `tier_2_broader_validated` | 67 |
| `excluded_non_treatment` | 59 |
| `tier_1_conservative` | 22 |
| `tier_3_exploratory` | 2 |

## Precision And False-Negative Results

- Tier 1 precision among sampled Tier 1 rows: 17 / 75 = 22.7%
- Tier 2 candidate precision among sampled Tier 2 rows: 34 / 50 = 68.0%
- Tier 2 exact-label agreement among sampled Tier 2 rows: 31 / 50 = 62.0%
- Excluded false-negative rate for Tier 1 / Tier 2 treatment candidates: 10 / 25 = 40.0%
- Overall disagreement rate: 87 / 150 = 58.0%

Tier 2 candidate precision counts sampled Tier 2 rows as valid when the audit label remained a validated treatment candidate, either `tier_1_conservative` or `tier_2_broader_validated`. Promotions from Tier 2 to Tier 1 are still label disagreements.

## Disagreement Summary

Main disagreement sources:

- `underserved markets`: frequently issuer market-entry or acquisition-growth language rather than external financial-access expansion.
- `unbanked`: several risk-section rows describe competitor banks targeting unbanked users rather than issuer access expansion.
- Marketplace-lending RFI language: often substantive enough for Tier 2, but not Tier 1 because it is regulatory context rather than issuer-specific action.
- CRA/FIO regulatory language: often identifies beneficiary and mechanism but usually does not satisfy Tier 1 issuer-action requirements.
- Affordable-housing language: still mixes genuine housing access, program definitions, loan categories, property development, sale/accounting, and community-program language.
- Fractional-share language: some customer-access rows were incorrectly excluded and need recovery rules.
- Retail-investor risk-section language: needs a sharper rule separating issuer access to retail channels from retail investor access to investment products.

## Decision Rule Assessment

- Tier 1 threshold: requires at least 90%; observed 22.7%.
- Tier 2 threshold: requires at least 80%; observed 68.0%.
- Excluded false-negative threshold: revise if above 20%; observed 40.0%.

## Proceed / Revise Recommendation

Revise the tiered classifier before treatment-variable construction.

Tier 1 is not valid enough for main treatment-candidate construction under the pre-specified 90% sampled precision rule. Tier 2 is not valid enough for broader or sensitivity treatment-candidate construction under the pre-specified 80% sampled candidate-precision rule. The excluded sample also exceeded the 20% false-negative threshold, so treatment construction should not proceed from `phrase_hits_tiered_v1.csv`.

## Remaining Classification Risks

- Risk-section language is over-admitted into Tier 1 and Tier 2.
- Competitor access, issuer-market-entry language, and issuer access to customer segments remain common false positives.
- Regulatory language needs a clearer separation between background/legal context and issuer-specific access mechanisms.
- Fractional-share product access needs a rule that recovers clear customer access while still excluding stock mechanics.
- Affordable-housing language needs more explicit treatment of sale/accounting, development-risk, LIHTC, and program-definition contexts.
- Retail-investor rows need clearer distinction between retail investors gaining access to products and issuers seeking access to retail distribution.
- The audit sample intentionally oversampled high-risk rows, so it is best interpreted as a stress test of construct validity rather than a random precision estimate.

## Guardrail Reminder

Returns, prices, benchmark outcomes, SEC requests, and empirical performance analysis remain off-limits. Treatment variables have not been constructed and must wait until a revised Tier 1 / Tier 2 classification layer is validated.
