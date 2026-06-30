# Phrase Hit Report

Generated at: 2026-06-29T04:50:28.197589+00:00

## Scope

- Source: local `data/extracted/filing_sections.csv` section text only.
- Matching layer: raw exact phrase hits only.
- No true-positive classification, price fetching, SEC requests, return analysis, or research claims were performed.
- Matcher: `local_exact_phrase_matcher` `access_phrase_matcher_v1`.
- Match rule: case-insensitive `word_phrase` matching with word boundaries and flexible whitespace between phrase tokens.
- Overlap rule: when candidate matches overlap within a section row, keep the longest span; ties use longer phrase text, then earliest offset.

## Warning

Raw phrase hits are not interpreted evidence. They are deterministic text matches that require later classification or manual audit before substantive interpretation.

## Input Counts

- Phrase taxonomy rows: 88
- Section rows scanned: 17862
- Section rows with non-empty text: 17323

## Dry-Run/Sample Validation Notes

- Sample section rows scanned before full matching: 250
- Sample rows with non-empty text: 250
- Sample raw candidate matches before overlap suppression: 63
- Sample retained hits after overlap suppression: 59
- Sample overlapping duplicate candidates suppressed: 4
- Sample run used the same taxonomy, regex construction, excerpt builder, and overlap-suppression logic as the full run.

## Aggregate Hit Counts

- Total phrase hits: 9400
- Candidate matches before overlap suppression: 10130
- Overlapping duplicate candidates suppressed: 730
- Unique filings with at least one hit: 3042

## Hit Counts By Phrase

| Phrase | Raw hit count |
| --- | --- |
| affordable housing | 2313 |
| retail investors | 1201 |
| individual investors | 1090 |
| underserved | 834 |
| fractional share | 631 |
| access to credit | 612 |
| market access | 548 |
| financial inclusion | 314 |
| underserved communities | 187 |
| access to investment | 177 |
| expand access to credit | 161 |
| underserved consumers | 135 |
| unbanked | 124 |
| underbanked | 123 |
| access to markets | 121 |
| underserved markets | 98 |
| credit access | 94 |
| institutional-grade | 69 |
| institutional quality | 68 |
| underserved borrowers | 40 |
| affordable credit | 34 |
| capital markets access | 32 |
| level playing field | 31 |
| underbanked consumers | 27 |
| affordable financial services | 26 |
| removing barriers | 26 |
| access to investing | 18 |
| underserved populations | 17 |
| lower barriers | 16 |
| access to affordable credit | 15 |
| reduced barriers | 15 |
| institutional grade | 14 |
| democratize finance | 13 |
| democratizing financial services | 12 |
| expanding access to credit | 12 |
| institutional caliber | 12 |
| affordable homeownership | 11 |
| reduce barriers | 11 |
| access to housing | 9 |
| democratized access | 9 |
| access to affordable housing | 8 |
| democratize access | 8 |
| democratizing access | 8 |
| eliminate barriers | 8 |
| affordable loans | 7 |
| expanded access to credit | 7 |
| remove barriers | 7 |
| unbanked populations | 7 |
| broader participation | 6 |
| eliminating barriers | 5 |
| democratize financial services | 4 |
| reducing barriers | 4 |
| expanding homeownership | 3 |
| low-cost financial services | 3 |
| unbanked consumers | 3 |
| access to homeownership | 2 |
| inclusive financial system | 2 |
| institutional level | 2 |
| promote financial inclusion | 2 |
| retail access | 2 |
| democratizing finance | 1 |
| improve financial inclusion | 1 |

## Hit Counts By Category

| Category | Raw hit count |
| --- | --- |
| retail access to investing | 3119 |
| homeownership access | 2346 |
| underserved / underbanked / unbanked | 1595 |
| expanded access to credit | 935 |
| broader market participation | 707 |
| financial inclusion | 319 |
| institutional-grade access for individuals | 165 |
| lower barriers / level playing field | 123 |
| democratized access | 55 |
| affordable financial products | 36 |

## Hit Counts By Year

| Filing year | Raw hit count |
| --- | --- |
| 2015 | 624 |
| 2016 | 578 |
| 2017 | 598 |
| 2018 | 634 |
| 2019 | 690 |
| 2020 | 698 |
| 2021 | 759 |
| 2022 | 1055 |
| 2023 | 1283 |
| 2024 | 1264 |
| 2025 | 1217 |

## Hit Counts By Section

| Section | Raw hit count |
| --- | --- |
| Item 1 Business | 4990 |
| Item 7 MD&A | 2336 |
| Item 1A Risk Factors | 2074 |

## Top 25 Firms By Raw Hit Count

