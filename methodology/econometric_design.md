# Econometric Design

Version: `econometric_design_v1`

As-of date for return-window observability: 2026-06-29.

## Scope

This document pre-specifies descriptive and econometric comparisons to be run only after return data and benchmark data are loaded, validated, and linked to filing observations. It does not load prices, run return analysis, make SEC requests, classify all hits automatically, or make empirical claims.

Raw phrase hits are not interpreted evidence. Classified treatment variables must be built only after manual or otherwise validated labels are stored separately from `data/extracted/phrase_hits.csv`.

## Unit Of Observation

Primary unit:

- Issuer-filing-window: one `cik` or security-linked issuer, one accession number, one filing date, and one forward return window.

Supporting units:

- Issuer-filing: used for text exposure, phrase counts, and first-hit timing.
- Raw phrase hit: used only for validation, classification, and phrase-level audit.
- Issuer-year: used only for robustness checks where filings are collapsed to annual observations.

The primary timing anchor is SEC filing date. If EDGAR acceptance time and market-close timing are later available, the preferred price anchor is the first tradable close after the filing became public.

## Treatment Definitions

### Raw-Hit Treatment

`raw_hit_i,t = 1` for issuer-filing `i,t` if the filing has at least one raw phrase hit in `data/extracted/phrase_hits.csv`.

Variants:

- Any-section raw hit.
- Business-section raw hit only.
- Excluding likely high-false-positive categories.
- Category-specific raw-hit indicators.

Raw-hit treatment is a dictionary exposure measure only. It does not imply that the filing substantively describes access expansion.

### Classified True-Positive Treatment

`classified_true_positive_i,t = 1` if at least one reviewed hit in the filing is labeled `true_positive_access_expansion` under `config/classification_guidelines.md`.

Use this treatment only after:

- Review labels are locked.
- Reviewer agreement or adjudication rules are documented.
- The classified-hit table preserves raw `hit_id`, label, confidence, reviewer notes, reviewer identity or anonymized reviewer ID, and classification-run metadata.

### First-Hit Event Treatment

`first_hit_event_i,t = 1` for the first filing in which issuer `i` has a raw or classified treatment, depending on the specification.

Rules:

- Define first event separately for raw-hit and classified true-positive treatments.
- Use all available prior sample filings for the issuer to determine whether a hit is first observed in sample.
- If the first observed filing for an issuer already has a hit, mark first-event status as `left_censored_first_observed_hit` in robustness checks.

### Intensity Treatment

Intensity can be measured at issuer-filing level as:

- `raw_hit_count`: number of raw phrase hits in the filing.
- `category_count`: number of distinct categories with raw hits.
- `phrase_count`: number of distinct phrases hit.
- `section_count`: number of sections with hits.
- `classified_true_positive_count`: number of reviewed true-positive hits after classification.

Pre-specified transformations:

- `log1p(raw_hit_count)`.
- Indicator bins: 0, 1, 2-4, 5+ hits.
- Winsorized count at the 99th percentile after return data linkage, documented before model estimation.

## Control Group Definitions

Primary control group:

- Issuer-filings in the same filing-year sample with no raw phrase hit.

Classified-control group:

- Issuer-filings with reviewed hits not labeled `true_positive_access_expansion`, plus issuer-filings with no raw hits, depending on the classification sample design.

Within-issuer control group:

- Earlier or later filings by the same issuer without the treatment of interest, used in firm fixed-effects specifications.

Matched-control option:

- Untreated issuer-filings matched on pre-filing observables such as filing year, industry, size proxy, exchange, prior returns, volatility, book-to-market or valuation proxy if available, and prior filing-level text controls.

Do not drop missing return observations silently. Missingness and right-censoring must be represented with reason codes.

## Outcomes

Forward raw returns:

- `ret_1y`: 1-year forward return from filing anchor.
- `ret_3y`: 3-year forward return from filing anchor.
- `ret_5y`: 5-year forward return from filing anchor.

Forward benchmark-adjusted or excess returns:

- `excess_ret_1y = ret_1y - benchmark_ret_1y`.
- `excess_ret_3y = ret_3y - benchmark_ret_3y`.
- `excess_ret_5y = ret_5y - benchmark_ret_5y`.

Return source and adjustment policy must be recorded before estimation:

- Price return versus total return.
- Split and dividend adjustment.
- Delisting treatment.
- Currency and trading calendar.
- Start and end price realization dates.

## Right-Censoring Rules

As of 2026-06-29:

- A 1-year window is observable only if the target date is on or before 2026-06-29.
- A 3-year window is observable only if the target date is on or before 2026-06-29.
- A 5-year window is observable only if the target date is on or before 2026-06-29.

If the target date is after 2026-06-29, set status to `WINDOW_NOT_MATURE_AS_OF_2026_06_29`.

Other non-complete statuses must be explicit:

- `SECURITY_LINK_UNRESOLVED`
- `START_PRICE_MISSING`
- `END_PRICE_MISSING`
- `DELISTING_RETURN_UNAVAILABLE`
- `MERGER_OR_ACQUISITION`
- `BANKRUPTCY_OR_LIQUIDATION`
- `BENCHMARK_PRICE_MISSING`
- `PROVIDER_UNAVAILABLE_OR_LICENSE_RESTRICTED`

Right-censored windows must not be treated as zero returns, poor returns, or missing at random.

## Benchmark Candidates

Pre-specified benchmark families:

- Broad US equity market benchmark: CRSP value-weighted market return, Russell 3000 total return, or S&P 500 total return, depending on licensed data availability.
- Financial-sector benchmark: financial-sector total-return index, a financial-sector ETF return series, or a CRSP/Compustat financial-sector portfolio.
- Fintech-oriented benchmark: use only if point-in-time construction, investability, and survivorship-bias controls can be documented.

