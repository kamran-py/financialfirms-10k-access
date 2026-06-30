# Classification Guidelines For Raw Access-Phrase Hits

Version: `classification_guidelines_v1`

## Purpose

These guidelines define the manual validation layer for raw phrase hits in `data/extracted/phrase_hits.csv`. Raw hits are deterministic text matches only. They are not interpreted evidence until reviewed and labeled under this codebook.

Reviewers should label the excerpt-level context, not the company, stock, later performance, or assumed business model. Do not use price outcomes, later news, SEC requests, or external research while assigning labels.

## Required Labels

Use exactly one `human_label` per hit:

- `true_positive_access_expansion`
- `generic_marketing`
- `risk_disclosure_only`
- `customer_access_unrelated_to_finance`
- `operational_access_or_platform_language`
- `ambiguous`
- `false_positive`

## Label Definitions

### `true_positive_access_expansion`

Use when the excerpt states or clearly describes expanding, broadening, democratizing, lowering barriers to, increasing affordability of, or improving availability of financial products, credit, banking, investing, markets, housing finance, insurance, or other financial services for customers, consumers, borrowers, investors, communities, or similar external users.

Examples of qualifying context:

- Expanding access to credit, banking, investing, homeownership, insurance, or financial services.
- Serving underserved, underbanked, or unbanked customers in a financial-services context.
- Making investment products or institutional-grade capabilities available to individual or retail investors.
- Lowering cost, minimums, or other barriers to financial-product participation.

Do not infer this label from the matched phrase alone. The excerpt must support the access-related interpretation.

### `generic_marketing`

Use when the wording is promotional or mission-oriented but the excerpt does not provide enough context to determine whether the claim concerns financial access expansion.

Typical cases:

- Broad brand statements about inclusion, access, empowerment, or opportunity.
- General market-positioning language without a specific financial product, customer group, or access mechanism.
- Slogans or mission statements that could be access-related but are not specific enough for substantive coding.

### `risk_disclosure_only`

Use when the phrase appears only in a risk factor, cautionary disclosure, regulatory discussion, litigation discussion, or adverse-scenario description and does not state that the issuer expanded or intends to expand access.

Typical cases:

- Loss of `market access`, reduced `access to credit`, or restricted access discussed as a risk.
- Legal, regulatory, macroeconomic, or capital-market risk language.
- Hypothetical warnings about inability to access financing, customers, markets, systems, or services.

Risk-factor section membership is not sufficient by itself; code the actual excerpt context.

### `customer_access_unrelated_to_finance`

Use when the excerpt concerns customer access, public access, service access, website access, facility access, healthcare access, data access, technology access, or product access that is not about financial products or financial-market participation.

Typical cases:

- Access to software, accounts, portals, customer support, physical locations, or digital services unrelated to financial inclusion or financial-product availability.
- Healthcare, education, telecommunications, entertainment, or other non-financial access language.

### `operational_access_or_platform_language`

Use when the phrase concerns issuer operations, internal systems, distribution channels, counterparties, infrastructure, or platform functionality rather than end-user financial access expansion.

Typical cases:

- Employee or partner access to systems, data, tools, networks, facilities, platforms, APIs, or operational resources.
- Capital markets access for the issuer's own financing needs.
- Market access in the sense of regulatory approval, exchange connectivity, broker-dealer routing, or institutional trading infrastructure.

### `ambiguous`

Use when the excerpt plausibly relates to access expansion but lacks enough context to distinguish it from marketing, risk disclosure, operational platform language, or unrelated use.

Typical cases:

- The excerpt is too short or truncated.
- The section extraction appears noisy or table-of-contents-like.
- Multiple interpretations remain plausible after reading the excerpt.

### `false_positive`

Use when the raw phrase match is clearly not about access expansion and fits none of the more specific negative labels above.

Typical cases:

- Phrase match is a lexical accident.
- The matched text is part of a list, heading, table artifact, boilerplate, or malformed extraction with no interpretable context.
- The phrase is negated or refers to an absence of access-related activity without any access-expansion claim.

## Confidence

Use one of:

- `high`: the excerpt clearly supports the selected label.
- `medium`: the label is likely but some context is missing.
- `low`: the label is tentative; another label is plausible.

Use `ambiguous` rather than forcing a low-confidence positive or negative label when the excerpt does not contain enough evidence.

## Reviewer Notes

Use `reviewer_notes` to record the reason for the label, especially for:

- Generic `market access`, `retail investors`, `individual investors`, `affordable housing`, or `institutional-grade` cases.
- Risk-factor hypotheticals.
- Operational platform language.
- Noisy extraction, table artifacts, or insufficient context.
- Cases where a longer filing excerpt should be reviewed before final coding.

## Guardrails

- Raw phrase hits remain separate from interpreted labels.
- A true-positive label means the excerpt contains access-expansion wording; it does not prove actual product availability, customer impact, management intent, or later stock-performance implications.
- Reviewers must not use stock returns, later news, later litigation, later product outcomes, or later firm events while coding text.
- Absence of a raw hit is not evidence that a filing lacks access-related strategy or language.
- No conclusion should use the word `causes` unless a separately justified identification strategy has been approved.

## Recommended Review Workflow

1. Review the excerpt and matched phrase.
2. Check whether the excerpt identifies a financial product, financial-market participation, credit, banking, investing, housing finance, insurance, or financial-services customer group.
3. Check whether the phrase is merely risk disclosure, operational access, generic marketing, or unrelated customer access.
4. Assign exactly one `human_label`.
5. Add `confidence` and `reviewer_notes`.
6. Flag cases that require longer context before final labeling.
