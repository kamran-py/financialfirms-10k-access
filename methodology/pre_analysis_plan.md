# Pre-Analysis Plan

Version: `pre_analysis_plan_v1`

As-of date for return-window observability: 2026-06-29.

## Status Before Return Collection

Completed inputs:

- EDGAR ingestion.
- Section extraction.
- Raw phrase matching.
- Classification guidelines.
- Manual review sample preparation.
- Econometric design pre-specification.

Not yet performed:

- No return data loaded.
- No benchmark returns loaded.
- No empirical return analysis run.
- No SEC requests made in this stage.
- No approved final treatment variables constructed.
- No revised post-failure classifier approved for treatment construction.

Important update after post-scale validation:

- Full-corpus V2 classification was scaled but failed the pre-specified post-scale precision threshold.
- The 150-row full-corpus V2 spot check included 100 sampled V2 positives, of which 55 were confirmed.
- Sampled V2 positive precision was 55.0%, below the required 85.0% threshold.
- Full-corpus V2 must not be used directly as the treatment variable.
- Treatment construction must wait until classification rules are revised, reclassified, and revalidated.

## Research Questions

Primary descriptive questions:

- Which issuer-filings contain raw access-related phrase hits?
- Which raw hits are manually validated as substantive access-expansion language?
- How do future raw and benchmark-adjusted returns differ between treated and control issuer-filings under pre-specified treatment definitions?

Interpretive boundary:

- Raw hits are not interpreted evidence.
- Classified true-positive hits are text evidence only; they do not establish actual access expansion, customer outcomes, management intent, or causal return effects.

## Analysis Sequence

1. Complete manual review of `data/review/phrase_hit_review_sample.csv`.
2. Estimate false-positive, ambiguous, and true-positive rates by phrase, category, year, section, and firm concentration.
3. Revise taxonomy only if documented as a new version; do not overwrite prior raw hits.
4. Build a classified-hit table that preserves raw `hit_id`.
5. Validate the full-corpus classification before any treatment construction.
6. If validation fails, revise classification rules and treatment definitions before constructing treatment variables.
7. Assign validated positives to narrative subcategories and treatment tiers.
8. Validate the revised treatment layer against the pre-specified precision threshold.
9. Load and validate security links, prices, corporate actions, delisting events, and benchmark returns only after treatment classification is approved.
10. Build return-window observations with explicit status and reason codes.
11. Run primary descriptive and econometric specifications.
12. Run robustness, placebo, pre-trend, falsification, and multiple-testing adjustments.
13. Report all planned specifications, missingness, and right-censoring counts.

## Construct Validity And Narrative Subcategories

Raw phrase hits are candidate signals, not evidence. A raw hit records the presence of dictionary language in an excerpt. It does not establish substantive access expansion, product availability, customer impact, management intent, or any relation to future returns.

The broad phrase family previously summarized as an `access-expansion narrative` is not a homogeneous construct. Before return analysis, validated positive hits must be separated into economically distinct narrative subcategories:

- Financial inclusion / underbanked / underserved.
- Consumer credit access.
- Affordable housing / homeownership access.
- Retail investing / brokerage democratization.
- Private-market or alternative-investment access.
- Payments / money movement / SMB commerce access.
- Insurance / benefits access.
- Smaller-issuer capital-market access.
- Fee / cost / minimum-reduction framing.
- Generic/other access-expansion.

Each validated positive must identify an external beneficiary and a direct financial-access mechanism. Narrative subcategories must be preserved in the hit-level and filing-level treatment construction so return analysis does not average over economically distinct strategies without disclosure.

Phrase meanings may drift over 2015-2025. The project must treat 2020-2021 as a high-risk vintage for both text meaning and return interpretation because retail trading, crypto, fintech, low-rate growth narratives, and platform language may have changed how access-related phrases were used.

## Failed V2 Spot Check And Treatment Redesign

Full-corpus V2 failed post-scale validation:

- Spot-check sample size: 150.
- Sampled full-corpus V2 positives: 100.
- Confirmed positives: 55.
- True-positive precision among sampled full-corpus positives: 55.0%.
- Required precision threshold: 85.0%.
- Sampled non-positive false-negative rate: 12.0%.
- Total disagreements: 59 / 150.