| Ticker | Firm ID | Raw hit count |
| --- | --- | --- |
| LSAK | CIK0001041514 | 293 |
| WD | CIK0001497770 | 233 |
| MORN | CIK0001289419 | 182 |
| HOPE | CIK0001128361 | 177 |
| BX | CIK0001393818 | 174 |
| AIG | CIK0000005272 | 154 |
| KKR | CIK0001404912 | 144 |
| IBKR | CIK0001381197 | 140 |
| GHI | CIK0001059142 | 125 |
| EWBC | CIK0001069157 | 103 |
| RF | CIK0001281761 | 96 |
| CG | CIK0001527166 | 95 |
| OPFI | CIK0001818502 | 88 |
| SCHW | CIK0000316709 | 88 |
| VOYA | CIK0001535929 | 86 |
| ARES | CIK0001176948 | 85 |
| LC | CIK0001409970 | 76 |
| ENVA | CIK0001529864 | 75 |
| BENF | CIK0001775734 | 72 |
| MA | CIK0001141391 | 69 |
| CATY | CIK0000861842 | 68 |
| CRBD | CIK0001889539 | 67 |
| HOOD | CIK0001783879 | 67 |
| FCNCA | CIK0000798941 | 66 |
| ATLC | CIK0001464343 | 65 |

## Representative Excerpts By Category


### affordable financial products

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| ASRV | 2018 | Item 7 MD&A | affordable loans | nsecutive year with a record of lending over 90% of deposits into our regional markets. This means we are always seeking fresh deposits because it is our responsibility to provide affordable loans to the local and regional businesses and consumers who are the backbone of our local economies. AmeriServ also has been a company with a higher level of overhead than most commun |
| BHB | 2021 | Item 7 MD&A | affordable loans | nd $3 million in community limited partnership investments made during 2020 reflected in the cash flow from investing activities. Community limited partnership investments provide affordable loans or equity funding typically for multifamily or residential real estate in qualified community reinvestment areas, some of which may involve low income housing tax credits. Partner |
| BGDE | 2022 | Item 1A Risk Factors | affordable financial services | y misuse of digital assets, (4) reinforce United States leadership in the global financial system and in technological and economic competitiveness, (5) promote access to safe and affordable financial services, and (6) support technological advances that promote responsible development and use of digital assets. The executive order was generally received as a positive for the digital as |
| LC | 2017 | Item 1 Business | affordable loans | uto Refinancing Loans. Commencing in the fourth quarter, we facilitate secured auto refinance loans that can be used to help eligible consumers save money by refinancing into more affordable loans with better rates, clear terms, and no hidden fees. Loans terms include amounts ranging from $5,000 to $50,000, with maturities ranging from 24 to 72 months. Borrowers are require |
| LC | 2018 | Item 1 Business | affordable loans | motional period as they choose. Auto Refinancing Loans. We facilitate secured auto refinance loans that can be used to help eligible consumers save money by refinancing into more affordable loans with better rates and clear terms. Installment loan terms include amounts ranging from $5,000 to $55,000, with maturities ranging from two to six years. Borrowers are required to |
| LC | 2019 | Item 1 Business | affordable loans | redetermined fixed interest rate. Auto Refinance Loans. We facilitate secured auto refinance loans that can be used to help eligible consumers save money by refinancing into more affordable loans with lower rates and better loan terms. Installment loan terms include amounts ranging from $5,000 to $55,000, with maturities ranging from two to six years. Borrowers are require |
| LSAK | 2015 | Item 1 Business | affordable financial services | includes the ability to have the smart card funded with pension or welfare payments, make retail purchases, enjoy the convenience of prepaid facilities and qualify for a range of affordable financial services, including insurance and short-term loans as well as standard EMV transactional capabilities to operate wherever MasterCard is accepted. The smart card also offers the card holder |
| LSAK | 2015 | Item 1 Business | affordable financial services | voice identification technology helps prevent fraud. Their personal security risks are reduced since they do not have to safeguard their cash. Recipient cardholders have access to affordable financial services, can save money on their smart cards and can perform money transfers to friends and relatives living in other provinces. Finally, recipient cardholders pay no transaction fees whe |
| LSAK | 2016 | Item 1 Business | affordable financial services | includes the ability to have the smart card funded with pension or welfare payments, make retail purchases, enjoy the convenience of prepaid facilities and qualify for a range of affordable financial services, including insurance and short-term loans as well as standard EMV transactional capabilities to operate wherever MasterCard is accepted. The smart card also offers the card holder |
| LSAK | 2016 | Item 1 Business | affordable financial services | voice identification technology helps prevent fraud. Their personal security risks are reduced since they do not have to safeguard their cash. Recipient cardholders have access to affordable financial services, can save money on their smart cards and can perform money transfers to friends and relatives living in other provinces. Finally, recipient cardholders pay no transaction fees whe |

