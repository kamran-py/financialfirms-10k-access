# Tiered Classification V1 Report

Generated at: 2026-06-29T19:58:13.995898+00:00

## Scope And Guardrails

- Classified the full raw phrase-hit corpus under `tiered_treatment_classification_guidelines_v1`.
- Used `data/extracted/phrase_hits.csv` as the classification input.
- Did not use full-corpus V2 as a treatment variable.
- Outputs are treatment candidates only until validated by a post-classification audit.
- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.
- Script version: `classify_phrase_hits_tiered_v1`.
- Classifier version: `tiered_treatment_classification_guidelines_v1`.

## File Integrity

- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged: yes
- V2 classified file SHA256 before: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- V2 classified file SHA256 after: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- V2 classified file unchanged: yes
- Tiered output SHA256: `c647e1d0acc4498d40426388e8f7046b664e7fee6eca3ffc817ddb50707159df`

## Row Counts

- Total rows classified: 9400
- Tier 1 row count: 725
- Tier 1 unique filing count: 451
- Tier 2 row count: 1292
- Tier 2 unique filing count: 845
- Tier 3 row count: 1571
- Excluded row count: 5812

## Counts By Tiered Label

| Tiered label | Rows |
| --- | --- |
| excluded_non_treatment | 5812 |
| tier_3_exploratory | 1571 |
| tier_2_broader_validated | 1292 |
| tier_1_conservative | 725 |

## Counts By Narrative Subcategory

| Narrative subcategory | Rows |
| --- | --- |
| excluded / non-treatment | 5812 |
| financial inclusion / underbanked / underserved | 1270 |
| retail investing / brokerage democratization | 934 |
| consumer credit access | 678 |
| affordable housing / homeownership access | 378 |
| smaller-issuer capital-market access | 248 |
| generic/other access-expansion | 36 |
| payments / money movement / SMB commerce access | 36 |
| fee / cost / minimum-reduction framing | 4 |
| insurance / benefits access | 2 |
| private-market or alternative-investment access | 2 |

## Counts By Phrase