Implication:

- Full-corpus V2 must not be used directly as the main treatment variable.
- Full-corpus V2 may be retained only as an auditable candidate layer and diagnostic artifact.
- The next classification stage must reduce over-called positives, especially in high-risk phrase families.
- Treatment construction must not begin until revised rules pass validation.

The dominant V2 failure modes were:

- `affordable housing` in tax-credit, partnership, portfolio, investment-income, sale, commitment-table, and accounting contexts.
- Institutional-quality language describing property quality, custody infrastructure, analyst-process quality, platform quality, or services to institutional/HNW clients.
- `access to credit` describing issuer funding, credit ratings, credit facilities, FHLB borrowing, or liquidity.
- Market-access language describing issuer access, competitor access, prime-broker access, exchange connectivity, market-data fees, or regulatory permissions.

## Conservative Main Treatment Definition

The main treatment must be Tier 1 unless a later approved design change states otherwise.

Tier 1: Conservative Main Treatment:

- High-confidence true positives only.
- Must identify an external beneficiary.
- Must identify a direct financial-access mechanism.
- Must be assigned to a narrative subcategory.
- Exclude high-risk phrases unless context rules explicitly validate them.
- Exclude generic regulatory boilerplate unless issuer action or substantive access mechanism is clear.
- Exclude generic mission language unless the financial-access mechanism is explicit.
- Exclude issuer financing, liquidity, own credit access, own capital-market access, operational access, platform quality, accounting, tax-credit, investment-income, stock-mechanics, and table-artifact contexts.

Tier 2: Broader Validated Treatment:

- Includes high- and medium-confidence true positives from a revised, validated classifier.
- Includes validated regulatory or CRA language only when beneficiary and access mechanism are clear.
- Includes repeated mission language only when financial-access mechanism is explicit.
- Used for secondary or robustness treatment definitions.

Tier 3: Exploratory Raw-Signal Treatment:

- Raw phrase hits or broad classifier positives.
- Used only for robustness and sensitivity analysis.
- Never used for main conclusions.
- Must be labeled raw-signal or exploratory, not substantive access-expansion evidence.

High-risk phrase families require explicit handling before entering Tier 1 or Tier 2:

- `affordable housing`.
- `fractional share`.
- `market access`.
- `access to markets`.
- `capital markets access`.
- `institutional quality`.
- `institutional-grade`.
- `institutional caliber`.
- `institutional level`.
- `access to credit`.
- `lower barriers`.
- `reduce barriers`.
- `reduced barriers`.
- `removing barriers`.
- `eliminate barriers`.

## Vintage And Calendar-Time Confounding

Treatment prevalence and phrase meaning must be reported by filing year before return analysis. The design must not allow filing-year vintage to masquerade as a text effect.

Required safeguards:

- Report treatment counts and rates by filing year and narrative subcategory.
- Report separate support for pre-2020, 2020-2021, and post-2021 filings.
- Include filing-year fixed effects in baseline regressions where sample support permits.
- Use benchmark-adjusted or excess returns as primary outcome comparisons.
- Consider sector, subsector, and size-matched benchmarks or controls when point-in-time data are available.
- Treat 2020-2021 access language as high-risk for semantic drift and macro/vintage confounding.

## Long-Horizon Return Methodology

Raw returns alone are insufficient. Primary return outcomes must be benchmark-adjusted or excess returns after benchmark definitions are locked.

Three-year and five-year buy-and-hold abnormal returns require special caution because long-horizon abnormal returns are sensitive to skewness, overlapping windows, cross-correlation, delisting treatment, and benchmark choice. Barber & Lyon 1997 and Mitchell & Stafford 2000 should be cited later as methodological cautions for long-horizon abnormal-return inference.

Design implications:

- Report raw returns descriptively, but use benchmark-adjusted returns as primary.
- Do not rely on naive cross-sectional t-tests of 3-year or 5-year BHARs as primary evidence.
- Use filing-year controls and issuer clustering where feasible.
- Consider calendar-time portfolio methods for long-horizon robustness if data support them.
- Report all pre-specified windows, not only favorable horizons.
- Treat 3-year and 5-year results as more sensitive to censoring and delisting assumptions than 1-year results.

