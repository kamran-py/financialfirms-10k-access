# Review Sample Classification Report

Generated at: 2026-06-29T05:22:40.708287+00:00

## Scope

- Text-signal validation for the 600-row review sample only.
- Manual calibration labels are preserved separately from Codex-assisted labels.
- Raw phrase hits remain separate from interpreted labels.
- No prices, returns, outcomes, SEC requests, later news, litigation, bankruptcies, acquisitions, or external firm events were used.
- Script version: `classify_review_sample_v1`.

## Acceptance Counts

- Total rows classified: 600
- Manual calibration row count: 120
- Codex-assisted row count: 480
- Label source counts: {'manual_calibration': 120, 'codex_assisted': 480}
- Raw `phrase_hits.csv` SHA256 before: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw `phrase_hits.csv` SHA256 after: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Raw file unchanged by this stage: yes

## Label Counts Overall

| Label | Count |
| --- | --- |
| ambiguous | 8 |
| customer_access_unrelated_to_finance | 6 |
| false_positive | 52 |
| generic_marketing | 44 |
| operational_access_or_platform_language | 83 |
| risk_disclosure_only | 42 |
| true_positive_access_expansion | 365 |

## Label Counts By Category

| Category | Final label | Count |
| --- | --- | --- |
| affordable financial products | ambiguous | 1 |
| affordable financial products | generic_marketing | 10 |
| affordable financial products | true_positive_access_expansion | 15 |
| broader market participation | customer_access_unrelated_to_finance | 1 |
| broader market participation | false_positive | 1 |
| broader market participation | operational_access_or_platform_language | 14 |
| broader market participation | risk_disclosure_only | 24 |
| broader market participation | true_positive_access_expansion | 4 |
| democratized access | generic_marketing | 6 |
| democratized access | operational_access_or_platform_language | 2 |
| democratized access | risk_disclosure_only | 3 |
| democratized access | true_positive_access_expansion | 32 |
| expanded access to credit | ambiguous | 6 |
| expanded access to credit | operational_access_or_platform_language | 1 |
| expanded access to credit | risk_disclosure_only | 11 |
| expanded access to credit | true_positive_access_expansion | 47 |
| financial inclusion | ambiguous | 1 |
| financial inclusion | generic_marketing | 1 |
| financial inclusion | operational_access_or_platform_language | 2 |
| financial inclusion | risk_disclosure_only | 1 |
| financial inclusion | true_positive_access_expansion | 32 |
| homeownership access | false_positive | 9 |
| homeownership access | operational_access_or_platform_language | 31 |
| homeownership access | true_positive_access_expansion | 56 |
| institutional-grade access for individuals | false_positive | 13 |
| institutional-grade access for individuals | operational_access_or_platform_language | 13 |
| institutional-grade access for individuals | true_positive_access_expansion | 13 |
| lower barriers / level playing field | customer_access_unrelated_to_finance | 4 |
| lower barriers / level playing field | false_positive | 1 |
| lower barriers / level playing field | generic_marketing | 26 |
| lower barriers / level playing field | operational_access_or_platform_language | 19 |
| lower barriers / level playing field | risk_disclosure_only | 1 |
| lower barriers / level playing field | true_positive_access_expansion | 2 |
| retail access to investing | false_positive | 28 |
| retail access to investing | operational_access_or_platform_language | 1 |
| retail access to investing | true_positive_access_expansion | 83 |
| underserved / underbanked / unbanked | customer_access_unrelated_to_finance | 1 |
| underserved / underbanked / unbanked | generic_marketing | 1 |
| underserved / underbanked / unbanked | risk_disclosure_only | 2 |
| underserved / underbanked / unbanked | true_positive_access_expansion | 81 |

## Label Counts By Phrase

