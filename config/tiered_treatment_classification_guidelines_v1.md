# Tiered Treatment Classification Guidelines

Version: `tiered_treatment_classification_guidelines_v1`

Date: 2026-06-29

## Purpose

These guidelines define a stricter, tiered treatment-candidate classification system after the failed full-corpus V2 spot check. They are for text-treatment candidate construction only. They do not define final empirical treatment variables, do not load returns, do not fetch prices, do not make SEC requests, and do not support empirical performance claims.

Raw phrase hits remain candidate signals, not evidence. Full-corpus V2 is not approved as a treatment variable and must not be used as the main treatment.

## Required Tiered Labels

Use exactly one `tiered_label` per raw phrase hit:

- `tier_1_conservative`
- `tier_2_broader_validated`
- `tier_3_exploratory`
- `excluded_non_treatment`

## Required Binary Fields

Each classified hit must include:

- `tier_1_treatment_candidate`: `yes` only for `tier_1_conservative`.
- `tier_2_treatment_candidate`: `yes` for `tier_1_conservative` or `tier_2_broader_validated`.
- `tier_3_exploratory_signal`: `yes` for `tier_1_conservative`, `tier_2_broader_validated`, or `tier_3_exploratory`.

Tier 2 is cumulative of Tier 1. Tier 3 is a raw-signal layer and must never be used as the main treatment.

## Universal Positive Standard

Tier 1 and Tier 2 require both:

- An external beneficiary: customers, consumers, borrowers, members, investors, retail or individual users, underserved or low- and moderate-income communities, small businesses, smaller issuers, homeowners, renters, residents, merchants, or similar external beneficiaries.
- A direct financial-access mechanism: credit, banking, payments, money movement, investing, brokerage, market participation, capital-market access for external beneficiaries, housing finance, mortgage access, insurance, benefits, savings, wealth management, affordable financial products, lower-cost financial services, or similar mechanisms.

If either element is absent or only implied vaguely, the row cannot enter Tier 1 or Tier 2.

## Tier 1: Conservative Main Treatment Candidate

Use `tier_1_conservative` only when the excerpt clearly contains a true access-expansion narrative.

Requirements:

- Must identify an external beneficiary.
- Must identify a direct financial-access mechanism.
- Must describe access expansion, broader availability, affordability, lower barriers, reduced minimums, democratized availability, or improved financial inclusion.
- Must be high confidence.
- Must be assigned to a narrative subcategory.

Exclusions:

- Generic mission language alone.
- Purely regulatory boilerplate.
- Issuer liquidity, issuer funding, issuer credit, issuer debt-market access, or issuer capital-market access.
- Platform, infrastructure, custody, API, exchange-connectivity, or operational language unless end-user financial access is explicit.
- Accounting, tax-credit, portfolio, investment-income, stock-mechanics, or table artifacts.
- Risk-disclosure-only language.
- Ambiguous high-risk language.

High-risk phrases may enter Tier 1 only when phrase-family rules explicitly validate the context.

## Tier 2: Broader Validated Treatment Candidate

Use `tier_2_broader_validated` when the excerpt is a validated access-expansion narrative but does not satisfy Tier 1 high-confidence requirements.

Requirements:

- Must identify an external beneficiary.
- Must identify a direct financial-access mechanism.
- Medium confidence is allowed.
- CRA or regulatory language is allowed only when it substantively describes expanded access for low- and moderate-income, underserved, or external communities.
- Mission language is allowed only when it names a beneficiary and financial-access mechanism.
- High-risk phrases are allowed only when context is clearly access-related.

Exclusions:

- Generic regulatory background or assessment-area language.
- Mission or ESG language without a financial-access mechanism.
- Issuer own financing, liquidity, credit ratings, funding sources, or market access.
- Operational, platform, infrastructure, custody, or distribution language without external end-user access.
- Accounting, tax-credit, portfolio, investment-income, stock-mechanics, or table artifacts.
- Ambiguous rows.

