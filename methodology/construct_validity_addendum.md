# Construct Validity Addendum

Version: `construct_validity_addendum_v1`

Date: 2026-06-29

## Purpose

This addendum incorporates methodological feedback and the failed full-corpus V2 spot check into the text-treatment design. It is a methodology artifact only. It does not revise classification rules, construct final treatment variables, load returns, fetch prices, make SEC requests, or make empirical performance claims.

## Core Construct-Validity Position

Raw keyword hits are candidate signals, not evidence. A raw phrase hit means only that a filing excerpt contains an exact phrase from the access-related dictionary. It does not establish that the filing substantively describes access expansion, a business strategy, product availability, customer impact, management intent, or any later return relation.

The working construct, previously described broadly as an `access-expansion narrative`, is not homogeneous. The same language family can refer to economically different mechanisms:

- A bank discussing credit access for low- and moderate-income communities.
- A brokerage discussing retail-investor access, fee compression, or direct indexing.
- A fintech platform discussing underbanked consumers or merchant payments.
- A private-market platform discussing alternative-investment access.
- A crypto or trading platform using democratization language in a 2020-2021 retail-trading context.
- A financial institution discussing issuer funding, market connectivity, regulatory access, tax-credit accounting, or property quality, which may not be access expansion at all.

Therefore, the project must distinguish economically different access narratives before any return analysis.

## Implication Of Failed Full-Corpus V2 Spot Check

Full-corpus V2 classification failed the pre-specified precision threshold:

- Spot-check sample: 150 rows.
- Sampled V2 positives: 100.
- Confirmed positives: 55.
- Positive precision: 55.0%.
- Required threshold: 85.0%.
- Disagreements: 59 / 150.

Full-corpus V2 must not be used as the treatment variable. It remains an auditable candidate-classification layer that diagnosed failure modes and informs stricter treatment construction. Treatment construction now requires stricter construct rules, a revised classification pass, and validation before any return data are loaded or analyzed.

## Phrase Meaning Drift

Phrase meanings may drift across 2015-2025. This is especially important around 2020-2021, when retail trading, crypto, fintech, low-rate growth narratives, and platform language became more salient. A static dictionary may capture different cultural and business meanings in different filing years. Examples:

- `democratizing finance` can describe mission language, retail trading, crypto access, payments, or broad fintech branding depending on year and issuer type.
- `retail investors` can describe direct customer access, distribution channels, risk disclosure, trading frictions, or market-structure regulation.
- `institutional-grade` can describe custody infrastructure, private-market access, platform quality, or consumer access to previously institutional capabilities.
- `market access` can describe customer access to markets, issuer access to funding, exchange connectivity, or regulatory permissions.

The treatment design must therefore preserve filing year, section, issuer context, phrase family, and narrative subcategory. It should support vintage checks, especially a 2020-2021 indicator or separate reporting for pre-2020, 2020-2021, and post-2021 language cohorts.

## Required Narrative Subcategories

Every validated positive should be assigned to one primary narrative subcategory before filing-level treatment variables are constructed. A secondary subcategory can be added only when the excerpt clearly supports multiple mechanisms.

### Financial Inclusion / Underbanked / Underserved

Language about serving underserved, underbanked, unbanked, low- and moderate-income, low-income, or otherwise excluded consumers, communities, borrowers, households, or businesses through financial services.

Required mechanism examples:

- Banking.
- Credit.
- Payments.
- Savings.
- Insurance.
- Financial education tied to product access.
- Community lending or investment with a clear access mechanism.

Common exclusions:

- Non-financial ESG, education, healthcare, career-readiness, philanthropy, or generic community language.
- Internal diversity or HR language.
- Mission statements without a financial-access mechanism.

### Consumer Credit Access

Language about expanded, affordable, broader, easier, or fairer access to credit for consumers, borrowers, members, households, small businesses, or similar external beneficiaries.

Required mechanism examples:

- Loans.
- Credit products.
- Underwriting access.
- Mortgage credit.
- Small-business credit.
- Consumer-credit protections that substantively address access.

Common exclusions:

- Issuer credit ratings.
- Issuer liquidity.
- FHLB borrowing by the issuer.
- Corporate access to credit facilities.
- Credit-market risk disclosure without external borrowers.

### Affordable Housing / Homeownership Access

Language about housing finance, mortgage access, affordable housing availability, homeownership access, renters, residents, low-income housing beneficiaries, or community housing access.

Required mechanism examples:

- Mortgage access.
- Homeownership programs.
- Financing affordable housing construction or preservation.
- Affordable housing programs for low- or moderate-income families.
- Loans supporting affordable housing properties or units.