| Phrase | Total rows | Tier 1 | Tier 2 | Tier 3 | Excluded | Tier 1 rate | Tier 1+2 rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| access to affordable credit | 15 | 0 | 10 | 4 | 1 | 0.0% | 66.7% |
| access to affordable housing | 8 | 0 | 0 | 0 | 8 | 0.0% | 0.0% |
| access to credit | 612 | 73 | 59 | 112 | 368 | 11.9% | 21.6% |
| access to homeownership | 2 | 0 | 0 | 0 | 2 | 0.0% | 0.0% |
| access to housing | 9 | 0 | 0 | 3 | 6 | 0.0% | 0.0% |
| access to investing | 18 | 0 | 0 | 0 | 18 | 0.0% | 0.0% |
| access to investment | 177 | 9 | 0 | 0 | 168 | 5.1% | 5.1% |
| access to markets | 121 | 0 | 10 | 44 | 67 | 0.0% | 8.3% |
| affordable credit | 34 | 0 | 16 | 1 | 17 | 0.0% | 47.1% |
| affordable financial services | 26 | 0 | 10 | 3 | 13 | 0.0% | 38.5% |
| affordable homeownership | 11 | 2 | 0 | 9 | 0 | 18.2% | 18.2% |
| affordable housing | 2313 | 135 | 219 | 0 | 1959 | 5.8% | 15.3% |
| affordable loans | 7 | 0 | 4 | 2 | 1 | 0.0% | 57.1% |
| broader participation | 6 | 0 | 0 | 6 | 0 | 0.0% | 0.0% |
| capital markets access | 32 | 0 | 0 | 9 | 23 | 0.0% | 0.0% |
| credit access | 94 | 0 | 33 | 35 | 26 | 0.0% | 35.1% |
| democratize access | 8 | 3 | 4 | 1 | 0 | 37.5% | 87.5% |
| democratize finance | 13 | 8 | 3 | 1 | 1 | 61.5% | 84.6% |
| democratize financial services | 4 | 4 | 0 | 0 | 0 | 100.0% | 100.0% |
| democratized access | 9 | 0 | 2 | 1 | 6 | 0.0% | 22.2% |
| democratizing access | 8 | 2 | 0 | 2 | 4 | 25.0% | 25.0% |
| democratizing finance | 1 | 1 | 0 | 0 | 0 | 100.0% | 100.0% |
| democratizing financial services | 12 | 12 | 0 | 0 | 0 | 100.0% | 100.0% |
| eliminate barriers | 8 | 0 | 0 | 0 | 8 | 0.0% | 0.0% |
| eliminating barriers | 5 | 0 | 0 | 0 | 5 | 0.0% | 0.0% |
| expand access to credit | 161 | 15 | 133 | 0 | 13 | 9.3% | 91.9% |
| expanded access to credit | 7 | 0 | 7 | 0 | 0 | 0.0% | 100.0% |
| expanding access to credit | 12 | 0 | 12 | 0 | 0 | 0.0% | 100.0% |
| expanding homeownership | 3 | 0 | 0 | 2 | 1 | 0.0% | 0.0% |
| financial inclusion | 314 | 19 | 147 | 0 | 148 | 6.1% | 52.9% |
| fractional share | 631 | 7 | 16 | 0 | 608 | 1.1% | 3.6% |
| improve financial inclusion | 1 | 0 | 1 | 0 | 0 | 0.0% | 100.0% |
| inclusive financial system | 2 | 0 | 0 | 0 | 2 | 0.0% | 0.0% |
| individual investors | 1090 | 14 | 217 | 286 | 573 | 1.3% | 21.2% |
| institutional caliber | 12 | 0 | 0 | 0 | 12 | 0.0% | 0.0% |
| institutional grade | 14 | 0 | 0 | 0 | 14 | 0.0% | 0.0% |
| institutional level | 2 | 0 | 0 | 0 | 2 | 0.0% | 0.0% |
| institutional quality | 68 | 0 | 1 | 0 | 67 | 0.0% | 1.5% |
| institutional-grade | 69 | 0 | 1 | 0 | 68 | 0.0% | 1.4% |
| level playing field | 31 | 0 | 1 | 0 | 30 | 0.0% | 3.2% |
| low-cost financial services | 3 | 3 | 0 | 0 | 0 | 100.0% | 100.0% |
| lower barriers | 16 | 0 | 4 | 0 | 12 | 0.0% | 25.0% |
| market access | 548 | 16 | 16 | 153 | 363 | 2.9% | 5.8% |
| promote financial inclusion | 2 | 0 | 1 | 0 | 1 | 0.0% | 50.0% |
| reduce barriers | 11 | 0 | 0 | 1 | 10 | 0.0% | 0.0% |
| reduced barriers | 15 | 0 | 3 | 0 | 12 | 0.0% | 20.0% |
| reducing barriers | 4 | 0 | 0 | 0 | 4 | 0.0% | 0.0% |
| remove barriers | 7 | 0 | 4 | 3 | 0 | 0.0% | 57.1% |
| removing barriers | 26 | 0 | 2 | 19 | 5 | 0.0% | 7.7% |
| retail access | 2 | 0 | 0 | 0 | 2 | 0.0% | 0.0% |
| retail investors | 1201 | 0 | 133 | 234 | 834 | 0.0% | 11.1% |
| unbanked | 124 | 74 | 7 | 33 | 10 | 59.7% | 65.3% |
| unbanked consumers | 3 | 3 | 0 | 0 | 0 | 100.0% | 100.0% |
| unbanked populations | 7 | 3 | 0 | 4 | 0 | 42.9% | 42.9% |
| underbanked | 123 | 65 | 19 | 11 | 28 | 52.8% | 68.3% |
| underbanked consumers | 27 | 24 | 2 | 0 | 1 | 88.9% | 96.3% |
| underserved | 834 | 15 | 70 | 575 | 174 | 1.8% | 10.2% |
| underserved borrowers | 40 | 36 | 0 | 0 | 4 | 90.0% | 90.0% |
| underserved communities | 187 | 94 | 33 | 8 | 52 | 50.3% | 67.9% |
| underserved consumers | 135 | 41 | 87 | 0 | 7 | 30.4% | 94.8% |
| underserved markets | 98 | 47 | 5 | 0 | 46 | 48.0% | 53.1% |
| underserved populations | 17 | 0 | 0 | 9 | 8 | 0.0% | 0.0% |

