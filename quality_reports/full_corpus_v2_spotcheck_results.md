# Full Corpus V2 Spot-Check Results

Generated at: 2026-06-29T19:38:43.362270+00:00

## Scope And Guardrails

- Manually audited the 150-row full-corpus V2 spot-check sample using only excerpts and `classification_guidelines_v3.md`.
- Did not use returns, prices, later news, outside firm knowledge, litigation, bankruptcies, acquisitions, or external events.
- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.
- Raw `phrase_hits.csv` and classified `phrase_hits_classified_v2.csv` were not modified.

## File Integrity

- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes
- Classified `phrase_hits_classified_v2.csv` SHA256 before: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- Classified `phrase_hits_classified_v2.csv` SHA256 after: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- Classified file unchanged: yes

## Full Corpus Counts

- Full classified row count: 9400
- Full-corpus true-positive row count: 7414
- Full-corpus true-positive filing count: 2520

## Spot-Check Counts

- Spot-check sample size: 150
- Sampled full-corpus positives: 100
- Sampled full-corpus non-positives: 50
- Spot-check fields filled: 150

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

## Agreement Metrics

- Total disagreements: 59 / 150 (39.3%)
- True-positive precision among sampled full-corpus positives: 55 / 100 (55.0%)
- False-negative rate among sampled full-corpus non-positives: 6 / 50 (12.0%)

## Disagreement Counts By Phrase

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
| affordable credit | 1 |
| capital markets access | 1 |
| financial inclusion | 1 |
| retail investors | 1 |
| underserved | 1 |

## Disagreement Counts By Category

| Category | Disagreements |
| --- | --- |
| homeownership access | 29 |
| institutional-grade access for individuals | 12 |
| broader market participation | 7 |
| expanded access to credit | 4 |
| retail access to investing | 3 |
| lower barriers / level playing field | 2 |
| financial inclusion | 1 |
| underserved / underbanked / unbanked | 1 |

## Disagreement Examples

| Sample row | Ticker | Phrase | Final V2 label | Spot-check label | Spot-check note | Excerpt start |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | AB | access to credit | true_positive_access_expansion | risk_disclosure_only | Issuer credit ratings and own access to credit, not external borrower access. | market conditions, our profitability, our creditworthiness as perceived by lenders and changes in government regulations, including tax rates and interest rates. Furthermore, our a |
| 3 | ABTC | capital markets access | customer_access_unrelated_to_finance | operational_access_or_platform_language | Capital markets access supports issuer growth strategy, not external access-oriented activity. | ients with integrated security, transparency, and scalability capabilities, all while maintaining compliance with their governing regulations. We intend to leverage our scale and c |
| 5 | AIG | affordable housing | true_positive_access_expansion | false_positive | Affordable housing appears as portfolio return/investment-income context. | gains on securities for which the fair value option was elected, and income from an initial public offering of a holding in the private equity portfolio, partially offset by lower  |
| 6 | AIG | affordable housing | true_positive_access_expansion | false_positive | Affordable Housing is a sold portfolio/accounting item. | tributable to AIG common shareholders increased $15.3 billion due to the following, on a pre-tax basis:  the recognition of a $3.0 billion gain on the closing of the sale of the A |
| 7 | AIG | affordable housing | true_positive_access_expansion | false_positive | Affordable Housing is referenced as sale-related expense/accounting context. | hstone. Partially offset by: •net favorable impact from the review and update of actuarial assumptions ($184 million); •lower interest expense on debt borrowings due to sale of Aff |
| 8 | ASRV | affordable housing | customer_access_unrelated_to_finance | true_positive_access_expansion | Affordable housing programs are for low-to-moderate-income families. | nt and leadership while fostering a positive corporate image. This will be accomplished by demonstrating our commitment to the communities we serve through assistance in providing  |
| 16 | BKKT | institutional-grade | true_positive_access_expansion | operational_access_or_platform_language | Institutional-grade platform and partner services lack external retail access in excerpt. | ontents and a number of key partnerships in 2021 furthered our payments and consumer crypto offerings. We have thoughtfully built a unique and powerful platform, melding together i |
| 18 | BKKT | institutional-grade | true_positive_access_expansion | operational_access_or_platform_language | Institutional-grade custodian describes custody infrastructure. | ”), our controlling shareholder prior to the Business Combination, has decades of experience building institutional products and solutions. We leveraged that expertise to build an  |
| 20 | BKKT | institutional-grade | customer_access_unrelated_to_finance | operational_access_or_platform_language | Institutional-grade custody/trading platform is operational platform quality. | ation with dozens of suppliers and millions of items, both through a mobile-first responsive web app or integrated into clients’ apps or sites. •Our crypto products operate in an i |
| 22 | BMRC | market access | true_positive_access_expansion | risk_disclosure_only | Competitors' capital-market access appears in competitive risk context. | itions and they may be able to benefit from economies of scale through their wider branch networks, more prominent national advertising campaigns, lower cost of borrowing, capital  |
| 23 | BMRC | market access | true_positive_access_expansion | risk_disclosure_only | Competitors' capital-market access appears in competitive risk context. | itions and they may be able to benefit from economies of scale through their wider branch networks, more prominent national advertising campaigns, lower cost of borrowing, capital  |
| 29 | BMNP | eliminate barriers | generic_marketing | operational_access_or_platform_language | Digital-assets bill is regulatory background, not end-user access-oriented disclosure. | apable of being implemented under the current state of the markets for exchange traded funds. On April 20, 2021, the U.S. House of Representatives passed a bipartisan bill titled “ |
| 31 | BXMT | institutional quality | true_positive_access_expansion | false_positive | Institutional quality describes commercial real estate assets. | re detail on the terms of the Management Agreement. Our Investment Strategy Our investment strategy is to originate loans and invest in debt and related instruments supported by in |
| 32 | BXMT | institutional quality | true_positive_access_expansion | false_positive | Institutional quality describes assets and sponsors. | ments as of December 31, 2021, with a weighted-average origination loan-to-value ratio of 64.4% and weighted-average all-in yield of + 3.54%. •Maintained our disciplined focus on i |
| 33 | BXMT | institutional quality | true_positive_access_expansion | false_positive | Institutional quality describes commercial real estate assets. | re detail on the terms of the Management Agreement. Our Investment Strategy Our investment strategy is to originate loans and invest in debt and related instruments supported by in |

## Decision Rule Result

- Precision threshold met: no
- False-negative threshold exceeded: no
- Recommendation: Revise classification rules before treatment-variable construction.

## Accuracy Assessment For Treatment-Candidate Construction

The sampled full-corpus V2 positives do not meet the 85% precision threshold in this high-risk post-scale spot check. Full-corpus V2 should not be used directly for treatment-variable construction until classification rules are revised and the affected rows are reclassified or filtered.

## Specific Remaining Cautions

- `affordable housing` has many false positives in tax-credit, portfolio, investment-income, sale, and accounting contexts.
- Institutional-quality phrases still over-call property quality, analyst-process quality, custody infrastructure, and services to institutional/HNW clients.
- Some `access to credit` positives describe issuer funding or credit facilities rather than external borrowers.
- Some market-access positives describe issuer or prime-broker operational access rather than customer, investor, borrower, or smaller-issuer access.
- A small number of non-positive rows appear under-called where excerpts describe external financial-market or credit access.
- Returns, prices, benchmark outcomes, and empirical performance analysis remain off-limits until treatment construction is complete and approved.
