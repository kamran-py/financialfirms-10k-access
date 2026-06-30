# Conservative Filing-Level Treatment Rules V3

Date: 2026-06-29

## Purpose

V3 revises the filing-level candidate rules after the V2 audit improved precision from V1 but still failed the conservative gate. V2 candidate-positive precision was 70.0%, below the 90% threshold.

V3 is designed as a high-precision candidate layer. It remains a candidate layer only. It does not create final treatment variables, fetch prices, compute returns, make SEC requests, or support empirical performance claims.

## V3 Revision Target

The V2 audit found the remaining false positives were concentrated in:

- FHLB membership, FHLB funding, and required affordable-housing-program boilerplate
- generic commercial-real-estate property-type lists that include affordable housing
- CRA-rule, regulatory-agency, congressional, or special-purpose-credit-program background
- card-issuing/API/infrastructure democratization rather than financial access for end users
- private/HNW democratized-access vehicles and generic retail-investor availability
- broad mission or vision language about financial inclusion without concrete products

V3 hard-excludes those contexts from the conservative main candidate set.

## Conservative Positive Standard

An accepted V3 candidate must still satisfy all three elements:

- external beneficiary
- direct financial-access mechanism
- issuer attribution through an offered, provided, enabled, funded, financed, originated, or facilitated product/program

Generic mission language, regulator descriptions, industry context, competitor discussion, issuer liquidity, and infrastructure access are insufficient.

## V3 Hard Exclusions

Exclude the following from conservative main candidates:

- any FHLB/Federal Home Loan Bank affordable-housing or housing-access context unless the issuer separately describes its own direct borrower/customer product in the same excerpt
- property-type lists such as office, industrial, multifamily, affordable housing, retail, hotel, or other CRE categories
- CRA Rule/Proposal goals, bank-regulatory-agency descriptions, congressional policy language, or legislative/regulatory objectives
- special purpose credit program descriptions unless the issuer itself states that it offers the program
- "potential claims" or risk disclosure about financial inclusion
- card-issuing technology, APIs, platform configurability, data/connectivity, or similar infrastructure access
- democratized access vehicles for individual investors when the text mainly describes fundraising/product distribution rather than broad financial access
- broad vision, mission, ESG, foundation, community-impact, or partnership language without a concrete financial product

## Validation Gate

V3 candidates must be manually audited before treatment construction. The conservative main treatment remains blocked until the sampled candidate-positive precision is at least 90%.