## Counts By Phrase Family

| Phrase family | Total rows | Tier 1 | Tier 2 | Tier 3 | Excluded | Tier 1 rate | Tier 1+2 rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| affordable financial products | 36 | 3 | 14 | 5 | 14 | 8.3% | 47.2% |
| broader market participation | 707 | 16 | 26 | 212 | 453 | 2.3% | 5.9% |
| democratized access | 55 | 30 | 9 | 5 | 11 | 54.5% | 70.9% |
| expanded access to credit | 935 | 88 | 270 | 152 | 425 | 9.4% | 38.3% |
| financial inclusion | 319 | 19 | 149 | 0 | 151 | 6.0% | 52.7% |
| homeownership access | 2346 | 137 | 219 | 14 | 1976 | 5.8% | 15.2% |
| institutional-grade access for individuals | 165 | 0 | 2 | 0 | 163 | 0.0% | 1.2% |
| lower barriers / level playing field | 123 | 0 | 14 | 23 | 86 | 0.0% | 11.4% |
| retail access to investing | 3119 | 30 | 366 | 520 | 2203 | 1.0% | 12.7% |
| underserved / underbanked / unbanked | 1595 | 402 | 223 | 640 | 330 | 25.2% | 39.2% |

## Counts By Section

| Section | Total rows | Tier 1 | Tier 2 | Tier 3 | Excluded | Tier 1 rate | Tier 1+2 rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Item 1 Business | 4990 | 538 | 996 | 1238 | 2218 | 10.8% | 30.7% |
| Item 1A Risk Factors | 2074 | 85 | 94 | 44 | 1851 | 4.1% | 8.6% |
| Item 7 MD&A | 2336 | 102 | 202 | 289 | 1743 | 4.4% | 13.0% |

## Counts By Filing Year

| Filing year | Total rows | Tier 1 | Tier 2 | Tier 3 | Excluded | Tier 1 rate | Tier 1+2 rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015 | 624 | 39 | 90 | 111 | 384 | 6.2% | 20.7% |
| 2016 | 578 | 43 | 74 | 121 | 340 | 7.4% | 20.2% |
| 2017 | 598 | 45 | 84 | 119 | 350 | 7.5% | 21.6% |
| 2018 | 634 | 48 | 80 | 123 | 383 | 7.6% | 20.2% |
| 2019 | 690 | 55 | 93 | 114 | 428 | 8.0% | 21.4% |
| 2020 | 698 | 68 | 74 | 123 | 433 | 9.7% | 20.3% |
| 2021 | 759 | 51 | 90 | 133 | 485 | 6.7% | 18.6% |
| 2022 | 1055 | 95 | 135 | 163 | 662 | 9.0% | 21.8% |
| 2023 | 1283 | 106 | 181 | 192 | 804 | 8.3% | 22.4% |
| 2024 | 1264 | 94 | 190 | 191 | 789 | 7.4% | 22.5% |
| 2025 | 1217 | 81 | 201 | 181 | 754 | 6.7% | 23.2% |

## High-Risk Phrase Positive Rates By Tier

