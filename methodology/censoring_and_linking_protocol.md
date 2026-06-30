# Censoring And Linking Protocol

Version: `censoring_and_linking_protocol_v1`

Date: 2026-06-29

## Purpose

This protocol defines identifier-linking and return-window status requirements before any price or return data are loaded. It is a design artifact only. It does not fetch prices, compute returns, run return analysis, make SEC requests, construct treatment variables, or make empirical performance claims.

## Core Principle

No filing-window observation may disappear silently. Every issuer-filing-window must either have an observed return or a documented status flag explaining why the return is unavailable, incomplete, ambiguous, or not yet observable.

## Return-Window Status Flags

Use exactly one primary status flag per issuer-filing-window:

- `observed`: start and end prices or total-return observations are available, the window is mature, identifier linking is resolved, and benchmark status is separately available or not required for raw-return calculation.
- `right_censored`: the target end date is after the fixed as-of date, so the window is not mature.
- `delisted_acquired`: the security delisted before the target end date due to merger or acquisition.
- `delisted_failure`: the security delisted before the target end date due to bankruptcy, liquidation, exchange removal, severe distress, or similar failure event.
- `delisted_unknown`: the security delisted before the target end date but the delisting reason is unresolved.
- `ticker_or_cik_link_failed`: the filing issuer could not be linked to a return security identifier.
- `price_unavailable`: identifier linking is resolved but required start or end price/return data are unavailable.
- `IPO_too_recent`: the issuer became publicly traded too recently to support the requested return window or start-price convention.
- `multiple_share_class_ambiguous`: multiple securities or share classes are plausible and the primary return security cannot be resolved under the pre-specified rule.
- `benchmark_unavailable`: issuer return can be measured but the required benchmark return is unavailable for the window.

Secondary reason fields may be added, but the primary status flag must not be blank.

## Required Identifier Fields

Every filing-level and return-window record must preserve:

- CIK.
- Accession number.
- Filing date.
- Filing year.
- Ticker at filing date where available.
- Company name at filing date where available.
- Price identifier used, such as PERMNO, FIGI, CUSIP, provider security ID, or equivalent.
- Price identifier source.
- Link start date and link end date where available.
- Link confidence or link status.
- Primary security selection rule.
- Return data source.
- Benchmark identifier and benchmark source where benchmark-adjusted returns are computed.

Current ticker alone is not sufficient for return linking.

## Linking Requirements

The linking pipeline must:

- Preserve CIK from EDGAR.
- Preserve ticker at filing date where available.
- Preserve accession number.
- Preserve filing date.
- Preserve the price identifier used.
- Record all CIK/ticker/PERMNO or equivalent link failures.
- Record multiple-match conflicts.
- Record ticker changes, name changes, exchange changes, mergers, acquisitions, bankruptcies, delistings, and unresolved events where source data allow.
- Avoid projecting current identifiers backward without dated evidence.
- Avoid using future firm attributes to decide filing-date eligibility unless explicitly labeled retrospective.

No failed link may be dropped silently. Link failures must remain in denominator counts with `ticker_or_cik_link_failed` or another explicit status.

## Primary Security Rule

Before return construction, the project must define a primary security rule. Candidate rule:

- Use the primary US-listed common equity security associated with the issuer at the filing date.
- Exclude non-common equity, warrants, units, preferred shares, funds, trusts, and blank-check securities unless explicitly in scope.
- If multiple common share classes exist, use a pre-specified hierarchy such as primary trading class, highest-volume class, CRSP share-code rule, or provider primary-security flag.
- If the primary class cannot be resolved, use `multiple_share_class_ambiguous`.

The chosen rule must be documented before return data are inspected.

## Delisting And Corporate Action Handling

Delistings are not ordinary missing data. The status flag must distinguish:

- Acquisition or merger exits.
- Failure, bankruptcy, liquidation, or distress exits.
- Unknown delisting reasons.

If a provider supplies delisting returns, the method for incorporating them must be documented before estimation. If delisting returns are unavailable, affected windows must not be treated as ordinary observed returns unless a justified imputation or truncation rule is pre-specified and clearly labeled.

Corporate actions must be handled through source-adjusted prices or explicit split and dividend adjustment. The adjustment policy must be recorded before return construction.

## Right-Censoring Rules

Use the fixed observability date already specified for the project. A window is `right_censored` when its target end date is after that as-of date.

Right-censored windows:

- Remain in status counts.
- Are not treated as zero returns.
- Are not treated as poor outcomes.
- Are not treated as missing at random.
- Are excluded from completed-window return comparisons only with explicit disclosure.

## Benchmark Availability

When benchmark-adjusted returns are primary, benchmark availability must be tracked separately from issuer return availability. If issuer returns are observed but benchmark returns are missing, the row should receive `benchmark_unavailable` for benchmark-adjusted specifications while retaining raw-return status where appropriate.

Benchmark fields should include:

- Benchmark name.
- Benchmark identifier.
- Benchmark source.
- Benchmark return convention.
- Benchmark start date and end date.
- Benchmark status flag.

## Public Price Data Limitations

If CRSP/WRDS or an equivalent point-in-time security-return source is unavailable, the project must document limitations of public price data:

- Delisting-return coverage may be incomplete.
- Historical ticker changes may be incomplete.
- Acquisitions, bankruptcies, and exchange changes may be difficult to classify.
- Adjusted-close methodology may vary by provider.
- Dividend treatment and total-return coverage may be incomplete.
- Multiple share classes may be harder to resolve.
- Survivorship bias may enter if the provider emphasizes currently active securities.

If these limitations cannot be resolved, affected analyses must be labeled exploratory or limited to the provider-observable sample with explicit missingness counts.

## Required Quality Reports

Before any return comparison, produce quality reports with:

- Count of issuer filings by link status.
- Count of filing-window observations by return-window status.
- Count of link failures by filing year.
- Count of delisted/acquired/failure/unknown cases by filing year.
- Count of right-censored windows by horizon.
- Count of price-unavailable windows by horizon.
- Count of benchmark-unavailable windows by horizon.
- Count of multiple-share-class ambiguous cases.
- Comparison of treatment prevalence by link status to detect differential attrition.

## Prohibited Practices

- Do not drop failed links silently.
- Do not drop delisted or acquired firms silently.
- Do not treat unavailable prices as zero returns.
- Do not treat right-censored windows as observed.
- Do not use current ticker or current listing status as a complete historical identifier.
- Do not select the benchmark after seeing return results.
