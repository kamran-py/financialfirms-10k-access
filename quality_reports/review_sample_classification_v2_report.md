# Review Sample Classification V2 Report

Generated at: 2026-06-29T05:46:53.362481+00:00

## Scope

- Reclassified the 600-row review sample using `classification_guidelines_v3.md`.
- Preserved v1 labels for comparison.
- Preserved manual calibration and manual audit labels as ground truth.
- Did not fetch prices, compute returns, make SEC requests, make empirical claims, scale to all 9,400 hits, or modify raw `phrase_hits.csv`.
- Script version: `classify_review_sample_v2`.

## Row Counts

- Total rows: 600
- Manual calibration rows: 120
- Manual audit rows: 150
- Codex-assisted v2 rows: 330
- Label source counts v2: {'manual_calibration': 120, 'codex_assisted_v2': 330, 'manual_audit': 150}
- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged by this stage: yes

## V1 Label Distribution

| V1 label | Count |
| --- | --- |
| ambiguous | 8 |
| customer_access_unrelated_to_finance | 6 |
| false_positive | 52 |
| generic_marketing | 44 |
| operational_access_or_platform_language | 83 |
| risk_disclosure_only | 42 |
| true_positive_access_expansion | 365 |

## V2 Label Distribution

| V2 label | Count |
| --- | --- |
| ambiguous | 3 |
| customer_access_unrelated_to_finance | 15 |
| false_positive | 61 |
| generic_marketing | 13 |
| operational_access_or_platform_language | 95 |
| risk_disclosure_only | 46 |
| true_positive_access_expansion | 367 |

## V1 To V2 Change Summary

- Rows changed from v1 to v2: 134
| V1 label | V2 label | Rows |
| --- | --- | --- |
| operational_access_or_platform_language | true_positive_access_expansion | 31 |
| true_positive_access_expansion | operational_access_or_platform_language | 30 |
| true_positive_access_expansion | false_positive | 14 |
| generic_marketing | true_positive_access_expansion | 13 |
| generic_marketing | operational_access_or_platform_language | 12 |
| generic_marketing | customer_access_unrelated_to_finance | 7 |
| false_positive | true_positive_access_expansion | 6 |
| ambiguous | true_positive_access_expansion | 5 |
| true_positive_access_expansion | risk_disclosure_only | 4 |
| true_positive_access_expansion | generic_marketing | 3 |
| operational_access_or_platform_language | false_positive | 2 |
| generic_marketing | risk_disclosure_only | 2 |
| true_positive_access_expansion | customer_access_unrelated_to_finance | 2 |
| risk_disclosure_only | operational_access_or_platform_language | 2 |
| false_positive | operational_access_or_platform_language | 1 |

## Changes By Category

| Category | Changed rows | Top transitions |
| --- | --- | --- |
| homeownership access | 36 | operational_access_or_platform_language -> true_positive_access_expansion: 29; operational_access_or_platform_language -> false_positive: 2; true_positive_access_expansion -> customer_access_unrelated_to_finance: 2; true_positive_access_expansion -> risk_disclosure_only: 2; true_positive_access_expansion -> false_positive: 1 |
| institutional-grade access for individuals | 19 | true_positive_access_expansion -> false_positive: 7; false_positive -> true_positive_access_expansion: 6; true_positive_access_expansion -> operational_access_or_platform_language: 5; false_positive -> operational_access_or_platform_language: 1 |
| lower barriers / level playing field | 19 | generic_marketing -> operational_access_or_platform_language: 9; generic_marketing -> customer_access_unrelated_to_finance: 7; generic_marketing -> risk_disclosure_only: 2; generic_marketing -> true_positive_access_expansion: 1 |
| democratized access | 18 | true_positive_access_expansion -> operational_access_or_platform_language: 13; generic_marketing -> true_positive_access_expansion: 3; generic_marketing -> operational_access_or_platform_language: 2 |
| affordable financial products | 10 | generic_marketing -> true_positive_access_expansion: 9; generic_marketing -> operational_access_or_platform_language: 1 |
| expanded access to credit | 10 | ambiguous -> true_positive_access_expansion: 5; true_positive_access_expansion -> operational_access_or_platform_language: 4; true_positive_access_expansion -> risk_disclosure_only: 1 |
| retail access to investing | 10 | true_positive_access_expansion -> false_positive: 6; true_positive_access_expansion -> operational_access_or_platform_language: 4 |
| broader market participation | 5 | operational_access_or_platform_language -> true_positive_access_expansion: 2; risk_disclosure_only -> operational_access_or_platform_language: 2; true_positive_access_expansion -> operational_access_or_platform_language: 1 |
| underserved / underbanked / unbanked | 5 | true_positive_access_expansion -> operational_access_or_platform_language: 3; true_positive_access_expansion -> risk_disclosure_only: 1; true_positive_access_expansion -> generic_marketing: 1 |
| financial inclusion | 2 | true_positive_access_expansion -> generic_marketing: 2 |