### broader market participation

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| AFL | 2015 | Item 1A Risk Factors | market access | e for reinvestment each year is deployed in yen-denominated instruments and subject to the low level of yen interest rates. Any potential deterioration in Japan's credit quality, market access, the overall economy of Japan, or Japanese market volatility could adversely impact the business of Aflac in general and specifically Aflac Japan and our related results of operat |
| AFL | 2016 | Item 1A Risk Factors | market access | e for reinvestment each year is deployed in yen-denominated instruments and subject to the low level of yen interest rates. Any potential deterioration in Japan's credit quality, market access, the overall economy of Japan, or Japanese market volatility could adversely impact the business of Aflac in general and specifically Aflac Japan and our related results of operat |
| AFL | 2017 | Item 1A Risk Factors | market access | e for reinvestment each year is deployed in yen-denominated instruments and subject to the low level of yen interest rates. Any potential deterioration in Japan's credit quality, market access, the overall economy of Japan, or Japanese market volatility could adversely impact the business of Aflac in general and specifically Aflac Japan and our related results of operat |
| AFL | 2018 | Item 1A Risk Factors | market access | e for reinvestment each year is deployed in yen-denominated instruments and subject to the low level of yen interest rates. Any potential deterioration in Japan's credit quality, market access, the overall economy of Japan, or Japanese market volatility could adversely impact the business of Aflac in general and specifically Aflac Japan and its related results of operat |
| AFL | 2019 | Item 1A Risk Factors | market access | e for reinvestment each year is deployed in yen-denominated instruments and subject to the low level of yen interest rates. Any potential deterioration in Japan's credit quality, market access, the overall economy of Japan, or Japanese market volatility could adversely impact the business of Aflac in general and specifically Aflac Japan and its related results of operat |
| AFL | 2020 | Item 1A Risk Factors | market access | e for reinvestment each year is deployed in yen-denominated instruments and subject to the low level of yen interest rates. Any potential deterioration in Japan's credit quality, market access, the overall economy of Japan, or Japanese market volatility could adversely impact the business of Aflac in general and specifically Aflac Japan and its related results of operat |
| AFL | 2021 | Item 1A Risk Factors | access to markets | and 70% 2018. The Japanese operations accounted for 83% of the Company's total assets at both December 31, 2020 and 2019. Any potential deterioration in Japan's credit quality or access to markets, the overall economy of Japan, or an increase in Japanese market volatility could adversely impact Aflac Japan's operations and its financial condition and thereby Aflac's overall |
| AFL | 2022 | Item 1A Risk Factors | access to markets | operations accounted for 82% of the Company's total assets at December 31, 2021, compared with 83% at December 31, 2020. Any potential deterioration in Japan's credit quality or access to markets, the overall economy of Japan, or an increase in Japanese market volatility could adversely impact Aflac Japan's operations and its financial condition and thereby Aflac's overall |
| AFL | 2023 | Item 1A Risk Factors | access to markets | operations accounted for 80% of the Company's total assets at December 31, 2022, compared with 82% at December 31, 2021. Any potential deterioration in Japan's credit quality or access to markets, the overall economy of Japan, or an increase in Japanese market volatility could adversely impact Aflac Japan's operations and its financial condition and thereby Aflac's overall |
| AFL | 2024 | Item 1A Risk Factors | access to markets | December 31, 2023 and 2022. See Note 2 of the Notes to the Consolidated Financial Statements for additional information. Any potential deterioration in Japan's credit quality or access to markets, the overall economy of Japan, or an increase in Japanese market volatility could adversely impact Aflac Japan's operations and its financial condition and thereby Aflac's overall |

### democratized access

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| BENF | 2024 | Item 1 Business | democratize access | ed globally among investor types, so has the need and demand for innovation relating to liquidity and capital formation. Increased industry innovation helped capital formation and democratize access into alternative investments. In fact, there is now over $2.7 trillion7 of net asset value owned by Ben’s target markets in the U.S. alone. While this industry has been slow to in |
| BENF | 2025 | Item 1 Business | democratize access | ed globally among investor types, so has the need and demand for innovation relating to liquidity and capital formation. Increased industry innovation helped capital formation and democratize access into alternative investments. In fact, there is now over $3.5 trillion7 of net asset value owned by Ben’s target markets in the U.S. alone. While this industry has been slow to in |
| FRHC | 2025 | Item 1 Business | democratize access | nt and travel ticketing services, e-commerce business, and telecommunications and media businesses in Kazakhstan that are in a developmental stage. Our mission has always been to democratize access to financial markets for global customers. Our company was founded to provide access to the international capital markets for retail brokerage customers and has rapidly grown prov |
| FRHC | 2025 | Item 7 MD&A | democratize access | mplement our core financial services businesses, including telecommunications and media businesses in Kazakhstan that are in a developmental stage. Our mission has always been to democratize access to financial markets for global customers. Our company was founded to provide access to the international capital markets for retail brokerage customers and has rapidly grown prov |
| HIT | 2025 | Item 1 Business | democratize access | rs whose workforce typically ranges from 5 to 150 employees. HIT seeks to make a difference in the growing healthcare market with a distinctive business model that: (a) strives to democratize access to self-funded benefits plans and stop loss insurance policies for small business organizations, significantly broadening the client base; (b) leverages an AI machine learning tec |
| KKR | 2023 | Item 1A Risk Factors | democratized access | ng of opportunities to invest in any funds registered under the Investment Company Act (or other non-U.S. funds) or other investment vehicles that we refer to as "semi-liquid" or "democratized access" vehicles, may result in increased risks, which could materially and adversely affect us. Our investment adviser subsidiaries or affiliates currently externally manage or advise a |
| KKR | 2023 | Item 1A Risk Factors | democratized access | ted a substantial amount of our historic investment vehicle investor base, it is likely that we will increasingly undertake business initiatives to increase the number and type of democratized access vehicles we offer to individual investors. We expect investment opportunities offered to individual investors to continue to grow to represent a larger percentage of our AUM as ou |
| KKR | 2023 | Item 1A Risk Factors | democratized access | se our product offerings and investment platform will begin to include a higher percentage of individual investors as compared to our historical investor base. In some cases, our democratized access vehicles are distributed to individual investors indirectly through third party managed vehicles sponsored by brokerage firms, banks or third-party feeder providers, and in other |
| KKR | 2023 | Item 1A Risk Factors | democratized access | investor assets under management will be successful. In addition, these aforementioned efforts to expand our individual investor base and/or our focus on the development of these democratized access vehicles could be negatively perceived as a strategic realignment of our focus by our traditional fund investors, which may be perceived as adverse to their interests, and which c |
| KKR | 2023 | Item 1A Risk Factors | democratized access | ially more capital and potentially receive stable fee revenues, while providing varying amounts of liquidity to investors in such vehicles (pursuant to the terms of the applicable democratized access vehicle governing agreements). However, these vehicles may be subject to the heightened regulatory requirements applicable to certain semi-liquid or democratized access vehicles, |

