# Classification Guidelines For Raw Access-Phrase Hits

Version: `classification_guidelines_v2`

## Purpose

These guidelines define the validation layer for raw phrase hits in `data/extracted/phrase_hits.csv`. Raw hits are deterministic text matches only. They are not interpreted evidence until reviewed and labeled under this codebook.

Reviewers and Codex-assisted classification rules must label only the excerpt-level filing text. Do not use prices, returns, later news, litigation, bankruptcies, acquisitions, external firm events, or assumptions about the issuer while assigning labels.

## Required Labels

Use exactly one label per hit:

- `true_positive_access_expansion`
- `generic_marketing`
- `risk_disclosure_only`
- `customer_access_unrelated_to_finance`
- `operational_access_or_platform_language`
- `ambiguous`
- `false_positive`

## Core Positive Standard

Use `true_positive_access_expansion` only when the excerpt contains both:

- An external beneficiary: customers, consumers, borrowers, investors, retail or individual users, underserved or LMI communities, small businesses, smaller issuers, homeowners, renters, or similar outside beneficiaries.
- A financial-access mechanism: credit, banking, investing, capital markets participation, homeownership, housing finance, insurance, payments, savings, wealth management, affordable financial products, or similar financial services.

The matched phrase alone is never enough. The excerpt must support the interpretation.

## Label Definitions

### `true_positive_access_expansion`

Use when the excerpt states or clearly describes expanding, broadening, democratizing, lowering barriers to, increasing affordability of, or improving availability of financial products, credit, banking, investing, markets, housing finance, insurance, or other financial services for external users.

Examples of qualifying context:

- Expanding access to credit for consumers, borrowers, underserved groups, LMI communities, small businesses, or customers.
- Serving unbanked, underbanked, or underserved customers in a financial-services context.
- Making investment products, markets, or institutional-grade capabilities available to individual, retail, consumer, small-business, or smaller-issuer users.
- Lowering minimums, costs, underwriting barriers, or other participation barriers for financial products.
- Regulatory or CRA language that substantively describes the issuer's action to expand credit, banking, investment, or housing access.

### `generic_marketing`

Use when the excerpt is promotional, mission-oriented, or brand-oriented but lacks enough specific context to determine that it concerns financial access-oriented disclosure.

Typical cases:

- Broad statements about inclusion, empowerment, opportunity, access, or democratization without a clear financial-access mechanism.
- Vague mission language without a specific beneficiary.
- General claims that could be positive but are too unspecific for substantive coding.

### `risk_disclosure_only`

Use when the phrase appears in risk, cautionary, regulatory-risk, litigation-risk, macroeconomic-risk, liquidity-risk, or adverse-scenario language and does not state that the issuer expanded or intends to expand external financial access.

Typical cases:

- Item 1A disclosure about the issuer's own access to credit, financing, capital markets, deposits, funding, liquidity, or markets.
- Hypothetical restrictions, deteriorations, loss of access, inability to access, or adverse market access.
- Regulatory or compliance risk language that does not describe issuer action benefiting external users.

Risk-factor section membership is not sufficient by itself; code the excerpt context.

### `customer_access_unrelated_to_finance`

Use when the excerpt concerns customer, user, public, patient, visitor, website, facility, data, healthcare, entertainment, education, or technology access that is not about financial products or financial-market participation.

### `operational_access_or_platform_language`

Use when the phrase concerns issuer operations, internal systems, infrastructure, distribution channels, platforms, counterparties, regulatory permissions, exchange routing, data access, partner access, or the issuer's own financing rather than expanded access for external financial users.

Typical cases:

- Capital markets access for the issuer's own financing needs.
- Market access as regulatory approval, distribution access, trading infrastructure, exchange connectivity, or competitive positioning.
- Platform, API, software, data, analytics, servicing, or back-office access without a clear external financial-access beneficiary.

### `ambiguous`

Use when the excerpt plausibly relates to access-oriented disclosure but lacks enough context to distinguish it from marketing, risk disclosure, operational platform language, or unrelated use.

Use this label rather than forcing a positive or negative label when the excerpt is too short, truncated, noisy, or missing the beneficiary or access mechanism.

