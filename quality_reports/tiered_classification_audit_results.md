# Tiered Classification Audit Results

Generated at: 2026-06-29T20:14:18.896792+00:00

## Scope And Guardrails

- Manually audited the post-tiered classification sample using only excerpts and tiered classification guidelines.
- Did not modify `data/extracted/phrase_hits.csv`.
- Did not modify `data/classified/phrase_hits_tiered_v1.csv`.
- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.
- These results validate text-treatment candidates only; they are not return or performance results.

## File Integrity

- Raw `phrase_hits.csv` SHA256: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Tiered classified SHA256: `c647e1d0acc4498d40426388e8f7046b664e7fee6eca3ffc817ddb50707159df`

## Full-Corpus Counts

- Total tiered classified rows: 9400
- Full-corpus Tier 1 rows: 725
- Full-corpus Tier 2 rows: 1292
- Full-corpus Tier 3 rows: 1571
- Full-corpus excluded rows: 5812

## Audit Sample Counts

- Audit sample size: 150
| Original tiered label | Rows |
| --- | ---: |
| tier_1_conservative | 75 |
| tier_2_broader_validated | 50 |
| excluded_non_treatment | 25 |

## Label Counts After Audit

| Audit tiered label | Rows |
| --- | ---: |
| tier_2_broader_validated | 67 |
| excluded_non_treatment | 59 |
| tier_1_conservative | 22 |
| tier_3_exploratory | 2 |

## Decision Metrics

- Tier 1 precision among sampled Tier 1 rows: 17 / 75 = 22.7%
- Tier 2 candidate precision among sampled Tier 2 rows: 34 / 50 = 68.0%
- Tier 2 exact-label agreement among sampled Tier 2 rows: 31 / 50 = 62.0%
- Excluded false-negative rate for Tier 1/Tier 2 treatment candidates: 10 / 25 = 40.0%
- Excluded broad-signal miss rate including Tier 3: 10 / 25 = 40.0%
- Overall disagreement rate: 87 / 150 = 58.0%

Interpretation of Tier 2 precision: counted as precise when the audit label remained a validated treatment candidate (`tier_1_conservative` or `tier_2_broader_validated`). Promotions from Tier 2 to Tier 1 count as candidate-precision successes but remain label disagreements.

## Disagreement Counts By Phrase

| Phrase | Disagreements |
| --- | ---: |
| underserved markets | 12 |
| unbanked | 12 |
| underserved borrowers | 11 |
| affordable housing | 9 |
| retail investors | 9 |
| access to credit | 5 |
| underserved communities | 5 |
| market access | 5 |
| expand access to credit | 4 |
| fractional share | 4 |
| individual investors | 3 |
| underbanked | 2 |
| affordable homeownership | 1 |
| democratizing finance | 1 |
| underserved consumers | 1 |
| financial inclusion | 1 |
| democratized access | 1 |
| removing barriers | 1 |

## Disagreement Counts By Phrase Family

| High-risk phrase family | Disagreements |
| --- | ---: |
| risk-section access language | 27 |
| CRA/regulatory language | 17 |
| CRA/regulatory language; risk-section access language | 11 |
| affordable housing | 8 |
| none | 8 |
| market access / access to markets / capital markets access; risk-section access language | 4 |
| access to credit | 3 |
| access to credit; risk-section access language | 2 |
| fractional share | 2 |
| fractional share; risk-section access language | 2 |
| affordable housing; risk-section access language | 1 |
| market access / access to markets / capital markets access | 1 |
| lower/reduce/remove/eliminate barriers | 1 |

## Disagreement Counts By Original Narrative Subcategory

| Original narrative subcategory | Disagreements |
| --- | ---: |
| financial inclusion / underbanked / underserved | 30 |
| consumer credit access | 23 |
| affordable housing / homeownership access | 10 |
| excluded / non-treatment | 10 |
| retail investing / brokerage democratization | 6 |
| smaller-issuer capital-market access | 5 |
| generic/other access-oriented disclosure | 2 |
| insurance / benefits access | 1 |

## Disagreement Examples