## Changes By Phrase

| Phrase | Changed rows | Top transitions |
| --- | --- | --- |
| affordable housing | 33 | operational_access_or_platform_language -> true_positive_access_expansion: 29; operational_access_or_platform_language -> false_positive: 2; true_positive_access_expansion -> false_positive: 1; true_positive_access_expansion -> customer_access_unrelated_to_finance: 1 |
| institutional quality | 9 | false_positive -> true_positive_access_expansion: 6; true_positive_access_expansion -> operational_access_or_platform_language: 2; false_positive -> operational_access_or_platform_language: 1 |
| affordable financial services | 8 | generic_marketing -> true_positive_access_expansion: 7; generic_marketing -> operational_access_or_platform_language: 1 |
| democratize finance | 6 | true_positive_access_expansion -> operational_access_or_platform_language: 6 |
| democratizing financial services | 6 | true_positive_access_expansion -> operational_access_or_platform_language: 6 |
| fractional share | 5 | true_positive_access_expansion -> false_positive: 5 |
| institutional caliber | 5 | true_positive_access_expansion -> false_positive: 5 |
| removing barriers | 5 | generic_marketing -> customer_access_unrelated_to_finance: 3; generic_marketing -> operational_access_or_platform_language: 2 |
| access to credit | 4 | true_positive_access_expansion -> operational_access_or_platform_language: 2; true_positive_access_expansion -> risk_disclosure_only: 1; ambiguous -> true_positive_access_expansion: 1 |
| eliminating barriers | 4 | generic_marketing -> customer_access_unrelated_to_finance: 4 |
| institutional-grade | 3 | true_positive_access_expansion -> operational_access_or_platform_language: 3 |
| access to affordable credit | 2 | ambiguous -> true_positive_access_expansion: 2 |
| access to housing | 2 | true_positive_access_expansion -> risk_disclosure_only: 2 |
| access to investment | 2 | true_positive_access_expansion -> operational_access_or_platform_language: 2 |
| affordable credit | 2 | ambiguous -> true_positive_access_expansion: 2 |
| affordable loans | 2 | generic_marketing -> true_positive_access_expansion: 2 |
| broader participation | 2 | operational_access_or_platform_language -> true_positive_access_expansion: 2 |
| capital markets access | 2 | risk_disclosure_only -> operational_access_or_platform_language: 2 |
| democratize access | 2 | generic_marketing -> true_positive_access_expansion: 2 |
| democratizing access | 2 | generic_marketing -> operational_access_or_platform_language: 2 |
| eliminate barriers | 2 | generic_marketing -> operational_access_or_platform_language: 2 |
| inclusive financial system | 2 | true_positive_access_expansion -> generic_marketing: 2 |
| individual investors | 2 | true_positive_access_expansion -> false_positive: 1; true_positive_access_expansion -> operational_access_or_platform_language: 1 |
| institutional level | 2 | true_positive_access_expansion -> false_positive: 2 |
| lower barriers | 2 | generic_marketing -> operational_access_or_platform_language: 2 |
| reduce barriers | 2 | generic_marketing -> risk_disclosure_only: 1; generic_marketing -> operational_access_or_platform_language: 1 |
| reduced barriers | 2 | generic_marketing -> risk_disclosure_only: 1; generic_marketing -> operational_access_or_platform_language: 1 |
| remove barriers | 2 | generic_marketing -> true_positive_access_expansion: 1; generic_marketing -> operational_access_or_platform_language: 1 |
| underserved consumers | 2 | true_positive_access_expansion -> operational_access_or_platform_language: 2 |
| access to affordable housing | 1 | true_positive_access_expansion -> customer_access_unrelated_to_finance: 1 |
| access to markets | 1 | true_positive_access_expansion -> operational_access_or_platform_language: 1 |
| credit access | 1 | true_positive_access_expansion -> operational_access_or_platform_language: 1 |
| democratize financial services | 1 | true_positive_access_expansion -> operational_access_or_platform_language: 1 |
| democratized access | 1 | generic_marketing -> true_positive_access_expansion: 1 |
| expand access to credit | 1 | true_positive_access_expansion -> operational_access_or_platform_language: 1 |
| retail investors | 1 | true_positive_access_expansion -> operational_access_or_platform_language: 1 |
| unbanked populations | 1 | true_positive_access_expansion -> operational_access_or_platform_language: 1 |
| underbanked consumers | 1 | true_positive_access_expansion -> risk_disclosure_only: 1 |
| underserved populations | 1 | true_positive_access_expansion -> generic_marketing: 1 |