| Phrase | Final label | Count |
| --- | --- | --- |
| access to affordable credit | ambiguous | 2 |
| access to affordable credit | true_positive_access_expansion | 1 |
| access to affordable housing | true_positive_access_expansion | 3 |
| access to credit | ambiguous | 2 |
| access to credit | operational_access_or_platform_language | 1 |
| access to credit | risk_disclosure_only | 9 |
| access to credit | true_positive_access_expansion | 18 |
| access to homeownership | true_positive_access_expansion | 2 |
| access to housing | true_positive_access_expansion | 3 |
| access to investing | true_positive_access_expansion | 4 |
| access to investment | operational_access_or_platform_language | 1 |
| access to investment | true_positive_access_expansion | 8 |
| access to markets | operational_access_or_platform_language | 6 |
| access to markets | risk_disclosure_only | 2 |
| access to markets | true_positive_access_expansion | 2 |
| affordable credit | ambiguous | 2 |
| affordable credit | true_positive_access_expansion | 2 |
| affordable financial services | ambiguous | 1 |
| affordable financial services | generic_marketing | 8 |
| affordable financial services | true_positive_access_expansion | 7 |
| affordable homeownership | true_positive_access_expansion | 3 |
| affordable housing | false_positive | 9 |
| affordable housing | operational_access_or_platform_language | 31 |
| affordable housing | true_positive_access_expansion | 42 |
| affordable loans | generic_marketing | 2 |
| affordable loans | true_positive_access_expansion | 5 |
| broader participation | operational_access_or_platform_language | 3 |
| capital markets access | risk_disclosure_only | 4 |
| credit access | risk_disclosure_only | 2 |
| credit access | true_positive_access_expansion | 8 |
| democratize access | generic_marketing | 2 |
| democratize access | true_positive_access_expansion | 6 |
| democratize finance | generic_marketing | 1 |
| democratize finance | true_positive_access_expansion | 8 |
| democratize financial services | true_positive_access_expansion | 3 |
| democratized access | generic_marketing | 1 |
| democratized access | risk_disclosure_only | 3 |
| democratized access | true_positive_access_expansion | 2 |
| democratizing access | generic_marketing | 2 |
| democratizing access | operational_access_or_platform_language | 2 |
| democratizing access | true_positive_access_expansion | 4 |
| democratizing finance | true_positive_access_expansion | 1 |
| democratizing financial services | true_positive_access_expansion | 8 |
| eliminate barriers | customer_access_unrelated_to_finance | 2 |
| eliminate barriers | generic_marketing | 3 |
| eliminate barriers | operational_access_or_platform_language | 1 |
| eliminating barriers | generic_marketing | 4 |
| expand access to credit | true_positive_access_expansion | 11 |
| expanded access to credit | true_positive_access_expansion | 3 |
| expanding access to credit | true_positive_access_expansion | 4 |
| expanding homeownership | true_positive_access_expansion | 3 |
| financial inclusion | ambiguous | 1 |
| financial inclusion | generic_marketing | 1 |
| financial inclusion | operational_access_or_platform_language | 1 |
| financial inclusion | risk_disclosure_only | 1 |
| financial inclusion | true_positive_access_expansion | 28 |
| fractional share | false_positive | 27 |
| fractional share | true_positive_access_expansion | 5 |
| improve financial inclusion | true_positive_access_expansion | 1 |
| inclusive financial system | true_positive_access_expansion | 2 |
| individual investors | false_positive | 1 |
| individual investors | true_positive_access_expansion | 27 |
| institutional caliber | true_positive_access_expansion | 5 |
| institutional grade | operational_access_or_platform_language | 4 |
| institutional level | true_positive_access_expansion | 2 |
| institutional quality | false_positive | 13 |
| institutional quality | true_positive_access_expansion | 2 |
| institutional-grade | operational_access_or_platform_language | 9 |
| institutional-grade | true_positive_access_expansion | 4 |
| level playing field | generic_marketing | 1 |
| level playing field | operational_access_or_platform_language | 8 |
| low-cost financial services | true_positive_access_expansion | 3 |
| lower barriers | generic_marketing | 2 |
| lower barriers | operational_access_or_platform_language | 5 |
| lower barriers | risk_disclosure_only | 1 |
| market access | customer_access_unrelated_to_finance | 1 |
| market access | false_positive | 1 |
| market access | operational_access_or_platform_language | 5 |
| market access | risk_disclosure_only | 18 |
| market access | true_positive_access_expansion | 2 |
| promote financial inclusion | operational_access_or_platform_language | 1 |
| promote financial inclusion | true_positive_access_expansion | 1 |
| reduce barriers | generic_marketing | 5 |
| reduce barriers | operational_access_or_platform_language | 1 |
| reduced barriers | generic_marketing | 4 |
| reduced barriers | operational_access_or_platform_language | 1 |
| reduced barriers | true_positive_access_expansion | 1 |
| reducing barriers | false_positive | 1 |
| reducing barriers | operational_access_or_platform_language | 2 |
| remove barriers | generic_marketing | 2 |
| remove barriers | true_positive_access_expansion | 1 |
| removing barriers | customer_access_unrelated_to_finance | 2 |
| removing barriers | generic_marketing | 5 |
| removing barriers | operational_access_or_platform_language | 1 |
| retail access | true_positive_access_expansion | 2 |
| retail investors | true_positive_access_expansion | 37 |
| unbanked | true_positive_access_expansion | 5 |
| unbanked consumers | true_positive_access_expansion | 3 |
| unbanked populations | true_positive_access_expansion | 3 |
| underbanked | true_positive_access_expansion | 8 |
| underbanked consumers | true_positive_access_expansion | 4 |
| underserved | customer_access_unrelated_to_finance | 1 |
| underserved | generic_marketing | 1 |
| underserved | true_positive_access_expansion | 32 |
| underserved borrowers | risk_disclosure_only | 1 |
| underserved borrowers | true_positive_access_expansion | 2 |
| underserved communities | true_positive_access_expansion | 7 |
| underserved consumers | risk_disclosure_only | 1 |
| underserved consumers | true_positive_access_expansion | 9 |
| underserved markets | true_positive_access_expansion | 5 |
| underserved populations | true_positive_access_expansion | 3 |