| Row | Ticker | Year | Phrase | Original label | Audit label | Audit note | Excerpt |
| ---: | --- | ---: | --- | --- | --- | --- | --- |
| 1 | EWBC | 2023 | affordable housing | tier_1_conservative | tier_2_broader_validated | Access-related community programs, but direct financial mechanism is broad rather than Tier 1 explicit. | unteer and charitable efforts. We aim to enhance the quality of life in our communities by engaging in meaningful and effective programs that help increase homeownership, preserve affordable housing, promote wealth build |
| 4 | ICE | 2019 | underserved markets | tier_1_conservative | excluded_non_treatment | Underserved markets refers to issuer acquisition/growth rationale, not external financial-access activity. | including leveraging our existing strengths to enter new markets in our industry or related industries, expanding our products and services, diversifying our business, addressing underserved markets, advancing our techno |
| 7 | LC | 2017 | underserved borrowers | tier_1_conservative | tier_2_broader_validated | Regulatory RFI discusses marketplace lending access for underserved borrowers; clear mechanism but not issuer-specific Tier 1 action. | I) to study the various business models and products offered by online marketplace lenders, the potential for online marketplace lending to expand access to credit to historically underserved borrowers and how the financ |
| 8 | FNB | 2018 | access to credit | tier_1_conservative | tier_2_broader_validated | Legislative access-to-credit context is substantive but regulatory rather than issuer-specific Tier 1 action. | h would have a similar, but more targeted, impact on the banking and financial services regulatory framework. The Senate legislation is focused more narrowly on improving consumer access to credit, providing regulatory r |
| 9 | GHI | 2025 | affordable housing | tier_1_conservative | tier_2_broader_validated | Affordable-housing language is in qualifying-activity/regulatory context; beneficiary and mechanism are present but not Tier 1 issuer action. | mall businesses or small farms with gross annual revenues of $250,000 or less; (6) directly facilitates the acquisition, construction, development, preservation, or improvement of affordable housing in High Opportunity A |
| 10 | ICE | 2025 | underserved markets | tier_1_conservative | excluded_non_treatment | Underserved markets is issuer market-entry and product-expansion language without external beneficiary access mechanism. | onal reasons, including leveraging our existing strengths to enter new markets or related asset classes, expanding our products and services, diversifying our business, addressing underserved markets, advancing our techn |
| 11 | LC | 2016 | expand access to credit | tier_1_conservative | tier_2_broader_validated | RFI language names underserved borrowers and credit access but is regulatory context, not Tier 1 issuer action. | the U.S. Treasury Department issued an RFI to study the various business models and products offered by online marketplace lenders, the potential for online marketplace lending to expand access to credit to historically  |
| 12 | LC | 2017 | expand access to credit | tier_1_conservative | tier_2_broader_validated | RFI language names underserved borrowers and credit access but is regulatory context, not Tier 1 issuer action. | nt) issued a request for information (RFI) to study the various business models and products offered by online marketplace lenders, the potential for online marketplace lending to expand access to credit to historically  |
| 14 | LC | 2016 | underserved borrowers | tier_1_conservative | tier_2_broader_validated | Regulatory RFI discusses borrower access to credit; substantive but not issuer-specific Tier 1 action. | I) to study the various business models and products offered by online marketplace lenders, the potential for online marketplace lending to expand access to credit to historically underserved borrowers and how the financ |
| 15 | LSAK | 2017 | unbanked | tier_1_conservative | excluded_non_treatment | Risk discussion describes competitor banks targeting the unbanked, not the issuer expanding access. | segment, which could limit growth in our transaction-based activities segment. Certain South African banks have also developed their own low-cost banking products targeted at the unbanked and under-banked market segment. |
| 16 | LSAK | 2018 | unbanked | tier_1_conservative | excluded_non_treatment | Risk discussion describes competitor banks targeting the unbanked, not the issuer expanding access. | segment, which could limit growth in our transaction-based activities segment. Certain South African banks have also developed their own low-cost banking products targeted at the unbanked and under-banked market segment. |
| 17 | LSAK | 2019 | unbanked | tier_1_conservative | excluded_non_treatment | Risk discussion describes competition in the unbanked segment rather than issuer access-oriented activity. | tional damage if our service levels are negatively impacted due to the unavailability of cash. We face competition from the incumbent retail banks in South Africa and SAPO in the unbanked market segment, which could limi |
| 18 | LSAK | 2020 | unbanked | tier_1_conservative | excluded_non_treatment | Risk discussion describes competitor low-cost products for unbanked users, not issuer action. | Africa and SAPO in the unbanked market segment, which could limit our growth. Certain South African banks have also developed their own low-cost banking products targeted at the unbanked and underbanked market segment. A |
| 19 | ICE | 2021 | underserved markets | tier_1_conservative | excluded_non_treatment | Underserved markets refers to issuer acquisition/growth rationale without direct external access mechanism. | onal reasons, including leveraging our existing strengths to enter new markets or related asset classes, expanding our products and services, diversifying our business, addressing underserved markets, advancing our techn |
| 21 | MTG | 2023 | underserved borrowers | tier_1_conservative | tier_2_broader_validated | GSE plan lowers mortgage-insurance costs for underserved borrowers; substantive but not issuer-specific Tier 1 action. | and policies. Specifically relating to mortgage insurance, (1) Fannie Mae’s Plan contemplates the creation of special purchase credit program(s) ("SPCPs") targeted to historically underserved borrowers with a goal of low |
| 22 | MTG | 2024 | underserved borrowers | tier_1_conservative | tier_2_broader_validated | GSE special-purpose credit program context is access-related but not issuer-specific Tier 1 action. | ices and policies. Specifically relating to mortgage insurance, (1) Fannie Mae’s Plan includes the creation of special purpose credit program(s) ("SPCPs") targeted to historically underserved borrowers with a goal of low |
| 23 | OPRT | 2025 | underserved borrowers | tier_1_conservative | excluded_non_treatment | Excerpt is competitor/risk discussion about firms focused on underserved borrowers, not issuer access-oriented activity. | onsumers who do not have access to mainstream credit, including online marketplace lenders, point-of-sale lending, payday lenders, and auto title lenders and pawn shops focused on underserved borrowers. We may compete wi |
| 24 | LSAK | 2016 | unbanked | tier_1_conservative | excluded_non_treatment | Risk discussion describes competitor banks targeting the unbanked, not issuer access-oriented activity. | segment, which could limit growth in our transaction-based activities segment. Certain South African banks have also developed their own low-cost banking products targeted at the unbanked and under-banked market segment. |
| 25 | LC | 2016 | expand access to credit | tier_1_conservative | tier_2_broader_validated | RFI language names underserved borrowers and credit access but is regulatory context. | ent issued a request for information (RFI) to study the various business models and products offered by online marketplace lenders, the potential for online marketplace lending to expand access to credit to historically  |
| 26 | RDN | 2021 | affordable homeownership | tier_1_conservative | tier_2_broader_validated | Policy/GSE context supports homeownership access for LMI borrowers but lacks issuer-specific Tier 1 action. | es set forth in the Biden Administration’s housing plan. These changes may include a less restrictive, more expansionary approach to the GSEs in order to provide broader access to affordable homeownership for low- and mo |