### expanded access to credit

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| SRCE | 2024 | Item 1 Business | expand access to credit | er 24, 2023, federal banking agencies issued a final rule designed to strengthen and modernize the regulations implementing the CRA. The changes are designed to encourage banks to expand access to credit, investment and banking services in low- and moderate-income communities, adapt to industry changes including mobile and internet banking, provide greater clarity and consistency |
| SRCE | 2025 | Item 1 Business | expand access to credit | The federal banking agencies issued a final rule in 2023 designed to strengthen and modernize the regulations implementing the CRA. The changes are designed to encourage banks to expand access to credit, investment and banking services in low- and moderate-income communities, adapt to industry changes including mobile and internet banking, provide greater clarity and consistency |
| AFRM | 2022 | Item 1 Business | access to credit | this with real-time response data. In some cases, we also are able to access and leverage SKU-level data to assess and underwrite risk for individual transactions before extending access to credit. Better outcomes generated by our proprietary risk models We believe our risk model informs our ability to better assess risk. Unlike legacy payment and credit systems, we can a |
| AFRM | 2023 | Item 1 Business | access to credit | this with real-time response data. In some cases, we also are able to access and leverage SKU-level data to assess and underwrite risk for individual transactions before extending access to credit. Better outcomes generated by our proprietary risk models We believe our risk model informs our ability to better assess risk. Unlike legacy payment and credit systems, we can a |
| AFRM | 2023 | Item 7 MD&A | access to credit | itiatives We have begun implementing certain pricing initiatives that have the dual purpose of offsetting our increased funding costs while also enabling us to responsibly extend access to credit to a larger number of consumers. These pricing initiatives include the following: •increasing the maximum APR for loans facilitated on our platform from 30% to 36%; •increasing |
| AFRM | 2024 | Item 1 Business | access to credit | this with real-time response data. In some cases, we also are able to access and leverage SKU-level data to assess and underwrite risk for individual transactions before extending access to credit. Better outcomes generated by our proprietary risk models We believe our risk model informs our ability to better assess risk. Unlike legacy payment and credit systems, we can a |
| ALRS | 2023 | Item 1 Business | expand access to credit | ere CRA activities are considered, and how CRA activities are evaluated. More specifically, the bank regulatory agencies described the goals of the CRA Proposal as follows: (i) to expand access to credit, investment, and basic banking services in low and moderate income communities; (ii) to adapt to changes in the banking industry, including mobile and internet banking by moderniz |
| ALRS | 2024 | Item 1 Business | expand access to credit | , where CRA activities are considered, and how CRA activities are evaluated. More specifically, the bank regulatory agencies described the goals of the CRA Rule as follows: (i) to expand access to credit, investment, and basic banking services in low and moderate income communities; (ii) to adapt to changes in the banking industry, including mobile and internet banking by moderniz |
| ALRS | 2025 | Item 1 Business | expand access to credit | , where CRA activities are considered, and how CRA activities are evaluated. More specifically, the federal banking agencies described the goals of the CRA Rule as follows: (i) to expand access to credit, investment, and basic banking services in low and moderate income communities; (ii) to adapt to changes in the banking industry, including mobile and internet banking by moderniz |
| AB | 2015 | Item 1A Risk Factors | access to credit | air our ability to maintain or grow our business. Maintaining adequate liquidity for our general business needs depends on certain factors, including operating cash flows and our access to credit on reasonable terms. Our financial condition is dependent on our cash flow from operations, which is subject to the performance of the capital markets, our ability to maintain an |