| High-risk family | Total rows | Tier 1 | Tier 2 | Tier 3 | Excluded | Tier 1 rate | Tier 1+2 rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CRA/regulatory language | 346 | 20 | 170 | 28 | 128 | 5.8% | 54.9% |
| CRA/regulatory language; risk-section access language | 85 | 4 | 6 | 0 | 75 | 4.7% | 11.8% |
| access to credit | 327 | 71 | 49 | 112 | 95 | 21.7% | 36.7% |
| access to credit; risk-section access language | 285 | 2 | 10 | 0 | 273 | 0.7% | 4.2% |
| affordable housing | 2228 | 134 | 219 | 0 | 1875 | 6.0% | 15.8% |
| affordable housing; risk-section access language | 85 | 1 | 0 | 0 | 84 | 1.2% | 1.2% |
| fractional share | 589 | 7 | 15 | 0 | 567 | 1.2% | 3.7% |
| fractional share; risk-section access language | 42 | 0 | 1 | 0 | 41 | 0.0% | 2.4% |
| institutional quality / institutional-grade / institutional caliber / institutional level | 144 | 0 | 2 | 0 | 142 | 0.0% | 1.4% |
| institutional quality / institutional-grade / institutional caliber / institutional level; risk-section access language | 7 | 0 | 0 | 0 | 7 | 0.0% | 0.0% |
| lower/reduce/remove/eliminate barriers | 66 | 0 | 9 | 20 | 37 | 0.0% | 13.6% |
| lower/reduce/remove/eliminate barriers; risk-section access language | 10 | 0 | 0 | 0 | 10 | 0.0% | 0.0% |
| market access / access to markets / capital markets access | 395 | 16 | 22 | 206 | 151 | 4.1% | 9.6% |
| market access / access to markets / capital markets access; risk-section access language | 306 | 0 | 4 | 0 | 302 | 0.0% | 1.3% |
| risk-section access language | 430 | 50 | 21 | 31 | 328 | 11.6% | 16.5% |

## Top Firms By Tier 1 Count

| Firm ID | Ticker | CIK | Tier 1 rows |
| --- | --- | --- | --- |
| CIK0001041514 | LSAK | 0001041514 | 71 |
| CIK0001141391 | MA | 0001141391 | 27 |
| CIK0001874071 | PDLB | 0001874071 | 27 |
| CIK0001633917 | PYPL | 0001633917 | 23 |
| CIK0001529864 | ENVA | 0001529864 | 19 |
| CIK0001059142 | GHI | 0001059142 | 18 |
| CIK0001123360 | GPN | 0001123360 | 16 |
| CIK0001519401 | RM | 0001519401 | 15 |
| CIK0000861842 | CATY | 0000861842 | 14 |
| CIK0000876437 | MTG | 0000876437 | 14 |
| CIK0000316709 | SCHW | 0000316709 | 14 |
| CIK0000109380 | ZION | 0000109380 | 14 |
| CIK0001801170 | CLOV | 0001801170 | 12 |
| CIK0001095073 | EG | 0001095073 | 12 |
| CIK0001538716 | OPRT | 0001538716 | 12 |
| CIK0001499422 | RBB | 0001499422 | 12 |
| CIK0001273813 | AGO | 0001273813 | 11 |
| CIK0001403475 | BMRC | 0001403475 | 11 |
| CIK0000022356 | CBSH | 0000022356 | 11 |
| CIK0001500375 | HFBL | 0001500375 | 11 |

## Top Firms By Tier 2 Count

| Firm ID | Ticker | CIK | Tier 2 rows |
| --- | --- | --- | --- |
| CIK0001041514 | LSAK | 0001041514 | 79 |
| CIK0001289419 | MORN | 0001289419 | 49 |
| CIK0001059142 | GHI | 0001059142 | 30 |
| CIK0001818502 | OPFI | 0001818502 | 24 |
| CIK0001409970 | LC | 0001409970 | 23 |
| CIK0001141391 | MA | 0001141391 | 23 |
| CIK0000316709 | SCHW | 0000316709 | 23 |
| CIK0001538716 | OPRT | 0001538716 | 20 |
| CIK0001529864 | ENVA | 0001529864 | 19 |
| CIK0001265131 | HTH | 0001265131 | 18 |
| CIK0001497770 | WD | 0001497770 | 18 |
| CIK0001393818 | BX | 0001393818 | 17 |
| CIK0001669162 | KNSL | 0001669162 | 17 |
| CIK0001281761 | RF | 0001281761 | 17 |
| CIK0001775734 | BENF | 0001775734 | 16 |
| CIK0001056288 | FHI | 0001056288 | 16 |
| CIK0000038777 | BEN | 0000038777 | 16 |
| CIK0000886982 | GS | 0000886982 | 16 |
| CIK0001519401 | RM | 0001519401 | 16 |
| CIK0001165002 | WHG | 0001165002 | 16 |