## Decision Rule Assessment

- Tier 1 threshold: requires at least 90%; observed 22.7%.
- Tier 2 threshold: requires at least 80%; observed 68.0%.
- Excluded false-negative threshold: revise if above 20%; observed 40.0%.

Proceed/revise recommendation: **revise classifier before treatment-variable construction**.

## Treatment-Construction Readiness

- Tier 1 is not valid enough for main treatment-candidate construction under the pre-specified 90% sampled precision rule.
- Tier 2 is not valid enough for broader/sensitivity treatment-candidate construction under the pre-specified 80% sampled candidate-precision rule.
- The excluded sample also exceeded the 20% treatment-candidate false-negative threshold, so the classifier should be revised before treatment construction.

## Remaining Cautions

- Risk-section language continues to admit competitor, regulatory, and issuer-market-entry context into treatment tiers.
- ICE-style `underserved markets` language is often issuer expansion into markets rather than external financial-access activity.
- Marketplace-lending RFI and CRA/FIO regulatory text is often substantive enough for Tier 2 but not Tier 1 issuer-action treatment.
- Fractional-share customer-access rows were under-called in the excluded sample and need specific recovery rules.
- Affordable-housing rows still mix housing finance, regulatory definitions, property development, sale/accounting, and community-program language.
- Retail-investor product-access language in risk sections needs a clearer distinction between issuer access to retail channels and retail investor access to products.
- Returns, prices, benchmarks, and empirical performance analysis remain off-limits until revised treatment classification is validated and treatment variables are constructed.
