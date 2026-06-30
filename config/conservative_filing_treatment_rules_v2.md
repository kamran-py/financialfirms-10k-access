# Conservative Filing-Level Treatment Rules V2

Date: 2026-06-29

## Purpose

V2 revises the filing-level candidate rules after the V1 manual audit failed the conservative precision gate. V1 produced only 42.0% strict precision among sampled candidate-positive filings, so V2 prioritizes construct validity and high precision over recall.

These rules define candidate treatment filings only. They do not create final treatment variables, do not authorize return analysis, do not fetch prices, do not make SEC requests, and do not support empirical performance claims.

## Unit

The unit is the 10-K filing/accession. A filing can be candidate-positive only when at least one excerpt in the filing contains a high-evidence access-oriented disclosure signal attributable to the issuer.

## Conservative Positive Standard

An accepted V2 candidate must contain all three elements:

- External beneficiary: consumers, borrowers, unbanked or underbanked users, low- or moderate-income individuals, small businesses, merchants, homeowners/residents, retail investors, municipal/public-purpose issuers, or similar non-issuer beneficiaries.
- Direct financial-access mechanism: credit, loans, banking, deposits, payments, money movement, remittances, insurance, brokerage/investing, mortgage finance, affordable housing finance, or municipal/public-purpose financing.
- Issuer attribution: the filing firm says it offers, provides, enables, funds, finances, develops, facilitates, expands, or operates the access mechanism. Regulator authority, industry background, competitor behavior, or issuer funding/liquidity is not enough.

## Accepted V2 Positive Families

### Direct Consumer Or Small-Business Credit Access

Accept when the issuer describes affordable credit, credit alternatives, lending, financing, or loan products for consumers, borrowers, financially underserved users, low/moderate-income beneficiaries, or small businesses.

Examples of acceptable evidence:

- marketplace or platform provides access to affordable credit for borrowers
- products/programs increase access to credit for low/moderate-income individuals
- financing solutions for small or medium businesses underserved by traditional lenders
- consumer-credit alternatives for financially underserved consumers

### Financial Inclusion / Underbanked / Banking Access

Accept only when financial inclusion, underbanked, unbanked, or underserved language is tied to issuer-provided banking, deposit, financial-service, or credit products.

Reject regulator boilerplate, branch-market expansion, general community language, or financial advisors in underserved geographic markets.

### Payments / Money Movement / Remittance Access

Accept when the issuer ties democratized financial services, movement of money, money transfer, bill payment, remittances, or merchant payment services to consumers, merchants, immigrant workers, unbanked users, or similar beneficiaries.

### Insurance Access

Accept when the issuer describes insurance products/programs offered to underserved homeowners, middle-income users, niche underserved insurance markets, or similar insurance beneficiaries.

Reject insurance regulator monitoring language, crop reimbursement/state reimbursement language, and distribution-channel expansion without beneficiary access.

### Affordable Housing / Homeownership Finance

Accept only when the excerpt says issuer activity funds, finances, constructs, operates, lends to, or otherwise directly supports affordable housing or homeownership for lower-income residents, borrowers, homeowners, renters, or communities.

Reject FHLB membership boilerplate, required stock ownership, required FHLB affordable-housing funding, affordable-housing tax-credit accounting, investment-book entries, portfolio notes, guarantees, letters of credit tables, and generic philanthropy/community donations.

### Public-Purpose Or Smaller-Issuer Capital-Market Access

Accept only when the issuer or issuer-owned platform explicitly delivers market access or lower financing cost to external municipal/public-purpose issuers, smaller issuers, or similar external financing beneficiaries.

Reject direct-market-access trading technology, exchange connectivity, issuer capital resources, competitor scale, firm geographic expansion, or generic customer access to trading venues.

## Borderline Excluded From Conservative Main Treatment

The following can be recorded for sensitivity-analysis design later, but are excluded from V2 conservative main candidates:

- institutional-quality products for high-net-worth or private-wealth channels without broad retail/public-access framing
- generic retail-investor product availability
- individual-investor fundraising or new-investor-base language
- capital access for other financial institutions unless a public/end-user beneficiary is explicit

## Hard Exclusions

Exclude these even if a phrase match appears:

- CFPB, FIO, Treasury, FHFA, CRA, or other regulator/agency language unless the issuer itself is acting through products or programs
- FHLB membership, advances, liquidity, required stock holdings, or required affordable-housing-program contributions
- issuer liquidity, issuer access to credit, issuer funding, credit facilities, credit ratings, or capital resources
- fractional-share, stock split, reverse split, merger exchange-ratio, conversion, dividend, or share-count mechanics
- affordable-housing accounting, LIHTC/tax-credit, proportional amortization, investment-book, portfolio, guarantee, commitment-table, or investment-income contexts
- generic market access, exchange access, direct market access, data/connectivity, platform/API/infrastructure, or operational technology
- generic philanthropy, foundation grants, ESG/community programs, or mission language without issuer-provided financial-access mechanism
- risk-only, competitor-only, or market-entry risk language
- non-financial access contexts such as health care, HR, sports, education, legislation, or internal operations

## Validation Gate

V2 candidates remain candidates only. They must pass a fresh filing-level manual audit before any final treatment variables, price data, return windows, benchmark comparisons, or empirical conclusions are constructed.

Pre-specified gate:

- candidate-positive precision should be at least 90% for the conservative main treatment
- candidate-negative false-negative rate should be documented and preferably remain below 15-20%
- borderline rows should not be counted as conservative positives
