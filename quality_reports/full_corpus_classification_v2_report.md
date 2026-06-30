# Full Corpus Classification V2 Report

Generated at: 2026-06-29T19:28:00.496730+00:00

## Scope And Guardrails

- Classified all rows in `data/extracted/phrase_hits.csv` under `classification_guidelines_v3.md`.
- Preserved all raw phrase-hit fields in the classified output.
- Preserved manual calibration, manual audit, and V2 validation-audit labels as label-source artifacts where their derived row-number `hit_id` matched the full corpus.
- Classification outputs are treatment-candidate construction only, not final empirical results.
- No prices, return outcomes, benchmarks, or empirical performance outcomes were loaded.
- No return analysis was run and no SEC requests were made.
- Script version: `classify_all_phrase_hits_v2`.
- Classifier version: `classification_guidelines_v3`.

## File Integrity

- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes
- Classified output SHA256: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`

## Row Counts

- Total classified rows: 9400
- Expected raw-hit count from checkpoint: 9,400
- Raw-hit count matches expected: yes
- True-positive count: 7414
- True-positive filings count: 2520
- High-risk phrase rows: 4484
- High-risk true-positive rows: 2738
- High-risk positive rate: 61.1%
- Low-confidence true positives: 0
- Review-sample artifact labels applied: 500
- V2 validation-audit labels applied: 100

## Label Distribution

| Final label V2 | Rows |
| --- | --- |
| ambiguous | 54 |
| customer_access_unrelated_to_finance | 179 |
| false_positive | 662 |
| generic_marketing | 29 |
| operational_access_or_platform_language | 514 |
| risk_disclosure_only | 548 |
| true_positive_access_expansion | 7414 |

## Confidence Distribution

| Final confidence V2 | Rows |
| --- | --- |
| high | 3825 |
| low | 52 |
| medium | 5523 |

## Label Source Distribution

| Label source V2 | Rows |
| --- | --- |
| codex_assisted_full_corpus_v2 | 8800 |
| codex_assisted_v2 | 230 |
| manual_audit | 150 |
| manual_calibration | 120 |
| v2_validation_audit | 100 |

## Label Distribution By Category

| Category | Rows | True positives | TP rate | Label distribution |
| --- | --- | --- | --- | --- |
| affordable financial products | 36 | 32 | 88.9% | ambiguous: 1; generic_marketing: 1; operational_access_or_platform_language: 2; true_positive_access_expansion: 32 |
| broader market participation | 707 | 78 | 11.0% | customer_access_unrelated_to_finance: 71; false_positive: 1; operational_access_or_platform_language: 251; risk_disclosure_only: 306; true_positive_access_expansion: 78 |
| democratized access | 55 | 23 | 41.8% | generic_marketing: 1; operational_access_or_platform_language: 28; risk_disclosure_only: 3; true_positive_access_expansion: 23 |
| expanded access to credit | 935 | 648 | 69.3% | ambiguous: 52; operational_access_or_platform_language: 5; risk_disclosure_only: 230; true_positive_access_expansion: 648 |
| financial inclusion | 319 | 309 | 96.9% | ambiguous: 1; generic_marketing: 3; operational_access_or_platform_language: 5; risk_disclosure_only: 1; true_positive_access_expansion: 309 |
| homeownership access | 2346 | 2252 | 96.0% | customer_access_unrelated_to_finance: 79; false_positive: 12; operational_access_or_platform_language: 1; risk_disclosure_only: 2; true_positive_access_expansion: 2252 |
| institutional-grade access for individuals | 165 | 80 | 48.5% | customer_access_unrelated_to_finance: 6; false_positive: 16; operational_access_or_platform_language: 63; true_positive_access_expansion: 80 |
| lower barriers / level playing field | 123 | 11 | 8.9% | customer_access_unrelated_to_finance: 22; false_positive: 1; generic_marketing: 22; operational_access_or_platform_language: 64; risk_disclosure_only: 3; true_positive_access_expansion: 11 |
| retail access to investing | 3119 | 2395 | 76.8% | false_positive: 632; operational_access_or_platform_language: 92; true_positive_access_expansion: 2395 |
| underserved / underbanked / unbanked | 1595 | 1586 | 99.4% | customer_access_unrelated_to_finance: 1; generic_marketing: 2; operational_access_or_platform_language: 3; risk_disclosure_only: 3; true_positive_access_expansion: 1586 |

## Label Distribution By Phrase

| Phrase | Rows | True positives | TP rate | Label distribution |
| --- | --- | --- | --- | --- |
| access to affordable credit | 15 | 15 | 100.0% | true_positive_access_expansion: 15 |
| access to affordable housing | 8 | 7 | 87.5% | customer_access_unrelated_to_finance: 1; true_positive_access_expansion: 7 |
| access to credit | 612 | 353 | 57.7% | ambiguous: 38; operational_access_or_platform_language: 3; risk_disclosure_only: 218; true_positive_access_expansion: 353 |
| access to homeownership | 2 | 2 | 100.0% | true_positive_access_expansion: 2 |
| access to housing | 9 | 7 | 77.8% | risk_disclosure_only: 2; true_positive_access_expansion: 7 |
| access to investing | 18 | 18 | 100.0% | true_positive_access_expansion: 18 |
| access to investment | 177 | 174 | 98.3% | operational_access_or_platform_language: 3; true_positive_access_expansion: 174 |
| access to markets | 121 | 23 | 19.0% | operational_access_or_platform_language: 68; risk_disclosure_only: 30; true_positive_access_expansion: 23 |
| affordable credit | 34 | 24 | 70.6% | ambiguous: 10; true_positive_access_expansion: 24 |
| affordable financial services | 26 | 22 | 84.6% | ambiguous: 1; generic_marketing: 1; operational_access_or_platform_language: 2; true_positive_access_expansion: 22 |
| affordable homeownership | 11 | 10 | 90.9% | operational_access_or_platform_language: 1; true_positive_access_expansion: 10 |
| affordable housing | 2313 | 2223 | 96.1% | customer_access_unrelated_to_finance: 78; false_positive: 12; true_positive_access_expansion: 2223 |
| affordable loans | 7 | 7 | 100.0% | true_positive_access_expansion: 7 |
| broader participation | 6 | 2 | 33.3% | operational_access_or_platform_language: 2; risk_disclosure_only: 2; true_positive_access_expansion: 2 |
| capital markets access | 32 | 0 | 0.0% | customer_access_unrelated_to_finance: 3; operational_access_or_platform_language: 10; risk_disclosure_only: 19 |
| credit access | 94 | 79 | 84.0% | ambiguous: 4; operational_access_or_platform_language: 1; risk_disclosure_only: 10; true_positive_access_expansion: 79 |
| democratize access | 8 | 8 | 100.0% | true_positive_access_expansion: 8 |
| democratize finance | 13 | 2 | 15.4% | generic_marketing: 1; operational_access_or_platform_language: 10; true_positive_access_expansion: 2 |
| democratize financial services | 4 | 2 | 50.0% | operational_access_or_platform_language: 2; true_positive_access_expansion: 2 |
| democratized access | 9 | 4 | 44.4% | operational_access_or_platform_language: 2; risk_disclosure_only: 3; true_positive_access_expansion: 4 |
| democratizing access | 8 | 4 | 50.0% | operational_access_or_platform_language: 4; true_positive_access_expansion: 4 |
| democratizing finance | 1 | 1 | 100.0% | true_positive_access_expansion: 1 |
| democratizing financial services | 12 | 2 | 16.7% | operational_access_or_platform_language: 10; true_positive_access_expansion: 2 |
| eliminate barriers | 8 | 0 | 0.0% | customer_access_unrelated_to_finance: 2; generic_marketing: 3; operational_access_or_platform_language: 3 |
| eliminating barriers | 5 | 0 | 0.0% | customer_access_unrelated_to_finance: 5 |
| expand access to credit | 161 | 158 | 98.1% | operational_access_or_platform_language: 1; risk_disclosure_only: 2; true_positive_access_expansion: 158 |
| expanded access to credit | 7 | 7 | 100.0% | true_positive_access_expansion: 7 |
| expanding access to credit | 12 | 12 | 100.0% | true_positive_access_expansion: 12 |
| expanding homeownership | 3 | 3 | 100.0% | true_positive_access_expansion: 3 |
| financial inclusion | 314 | 307 | 97.8% | ambiguous: 1; generic_marketing: 1; operational_access_or_platform_language: 4; risk_disclosure_only: 1; true_positive_access_expansion: 307 |
| fractional share | 631 | 1 | 0.2% | false_positive: 630; true_positive_access_expansion: 1 |
| improve financial inclusion | 1 | 1 | 100.0% | true_positive_access_expansion: 1 |
| inclusive financial system | 2 | 0 | 0.0% | generic_marketing: 2 |
| individual investors | 1090 | 1055 | 96.8% | false_positive: 2; operational_access_or_platform_language: 33; true_positive_access_expansion: 1055 |
| institutional caliber | 12 | 7 | 58.3% | false_positive: 5; true_positive_access_expansion: 7 |
| institutional grade | 14 | 1 | 7.1% | customer_access_unrelated_to_finance: 1; false_positive: 1; operational_access_or_platform_language: 11; true_positive_access_expansion: 1 |
| institutional level | 2 | 0 | 0.0% | false_positive: 2 |
| institutional quality | 68 | 57 | 83.8% | customer_access_unrelated_to_finance: 1; false_positive: 6; operational_access_or_platform_language: 4; true_positive_access_expansion: 57 |
| institutional-grade | 69 | 15 | 21.7% | customer_access_unrelated_to_finance: 4; false_positive: 2; operational_access_or_platform_language: 48; true_positive_access_expansion: 15 |
| level playing field | 31 | 0 | 0.0% | generic_marketing: 5; operational_access_or_platform_language: 26 |
| low-cost financial services | 3 | 3 | 100.0% | true_positive_access_expansion: 3 |
| lower barriers | 16 | 3 | 18.8% | customer_access_unrelated_to_finance: 1; operational_access_or_platform_language: 11; risk_disclosure_only: 1; true_positive_access_expansion: 3 |
| market access | 548 | 53 | 9.7% | customer_access_unrelated_to_finance: 68; false_positive: 1; operational_access_or_platform_language: 171; risk_disclosure_only: 255; true_positive_access_expansion: 53 |
| promote financial inclusion | 2 | 1 | 50.0% | operational_access_or_platform_language: 1; true_positive_access_expansion: 1 |
| reduce barriers | 11 | 0 | 0.0% | generic_marketing: 8; operational_access_or_platform_language: 2; risk_disclosure_only: 1 |
| reduced barriers | 15 | 3 | 20.0% | customer_access_unrelated_to_finance: 1; generic_marketing: 4; operational_access_or_platform_language: 6; risk_disclosure_only: 1; true_positive_access_expansion: 3 |
| reducing barriers | 4 | 0 | 0.0% | customer_access_unrelated_to_finance: 1; false_positive: 1; operational_access_or_platform_language: 2 |
| remove barriers | 7 | 5 | 71.4% | operational_access_or_platform_language: 2; true_positive_access_expansion: 5 |
| removing barriers | 26 | 0 | 0.0% | customer_access_unrelated_to_finance: 12; generic_marketing: 2; operational_access_or_platform_language: 12 |
| retail access | 2 | 2 | 100.0% | true_positive_access_expansion: 2 |
| retail investors | 1201 | 1145 | 95.3% | operational_access_or_platform_language: 56; true_positive_access_expansion: 1145 |
| unbanked | 124 | 124 | 100.0% | true_positive_access_expansion: 124 |
| unbanked consumers | 3 | 3 | 100.0% | true_positive_access_expansion: 3 |
| unbanked populations | 7 | 6 | 85.7% | operational_access_or_platform_language: 1; true_positive_access_expansion: 6 |
| underbanked | 123 | 123 | 100.0% | true_positive_access_expansion: 123 |
| underbanked consumers | 27 | 26 | 96.3% | risk_disclosure_only: 1; true_positive_access_expansion: 26 |
| underserved | 834 | 832 | 99.8% | customer_access_unrelated_to_finance: 1; generic_marketing: 1; true_positive_access_expansion: 832 |
| underserved borrowers | 40 | 39 | 97.5% | risk_disclosure_only: 1; true_positive_access_expansion: 39 |
| underserved communities | 187 | 187 | 100.0% | true_positive_access_expansion: 187 |
| underserved consumers | 135 | 132 | 97.8% | operational_access_or_platform_language: 2; risk_disclosure_only: 1; true_positive_access_expansion: 132 |
| underserved markets | 98 | 98 | 100.0% | true_positive_access_expansion: 98 |
| underserved populations | 17 | 16 | 94.1% | generic_marketing: 1; true_positive_access_expansion: 16 |

## Label Distribution By Section

| Section | Rows | True positives | TP rate | Label distribution |
| --- | --- | --- | --- | --- |
| Item 1 Business | 4990 | 4175 | 83.7% | ambiguous: 37; customer_access_unrelated_to_finance: 131; false_positive: 275; generic_marketing: 12; operational_access_or_platform_language: 349; risk_disclosure_only: 11; true_positive_access_expansion: 4175 |
| Item 1A Risk Factors | 2074 | 1306 | 63.0% | ambiguous: 1; customer_access_unrelated_to_finance: 9; false_positive: 153; generic_marketing: 13; operational_access_or_platform_language: 115; risk_disclosure_only: 477; true_positive_access_expansion: 1306 |
| Item 7 MD&A | 2336 | 1933 | 82.7% | ambiguous: 16; customer_access_unrelated_to_finance: 39; false_positive: 234; generic_marketing: 4; operational_access_or_platform_language: 50; risk_disclosure_only: 60; true_positive_access_expansion: 1933 |

## Label Distribution By Filing Year

| Filing year | Rows | True positives | TP rate | Label distribution |
| --- | --- | --- | --- | --- |
| 2015 | 624 | 525 | 84.1% | ambiguous: 5; customer_access_unrelated_to_finance: 13; false_positive: 22; generic_marketing: 2; operational_access_or_platform_language: 18; risk_disclosure_only: 39; true_positive_access_expansion: 525 |
| 2016 | 578 | 489 | 84.6% | ambiguous: 3; customer_access_unrelated_to_finance: 7; false_positive: 18; generic_marketing: 1; operational_access_or_platform_language: 23; risk_disclosure_only: 37; true_positive_access_expansion: 489 |
| 2017 | 598 | 492 | 82.3% | ambiguous: 3; customer_access_unrelated_to_finance: 10; false_positive: 18; generic_marketing: 1; operational_access_or_platform_language: 33; risk_disclosure_only: 41; true_positive_access_expansion: 492 |
| 2018 | 634 | 522 | 82.3% | ambiguous: 1; customer_access_unrelated_to_finance: 9; false_positive: 33; operational_access_or_platform_language: 33; risk_disclosure_only: 36; true_positive_access_expansion: 522 |
| 2019 | 690 | 552 | 80.0% | ambiguous: 3; customer_access_unrelated_to_finance: 13; false_positive: 43; generic_marketing: 4; operational_access_or_platform_language: 32; risk_disclosure_only: 43; true_positive_access_expansion: 552 |
| 2020 | 698 | 552 | 79.1% | ambiguous: 4; customer_access_unrelated_to_finance: 13; false_positive: 57; generic_marketing: 3; operational_access_or_platform_language: 32; risk_disclosure_only: 37; true_positive_access_expansion: 552 |
| 2021 | 759 | 579 | 76.3% | ambiguous: 3; customer_access_unrelated_to_finance: 14; false_positive: 56; generic_marketing: 5; operational_access_or_platform_language: 37; risk_disclosure_only: 65; true_positive_access_expansion: 579 |
| 2022 | 1055 | 786 | 74.5% | ambiguous: 9; customer_access_unrelated_to_finance: 26; false_positive: 103; generic_marketing: 4; operational_access_or_platform_language: 62; risk_disclosure_only: 65; true_positive_access_expansion: 786 |
| 2023 | 1283 | 1001 | 78.0% | ambiguous: 6; customer_access_unrelated_to_finance: 26; false_positive: 105; generic_marketing: 4; operational_access_or_platform_language: 80; risk_disclosure_only: 61; true_positive_access_expansion: 1001 |
| 2024 | 1264 | 983 | 77.8% | ambiguous: 8; customer_access_unrelated_to_finance: 26; false_positive: 108; generic_marketing: 2; operational_access_or_platform_language: 78; risk_disclosure_only: 59; true_positive_access_expansion: 983 |
| 2025 | 1217 | 933 | 76.7% | ambiguous: 9; customer_access_unrelated_to_finance: 22; false_positive: 99; generic_marketing: 3; operational_access_or_platform_language: 86; risk_disclosure_only: 65; true_positive_access_expansion: 933 |

## High-Risk Phrase Counts And Positive Rates

| Phrase | Rows | True positives | TP rate | Label distribution |
| --- | --- | --- | --- | --- |
| access to credit | 612 | 353 | 57.7% | ambiguous: 38; operational_access_or_platform_language: 3; risk_disclosure_only: 218; true_positive_access_expansion: 353 |
| access to markets | 121 | 23 | 19.0% | operational_access_or_platform_language: 68; risk_disclosure_only: 30; true_positive_access_expansion: 23 |
| affordable housing | 2313 | 2223 | 96.1% | customer_access_unrelated_to_finance: 78; false_positive: 12; true_positive_access_expansion: 2223 |
| capital markets access | 32 | 0 | 0.0% | customer_access_unrelated_to_finance: 3; operational_access_or_platform_language: 10; risk_disclosure_only: 19 |
| eliminate barriers | 8 | 0 | 0.0% | customer_access_unrelated_to_finance: 2; generic_marketing: 3; operational_access_or_platform_language: 3 |
| fractional share | 631 | 1 | 0.2% | false_positive: 630; true_positive_access_expansion: 1 |
| institutional caliber | 12 | 7 | 58.3% | false_positive: 5; true_positive_access_expansion: 7 |
| institutional level | 2 | 0 | 0.0% | false_positive: 2 |
| institutional quality | 68 | 57 | 83.8% | customer_access_unrelated_to_finance: 1; false_positive: 6; operational_access_or_platform_language: 4; true_positive_access_expansion: 57 |
| institutional-grade | 69 | 15 | 21.7% | customer_access_unrelated_to_finance: 4; false_positive: 2; operational_access_or_platform_language: 48; true_positive_access_expansion: 15 |
| lower barriers | 16 | 3 | 18.8% | customer_access_unrelated_to_finance: 1; operational_access_or_platform_language: 11; risk_disclosure_only: 1; true_positive_access_expansion: 3 |
| market access | 548 | 53 | 9.7% | customer_access_unrelated_to_finance: 68; false_positive: 1; operational_access_or_platform_language: 171; risk_disclosure_only: 255; true_positive_access_expansion: 53 |
| reduce barriers | 11 | 0 | 0.0% | generic_marketing: 8; operational_access_or_platform_language: 2; risk_disclosure_only: 1 |
| reduced barriers | 15 | 3 | 20.0% | customer_access_unrelated_to_finance: 1; generic_marketing: 4; operational_access_or_platform_language: 6; risk_disclosure_only: 1; true_positive_access_expansion: 3 |
| removing barriers | 26 | 0 | 0.0% | customer_access_unrelated_to_finance: 12; generic_marketing: 2; operational_access_or_platform_language: 12 |

## Top Firms By Classified True-Positive Count

| Firm ID | Ticker | CIK | True-positive rows |
| --- | --- | --- | --- |
| CIK0001041514 | LSAK | 0001041514 | 288 |
| CIK0001497770 | WD | 0001497770 | 230 |
| CIK0001289419 | MORN | 0001289419 | 173 |
| CIK0001128361 | HOPE | 0001128361 | 172 |
| CIK0001393818 | BX | 0001393818 | 154 |
| CIK0000005272 | AIG | 0000005272 | 136 |
| CIK0001404912 | KKR | 0001404912 | 121 |
| CIK0001059142 | GHI | 0001059142 | 119 |
| CIK0001069157 | EWBC | 0001069157 | 101 |
| CIK0001281761 | RF | 0001281761 | 92 |
| CIK0000316709 | SCHW | 0000316709 | 87 |
| CIK0001535929 | VOYA | 0001535929 | 86 |
| CIK0001381197 | IBKR | 0001381197 | 81 |
| CIK0001818502 | OPFI | 0001818502 | 73 |
| CIK0001775734 | BENF | 0001775734 | 71 |
| CIK0000861842 | CATY | 0000861842 | 67 |
| CIK0001889539 | CRBD | 0001889539 | 67 |
| CIK0001527166 | CG | 0001527166 | 66 |
| CIK0001529864 | ENVA | 0001529864 | 65 |
| CIK0001409970 | LC | 0001409970 | 65 |
| CIK0001464343 | ATLC | 0001464343 | 64 |
| CIK0000798941 | FCNCA | 0000798941 | 62 |
| CIK0001587987 | NEWT | 0001587987 | 61 |
| CIK0001127703 | PRA | 0001127703 | 61 |
| CIK0001141391 | MA | 0001141391 | 57 |

## Top Phrases Driving True Positives

| Phrase | True-positive rows |
| --- | --- |
| affordable housing | 2223 |
| retail investors | 1145 |
| individual investors | 1055 |
| underserved | 832 |
| access to credit | 353 |
| financial inclusion | 307 |
| underserved communities | 187 |
| access to investment | 174 |
| expand access to credit | 158 |
| underserved consumers | 132 |
| unbanked | 124 |
| underbanked | 123 |
| underserved markets | 98 |
| credit access | 79 |
| institutional quality | 57 |
| market access | 53 |
| underserved borrowers | 39 |
| underbanked consumers | 26 |
| affordable credit | 24 |
| access to markets | 23 |
| affordable financial services | 22 |
| access to investing | 18 |
| underserved populations | 16 |
| institutional-grade | 15 |
| access to affordable credit | 15 |

## Recommended Post-Scale Spot Checks

- Audit high-risk phrase positives, especially `affordable housing`, market-access phrases, `access to credit`, institutional-quality phrases, `fractional share`, and barrier-reduction phrases.
- Audit low-confidence true positives and a small sample of medium-confidence positives from each category.
- Review firms with the largest true-positive counts for repeated boilerplate or section-extraction artifacts.
- Review phrases with unusually high true-positive concentration before constructing filing-level treatment variables.
- Confirm that validation-source rows remain locked before any downstream treatment-variable build.

## Guardrail Warning

No return outcomes, prices, benchmark returns, or empirical performance data have been loaded. This report makes no empirical performance claims and should not be used as a return-analysis result.