## Censoring, Delisting, And Identifier Linking

No filing-window observation may disappear silently. Every issuer-filing-window must receive a status flag.

Required return-window status flags:

- `observed`.
- `right_censored`.
- `delisted_acquired`.
- `delisted_failure`.
- `delisted_unknown`.
- `ticker_or_cik_link_failed`.
- `price_unavailable`.
- `IPO_too_recent`.
- `multiple_share_class_ambiguous`.
- `benchmark_unavailable`.

Identifier-linking requirements:

- Preserve CIK.
- Preserve ticker at filing date where available.
- Preserve accession number.
- Preserve filing date.
- Preserve price identifier used, such as PERMNO or equivalent.
- Record all CIK/ticker/PERMNO or equivalent link failures.
- Record multiple-share-class ambiguities.
- Do not drop failed links silently.
- Do not use current ticker or current listing status as a complete historical identifier.

If CRSP/WRDS or an equivalent point-in-time source is unavailable, the project must document limitations of public price data, especially delisting-return coverage, ticker-history coverage, multiple-share-class resolution, and survivorship risk.

## Permitted Claims And Prohibited Claims

Permitted language after approved treatment construction and return analysis:

- `associated with`.
- `conditional on`.
- `followed by`.
- `relative to the benchmark`.
- `within the validated treatment definition`.

Prohibited language without a separate identification strategy:

- `caused by`.
- `led to`.
- `resulted in`.
- `drove`.
- Any claim that the filing language caused later returns.

Additional prohibited claims:

- No claim that raw phrase hits are access-expansion evidence.
- No claim that full-corpus V2 positives are valid treatment observations.
- No claim that disclosure text proves actual product availability, customer impact, or management sincerity.
- No claim that right-censored, delisted, acquired, bankrupt, failed-link, or missing-price windows are ordinary complete observations.
- No empirical performance claim before returns and benchmarks are loaded under the approved protocol.

## Classification Plan

Allowed labels:

- `true_positive_access_expansion`
- `generic_marketing`
- `risk_disclosure_only`
- `customer_access_unrelated_to_finance`
- `operational_access_or_platform_language`
- `ambiguous`
- `false_positive`

The first review batch is 600 raw hits, stratified by category, phrase, filing year, section, and firm. The batch is intended to calibrate reviewers and estimate label distribution before full classification.

If reviewers disagree:

- Preserve all initial labels.
- Add adjudicated label in a separate field.
- Report agreement rates by category and phrase.

Do not use stock returns or later firm outcomes while reviewing text.

## Primary Treatment Variables

Raw-hit treatment:

- `raw_hit_any`: at least one raw phrase hit in a filing.
- `raw_hit_category_[category]`: category-specific raw-hit indicators.

Classified treatment:

- `true_positive_any`: at least one reviewed or adjudicated hit labeled `true_positive_access_expansion`.
- `true_positive_category_[category]`: category-specific true-positive indicators where sample support is adequate.

First-hit event treatment:

- First sample filing for an issuer with `raw_hit_any`.
- First sample filing for an issuer with `true_positive_any`, after classification.

Intensity treatment:

- `raw_hit_count`.
- `log1p(raw_hit_count)`.
- Distinct category count.
- Distinct phrase count.
- Classified true-positive count.

## Control Groups

Primary raw-hit control:

- Issuer-filings with no raw phrase hit.

Primary classified control:

- Issuer-filings with no classified true-positive hit, including no-hit filings and reviewed non-positive hits, with missing review status documented.

Within-firm control:

- Untreated filings by the same issuer where within-issuer variation exists.

Matched-control robustness:

- Untreated filings matched within filing year and industry on pre-filing characteristics after point-in-time covariates are available.

## Outcomes

Primary return outcomes:

- 1-year forward raw return.
- 3-year forward raw return.
- 5-year forward raw return.
- 1-year benchmark-adjusted or excess return.
- 3-year benchmark-adjusted or excess return.
- 5-year benchmark-adjusted or excess return.

Outcome construction must record:

- Filing anchor date.
- Target end date.
- Realized start price date.
- Realized end price date.
- Start and end prices.
- Benchmark start and end values.
- Return-source metadata.
- Window status and reason code.

