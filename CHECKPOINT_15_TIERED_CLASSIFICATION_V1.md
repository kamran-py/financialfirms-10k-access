# CHECKPOINT 15: Tiered Classification V1

Generated at: 2026-06-29T15:58:50.4382109-04:00

## Completed

- Created tiered treatment classification guidelines.
- Created a stricter full-corpus tiered classifier.
- Applied the classifier to all raw phrase hits in `data/extracted/phrase_hits.csv`.
- Wrote the tiered classified output.
- Wrote the tiered classification quality report.
- Preserved raw phrase-hit fields in the tiered output.
- Preserved raw `data/extracted/phrase_hits.csv` unchanged.
- Preserved `data/classified/phrase_hits_classified_v2.csv` unchanged.
- Did not use full-corpus V2 as a treatment variable.

## Files Created

- `config/tiered_treatment_classification_guidelines_v1.md`
- `scripts/classify_phrase_hits_tiered_v1.py`
- `data/classified/phrase_hits_tiered_v1.csv`
- `quality_reports/tiered_classification_v1_report.md`
- `CHECKPOINT_15_TIERED_CLASSIFICATION_V1.md`

## Explicit Non-Actions

- No prices fetched.
- No returns computed.
- No return analysis run.
- No benchmark outcomes loaded.
- No SEC requests made.
- No empirical performance claims made.
- No modification of `data/extracted/phrase_hits.csv`.
- No use of full-corpus V2 as a treatment variable.
- No final treatment variables constructed.

## File Integrity

- Raw `data/extracted/phrase_hits.csv` SHA256: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- V2 classified `data/classified/phrase_hits_classified_v2.csv` SHA256: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- Tiered output `data/classified/phrase_hits_tiered_v1.csv` SHA256: `c647e1d0acc4498d40426388e8f7046b664e7fee6eca3ffc817ddb50707159df`
- Raw file unchanged: yes
- V2 classified file unchanged: yes

## Row Counts

- Total raw hits classified: 9,400
- Rows with blank `tiered_label`, `tiered_confidence`, `narrative_subcategory`, `classifier_version`, or `high_risk_phrase_flag`: 0
- Classifier version: `tiered_treatment_classification_guidelines_v1`

## Tier Counts

| Tiered label | Rows |
| --- | --- |
| `tier_1_conservative` | 725 |
| `tier_2_broader_validated` | 1,292 |
| `tier_3_exploratory` | 1,571 |
| `excluded_non_treatment` | 5,812 |

Additional filing-level support diagnostics:

- Tier 1 unique filing count: 451
- Tier 2 unique filing count: 845

## Narrative Subcategory Counts

| Narrative subcategory | Rows |
| --- | --- |
| excluded / non-treatment | 5,812 |
| financial inclusion / underbanked / underserved | 1,270 |
| retail investing / brokerage democratization | 934 |
| consumer credit access | 678 |
| affordable housing / homeownership access | 378 |
| smaller-issuer capital-market access | 248 |
| generic/other access-expansion | 36 |
| payments / money movement / SMB commerce access | 36 |
| fee / cost / minimum-reduction framing | 4 |
| insurance / benefits access | 2 |
| private-market or alternative-investment access | 2 |

## High-Risk Phrase Handling Summary

- `affordable housing` now defaults out unless the excerpt names an external housing beneficiary or a direct housing finance/access mechanism.
- `fractional share` defaults out unless the excerpt describes fractional investing access for retail, individual, consumer, or other external investors.
- Market-access phrases default out unless the excerpt identifies external beneficiaries gaining financial-market or capital-market access.
- Institutional-quality phrases default out unless the excerpt explicitly gives non-institutional external users access to institutional-quality capabilities.
- `access to credit` defaults out for issuer credit ratings, issuer liquidity, funding, FHLB borrowing, or credit-facility contexts.
- Barrier-reduction phrases default out for affiliation, product-listing, competitor-entry, technology, internal operations, and generic legislation contexts.
- CRA/regulatory language without issuer-specific action is generally Tier 2 rather than Tier 1 when it clearly names external beneficiaries and financial-access mechanisms.
- Risk-section access language is excluded unless it clearly describes external financial access rather than issuer or competitive risk.

High-risk rows remain a required focus for post-tiered audit.

## Report Coverage

`quality_reports/tiered_classification_v1_report.md` includes:

- Total rows classified.
- Counts by `tiered_label`.
- Tier 1 row and unique filing counts.
- Tier 2 row and unique filing counts.
- Tier 3 row count.
- Excluded row count.
- Counts by narrative subcategory.
- Counts by phrase.
- Counts by phrase family.
- Counts by section.
- Counts by filing year.
- High-risk phrase positive rates by tier.
- Top firms by Tier 1 count.
- Top firms by Tier 2 count.
- Examples of Tier 1 rows.
- Examples of excluded high-risk rows.
- Warnings about remaining construct-validity risks.
- Clear statement that outputs are treatment candidates, not empirical findings.

## Recommendation For Post-Tiered Audit Sample

Next stage should validate `phrase_hits_tiered_v1.csv` before constructing treatment variables.

Recommended audit design:

- At least 150 rows.
- Oversample Tier 1 rows, especially high-risk Tier 1 rows.
- Include Tier 2 rows to estimate whether broader validated candidates are precise enough for robustness use.
- Include Tier 3 and excluded rows to estimate false negatives.
- Oversample `affordable housing`, `access to credit`, market-access, institutional-quality, fractional-share, barrier-reduction, CRA/regulatory, and risk-section access language.
- Cover all three sections and filing years 2015-2025.
- Report Tier 1 precision separately from Tier 2 precision.
- Require Tier 1 sampled precision of at least 85% before Tier 1 treatment construction proceeds.

## Remaining Classification Risks

- Tier 1 is deliberately conservative and may under-call valid access-expansion language.
- Tier 2 includes medium-confidence and regulatory/CRA cases that require validation before any robustness use.
- High-risk phrase families can still contain false positives despite stricter defaults.
- Narrative subcategories with low support may need aggregation or exclusion before treatment construction.
- Outputs are treatment candidates only until validated by a post-classification audit.

## Guardrail Reminder

Returns, prices, benchmark outcomes, and empirical performance analysis remain off-limits until Tier 1 and Tier 2 classification is validated and approved. Treatment variables have not yet been constructed.