## True-Positive Rate By Category

| Category | Rows | True positives | Rate |
| --- | --- | --- | --- |
| affordable financial products | 26 | 15 | 57.7% |
| broader market participation | 44 | 4 | 9.1% |
| democratized access | 43 | 32 | 74.4% |
| expanded access to credit | 65 | 47 | 72.3% |
| financial inclusion | 37 | 32 | 86.5% |
| homeownership access | 96 | 56 | 58.3% |
| institutional-grade access for individuals | 39 | 13 | 33.3% |
| lower barriers / level playing field | 53 | 2 | 3.8% |
| retail access to investing | 112 | 83 | 74.1% |
| underserved / underbanked / unbanked | 85 | 81 | 95.3% |

## High-False-Positive Phrases

| Phrase | Rows | Negative/noise labels | Noise rate | True positives |
| --- | --- | --- | --- | --- |
| capital markets access | 4 | 4 | 100.0% | 0 |
| institutional grade | 4 | 4 | 100.0% | 0 |
| broader participation | 3 | 3 | 100.0% | 0 |
| reducing barriers | 3 | 3 | 100.0% | 0 |
| market access | 27 | 25 | 92.6% | 2 |
| level playing field | 9 | 8 | 88.9% | 0 |
| institutional quality | 15 | 13 | 86.7% | 2 |
| fractional share | 32 | 27 | 84.4% | 5 |
| access to markets | 10 | 8 | 80.0% | 2 |
| lower barriers | 8 | 6 | 75.0% | 0 |
| institutional-grade | 13 | 9 | 69.2% | 4 |

## Examples Of Ambiguous Cases