## Right-Censoring

Use 2026-06-29 as the fixed observability date.

Rules:

- 1-year windows with target date after 2026-06-29 are `WINDOW_NOT_MATURE_AS_OF_2026_06_29`.
- 3-year windows with target date after 2026-06-29 are `WINDOW_NOT_MATURE_AS_OF_2026_06_29`.
- 5-year windows with target date after 2026-06-29 are `WINDOW_NOT_MATURE_AS_OF_2026_06_29`.

Right-censored windows remain in window-status counts and are excluded from completed-window return regressions only with explicit disclosure.

## Benchmark Plan

Primary benchmark candidates, subject to data availability:

- CRSP value-weighted market return or equivalent broad US total-market return.
- CRSP financial-sector portfolio or equivalent financial-sector total-return benchmark.

Sensitivity candidates:

- S&P 500 total return.
- Russell 3000 total return.
- Financial-sector ETF proxy.

Benchmark source and selection must be locked before return results are inspected.

## Baseline Specifications

Primary models:

```text
ForwardReturn_i,t,w = alpha + beta * Treatment_i,t + YearFE_t + epsilon_i,t,w
```

```text
ExcessReturn_i,t,w = alpha + beta * Treatment_i,t + YearFE_t + epsilon_i,t,w
```

Panel models where within-firm support exists:

```text
Outcome_i,t,w = alpha_i + beta * Treatment_i,t + YearFE_t + gamma'X_i,t + epsilon_i,t,w
```

Industry-year specification where industry data and cell sizes support it:

```text
Outcome_i,t,w = beta * Treatment_i,t + IndustryYearFE_ind,t + gamma'X_i,t + epsilon_i,t,w
```

Cluster standard errors by issuer where feasible. Consider issuer and year clustering as a robustness check if sample size supports it.

## Event-Study Plan

For first-hit event analysis:

- Define event filing as `k = 0`.
- Use issuer filing order for event time.
- Include leads `k = -3, -2, -1` and lags `k = +1, +2, +3` when available.
- Report support counts for each event-time bin.

Pre-trend checks use lead coefficients and pre-event returns. Event-study output is descriptive unless a separate identification strategy is approved.

## Robustness And Validation Checks

Classification robustness:

- Compare raw-hit results with classified true-positive results.
- Exclude high-false-positive-risk categories.
- Exclude `risk_disclosure_only`, `operational_access_or_platform_language`, `generic_marketing`, and `false_positive` labels.
- Run category-specific models only where reviewed sample support is adequate.

Matched-control robustness:

- Use propensity-score or nearest-neighbor matching within filing year and industry.
- Report balance before outcome comparisons.

Placebo and falsification tests:

- Future treatment predicting pre-filing returns.
- Randomly assigned treatment within filing year and industry.
- Low-signal phrases and high-risk taxonomy categories.
- Pre-event windows ending before filing date.
- Risk-disclosure-only labels as a negative-control text category.

Multiple-testing controls:

- Report all planned windows, treatments, and benchmarks.
- Apply false-discovery-rate control within the primary outcome family.
- Label exploratory subgroup and category analyses.

## Evidence Standards

Evidence supporting descriptive association requires:

- Locked treatment definitions.
- Validated return-window construction.
- Explicit right-censoring and missingness counts.
- Reported estimates for every planned window and benchmark family.
- Classification validation showing the distribution of true-positive, ambiguous, and false-positive labels.

Additional assumptions for causal interpretation:

- No unobserved firm shocks jointly determine filing language and future returns after controls.
- Treatment timing is conditionally independent of unobserved future-return drivers.
- Missing return data and classification errors are not systematically related to treatment and outcomes.
- The selected control group approximates the relevant counterfactual return path.

## Claims Not Allowed

- No causal claims without a separately justified identification strategy.
- No claims about management intent or sincerity.
- No claims that raw phrase hits are substantively about access expansion without classification.
- No claims about actual customer outcomes or product availability beyond the filing text.
- No claims that right-censored, delisted, merged, bankrupt, or missing-price observations are ordinary complete observations.
- No conclusion should use the word `causes` unless a separate identification strategy has been approved.