Common exclusions:

- Tax-credit accounting.
- Affordable housing partnership investments.
- Portfolio returns.
- Investment-income tables.
- Sale of an affordable-housing portfolio.
- Generic philanthropic focus areas without concrete housing-access mechanism.

### Retail Investing / Brokerage Democratization

Language about retail or individual investors gaining access to investing, brokerage, trading, investment products, advice, direct indexing, fractional investing, or market participation.

Required mechanism examples:

- Brokerage or investing products available to retail or individual investors.
- Fractional investing with explicit customer access.
- Low-cost retail trading or investment access.
- Investment education tied to a financial product or investing service.

Common exclusions:

- Investor-relations references.
- Regulatory market-structure discussion without issuer access expansion.
- Risk disclosure about retail-investor trading behavior.
- Share mechanics, stock splits, cash-in-lieu, or fractional share accounting.

### Private-Market Or Alternative-Investment Access

Language about giving retail, individual, smaller, or non-institutional investors access to private markets, alternative assets, secondary liquidity, or other capabilities previously restricted to institutional or high-net-worth investors.

Required mechanism examples:

- Private equity, private credit, alternatives, secondary liquidity, or other private-market products offered to external non-institutional users.
- Explicit contrast with previously institutional-only access.

Common exclusions:

- Services only to institutional investors, hedge funds, advisors, or high-net-worth clients.
- Internal investment sourcing.
- Custody or platform quality without external beneficiary.

### Payments / Money Movement / SMB Commerce Access

Language about expanding access to payments, money movement, merchant commerce, point-of-sale systems, digital wallets, remittances, or financial tools for small businesses, merchants, consumers, or underserved users.

Required mechanism examples:

- Payment acceptance for merchants.
- Money movement for consumers or small businesses.
- Digital financial services for underbanked users.
- SMB commerce enablement tied to financial transactions.

Common exclusions:

- Internal payment processing infrastructure.
- Partner integrations without external access expansion.
- Generic technology-platform quality.

### Insurance / Benefits Access

Language about access to insurance, protection products, benefits, retirement products, or employee/customer financial protection for external beneficiaries.

Required mechanism examples:

- Insurance availability or affordability.
- Benefits access for customers, members, employees, or underserved groups.
- Retirement or protection products offered to external users with an access mechanism.

Common exclusions:

- Internal employee-benefit administration.
- Insurer capital, reinsurance, or market-access language.
- Risk-disclosure references without external access expansion.

### Smaller-Issuer Capital-Market Access

Language about smaller issuers, municipalities, emerging companies, borrowers, or other external capital seekers gaining access to capital markets, financing, securities placement, bond markets, or market liquidity.

Required mechanism examples:

- Smaller issuers gaining capital-market access.
- Bond insurance or advisory products that lower financing barriers for external issuers.
- Capital markets services provided to external issuers as an access mechanism.

Common exclusions:

- The reporting issuer's own funding access.
- Competitor capital-market access.
- Prime-broker, exchange-connectivity, or regulatory market access.
- Country-risk or macro-liquidity discussion.

### Fee / Cost / Minimum-Reduction Framing

Language that frames access expansion through lower fees, lower minimums, reduced costs, lower barriers, or reduced investment thresholds.

Required mechanism examples:

- Lower minimum investment amounts.
- Lower-cost financial products for external users.
- Reduced fees tied to product availability or participation.
- Fractional investing with explicit lower-dollar access.

Common exclusions:

- Lower barriers to entry for competitors.
- Internal cost reduction.
- Fee compression as issuer risk without external access benefit.
- Regulatory or product-listing barriers unrelated to end-user access.

### Generic / Other Access-Expansion

Validated access-expansion language that meets the external beneficiary and financial-access mechanism standard but does not fit the other categories.

Use this category sparingly. It should not become a catch-all for vague mission language. If a row cannot identify an external beneficiary and a direct financial-access mechanism, it should not enter a positive treatment tier.

## Required Before Return Analysis

Before return analysis, the project must:

- Revise or replace the failed full-corpus V2 classification rules.
- Reclassify or filter high-risk phrase families under stricter construct-validity rules.
- Assign validated positives to narrative subcategories.
- Validate the revised classification with a post-revision audit sample.
- Meet the pre-specified precision threshold for the treatment tier used as the main treatment.
- Preserve full audit trails back to raw hit, excerpt, phrase, category, section, filing date, accession number, label, confidence, and classification version.

## Interpretive Boundary

Even after revised validation, a positive treatment label means only that the filing text contains validated access-expansion wording. It does not prove actual product availability, actual customer outcomes, management sincerity, operational success, or future stock-performance effects.