| Hit ID | Ticker | Year | Phrase | Category | Excerpt |
| --- | --- | --- | --- | --- | --- |
| 1176 | BGDE | 2022 | affordable financial services | affordable financial products | y misuse of digital assets, (4) reinforce United States leadership in the global financial system and in technological and economic competitiveness, (5) promote access to safe and affordable financial services, and (6) support technological advances that pr... |
| 3965 | LC | 2024 | access to affordable credit | expanded access to credit | trusted partner, which is especially important for banks participating on our marketplace. LendingClub’s key competitive advantages also extend to our members, including: •Easy access to affordable credit. We allow members to easily apply for a loan from a... |
| 5640 | MA | 2020 | financial inclusion | financial inclusion | (“B2C”) and government payments. GROW DIVERSIFY BUILD CORE CUSTOMERS AND GEOGRAPHIES NEW AREAS Credit Debit Commercial Prepaid Digital-Physical Convergence Acceptance Financial Inclusion New Markets Businesses Governments Merchants Digital Players Local Sch... |
| 6068 | NKSH | 2020 | access to credit | expanded access to credit | nsumer protection responsibility formerly handled by other banking regulators was consolidated in the CFPB. It oversees the enforcement of all federal laws intended to ensure fair access to credit. For smaller financial institutions such as NBI and NBB, the... |
| 6473 | OPRT | 2021 | access to affordable credit | expanded access to credit | using 8.4 billion data points, and our targeted marketing models were developed making use of over 100 billion data points. Our solution delivers the following benefits: •Expands access to affordable credit—Our A.I-driven technology platform is central to o... |
| 6607 | OPFI | 2024 | affordable credit | expanded access to credit | is a mobile-optimized online application where eligible applicants, at their request, are able to opt into the OppFi TurnUp Program. This program helps these applicants find more affordable credit options by checking the market voluntarily on their behalf f... |
| 8235 | SYBT | 2016 | access to credit | expanded access to credit | lable to meet daily needs include the sales of securities under agreements to repurchase. Also, Bancorp is a member of the FHLB of Cincinnati. As a member of the FHLB, Bancorp has access to credit products of the FHLB. Bancorp views these borrowings as a lo... |
| 8580 | UPST | 2023 | affordable credit | expanded access to credit | a fundamental ingredient of life, and unless you are in the few percent of Americans with significant wealth, the price of borrowing affects you every day. Through all of history, affordable credit has been central to unlocking mobility and opportunity. The... |

## Recommended Phrase Exclusions Or High-Risk Flags

| Phrase | Rows | True positives | Other labels | Recommendation |
| --- | --- | --- | --- | --- |
| level playing field | 9 | 0 | 9 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| lower barriers | 8 | 0 | 8 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| removing barriers | 8 | 0 | 8 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| eliminate barriers | 6 | 0 | 6 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| reduce barriers | 6 | 0 | 6 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| capital markets access | 4 | 0 | 4 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| eliminating barriers | 4 | 0 | 4 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| institutional grade | 4 | 0 | 4 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| broader participation | 3 | 0 | 3 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| reducing barriers | 3 | 0 | 3 | exclude from primary classified-treatment construction; retain for sensitivity/audit |
| reduced barriers | 6 | 1 | 5 | high-risk flag; require manual review before treatment use |
| market access | 27 | 2 | 25 | high-risk flag; require manual review before treatment use |
| institutional quality | 15 | 2 | 13 | high-risk flag; require manual review before treatment use |
| access to markets | 10 | 2 | 8 | high-risk flag; require manual review before treatment use |
| fractional share | 32 | 5 | 27 | high-risk flag; require manual review before treatment use |

## Recommended Treatment-Variable Construction For Future Analysis

- Do not use raw phrase hits as treatment without validation.
- Primary text-valid treatment should be `final_label == true_positive_access_expansion`, auditable by `hit_id`, accession number, section, phrase, excerpt, final label, confidence, and label source.
- Preserve separate indicators for `label_source == manual_calibration` and `label_source == codex_assisted` in any downstream table.
- Build filing-level treatment only after aggregating validated labels by accession number and documenting unresolved or ambiguous rows.
- Exclude or separately flag high-risk phrases from primary treatment construction unless manually reviewed.
- Keep `risk_disclosure_only`, `operational_access_or_platform_language`, `customer_access_unrelated_to_finance`, `generic_marketing`, `ambiguous`, and `false_positive` as non-treatment or sensitivity categories.

## Explicit Warning

No returns, prices, benchmarks, outcomes, SEC requests, later news, litigation, bankruptcies, acquisitions, or empirical performance information were used in this classification stage.