## Examples Of Tier 1 Rows

| Ticker | Year | Section | Phrase | Tier | Subcategory | Notes | Excerpt start |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AXP | 2015 | Item 1 Business | underserved consumers | tier_1_conservative | consumer credit access | Underserved external beneficiaries are tied to a financial-access mechanism. | sumer restitution in the event of violations, engage in consumer financial education, track consumer complaints, request data and promote the availability of financial services to underserved consumers and communities. I |
| AXP | 2016 | Item 1 Business | underserved consumers | tier_1_conservative | consumer credit access | Underserved external beneficiaries are tied to a financial-access mechanism. | sumer restitution in the event of violations, engage in consumer financial education, track consumer complaints, request data and promote the availability of financial services to underserved consumers and communities. I |
| AXP | 2022 | Item 1 Business | underserved consumers | tier_1_conservative | consumer credit access | Underserved external beneficiaries are tied to a financial-access mechanism. | sumer restitution in the event of violations, engage in consumer financial education, track consumer complaints, request data and promote the availability of financial services to underserved consumers and communities. I |
| AXP | 2023 | Item 1 Business | underserved consumers | tier_1_conservative | consumer credit access | Underserved external beneficiaries are tied to a financial-access mechanism. | sumer restitution in the event of violations, engage in consumer financial education, track consumer complaints, request data and promote the availability of financial services to underserved consumers and communities. I |
| AXP | 2024 | Item 1 Business | underserved consumers | tier_1_conservative | consumer credit access | Underserved external beneficiaries are tied to a financial-access mechanism. | sumer restitution in the event of violations, engage in consumer financial education, track consumer complaints, request data and promote the availability of financial services to underserved consumers and communities. I |
| AXP | 2025 | Item 1 Business | underserved consumers | tier_1_conservative | consumer credit access | Underserved external beneficiaries are tied to a financial-access mechanism. | sumer restitution in the event of violations, engage in consumer financial education, track consumer complaints, request data and promote the availability of financial services to underserved consumers and communities. I |
| ASRV | 2019 | Item 7 MD&A | affordable housing | tier_1_conservative | affordable housing / homeownership access | Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism. | t and leadership while fostering a positive corporate image. This will be accomplished by demonstrating our commitment to the communities it serves through assistance in providing affordable housing programs for low-to-m |
| ASRV | 2020 | Item 7 MD&A | affordable housing | tier_1_conservative | affordable housing / homeownership access | Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism. | nt and leadership while fostering a positive corporate image. This will be accomplished by demonstrating our commitment to the communities we serve through assistance in providing affordable housing programs for low-to-m |
| ASRV | 2021 | Item 7 MD&A | affordable housing | tier_1_conservative | affordable housing / homeownership access | Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism. | nt and leadership while fostering a positive corporate image. This will be accomplished by demonstrating our commitment to the communities we serve through assistance in providing affordable housing programs for low-to-m |
| ASRV | 2022 | Item 7 MD&A | affordable housing | tier_1_conservative | affordable housing / homeownership access | Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism. | nt and leadership while fostering a positive corporate image. This will be accomplished by demonstrating our commitment to the communities we serve through assistance in providing affordable housing programs for low-to-m |
| ASRV | 2023 | Item 7 MD&A | affordable housing | tier_1_conservative | affordable housing / homeownership access | Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism. | nt and leadership while fostering a positive corporate image. This will be accomplished by demonstrating our commitment to the communities we serve through assistance in providing affordable housing programs for low-to-m |
| ASRV | 2024 | Item 7 MD&A | affordable housing | tier_1_conservative | affordable housing / homeownership access | Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism. | nt and leadership while fostering a positive corporate image. This will be accomplished by demonstrating our commitment to the communities we serve through assistance in providing affordable housing programs for low-to-m |
| ASRV | 2025 | Item 7 MD&A | affordable housing | tier_1_conservative | affordable housing / homeownership access | Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism. | nt and leadership while fostering a positive corporate image. This will be accomplished by demonstrating our commitment to the communities we serve through assistance in providing affordable housing programs for low-to-m |
| ACGL | 2023 | Item 1A Risk Factors | underserved communities | tier_1_conservative | consumer credit access | Underserved external beneficiaries are tied to a financial-access mechanism. | 647,000) and mortgages on second homes. On October 24, 2022, FHFA announced that the GSEs are eliminating upfront fees for certain first-time homebuyers, low-income borrowers, and underserved communities and is increasin |
| AROW | 2023 | Item 1 Business | unbanked | tier_1_conservative | financial inclusion / underbanked / underserved | Unbanked/underbanked external users are tied to financial services or transactions. | ensive pandemic-related support to customers in need, including loan deferrals and over $234.2 million of 2,400 PPP loans through 2022 •Bank On-certified checking product for the unbanked or underbanked population with n |
| AROW | 2023 | Item 1 Business | underbanked | tier_1_conservative | financial inclusion / underbanked / underserved | Unbanked/underbanked external users are tied to financial services or transactions. | mic-related support to customers in need, including loan deferrals and over $234.2 million of 2,400 PPP loans through 2022 •Bank On-certified checking product for the unbanked or underbanked population with no overdraft  |
| AROW | 2024 | Item 1 Business | affordable housing | tier_1_conservative | affordable housing / homeownership access | Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism. | 2022, in support of arts and culture, child care, economic and workforce development, emergency assistance, food security, financial literacy, mental and physical health, safe and affordable housing, transportation and m |
| AGO | 2015 | Item 7 MD&A | market access | tier_1_conservative | smaller-issuer capital-market access | Market-access wording identifies external beneficiaries and a direct financial-market access mechanism. | the Company for analyzing municipal bonds, to purchase such bonds; enables institutional investors to operate more efficiently; and allows smaller, less well-known issuers to gain market access on a more cost-effective b |
| AGO | 2016 | Item 7 MD&A | market access | tier_1_conservative | smaller-issuer capital-market access | Market-access wording identifies external beneficiaries and a direct financial-market access mechanism. | the Company for analyzing municipal bonds, to purchase such bonds; enables institutional investors to operate more efficiently; and allows smaller, less well-known issuers to gain market access on a more cost-effective b |
| AGO | 2017 | Item 7 MD&A | market access | tier_1_conservative | smaller-issuer capital-market access | Market-access wording identifies external beneficiaries and a direct financial-market access mechanism. | any for analyzing municipal bonds, to purchase such bonds; • enables institutional investors to operate more efficiently; and • allows smaller, less well-known issuers to gain market access on a more cost-effective basis |