## True-Positive Rate By Category Under V2

| Category | Rows | V2 true positives | V2 TP rate |
| --- | --- | --- | --- |
| affordable financial products | 26 | 24 | 92.3% |
| broader market participation | 44 | 5 | 11.4% |
| democratized access | 43 | 22 | 51.2% |
| expanded access to credit | 65 | 47 | 72.3% |
| financial inclusion | 37 | 30 | 81.1% |
| homeownership access | 96 | 80 | 83.3% |
| institutional-grade access for individuals | 39 | 7 | 17.9% |
| lower barriers / level playing field | 53 | 3 | 5.7% |
| retail access to investing | 112 | 73 | 65.2% |
| underserved / underbanked / unbanked | 85 | 76 | 89.4% |

## High-Risk Phrases Still Requiring Caution

| Phrase | Rows | V2 true positives | V2 TP rate | V2 labels |
| --- | --- | --- | --- | --- |
| access to credit | 30 | 16 | 53.3% | {'risk_disclosure_only': 10, 'true_positive_access_expansion': 16, 'operational_access_or_platform_language': 3, 'ambiguous': 1} |
| access to markets | 10 | 1 | 10.0% | {'risk_disclosure_only': 2, 'operational_access_or_platform_language': 7, 'true_positive_access_expansion': 1} |
| affordable housing | 82 | 69 | 84.1% | {'false_positive': 12, 'true_positive_access_expansion': 69, 'customer_access_unrelated_to_finance': 1} |
| capital markets access | 4 | 0 | 0.0% | {'operational_access_or_platform_language': 2, 'risk_disclosure_only': 2} |
| fractional share | 32 | 0 | 0.0% | {'false_positive': 32} |
| institutional caliber | 5 | 0 | 0.0% | {'false_positive': 5} |
| institutional grade | 4 | 0 | 0.0% | {'operational_access_or_platform_language': 4} |
| institutional level | 2 | 0 | 0.0% | {'false_positive': 2} |
| institutional quality | 15 | 6 | 40.0% | {'false_positive': 6, 'operational_access_or_platform_language': 3, 'true_positive_access_expansion': 6} |
| institutional-grade | 13 | 1 | 7.7% | {'operational_access_or_platform_language': 12, 'true_positive_access_expansion': 1} |
| market access | 27 | 2 | 7.4% | {'true_positive_access_expansion': 2, 'risk_disclosure_only': 18, 'false_positive': 1, 'operational_access_or_platform_language': 5, 'customer_access_unrelated_to_finance': 1} |

## Directional Checks

- Institutional/platform/market-access phrase rows: 80
- V1 true positives in those rows: 17
- V2 true positives in those rows: 10
- V2 appears more conservative on institutional/platform/market-access language: yes
- Explicit financial-access mission phrase rows: 51
- V1 true positives in those rows: 37
- V2 true positives in those rows: 36
- V2 recovers under-called explicit financial-access mission language: mixed/no

## Recommendation

Run a second smaller audit before full-corpus scaling. The revised rules incorporate audit lessons, but v2 still depends on Codex-assisted labels for rows without manual calibration or audit coverage. A targeted 75-100 row audit should oversample changed rows, high-risk phrases, and newly positive mission-language cases before classifying all 9,400 raw hits.

## Guardrail Reminder

Treatment construction is not finalized. Returns, prices, benchmark outcomes, and empirical performance analysis remain off-limits until post-revision classification quality is checked and approved.
