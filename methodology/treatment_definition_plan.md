# Treatment Definition Plan

Version: `treatment_definition_plan_v1`

Date: 2026-06-29

## Purpose

This plan redesigns treatment construction after the full-corpus V2 spot check failed the precision threshold. It defines treatment tiers and high-risk phrase handling for a future classification revision. It does not revise the classifier, construct final treatment variables, fetch prices, load returns, make SEC requests, or make empirical performance claims.

## Status Of Full-Corpus V2

Full-corpus V2 is not approved for treatment-variable construction:

- Sampled V2 positives: 100.
- Confirmed positives: 55.
- Positive precision: 55.0%.
- Required threshold: 85.0%.
- Disagreements: 59 / 150.

The failed precision result means V2 can be used only as a diagnostic candidate layer. Any treatment variable must be based on a revised and revalidated classification layer.

## Universal Positive Requirements

Every positive treatment candidate must identify:

- An external beneficiary: customers, consumers, borrowers, members, investors, retail or individual users, underserved or low- and moderate-income communities, small businesses, smaller issuers, homeowners, renters, residents, merchants, or similar external beneficiaries.
- A direct financial-access mechanism: credit, banking, payments, money movement, investing, brokerage, capital-market participation, housing finance, mortgage access, insurance, benefits, savings, wealth management, affordable financial products, lower-cost financial services, or similar mechanisms.

Rows that lack either element do not qualify for Tier 1 or Tier 2.

## Treatment Tiers

### Tier 1: Conservative Main Treatment

Tier 1 is the preferred main treatment if and only if the revised classification passes validation.

Definition:

- High-confidence true positives only.
- Must identify an external beneficiary.
- Must identify a direct financial-access mechanism.
- Must be assigned to a narrative subcategory.
- Must be auditable to excerpt, phrase, section, filing date, accession number, label, confidence, label source, and classifier version.

Exclusions:

- High-risk phrases are excluded unless context rules explicitly validate them.
- Generic regulatory boilerplate is excluded unless issuer action or a substantive access mechanism is clear.
- Generic mission statements are excluded unless the financial-access mechanism is explicit.
- Risk-disclosure-only rows are excluded.
- Issuer financing, liquidity, funding, credit facilities, and own market access are excluded.
- Accounting, tax-credit, investment-income, portfolio-return, table, and stock-mechanics contexts are excluded.

Use:

- Main descriptive treatment-candidate variable after revised validation.
- Main return-analysis treatment only after treatment construction is complete and return methodology is approved.

### Tier 2: Broader Validated Treatment

Tier 2 broadens coverage while requiring validation.

Definition:

- Includes high- and medium-confidence true positives from the revised classifier.
- Includes validated regulatory or CRA language when beneficiary and access mechanism are clear.
- Includes repeated mission language only when the financial-access mechanism is explicit.
- Must identify an external beneficiary and direct financial-access mechanism.
- Must be assigned to a narrative subcategory.

Exclusions:

- Low-confidence positives are excluded.
- High-risk phrase positives require explicit phrase-family validation.
- Generic boilerplate, issuer own financing, operational platform quality, and accounting contexts are excluded.

Use:

- Secondary treatment-candidate definition.
- Robustness comparison to Tier 1.
- Not a substitute for Tier 1 if Tier 2 precision fails validation.

### Tier 3: Exploratory Raw-Signal Treatment

Tier 3 captures broad text exposure but is not evidence of substantive access-oriented disclosure.

Definition:

- Raw phrase hits or broad classifier positives.
- May include V2 output, high-risk phrases, or lower-confidence candidate labels.
- Does not require final validated positive status.

Use:

- Robustness and sensitivity analysis only.
- Dictionary exposure measure.
- Never used for main conclusions.
- Always labeled exploratory or raw-signal.

Exclusions:

- Tier 3 cannot be described as access-oriented disclosure evidence.
- Tier 3 cannot be used as the main treatment if validated classification is available.

