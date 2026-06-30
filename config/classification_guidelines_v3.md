# Classification Guidelines For Raw Access-Phrase Hits

Version: `classification_guidelines_v3`

## Purpose

These guidelines revise `classification_guidelines_v2` using the 2026-06-29 manual audit of Codex-assisted labels. They are for text-treatment validation only.

Raw phrase hits are deterministic text matches. They are not interpreted evidence until reviewed or classified under a documented codebook. Do not use prices, returns, later news, litigation, bankruptcies, acquisitions, external firm events, or assumptions about the issuer when assigning labels.

Manual calibration labels and manual audit labels are ground truth for the current 600-row review-sample revision. Codex-assisted rules apply only to rows without manual calibration or audit labels.

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

- An external beneficiary: customers, consumers, borrowers, members, investors, retail or individual users, underserved or LMI communities, small businesses, smaller issuers, homeowners, renters/residents, or similar outside beneficiaries.
- A financial-access mechanism: credit, banking, payments, money movement, investing, capital-market participation, homeownership, housing finance, insurance, savings, wealth management, affordable financial products, affordable credit, low-cost financial services, or similar financial services.

Do not under-call explicit mission statements when they name both elements. Payments, SMB commerce, affordable credit, low-cost financial services, democratized money movement, and customer financial-service access can be true positives when the excerpt identifies both beneficiary and mechanism.

## Label Definitions

### `true_positive_access_expansion`

Use when the excerpt states or clearly describes expanded, democratized, broadened, more affordable, lower-barrier, or more available financial access for external users.

Qualifying examples:

- Access to credit for consumers, borrowers, members, customers, LMI communities, underserved groups, or small businesses.
- Banking, payments, money movement, savings, or financial services for underserved, unbanked, underbanked, SMB, or consumer users.
- Investment, brokerage, market, or institutional-quality capability made available to retail, individual, consumer, small-business, underserved, or smaller-issuer users.
- Housing finance, mortgage access, homeownership, renters/residents, or community housing access for external beneficiaries.
- CRA or regulatory language that substantively describes expanded credit, banking, investment, or housing access for LMI, underserved, or external communities.

### `generic_marketing`

Use when the excerpt is promotional, mission-oriented, or brand-oriented but lacks a specific external beneficiary or financial-access mechanism.

Do not use `generic_marketing` for explicit mission statements that clearly name both the beneficiary and mechanism; those may be true positives.

### `risk_disclosure_only`

Use when the phrase appears in risk, cautionary, liquidity, funding, litigation, regulatory-risk, macroeconomic-risk, or adverse-scenario language and does not describe external financial-access activity.

`access to credit` in risk sections defaults to `risk_disclosure_only` unless the beneficiary is clearly consumers, borrowers, members, customers, LMI communities, underserved populations, or similar external users.

### `customer_access_unrelated_to_finance`

Use when the excerpt concerns customer, public, patient, visitor, website, facility, data, healthcare, sports, entertainment, education, HR, AI innovation, technology, or internal inclusion access that is not financial-access treatment.

Generic ESG, HR, healthcare, sports, AI innovation, or internal inclusion language is not financial-access treatment.

### `operational_access_or_platform_language`

Use when the phrase concerns issuer operations, internal systems, infrastructure, platform quality, API quality, custodian quality, advisor analytics, analyst processes, data access, exchange connectivity, distribution channels, regulatory permissions, partner access, or the issuer's own financing rather than external financial-access activity.

### `ambiguous`

Use when the excerpt plausibly relates to access-oriented disclosure but lacks enough context to determine whether the beneficiary and financial-access mechanism are both present.

### `false_positive`

Use when the phrase match is clearly not access-oriented disclosure and fits none of the more specific negative labels. This includes table artifacts, headings, boilerplate, malformed extraction, stock mechanics, property-quality descriptions, and lexical accidents.

## Audit Lessons Incorporated In Version 3

### Institutional-Quality Family

`institutional caliber`, `institutional quality`, `institutional level`, `institutional-grade`, and close variants default to `false_positive` or `operational_access_or_platform_language`.

Code positive only when the excerpt explicitly gives retail, individual, consumer, small-business, underserved, or similar external users access to institutional-quality capabilities.

Not true positives without external access mechanism:

- Real estate or property quality.
- Custodian quality.
- Analyst-process quality.
- API quality.
- Platform quality.
- Advisor analytics.
- Internal infrastructure, controls, security, data, or technology quality.

### Market-Access Family

`market access`, `access to markets`, and `capital markets access` default to `operational_access_or_platform_language` or `risk_disclosure_only`.

Code positive only when smaller issuers, customers, investors, borrowers, communities, or other external beneficiaries gain financial-market access.

Issuer financing, liquidity, regulatory access, competitive positioning, exchange connectivity, country risk, and distribution access are not true positives.

### CRA And Regulatory Language

CRA/regulatory language is `true_positive_access_expansion` with medium confidence only when the excerpt substantively describes expanded access to credit, banking, investment, or housing for LMI, underserved, or external communities.

If the excerpt is only compliance background, agency authority, regulation description, assessment-area language, or general obligation language without issuer action or external access mechanism, code `operational_access_or_platform_language`.

### Access To Credit

`access to credit` in risk sections defaults to `risk_disclosure_only`.

Code positive only when the beneficiary is clearly consumers, borrowers, members, customers, LMI communities, underserved populations, small businesses, or similar external users.

Issuer access to credit, funding, deposits, liquidity, debt markets, capital markets, or financing is not a true positive.

### Fractional Share

`fractional share` defaults to `false_positive`.

Code positive only when the excerpt clearly concerns fractional investing access for retail, individual, consumer, or other external investors. Stock split, merger, share issuance, conversion, exchange-ratio, and cash-in-lieu mechanics are false positives.

### Affordable Housing

`affordable housing` defaults to `false_positive` when it appears in tax-credit, partnership, portfolio, investment-income, commitment-table, CRA commitments, or accounting context.

Code positive only when tied to housing finance, mortgage access, homeownership, renters/residents, community housing access, or expanded housing availability for external beneficiaries.

### Explicit Financial-Access Mission Language

Do not under-call explicit mission statements when they include both beneficiary and mechanism. The following can be true positives when externally directed:

- Payments access.
- SMB commerce enablement.
- Affordable credit.
- Low-cost financial services.
- Democratized money movement.
- Banking, savings, investing, or insurance access for customers, consumers, small businesses, or underserved groups.

## Confidence

Use one of:

- `high`: the excerpt clearly supports the selected label.
- `medium`: the label is likely but some context is missing, or the positive label depends on regulatory/CRA interpretation.
- `low`: the label is tentative; another label is plausible.

Use `medium` rather than `high` for CRA/regulatory positives unless issuer action and beneficiary are explicit.

## Guardrails

- Preserve raw hits separately from interpreted labels.
- Preserve manual calibration labels separately from manual audit labels and Codex-assisted labels.
- Future treatment variables must be auditable back to `hit_id`, accession number, section, phrase, excerpt, label, confidence, and reviewer/source.
- A true-positive label means only that the excerpt contains validated access-oriented disclosure wording. It does not prove actual product availability, customer impact, management intent, or future stock-performance implications.
- Treatment construction is not finalized until post-revision classification quality is checked.
- No return analysis should start until treatment classification is validated.