## Tier 3: Exploratory Raw-Signal Candidate

Use `tier_3_exploratory` for broad access-related signals or raw phrase patterns that may be useful for sensitivity or robustness checks but are not validated treatment candidates.

Tier 3 includes:

- Generic access-related mission wording without enough detail for Tier 1 or Tier 2.
- Broad phrase hits with possible access relevance but unclear beneficiary or mechanism.
- High-risk phrase hits with access-adjacent wording that fails stricter Tier 1 or Tier 2 rules.
- Raw dictionary hits that should remain available for sensitivity analysis.

Tier 3 is not allowed as the main treatment and must not support main conclusions.

## Excluded / Non-Treatment

Use `excluded_non_treatment` when the excerpt is:

- False positive.
- Operational or platform language only.
- Issuer funding, issuer liquidity, issuer credit, issuer debt-market, or issuer capital-market access.
- Risk-disclosure-only.
- Generic marketing without access mechanism.
- Non-financial access.
- Ambiguous.
- Accounting, tax-credit, portfolio, investment-income, stock-mechanics, table, or malformed extraction artifact.

Excluded rows are not treatment candidates.

## Narrative Subcategories

Assign one `narrative_subcategory` to every row. For excluded rows, use `excluded / non-treatment`.

Positive subcategories:

- `financial inclusion / underbanked / underserved`
- `consumer credit access`
- `affordable housing / homeownership access`
- `retail investing / brokerage democratization`
- `private-market or alternative-investment access`
- `payments / money movement / SMB commerce access`
- `insurance / benefits access`
- `smaller-issuer capital-market access`
- `fee / cost / minimum-reduction framing`
- `generic/other access-expansion`

## High-Risk Phrase Families

### Affordable Housing

Default:

- `excluded_non_treatment`.

Required for Tier 1 or Tier 2:

- Explicit external housing beneficiary or access mechanism, such as low- or moderate-income families, homeowners, renters, residents, affordable units, housing finance, mortgage access, construction or preservation financing, or community housing access.

Common exclusions:

- Tax-credit accounting.
- Partnership investments.
- Portfolio returns.
- Investment-income tables.
- Sale of affordable-housing portfolio.
- Commitment tables.
- Generic philanthropic focus area without mechanism.

Tier:

- Tier 1 only when beneficiary and direct housing-access or financing mechanism are explicit and confidence is high.
- Tier 2 when context is clearly access-related but depends on regulatory/CRA or partial context.
- Tier 3 for access-adjacent raw signals that are not validated.

### Fractional Share

Default:

- `excluded_non_treatment`.

Required for Tier 1 or Tier 2:

- Fractional investing access for retail, individual, consumer, or other external investors, usually with lower-dollar access or reduced minimums.

Common exclusions:

- Stock splits, reverse splits, merger ratios, share issuance, conversions, cash-in-lieu, dividend reinvestment mechanics, and cryptocurrency mining-pool reward allocation.

Tier:

- Tier 1 when customer fractional investing access is explicit and high confidence.
- Tier 2 when clearly access-related but less complete.
- Tier 3 for raw fractional-share access-adjacent signals.

### Market Access / Access To Markets / Capital Markets Access

Default:

- `excluded_non_treatment`.

Required for Tier 1 or Tier 2:

- External beneficiaries such as smaller issuers, municipalities, customers, investors, borrowers, small businesses, or communities gain financial-market or capital-market access.

Common exclusions:

- Issuer own financing or liquidity.
- Competitor access.
- Prime-broker or exchange connectivity.
- Regulatory permissions.
- Market-data or exchange-fee language.
- Country-risk or macro-risk discussion.

Tier:

- Tier 1 when external beneficiary and access mechanism are explicit and not risk/issuer-own context.
- Tier 2 when clearly access-related with medium confidence.
- Tier 3 for broad market-access signals only.

### Institutional Quality / Institutional-Grade / Institutional Caliber / Institutional Level

Default:

- `excluded_non_treatment`.

Required for Tier 1 or Tier 2:

- The excerpt explicitly gives retail, individual, consumer, small-business, underserved, or other non-institutional users access to institutional-quality capabilities.

Common exclusions:

- Real estate or property quality.
- Custody infrastructure.
- Platform quality.
- API quality.
- Advisor analytics.
- Analyst-process quality.
- Services to hedge funds, institutional investors, or high-net-worth clients.
- Internal systems, controls, security, or technology.

Tier:

- Tier 1 when non-institutional external user access is explicit and high confidence.
- Tier 2 when non-institutional access is clear but less complete.
- Tier 3 for broad institutional-quality access-adjacent signals only.

### Access To Credit

Default:

- `excluded_non_treatment` or `tier_3_exploratory` depending on access-adjacent language.

Required for Tier 1 or Tier 2:

- External borrowers, consumers, customers, members, low- and moderate-income communities, underserved populations, small businesses, or similar beneficiaries gain access to credit, loans, lending, underwriting, affordable credit, or mortgage credit.

Common exclusions:

- Issuer credit ratings.
- Issuer access to credit facilities.
- Issuer funding or liquidity.
- FHLB borrowing by the issuer.
- Debt-market or capital-market access by the issuer.
- Credit-market risk without external beneficiary.

Tier:

- Tier 1 when borrower/customer beneficiary and credit mechanism are explicit and high confidence.
- Tier 2 for clear medium-confidence access cases, including substantive CRA language.
- Tier 3 for broad access-to-credit signals that lack full support.

### Lower / Reduce / Remove / Eliminate Barriers

Default:

- `excluded_non_treatment` or `tier_3_exploratory`.

Required for Tier 1 or Tier 2:

- A specific external beneficiary and a financial-access mechanism are explicit.
- The barrier reduction concerns access to credit, banking, investing, payments, insurance, housing, capital-market participation, or similar financial services.

Common exclusions:

- Regulatory barriers among financial institutions.
- Product-listing barriers.
- Competitor entry.
- AI or technology competition.
- Internal operations.
- Generic innovation legislation.
- Generic marketing without financial mechanism.

Tier:

- Tier 1 only when beneficiary, mechanism, and barrier reduction are explicit and high confidence.
- Tier 2 when clearly access-related with medium confidence.
- Tier 3 for broad barrier-reduction signals only.

### CRA / Regulatory Language

Default:

- `excluded_non_treatment` unless substantive access is clear.

Required for Tier 1 or Tier 2:

- The excerpt substantively describes expanded credit, banking, investment, or housing access for low- and moderate-income, underserved, or external communities.
- Tier 1 requires issuer action or concrete access mechanism and high confidence.
- Tier 2 can include clear regulatory/CRA access language with medium confidence.

Common exclusions:

- Compliance background.
- Agency authority.
- Assessment-area descriptions.
- Generic obligation language.
- Pure legal or regulatory risk.

### Risk-Section Access Language

Default:

- `excluded_non_treatment`.

Required for Tier 1 or Tier 2:

- Despite appearing in a risk section, the excerpt clearly describes external beneficiary access and a financial-access mechanism rather than issuer risk.

Common exclusions:

- Issuer funding or liquidity risks.
- Competitive risks.
- Macro risks.
- Reduced credit-market access.
- Deterioration in market access.

## Confidence

Use:

- `high`: clear beneficiary, mechanism, and access-expansion narrative.
- `medium`: beneficiary and mechanism are present but context depends on regulatory interpretation or is less direct.
- `low`: raw-signal or access-adjacent language that should not enter Tier 1 or Tier 2.

Excluded rows can use `high`, `medium`, or `low` depending on how certain the exclusion is.

## Guardrails

- Outputs are treatment candidates only until validated by a post-classification audit.
- No return outcomes, prices, or benchmarks may be loaded during classification.
- No empirical performance claims may be made from tiered classification counts.
- Tier 1 and Tier 2 cannot be used in return analysis until post-tiered validation passes the pre-specified threshold.