## Examples Of Excluded High-Risk Rows

| Ticker | Year | Section | Phrase | Tier | Subcategory | Notes | Excerpt start |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRCE | 2015 | Item 1 Business | removing barriers | excluded_non_treatment | excluded / non-treatment | Barrier language concerns affiliation, listing, competitor entry, technology, or legislation rather than end-user financial access. | branch was to be located had each enacted reciprocal de novo interstate branching laws. Gramm-Leach-Bliley Act of 1999 — The GLBA is intended to modernize the banking industry by removing barriers to affiliation among ba |
| SRCE | 2016 | Item 1 Business | removing barriers | excluded_non_treatment | excluded / non-treatment | Barrier language concerns affiliation, listing, competitor entry, technology, or legislation rather than end-user financial access. | branch was to be located had each enacted reciprocal de novo interstate branching laws. Gramm-Leach-Bliley Act of 1999 — The GLBA is intended to modernize the banking industry by removing barriers to affiliation among ba |
| SRCE | 2017 | Item 1 Business | removing barriers | excluded_non_treatment | excluded / non-treatment | Barrier language concerns affiliation, listing, competitor entry, technology, or legislation rather than end-user financial access. | he laws of the other state both permitted out-of-state banks to open de noveo branches. Gramm-Leach-Bliley Act of 1999 — The GLBA is intended to modernize the banking industry by removing barriers to affiliation among ba |
| SRCE | 2017 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | t generate returns as anticipated and may have an adverse impact on the Company’s financial results — The Company invests and/or finances certain tax-advantaged projects promoting affordable housing, community redevelopm |
| SRCE | 2018 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopm |
| SRCE | 2019 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopm |
| SRCE | 2020 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopm |
| SRCE | 2021 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopm |
| SRCE | 2022 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopm |
| SRCE | 2023 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopm |
| SRCE | 2024 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopm |
| SRCE | 2025 | Item 1A Risk Factors | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopm |
| ACNB | 2015 | Item 1 Business | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | ccounting Standards Board (FASB) issued Accounting Standard Update (ASU) 2014-01, Investments—Equity Method and Joint Ventures (Topic 323): Accounting for Investments in Qualified Affordable Housing Projects (a consensus |
| ACNB | 2015 | Item 1 Business | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context. | tation of low-income housing, which provides certain tax benefits to investors in those projects. The amendments in this Update permit a reporting entity that invests in qualified affordable housing projects to account f |
| ACNB | 2015 | Item 1 Business | affordable housing | excluded_non_treatment | excluded / non-treatment | Affordable-housing phrase lacks explicit external housing-access or financing mechanism. | ted, the amendments should be applied retrospectively to all periods presented. A reporting entity that uses the effective yield method to account for its investments in qualified affordable housing projects before the d |
| ACNB | 2020 | Item 1 Business | fractional share | excluded_non_treatment | excluded / non-treatment | Fractional-share wording does not describe end-user fractional investing access. | share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued approximately 1,600,000 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the |
| ACNB | 2020 | Item 1 Business | fractional share | excluded_non_treatment | excluded / non-treatment | Fractional-share wording does not describe end-user fractional investing access. | share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued approximately 1,600,000 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the |
| ACNB | 2020 | Item 1A Risk Factors | fractional share | excluded_non_treatment | excluded / non-treatment | Fractional-share wording is stock split, share mechanics, cash-in-lieu, or mining-pool allocation context. | ock was converted into the right to receive 0.9900 share of ACNB common stock. As a result of the merger, ACNB issued 1,590,547 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the |
| ACNB | 2020 | Item 7 MD&A | fractional share | excluded_non_treatment | excluded / non-treatment | Fractional-share wording does not describe end-user fractional investing access. | tock for each share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued 1,590,547 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the |
| ACNB | 2021 | Item 1 Business | fractional share | excluded_non_treatment | excluded / non-treatment | Fractional-share wording does not describe end-user fractional investing access. | share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued approximately 1,600,000 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the |

## Remaining Construct-Validity Risks

- Tier 1 and Tier 2 are treatment candidates only and require a post-tiered audit before use.
- High-risk phrase families may still contain false positives despite stricter defaults.
- Conservative Tier 1 rules prioritize precision over recall and may understate access-expansion language.
- Narrative subcategories should be reviewed for support before any filing-level treatment aggregation.
- V2 failed validation and was not used as the treatment variable in this classifier.
- Returns remain off-limits until Tier 1 and Tier 2 classification is validated.

## Warning

These counts are classification diagnostics and treatment-candidate counts, not empirical findings. No return outcomes, prices, benchmarks, or performance data were loaded.