Primary benchmark preference:

1. CRSP value-weighted market return and CRSP financial-sector portfolio if available.
2. Total-return index series with documented methodology if CRSP is unavailable.
3. ETF proxy only as a sensitivity analysis, because ETF history, fees, and composition may not match the issuer universe.

Benchmark selection must be locked before looking at return results.

## Baseline Specifications

For filing `f`, issuer `i`, filing year `t`, window `w`, and outcome `R`:

```text
R_i,t,w = alpha + beta * Treatment_i,t + gamma' X_i,t + FE + epsilon_i,t,w
```

Baseline descriptive specifications:

- Raw return on raw-hit indicator by window.
- Excess return on raw-hit indicator by window.
- Raw return on classified true-positive indicator by window, after labels are locked.
- Excess return on classified true-positive indicator by window, after labels are locked.

Controls may include:

- Filing year.
- Section extraction status flags.
- Hit category indicators for category-specific models.
- Firm size, book-to-market, profitability, leverage, prior returns, and volatility only after a validated point-in-time source is available.

Standard errors:

- Cluster by issuer where panel structure permits.
- Consider two-way clustering by issuer and filing year if sample size supports it.

## Fixed Effects

Use fixed effects according to identification needs and sample support:

- Year fixed effects: absorb sample-wide filing-year return conditions.
- Firm fixed effects: compare treated and untreated filings within the same issuer.
- Industry fixed effects: control for persistent differences across industry groups.
- Industry-year fixed effects: absorb sector-year shocks when industry data are available and cell sizes are adequate.

Firm fixed effects require within-issuer treatment variation. If many treated issuers are always treated after first use, report limited within-firm support.

## Event-Study Style Specifications

For first-hit events, define event time by issuer filing order or calendar filing year relative to first treated filing.

Event-study indicators:

- Leads: `k = -3, -2, -1`
- Event filing: `k = 0`
- Lags: `k = +1, +2, +3`

Preferred event-study outcome:

- Forward returns by filing window for each event-time filing, with year and firm fixed effects where feasible.

Pre-trend check:

- Lead coefficients should be reported for descriptive diagnostics.
- Evidence of differential pre-event outcomes weakens any causal interpretation.

## Matched-Control Or Propensity-Score Robustness

Optional robustness:

- Estimate propensity for raw-hit or classified treatment using only pre-filing variables.
- Match treated filings to untreated filings within filing year and industry where possible.
- Use nearest-neighbor or caliper matching, with balance diagnostics reported before outcome comparison.

Candidate matching variables, if available:

- Prior-year return.
- Prior-year volatility.
- Market capitalization or size proxy.
- Exchange.
- Industry.
- Filing year.
- Prior text length and section extraction status.
- Prior raw-hit history.

Matching is a robustness design, not a substitute for a credible identification strategy.

## Placebo Tests

Pre-specified placebo checks:

- Use future treatment status to predict pre-filing returns.
- Assign placebo event dates to untreated firms within the same filing year and industry.
- Test low-signal phrase categories separately, such as generic `market access`, `retail investors`, and `individual investors`.
- Use sections where language is more likely to be risk disclosure, especially risk-factor-only hits.

## Pre-Trend Checks

Before interpreting post-filing associations:

- Compare treated and control issuers' prior 1-year returns where observable.
- Compare prior volatility and size proxies where available.
- Compare pre-event filing text intensity for issuers with multiple filings.
- In event-study specifications, report lead coefficients and confidence intervals.

## Falsification Tests

Falsification tests should include:

- Pre-event return windows ending before the filing date.
- Low-signal phrases and high false-positive-risk categories from the taxonomy.
- Hits labeled `risk_disclosure_only`, `operational_access_or_platform_language`, or `false_positive`, after classification.
- Randomly permuted treatment within filing year and industry.

## Multiple-Testing Controls

Primary outcome family:

- `ret_1y`, `ret_3y`, `ret_5y`, `excess_ret_1y`, `excess_ret_3y`, `excess_ret_5y`.

Primary treatment family:

- Raw-hit indicator.
- Classified true-positive indicator.
- First-hit event indicator.
- Intensity treatment.

Controls:

- Report all tested windows and treatment variants.
- Use false-discovery-rate control within planned outcome families.
- Label exploratory category, section, and subgroup tests clearly.
- Do not select a benchmark after seeing which benchmark gives the preferred result.

## Interpretation Standards

Evidence supporting descriptive association:

- Pre-specified treatment, control, outcome, and benchmark definitions.
- Complete accounting for right-censored and missing return windows.
- Consistent estimates across raw and benchmark-adjusted returns, or a documented explanation for differences.
- Reported uncertainty, sample sizes, and missingness reason codes.
- Classification validation showing how often raw hits are substantive, ambiguous, or false-positive contexts.

Additional assumptions needed for causal interpretation:

- Treatment timing is conditionally independent of unobserved determinants of future returns after controls and fixed effects.
- No unmeasured contemporaneous firm shocks jointly drive access-related language and future returns.
- Security-linking and return data are not differentially missing by treatment.
- Classification errors are not systematically related to later return outcomes.
- The chosen benchmark and control group represent the relevant counterfactual return path.

## Claims Not Allowed

- No causal claims without a separately justified identification strategy.
- No claims about management intent, sincerity, operational effectiveness, customer impact, or real-world access expansion beyond what the filing text states.
- No claim that raw phrase hits are substantively positive without classification or audit evidence.
- No claim that missing or right-censored return windows are complete observations.
- No claim that absence of a raw phrase hit means absence of access-related strategy or language.
- No conclusion should use the word `causes` unless a separate identification strategy has been approved.