### financial inclusion

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| AUBN | 2025 | Item 1 Business | financial inclusion | egal credit practices. The New CRA Regulations’ objectives include: ● Update CRA regulations to strengthen the achievement of the core purpose of the statute and to encourage financial inclusion; ● Adapt to changes in the banking industry, including the expanded role of mobile and online banking; ● Provide greater clarity and consistency in the application of the reg |
| BBT | 2023 | Item 1 Business | financial inclusion | ement •Education and training •Workplace programming through employee resource groups (ERGs) •Financial solutions which drive economic equity •Community programming focused on financial inclusion and entrepreneurship •Supplier diversity The Company has a strong foundation of governance practices to ensure that diversity, equity and inclusion is embedded into Berkshire’s |
| BBT | 2023 | Item 7 MD&A | financial inclusion | en buildings; renewable energy technology, storage and manufacturing; energy efficiency in commercial, residential and public buildings; affordable housing; workforce housing; and financial inclusion and access activities. The framework was independently verified by Sustainalytics, a Morningstar Company, for its impact and alignment with the International Capital Market Associ |
| BETR | 2025 | Item 1A Risk Factors | financial inclusion | ommunity Reinvestment Act of 1977 (“CRA”). The federal CRA was enacted as part of several landmark pieces of legislation to address systemic inequities in access to credit, expand financial inclusion, and reverse the impact of decades of redlining in low and moderate-income (“LMI”) communities and minority communities. The federal CRA currently only applies to federally insure |
| XYZ | 2024 | Item 1A Risk Factors | financial inclusion | stomers, employees and other stakeholders are increasingly focused on environmental, social, and governance (“ESG”) matters. Our ESG strategy is focused on four key areas: driving financial inclusion throughout our ecosystem and in our communities, taking climate action for a more resilient and sustainable future, advancing inclusion and diversity across our distributed workpl |
| CCBG | 2022 | Item 1 Business | financial inclusion | ssociates and directors. We continue to focus on ways to better our communities in which we operate through monetary resources and volunteer hours. Access, affordability, and financial inclusion. In 2021, our foundation made grants totaling approximately $0.1 million to Community Reinvestment Act eligible organizations in our market area. Working with CCHL, we are c |
| CCBG | 2023 | Item 1 Business | financial inclusion | iates and directors. We continue to focus on ways to better our communities in which we operate through monetary resources and volunteer hours. 10 Access, affordability, and financial inclusion. In 2022, the CCBG Foundation made grants totaling $150,000 to Community Reinvestment Act eligible organizations in our market area. Working with CCHL, we are committed to pr |
| CCBG | 2024 | Item 1 Business | financial inclusion | inancial information for its annual grant review process. Many of these grants are provided to low-moderate income communities in the Big Bend area. Access, affordability, and financial inclusion. Our community commitment to further financial literacy in the markets we service remains an ongoing focus. In 2023, the CCBG Foundation made grants totaling $143,000 to Commun |
| CCBG | 2025 | Item 1 Business | financial inclusion | inancial information for its annual grant review process. Many of these grants are provided to low-moderate income communities in the Big Bend area. Access, affordability, and financial inclusion. Our community commitment to further financial literacy in the markets we service remains an ongoing focus. In 2024, the CCBG Foundation made grants totaling $167,000 to Commun |
| CCNE | 2025 | Item 1 Business | financial inclusion | economic empowerment for women by offering innovative financial solutions, mentorship, and leadership development opportunities. BankOnBuffalo’s BankOnWheels initiative enhances financial inclusion by delivering banking services to underserved communities. By addressing disparities in access to financial resources, BankOnWheels empowers individuals and communities to fully p |

### homeownership access

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| SRCE | 2017 | Item 1A Risk Factors | affordable housing | t generate returns as anticipated and may have an adverse impact on the Company’s financial results — The Company invests and/or finances certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. The Company’s investments in these projects are designed to generate a return primarily through the realization of federal a |
| SRCE | 2018 | Item 1A Risk Factors | affordable housing | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. Our investments in these projects are designed to generate a return primarily through the realization of federal and state i |
| SRCE | 2019 | Item 1A Risk Factors | affordable housing | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. Our investments in these projects are designed to generate a return primarily through the realization of federal and state i |
| SRCE | 2020 | Item 1A Risk Factors | affordable housing | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. Our investments in these projects are designed to generate a return primarily through the realization of federal and state i |
| SRCE | 2021 | Item 1A Risk Factors | affordable housing | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. Our investments in these projects are designed to generate a return primarily through the realization of federal and state i |
| SRCE | 2022 | Item 1A Risk Factors | affordable housing | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. Our investments in these projects are designed to generate a return primarily through the realization of federal and state i |
| SRCE | 2023 | Item 1A Risk Factors | affordable housing | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. Our investments in these projects are designed to generate a return primarily through the realization of federal and state i |
| SRCE | 2024 | Item 1A Risk Factors | affordable housing | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. Our investments in these projects are designed to generate a return primarily through the realization of federal and state i |
| SRCE | 2025 | Item 1A Risk Factors | affordable housing | taged projects may not generate returns as anticipated and may have an adverse impact on our financial results — We invest and/or finance certain tax-advantaged projects promoting affordable housing, community redevelopment and renewable energy sources. Our investments in these projects are designed to generate a return primarily through the realization of federal and state i |
| ACNB | 2015 | Item 1 Business | affordable housing | ccounting Standards Board (FASB) issued Accounting Standard Update (ASU) 2014-01, Investments—Equity Method and Joint Ventures (Topic 323): Accounting for Investments in Qualified Affordable Housing Projects (a consensus of the FASB Emerging Issues Task Force). The Low-Income Housing Tax Credit is a program designed to encourage investment of private capital for use in the c |