## High-Risk Phrase Handling

### Affordable Housing

Default label:

- `false_positive` or `operational_access_or_platform_language`.

Conditions required for true positive:

- The excerpt directly ties affordable housing to housing finance, mortgage access, homeownership access, renters, residents, low-income beneficiaries, community housing access, preservation or construction financing, or expanded housing availability for external beneficiaries.
- The beneficiary and mechanism must be explicit.

Common false-positive contexts:

- Tax-credit accounting.
- Partnership investments.
- Portfolio returns.
- Investment-income tables.
- Sale of affordable-housing portfolio.
- Commitment tables.
- CRA commitments without specific access mechanism.
- Generic philanthropic focus areas.

Tier eligibility:

- Tier 1: allowed only with explicit external beneficiary and direct housing-access or finance mechanism; confidence must be high.
- Tier 2: allowed with medium confidence when beneficiary and mechanism are clear, including substantive CRA or housing-finance language.
- Tier 3: raw affordable-housing hits and broad positives only.

### Fractional Share

Default label:

- `false_positive`.

Conditions required for true positive:

- The excerpt clearly describes fractional investing access for retail, individual, consumer, or other external investors.
- The excerpt should show reduced minimums, lower-dollar access, or availability of fractional investing.

Common false-positive contexts:

- Stock splits.
- Reverse splits.
- Merger exchange ratios.
- Share issuance mechanics.
- Conversion mechanics.
- Cash-in-lieu mechanics.
- Fractional cryptocurrency mining-pool rewards.

Tier eligibility:

- Tier 1: allowed when retail/customer fractional investing access is explicit and confidence is high.
- Tier 2: allowed when retail/customer fractional investing access is clear but confidence is medium.
- Tier 3: raw fractional-share hits only.

### Market Access / Access To Markets / Capital Markets Access

Default label:

- `operational_access_or_platform_language` or `risk_disclosure_only`.

Conditions required for true positive:

- The excerpt identifies external beneficiaries gaining financial-market or capital-market access.
- Eligible beneficiaries include smaller issuers, municipalities, customers, investors, borrowers, small businesses, communities, or other external capital seekers.
- The mechanism must be capital-market participation, securities placement, bond-market access, investment-market access, or similar financial-market access.

Common false-positive contexts:

- Reporting issuer's own financing.
- Reporting issuer's liquidity.
- Competitor market access.
- Exchange connectivity.
- Prime-broker access.
- Regulatory permissions.
- Country-risk or macro-risk language.
- Distribution-channel access.
- Market-data or exchange-fee language.

Tier eligibility:

- Tier 1: allowed only when external beneficiary and access mechanism are explicit and not in issuer-own financing or risk context.
- Tier 2: allowed when external beneficiary and mechanism are clear with medium confidence.
- Tier 3: generic market-access phrase hits and broad positives only.

### Institutional Quality / Institutional-Grade / Institutional Caliber / Institutional Level

Default label:

- `false_positive` or `operational_access_or_platform_language`.

Conditions required for true positive:

- The excerpt explicitly gives retail, individual, consumer, small-business, underserved, or otherwise non-institutional external users access to institutional-quality capabilities.
- The excerpt should show a bridge from institutional capability to external access.

Common false-positive contexts:

- Real estate or property quality.
- Custody infrastructure.
- Platform quality.
- API quality.
- Advisor analytics.
- Analyst-process quality.
- Services for hedge funds, institutional investors, or high-net-worth clients.
- Internal technology, controls, security, or infrastructure.

Tier eligibility:

- Tier 1: allowed only when non-institutional external user access is explicit and confidence is high.
- Tier 2: allowed when non-institutional access is clear but confidence is medium.
- Tier 3: raw institutional-quality phrase hits and broad positives only.

### Access To Credit

Default label:

- `risk_disclosure_only`, `operational_access_or_platform_language`, or `ambiguous` depending on context.

Conditions required for true positive:

- The excerpt identifies external borrowers, consumers, customers, members, low- and moderate-income communities, underserved populations, small businesses, or similar external beneficiaries.
- The mechanism must be credit, loans, lending, underwriting, affordable credit, mortgage credit, or similar financial access.

Common false-positive contexts:

- Issuer credit ratings.
- Issuer access to credit facilities.
- Issuer funding or liquidity.
- FHLB advances or borrowing by the issuer.
- Debt markets or capital markets access by the issuer.
- Credit-market risk without external beneficiary.

Tier eligibility:

- Tier 1: allowed when borrower/customer beneficiary and credit mechanism are explicit and confidence is high.
- Tier 2: allowed with medium confidence, including validated CRA language, when beneficiary and mechanism are clear.
- Tier 3: raw access-to-credit hits and broad positives only.

### Lower Barriers / Reduce Barriers / Reduced Barriers / Removing Barriers / Eliminate Barriers

Default label:

- `generic_marketing`, `operational_access_or_platform_language`, or `false_positive`.

Conditions required for true positive:

- The excerpt identifies a specific external beneficiary and a direct financial-access mechanism.
- The barrier reduction must concern access to credit, banking, investing, payments, insurance, housing, capital-market participation, or similar financial services.

Common false-positive contexts:

- Regulatory barriers among financial institutions.
- Barriers to product listing.
- Barriers to competitor entry.
- Technology or AI competitive dynamics.
- Internal operational barriers.
- Generic innovation legislation.
- Marketing language without financial mechanism.

Tier eligibility:

- Tier 1: allowed only when beneficiary, financial mechanism, and barrier reduction are explicit with high confidence.
- Tier 2: allowed with medium confidence when beneficiary and mechanism are clear.
- Tier 3: raw barrier phrase hits and broad positives only.

## Regulatory And CRA Language

Regulatory or CRA language can enter Tier 2 when it substantively describes expanded credit, banking, investment, or housing access for low- and moderate-income, underserved, or external communities. It can enter Tier 1 only when issuer action or a concrete access mechanism is clear and confidence is high.

Generic regulatory background, agency authority, assessment-area descriptions, compliance obligations, or general CRA references are excluded from Tier 1 and Tier 2.

## Filing-Level Aggregation Rules For Future Stage

Treatment variables must be constructed only after revised classification passes validation. Candidate aggregation rules:

- `tier1_true_positive_any`: one or more Tier 1 hit in an issuer filing.
- `tier2_true_positive_any`: one or more Tier 1 or Tier 2 hit in an issuer filing.
- `tier1_true_positive_count`: count of Tier 1 hits in an issuer filing.
- `tier2_true_positive_count`: count of Tier 1 or Tier 2 hits in an issuer filing.
- `tier1_subcategory_[name]`: one or more Tier 1 hit in a narrative subcategory.
- `tier2_subcategory_[name]`: one or more Tier 1 or Tier 2 hit in a narrative subcategory.
- `tier3_raw_signal_any`: one or more raw phrase hit; exploratory only.

Filing-level treatment construction must preserve the hit-level audit trail. No row may be dropped silently.

## Validation Requirement Before Use

Before Tier 1 or Tier 2 treatment variables are used:

- Reclassification must be versioned.
- The spot-check sample must oversample high-risk phrases, high-count firms, all sections, and filing years.
- Positive precision must meet or exceed 85% for the tier used as main treatment.
- False negatives among sampled non-positives must not exceed 20%.
- Disagreement counts by phrase, category, section, filing year, and firm concentration must be reported.

## Prohibited Use

- Full-corpus V2 must not be used directly as the main treatment variable.
- Tier 3 must not support main conclusions.
- No treatment tier can be used for return analysis until return methodology, identifier linking, censoring flags, and benchmark definitions are approved.
