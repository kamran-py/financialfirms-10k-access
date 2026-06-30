# Codex-Assisted Label Audit Results

Generated at: 2026-06-29

## Scope

- Audited 150 Codex-assisted review-sample rows.
- No manual calibration rows were included.
- No prices, return outcomes, SEC requests, later news, or external firm events were used.
- Raw `phrase_hits.csv` was not modified.

## Validation

- Audit rows: 150
- Blank audit labels: 0
- Raw `phrase_hits.csv` hash before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` hash after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes

## Label Counts

| Label | Final pre-audit | Audit |
| --- | ---: | ---: |
| ambiguous | 4 | 0 |
| customer_access_unrelated_to_finance | 0 | 2 |
| false_positive | 4 | 16 |
| generic_marketing | 23 | 4 |
| operational_access_or_platform_language | 14 | 35 |
| risk_disclosure_only | 5 | 11 |
| true_positive_access_expansion | 100 | 82 |

## Agreement

- Total label disagreements: 64 / 150 (42.7%)
- Codex-assisted true-positive precision in audited positive sample: 67 / 100 (67.0%)
- Positive audit labels among audited non-positive rows: 15 / 50 (30.0%)

## Category Audit Counts

| Category | true_positive_access_expansion | risk_disclosure_only | operational_access_or_platform_language | false_positive | customer_access_unrelated_to_finance | generic_marketing | ambiguous |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| affordable financial products | 8 | 0 | 0 | 0 | 0 | 0 | 0 |
| broader market participation | 3 | 3 | 4 | 0 | 0 | 0 | 0 |
| democratized access | 13 | 0 | 2 | 0 | 0 | 1 | 0 |
| expanded access to credit | 18 | 3 | 4 | 0 | 0 | 0 | 0 |
| financial inclusion | 3 | 0 | 0 | 0 | 0 | 2 | 0 |
| homeownership access | 10 | 2 | 0 | 3 | 0 | 0 | 0 |
| institutional-grade access for individuals | 1 | 0 | 7 | 8 | 0 | 0 | 0 |
| lower barriers / level playing field | 2 | 2 | 13 | 0 | 2 | 0 | 0 |
| retail access to investing | 7 | 0 | 2 | 5 | 0 | 0 | 0 |
| underserved / underbanked / unbanked | 17 | 1 | 3 | 0 | 0 | 1 | 0 |

## Highest-Disagreement Phrases

| Phrase | Disagreements |
| --- | ---: |
| institutional caliber | 5 |
| institutional quality | 3 |
| affordable housing | 3 |
| access to credit | 3 |
| institutional-grade | 3 |
| eliminate barriers | 2 |
| reduce barriers | 2 |
| access to investment | 2 |
| removing barriers | 2 |
| access to affordable credit | 2 |
| eliminating barriers | 2 |
| broader participation | 2 |
| democratizing access | 2 |
| affordable loans | 2 |
| inclusive financial system | 2 |
| institutional level | 2 |
| underserved consumers | 2 |
| democratize access | 2 |
| affordable financial services | 2 |
| affordable credit | 2 |

## Research Design Implications

- Codex-assisted labels are usable but not clean enough to scale without rule revisions.
- The main over-call risk remains true-positive labels for issuer/operational access, regulatory boilerplate, and institutional-quality/platform language.
- The main under-call risk is generic labels assigned to explicit financial-access mission language, especially payments, SMB commerce, and affordable/low-cost credit products.
- Future treatment construction should use audited/classified true positives, not raw phrase hits.
- No return analysis should begin until the full-corpus classifier is revised using this audit and then revalidated.