### institutional-grade access for individuals

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| ALTI | 2023 | Item 1 Business | institutional-grade | come and capital growth over the medium-term for its shareholders through investing in a diversified portfolio of UK property that benefits from long-term index-linked leases with institutional-grade tenants. LXi pursues its investment objective by targeting a wide range of defensive and robust sectors, including, but not limited to, office, leisure, industrial, distribution, |
| ALTI | 2024 | Item 1 Business | institutional-grade | come and capital growth over the medium-term for its shareholders through investing in a diversified portfolio of UK property that benefits from long-term index-linked leases with institutional-grade tenants. As of December 31, 2023, LXi’s market capitalization was approximately £1.8 billion ($2.3 billion). On January 9, 2024, LXi and LondonMetric announced their intention to |
| ALTI | 2025 | Item 1 Business | institutional-grade | come and capital growth over the medium-term for its shareholders through investing in a diversified portfolio of UK property that benefits from long-term index-linked leases with institutional-grade tenants. On January 9, 2024, AlTi RE Public Markets Limited entered into heads of terms to sell 100% of the equity of LXi REIT Advisors Limited (“LRA”), the advisor to the public |
| NYC | 2015 | Item 7 MD&A | institutional quality | ability to make distributions. 123 William Street On March 27, 2015, we, through a wholly owned subsidiary of our OP, completed the acquisition of the fee simple interest in an institutional quality office building (the "Property") located at 123 William Street in Downtown Manhattan. The contract purchase price of the Property was $253.0 million, exclusive of closing costs. |
| ARI | 2015 | Item 1 Business | institutional quality | ns, subordinate financings, CMBS and other commercial real-estate related debt investments at attractive risk-adjusted yields. The Company targets investments that are secured by institutional quality real estate. The Company’s underwriting includes a focus on stressed in-place cash flows, debt yields, debt service coverage ratios, loan-to-values, property quality and market an |
| ARI | 2016 | Item 1 Business | institutional quality | ns, subordinate financings, CMBS and other commercial real-estate related debt investments at attractive risk-adjusted yields. The Company targets investments that are secured by institutional quality real estate. The Company’s underwriting includes a focus on stressed in-place cash flows, debt yields, debt service coverage ratios, loan-to-values, property quality and market an |
| ARI | 2017 | Item 1 Business | institutional quality | subordinate financings, CMBS and other commercial real-estate related debt investments at attractive risk-adjusted yields. 1 The Company targets investments that are secured by institutional quality real estate. The Company’s underwriting includes a focus on stressed in-place cash flows, debt yields, debt service coverage ratios, loan-to-values, property quality and market an |
| ARI | 2018 | Item 1 Business | institutional quality | ge loans, subordinate financings and other commercial real-estate related debt investments at attractive risk-adjusted yields. The Company targets investments that are secured by institutional quality real estate. The Company’s underwriting includes a focus on stressed in-place cash flows, debt yields, debt service coverage ratios, loan-to-values, property quality and market an |
| ARI | 2019 | Item 1 Business | institutional quality | mmercial mortgage loans, subordinate financings and other commercial real estate-related debt investments at attractive risk-adjusted yields. We target assets that are secured by institutional quality real estate. Our underwriting includes a focus on stressed in-place cash flows, debt yields, debt service coverage ratios, loan-to-values, property quality and market and sub-mark |
| ARI | 2020 | Item 1 Business | institutional quality | al first mortgage loans, subordinate financings and other commercial real estate-related debt investments at attractive risk-adjusted yields. We target assets that are secured by institutional quality real estate throughout the United States and Europe. Our underwriting includes a focus on stressed in-place cash flows, debt yields, debt service coverage ratios, loan-to-values, |