### `false_positive`

Use when the raw phrase match is clearly not about access-oriented disclosure and fits none of the more specific negative labels above.

Typical cases:

- Table artifacts, headings, boilerplate, malformed extraction, or lexical accidents.
- Negative, historical, or unrelated statements with no interpretable access-oriented disclosure context.

## Calibration Lessons Incorporated In Version 2

### `fractional share`

Usually code as `false_positive` or `operational_access_or_platform_language` when the excerpt discusses stock splits, merger consideration, share issuance, accounting mechanics, or cash in lieu of fractional shares.

Code as `true_positive_access_expansion` only when the excerpt clearly discusses investor access to fractional investing, lower investment minimums, or retail/individual investor participation.

### `affordable housing`

Usually not a true positive when the excerpt appears in:

- Tax-credit investment descriptions.
- Limited partnership accounting.
- Community investment portfolio exposure.
- CRA commitments tables.
- Loan portfolio tables.
- Tax-benefit or asset-quality language.

Code as `true_positive_access_expansion` only when the excerpt substantively describes expanded housing, homeownership, mortgage, lending, or financing access for external beneficiaries.

### `market access`

High-risk phrase. Usually code as `risk_disclosure_only` or `operational_access_or_platform_language` when it refers to:

- Issuer financing or liquidity.
- Regulatory access.
- Competitive positioning.
- Distribution channels.
- Exchange, trading, or infrastructure access.
- Macroeconomic or country-risk disclosure.

Code as `true_positive_access_expansion` only when the beneficiary is clearly customers, borrowers, investors, communities, small businesses, or smaller issuers gaining financial-market access.

### `institutional quality`

Usually code as `false_positive` when it describes real estate quality, property quality, asset quality, portfolio quality, underwriting quality, governance quality, or investment quality without expanded access for external users.

### `institutional-grade`

Usually code as `operational_access_or_platform_language` when it describes platform, infrastructure, security, technology, analytics, controls, or internal capability.

Code as `true_positive_access_expansion` only when the excerpt ties institutional-grade capability to expanded access for retail, individual, consumer, small-business, underserved, or similar external users.

### `access to credit`

In Item 1A and liquidity discussions, often code as `risk_disclosure_only` when the excerpt concerns issuer liquidity, capital, funding, deposits, market disruption, or adverse credit-market access.

Code as `true_positive_access_expansion` only when the beneficiary is consumers, borrowers, LMI communities, underserved groups, small businesses, or customers.

### Regulatory And CRA Language

Code as `true_positive_access_expansion` when the excerpt substantively describes expanded access to credit, banking, investment, housing, or financial services for external beneficiaries.

Code as `operational_access_or_platform_language` or `risk_disclosure_only` when the excerpt merely lists compliance objectives, regulations, CRA assessment areas, CRA commitments, tax credits, or regulatory obligations without issuer action or external financial-access mechanism.

## Confidence

Use one of:

- `high`: the excerpt clearly supports the selected label.
- `medium`: the label is likely but some context is missing.
- `low`: the label is tentative; another label is plausible.

Use `ambiguous` with low or medium confidence when the excerpt lacks enough evidence.

## Reviewer Notes

Notes should state the decisive coding reason, especially for:

- `fractional share`, `affordable housing`, `market access`, `institutional quality`, `institutional-grade`, and `access to credit`.
- Risk-factor hypotheticals.
- Operational platform or issuer-financing language.
- Regulatory or CRA language.
- Noisy extraction, table artifacts, or insufficient context.

## Guardrails

- Preserve raw hits separately from interpreted labels.
- Preserve human labels separately from Codex-assisted labels.
- Future treatment variables must be auditable back to `hit_id`, accession number, section, phrase, excerpt, label, confidence, and reviewer/source.
- A true-positive label means only that the excerpt contains validated access-oriented disclosure wording. It does not prove actual product availability, customer impact, management intent, or future stock-performance implications.
- Absence of a raw hit is not evidence that a filing lacks access-related strategy or language.
- No conclusion should use the word `causes` unless a separately justified identification strategy has been approved.
