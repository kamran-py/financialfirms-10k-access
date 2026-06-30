# CHECKPOINT 13: Full Corpus V2 Spot Check

Generated at: 2026-06-29T15:39:18.0832243-04:00

## Completed

- Created a deterministic post-scale full-corpus V2 spot-check sampler.
- Prepared a 150-row spot-check sample from `data/classified/phrase_hits_classified_v2.csv`.
- Manually audited all 150 sampled rows using only excerpts and `config/classification_guidelines_v3.md`.
- Wrote the audited spot-check sample.
- Wrote the post-scale spot-check quality report.
- Preserved raw `data/extracted/phrase_hits.csv` unchanged.
- Preserved classified `data/classified/phrase_hits_classified_v2.csv` unchanged.

## Files Created

- `scripts/prepare_full_corpus_classification_spotcheck.py`
- `data/review/full_corpus_v2_spotcheck_sample.csv`
- `quality_reports/full_corpus_v2_spotcheck_plan.md`
- `data/review/full_corpus_v2_spotcheck_sample_audited.csv`
- `quality_reports/full_corpus_v2_spotcheck_results.md`
- `CHECKPOINT_13_FULL_CORPUS_V2_SPOTCHECK.md`

## Explicit Non-Actions

- No prices fetched.
- No returns computed.
- No return analysis run.
- No benchmark outcomes loaded.
- No SEC requests made.
- No empirical performance claims made.
- No modification of `data/extracted/phrase_hits.csv`.
- No modification of `data/classified/phrase_hits_classified_v2.csv`.
- No treatment variables constructed.

## File Integrity

- Raw `data/extracted/phrase_hits.csv` SHA256: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Classified `data/classified/phrase_hits_classified_v2.csv` SHA256: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- Raw file unchanged: yes
- Classified file unchanged: yes

## Full Corpus Counts

- Full classified row count: 9,400
- Full-corpus true-positive row count: 7,414
- Full-corpus true-positive filing count: 2,520

## Spot-Check Sample Counts

- Spot-check sample size: 150
- Sampled full-corpus positives: 100
- Sampled full-corpus non-positives: 50
- Spot-check rows with all audit fields filled: 150
- Sampled high-risk phrase rows: 121
- Sampled high-risk phrase rows labeled true positive before audit: 73
- Sample covered all three sections and all filing years from 2015 through 2025.

## Precision Result

- Confirmed true positives among sampled full-corpus positives: 55 / 100
- True-positive precision among sampled full-corpus positives: 55.0%
- Recovered true positives among sampled full-corpus non-positives: 6 / 50
- False-negative rate among sampled full-corpus non-positives: 12.0%
- Total disagreements: 59 / 150 (39.3%)

## Label Counts Before Spot Check

| Final label V2 | Rows |
| --- | --- |
| true_positive_access_expansion | 100 |
| operational_access_or_platform_language | 14 |
| false_positive | 13 |
| risk_disclosure_only | 12 |
| customer_access_unrelated_to_finance | 7 |
| ambiguous | 2 |
| generic_marketing | 2 |

## Label Counts After Spot Check

| Spot-check label | Rows |
| --- | --- |
| true_positive_access_expansion | 61 |
| false_positive | 43 |
| operational_access_or_platform_language | 26 |
| risk_disclosure_only | 17 |
| generic_marketing | 2 |
| customer_access_unrelated_to_finance | 1 |

## Disagreement Summary

Top disagreement phrases:

| Phrase | Disagreements |
| --- | --- |
| affordable housing | 29 |
| institutional caliber | 4 |
| institutional quality | 4 |
| institutional-grade | 4 |
| market access | 4 |
| access to credit | 3 |
| access to markets | 2 |
| eliminate barriers | 2 |
| individual investors | 2 |

Top disagreement categories:

| Category | Disagreements |
| --- | --- |
| homeownership access | 29 |
| institutional-grade access for individuals | 12 |
| broader market participation | 7 |
| expanded access to credit | 4 |
| retail access to investing | 3 |

Primary disagreement pattern:

- `affordable housing` positives were frequently tax-credit, portfolio, investment-income, sale, or accounting references rather than external housing-access activity.
- Institutional-quality positives included property quality, analyst-process quality, custody infrastructure, and services to hedge funds or institutional/HNW clients.
- Some credit-access positives described issuer funding, credit ratings, FHLB borrowing, or credit facilities rather than external borrowers.
- Some market-access positives described issuer, competitor, prime-broker, exchange-fee, or operational access rather than customer or smaller-issuer access.

## Proceed Or Revise Recommendation

Decision rule result:

- Precision threshold met: no.
- False-negative threshold exceeded: no.
- Recommendation: revise classification rules before treatment-variable construction.

The sampled full-corpus true-positive precision of 55.0% is below the 85% threshold. Because the false-negative rate among sampled non-positives is 12.0%, the main revision need is reducing over-called positives rather than broadly recovering under-called positives.

## Remaining Classification Risks

- Full-corpus V2 should not be used directly for treatment-variable construction until high-risk positive rules are revised or filtered.
- `affordable housing` needs a stricter exclusion for tax-credit, investment, sale, partnership, and accounting contexts unless the excerpt directly ties the phrase to external housing access, mortgage access, residents, renters, or low-income beneficiaries.
- Institutional-quality phrases need a stricter exclusion for property quality, platform/custody infrastructure, analyst process, and services to institutional/HNW clients.
- `access to credit` needs a stricter exclusion for issuer credit ratings, issuer liquidity, FHLB borrowing, funding sources, credit facilities, and capital-market financing.
- Market-access phrases need a stricter exclusion for issuer operational access, prime-broker access, exchange connectivity, competitor advantages, and regulatory fee language.
- A smaller set of non-positive rows may need recovery where excerpts clearly describe external credit or financial-market access.

## Guardrail Reminder

Returns, prices, benchmark outcomes, and empirical performance analysis remain off-limits. Treatment construction should not begin until classification revisions are completed and approved.