### lower barriers / level playing field

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| SRCE | 2015 | Item 1 Business | removing barriers | branch was to be located had each enacted reciprocal de novo interstate branching laws. Gramm-Leach-Bliley Act of 1999 — The GLBA is intended to modernize the banking industry by removing barriers to affiliation among banks, insurance companies, the securities industry, and other financial service providers. It provides financial organizations with the flexibility of struct |
| SRCE | 2016 | Item 1 Business | removing barriers | branch was to be located had each enacted reciprocal de novo interstate branching laws. Gramm-Leach-Bliley Act of 1999 — The GLBA is intended to modernize the banking industry by removing barriers to affiliation among banks, insurance companies, the securities industry, and other financial service providers. It provides financial organizations with the flexibility of struct |
| SRCE | 2017 | Item 1 Business | removing barriers | he laws of the other state both permitted out-of-state banks to open de noveo branches. Gramm-Leach-Bliley Act of 1999 — The GLBA is intended to modernize the banking industry by removing barriers to affiliation among banks, insurance companies, the securities industry, and other financial service providers. It provides financial organizations with the flexibility of struct |
| ACGL | 2024 | Item 1 Business | reduce barriers | -life insurers and the proposal to remove branch capital requirements. This will benefit branches of foreign insurers based in the U.K. immediately upon implementation, as well as reduce barriers for foreign insurers wishing to establish a U.K. branch in the future. The U.K. government has also decided to introduce a new mobilization scheme for insurers which would create |
| ASB | 2025 | Item 1 Business | reducing barriers | cial Services issued an industry letter on combating cybersecurity risks associated with AI. Additionally, on January 23, 2025, President Trump issued an Executive Order aimed at reducing barriers to AI innovation in the U.S. economy. The Order requires relevant persons and bodies within the federal government to develop an AI action plan to carry out this objective, and re |
| ATHS | 2017 | Item 1A Risk Factors | level playing field | es and regulations promulgated thereunder. Additionally, the BMA sought regulatory equivalency, which enables Bermuda’s commercial insurers to transact business with the EU on a “level playing field.” In connection with its initial efforts to achieve equivalency under Solvency II, the BMA implemented and imposed additional requirements on the companies it regulates, such as A |
| BMNP | 2021 | Item 1 Business | eliminate barriers | apable of being implemented under the current state of the markets for exchange traded funds. On April 20, 2021, the U.S. House of Representatives passed a bipartisan bill titled “Eliminate Barriers to Innovation Act of 2021” (H.R. 1602). If passed by the Senate and enacted into law, the bipartisan bill would create a digital assets working group to evaluate the current legal |
| BMNP | 2023 | Item 1A Risk Factors | eliminate barriers | apable of being implemented under the current state of the markets for exchange traded funds. On April 20, 2021, the U.S. House of Representatives passed a bipartisan bill titled “Eliminate Barriers to Innovation Act of 2021” (H.R. 1602). If passed by the Senate and enacted into law, the bipartisan bill would create a digital assets working group to evaluate the current legal |
| BOKF | 2015 | Item 1A Risk Factors | reduced barriers | primary mortgage interest rates, the rates paid by borrowers, and secondary mortgage interest rates, the rates required by investors in mortgage backed securities. They have also reduced barriers to mortgage refinancing such as insufficient home values. BOK Financial derives a substantial amount of revenue from mortgage activities, including $61 million from the productio |
| BOKF | 2016 | Item 1A Risk Factors | reduced barriers | primary mortgage interest rates, the rates paid by borrowers, and secondary mortgage interest rates, the rates required by investors in mortgage backed securities. They have also reduced barriers to mortgage refinancing such as insufficient home values. BOK Financial derives a substantial amount of revenue from mortgage banking activities, including $78 million from the p |

### retail access to investing

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| ACNB | 2020 | Item 1 Business | fractional share | share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued approximately 1,600,000 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the determined market share price of ACNB Corporation common stock in accordance with the Reorganization Agreement. With the combination of the two organizatio |
| ACNB | 2020 | Item 1 Business | fractional share | share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued approximately 1,600,000 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the determined market share price of ACNB Corporation common stock in accordance with the Reorganization Agreement. With the combination of the two organizatio |
| ACNB | 2020 | Item 1A Risk Factors | fractional share | ock was converted into the right to receive 0.9900 share of ACNB common stock. As a result of the merger, ACNB issued 1,590,547 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the determined market share price of ACNB common stock in accordance with the Reorganization Agreement. Effective January 11, 2020, in connection with the merg |
| ACNB | 2020 | Item 7 MD&A | fractional share | tock for each share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued 1,590,547 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the determined market share price of ACNB Corporation common stock in accordance with the Reorganization Agreement. 61 Table of Contents With the combination |
| ACNB | 2021 | Item 1 Business | fractional share | share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued approximately 1,600,000 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the determined market share price of ACNB Corporation common stock in accordance with the Reorganization Agreement. |
| ACNB | 2021 | Item 7 MD&A | fractional share | tock for each share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued 1,590,547 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the determined market share price of ACNB Corporation common stock in accordance with the Reorganization Agreement. With the combination of the two organizatio |
| ACNB | 2022 | Item 1 Business | fractional share | share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued approximately 1,600,000 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the determined market share price of ACNB Corporation common stock in accordance with the Reorganization Agreement. On February 28, 2022, ACNB Insurance Servic |
| ACNB | 2022 | Item 7 MD&A | fractional share | tock for each share of FCBI common stock that they owned as of the closing date. As a result, ACNB Corporation issued 1,590,547 shares of its common stock and cash in exchange for fractional shares based upon $36.43, the determined market share price of ACNB Corporation common stock in accordance with the Reorganization Agreement. With the combination of the two organizatio |
| AMG | 2017 | Item 1 Business | retail investors | addition, we have retail distribution platforms through our wholly-owned subsidiaries, AMG Funds, LLC in Greenwich, Connecticut and AMG Funds PLC in Dublin, Ireland, which provide retail investors with access to our Affiliates’ investment services through registered investment companies and a family of UCITS funds. Our Affiliates currently manage active return-oriented str |
| AMG | 2018 | Item 1 Business | retail investors | s, and multi-employer plans. Through our retail distribution platform and the retail distribution efforts of our Affiliates, we provide boutique investment management expertise to retail investors through advisory and sub-advisory services to active return-oriented mutual funds, Undertakings for the Collective Investment of Transferable Securities (“UCITS”) and other retail |

### underserved / underbanked / unbanked

