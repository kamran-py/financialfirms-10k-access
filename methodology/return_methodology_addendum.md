# Return Methodology Addendum

Version: `return_methodology_addendum_v1`

Date: 2026-06-29

## Purpose

This addendum integrates methodological feedback on return measurement before any return data are loaded. It is a design artifact only. It does not fetch prices, compute returns, run return analysis, construct treatment variables, make SEC requests, or make empirical performance claims.

## Raw Returns Are Insufficient

Raw post-filing returns alone are insufficient for inference because access-related language may cluster by filing year, subsector, firm size, growth profile, listing history, and market cycle. Raw returns can be reported descriptively, but they cannot be the primary basis for interpreting whether access-related language is associated with relative performance.

Primary return comparisons should use benchmark-adjusted or excess returns after benchmark definitions are locked. Raw returns should be retained as supporting descriptive outcomes.

## Primary Return Metric

Preferred primary outcome family:

- 1-year benchmark-adjusted or excess return.
- 3-year benchmark-adjusted or excess return, with long-horizon cautions.
- 5-year benchmark-adjusted or excess return, with stronger long-horizon cautions.

Raw returns remain a secondary descriptive outcome. The benchmark, adjustment method, and data source must be pre-specified before looking at return results.

## Filing-Year And Calendar-Time Confounding

Language adoption can cluster in particular calendar periods. This matters because the return windows also begin in those same calendar periods. A treatment group concentrated in 2020-2021 could appear to perform differently because of low rates, retail-trading activity, fintech valuation cycles, crypto cycles, or the 2022 growth-stock drawdown, independent of the filing language.

Required controls or design features:

- Filing-year fixed effects in baseline regressions.
- Calendar-time or event-time cohort reporting.
- Subperiod reporting for pre-2020, 2020-2021, and post-2021 filings.
- Subsector and size controls or matched benchmarks where available.
- Explicit reporting of treated and control support by filing year.

## 2020-2021 Vintage Effects

The project must treat 2020-2021 as a high-risk vintage for both text meaning and return outcomes. Retail trading, crypto language, fintech growth narratives, zero-commission brokerage, stimulus-era trading behavior, and low-rate valuation conditions may all interact with access-related wording.

Required checks:

- Report treatment prevalence by filing year and narrative subcategory.
- Report whether treatment concentration is materially higher in 2020-2021.
- Include 2020-2021 vintage indicators or separate subgroup tables before interpreting results.
- Avoid attributing 2022 or later return patterns to filing language without conditioning on vintage, sector, and benchmark controls.

## Benchmark Selection

Benchmark-adjusted returns are primary. Candidate benchmark families must be locked before return analysis:

- Broad US equity benchmark.
- Financial-sector benchmark.
- Subsector benchmark where support and data quality permit.
- Size-matched benchmark or portfolio.
- Fintech-oriented benchmark only if point-in-time construction and survivorship-bias controls are documented.

Preferred benchmark hierarchy:

1. CRSP or similarly robust point-in-time market and sector portfolios if available.
2. Documented total-return index series with clear methodology if CRSP is unavailable.
3. ETF proxy benchmarks only as sensitivity analyses, with explicit limitations.

If benchmark data are unavailable for a window, the return-window row must receive a benchmark status flag rather than being dropped silently.

## Sector, Subsector, And Size Matching

Access-related language is likely correlated with issuer type. A neobank, crypto platform, broker, mortgage lender, insurer, regional bank, private-equity manager, and exchange operator face different risk exposures. Treatment comparisons should not rely only on treated versus untreated means if treated firms are concentrated in specific subsectors.

Preferred controls:

- Financial subsector fixed effects or matched portfolios where point-in-time classification is available.
- Size controls or size-matched benchmarks.
- Filing-year fixed effects.
- Interaction or subgroup reporting for narrative subcategories with sufficient support.

If only current subsector or size data are available, the limitation must be documented and any analysis using those data should be labeled as potentially affected by look-ahead bias.

## Event-Time Returns Versus Calendar-Time Portfolios

Event-time buy-and-hold returns are intuitive but can overstate precision when observations overlap in calendar time or cluster by vintage. Calendar-time portfolio methods can reduce the impact of overlapping long-horizon event windows and cross-correlation.

Recommended design:

- Use event-time returns for transparent filing-window descriptions.
- Use benchmark-adjusted event-time returns with filing-year controls as baseline descriptive comparisons.
- Consider calendar-time portfolio analysis as a robustness or primary long-horizon method if return data and sample support permit.
- Report treated-portfolio membership rules and rebalancing rules before looking at results.

## Caution Around 3-Year And 5-Year BHARs

Three-year and five-year buy-and-hold abnormal returns are vulnerable to skewness, compounding effects, overlapping windows, delisting treatment, benchmark choice, and inflated test statistics under naive cross-sectional tests. The project should cite Barber & Lyon 1997 and Mitchell & Stafford 2000 later as methodological cautions for long-horizon abnormal-return inference.

Design implications:

- Do not rely on naive t-tests of 3-year or 5-year BHARs as primary evidence.
- Report distributional summaries, medians, and winsorization policy if used.
- Use robust standard errors and clustering by issuer, and consider calendar-time portfolio methods.
- Treat 3-year and 5-year results as more sensitive to censoring and delisting assumptions than 1-year results.
- Pre-specify all windows and report all of them, not only favorable horizons.

## Preferred Interpretation

Unless a separate identification strategy is established and approved, all return analysis is descriptive or associational.

Required language:

- `associated with`.
- `conditional on`.
- `followed by`.
- `relative to the benchmark`.
- `within the validated treatment definition`.

Prohibited causal language:

- `caused by`.
- `led to`.
- `resulted in`.
- `drove`.
- `because of the narrative`.

Acceptable example:

- Filings with validated Tier 1 access-oriented disclosure language were followed by different benchmark-adjusted returns than comparison filings, conditional on filing year and available controls.

Unacceptable example:

- Access-oriented disclosure language caused firms to underperform.

## Required Before Return Analysis

Before return analysis:

- Treatment classification must be revised and validated.
- Treatment tiers must be locked.
- Narrative subcategories must be assigned.
- Benchmark definitions must be locked.
- Identifier linking and censoring protocols must be implemented.
- Return-window status flags must be created for every filing-window pair.
- Missingness and right-censoring counts must be reported before any outcome comparison.