| Ticker | Year | Section | Phrase | Excerpt |
| --- | --- | --- | --- | --- |
| AFRM | 2021 | Item 1 Business | underserved consumers | sumer restitution in the event of violations, engage in consumer financial education, track consumer complaints, request data and promote the availability of financial services to underserved consumers and communities. The CFPB, through its enforcement authority, could increase our compliance costs, potentially hinder our ability to respond to marketplace changes, impose require |
| AFRM | 2022 | Item 1 Business | underserved consumers | sumer restitution in the event of violations, engage in consumer financial education, track consumer complaints, request data and promote the availability of financial services to underserved consumers and communities. The CFPB, through its enforcement authority, could increase our compliance costs, potentially hinder our ability to respond to marketplace changes, impose require |
| ALRS | 2024 | Item 1 Business | underserved | tion of the regulations through the use of standardized metrics as part of CRA evaluation and clarifying eligible CRA activities focused on low and moderate income communities and underserved rural communities; (iv) to tailor CRA rules and data collection to bank size and business model; and (v) to maintain a unified approach among the regulators. Management of the Ban |
| ALRS | 2025 | Item 1 Business | underserved | ion of the regulations through the use of standardized metrics as part of CRA evaluation and clarifying eligible CRA activities focused on low- and moderate-income communities and underserved rural communities; (iv) to tailor CRA rules and data collection to bank size and business model; and (v) to maintain a unified approach among the regulators. Anti-Money Launderin |
| ALHC | 2022 | Item 1 Business | underserved | r levels of hospital utilization and greater prevalence of chronic conditions. A significant portion of our nation’s unsustainably high healthcare costs are a direct result of the underserved senior population, especially high-risk and high-acuity seniors. The fragmented U.S. healthcare system is complex and burdensome for seniors, particularly those with chronic, com |
| ALHC | 2022 | Item 1 Business | underserved | -pocket cost Virtual Care Tech-savvy; Telehealth Oriented Virtual-first primary care offering with rich and expansive supplemental benefits Ethnic Product Lines Traditionally Underserved Ethnic Communities Features products designed with the Asian and Hispanic communities in-mind Traditional Medicare/Direct Contracting Entity Original Medicare; Strong PCP Relat |
| ALHC | 2023 | Item 1 Business | underserved | r levels of hospital utilization and greater prevalence of chronic conditions. A significant portion of our nation’s unsustainably high healthcare costs are a direct result of the underserved senior population, especially high-risk and high-acuity seniors. The fragmented U.S. healthcare system is complex and burdensome for seniors, particularly those with chronic, com |
| ALHC | 2023 | Item 1 Business | underserved | -pocket cost Virtual Care Tech-savvy; Telehealth Oriented Virtual-first primary care offering with rich and expansive supplemental benefits Ethnic Product Lines Traditionally Underserved Ethnic Communities Features products designed with the Asian and Hispanic communities in-mind Traditional Medicare/ACO REACH Original Medicare; Strong Primary Care Physician “P |
| ALHC | 2023 | Item 1A Risk Factors | underserved | ealth equity, including the creation of a health equity plan, and will introduce a health equity benchmark adjustment to payments to help support care delivery and coordination in underserved areas. ACO REACH also requires that doctors and other health care providers make up 75% of governing or voting rights on the participating accountable care organization's board. T |
| ALHC | 2024 | Item 1 Business | underserved | r levels of hospital utilization and greater prevalence of chronic conditions. A significant portion of our nation’s unsustainably high healthcare costs are a direct result of the underserved senior population, especially high-risk and high-acuity seniors. The fragmented U.S. healthcare system is complex and burdensome for seniors, particularly those with chronic, com |

## Phrases With Likely High False-Positive Risk

| Phrase | Category | Notes |
| --- | --- | --- |
| underserved | underserved / underbanked / unbanked | Single-word term; may refer to non-financial markets or generic populations. |
| affordable housing | homeownership access | Broad housing phrase; may not indicate access expansion. |
| retail access | retail access to investing | Broad phrase; may refer to stores or distribution channels. |
| retail investors | retail access to investing | Common securities-law phrase; not necessarily access expansion. |
| individual investors | retail access to investing | Common investor-relations phrase; not necessarily access expansion. |
| institutional-grade | institutional-grade access for individuals | Broad quality phrase; may describe internal services. |
| institutional grade | institutional-grade access for individuals | Broad quality phrase; may describe internal services. |
| institutional quality | institutional-grade access for individuals | Broad quality phrase; may describe assets or controls. |
| institutional caliber | institutional-grade access for individuals | Broad quality phrase; may describe internal services. |
| institutional-level | institutional-grade access for individuals | Broad quality phrase; may describe internal services. |
| institutional level | institutional-grade access for individuals | Broad quality phrase; may describe internal services. |
| access to markets | broader market participation | Common broad phrase; may refer to distribution or capital markets. |
| market access | broader market participation | Common broad phrase; may refer to distribution or regulatory access. |
| capital markets access | broader market participation | Common broad phrase; may refer to issuer financing. |

## Output Files

- `data\extracted\phrase_hits.csv`
- `quality_reports\phrase_hit_report.md`
- `CHECKPOINT_05_PHRASE_MATCHING.md`
