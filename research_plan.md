# Research Plan

## Objective

Build a reproducible filing-level dataset of US-listed financial and fintech-related firms' Form 10-K filings for filing years 2015 through 2025. The dataset will identify filing language about expanding, democratizing, broadening, or lowering barriers to access for financial products, credit, housing, banking, investing, markets, or institutional-grade services. It will then measure subsequent stock performance 1, 3, and 5 years after each filing date where those return windows are observable as of 2026-06-27.

This project is descriptive unless a separate, pre-specified research design justifies causal interpretation.

## Scope

- Filing type: Form 10-K, including 10-K/A only if a later design decision explicitly includes amendments.
- Filing years: 2015-2025, based on SEC filing date unless revised by design decision.
- Issuers: US-listed financial and fintech-related firms.
- Text unit: filing section and phrase-level excerpt.
- Price outcomes: post-filing total or price returns over 1, 3, and 5 years, depending on selected market data source and adjustment policy.
- Benchmark outcomes: raw returns and, if benchmark data are available, excess returns against pre-specified market and financial-sector benchmarks.
- As-of date: 2026-06-27.

## Primary Research Questions

1. Which firms and filing sections contain exact language related to expanding access to financial products, credit, housing, banking, investing, markets, or institutional-grade services?
2. How frequently does this language appear by filing year, firm type, section, and phrase family?
3. How do subsequent 1-, 3-, and 5-year stock returns differ across filings with and without these raw phrase hits?
4. How do results differ when using interpreted/classified access-language categories rather than raw exact phrase hits?

The first three questions can be answered descriptively. Any statement that the language caused later stock performance is out of scope unless supported by a separate identification strategy.

## Unit Of Observation

The canonical unit is one issuer-filing:

- `cik`
- accession number
- filing date
- filing URL
- filing year

Phrase hits are stored at the excerpt level and linked back to the issuer-filing. Return observations are stored at the filing-window level.

## Data Sources

Planned sources:

- SEC EDGAR submissions and filing documents for 10-K metadata and text.
- SEC company identifiers or entity metadata for CIK and ticker linkage where available.
- A market data source for adjusted prices or total returns. The final provider remains unresolved.
- Point-in-time reference data for exchange, SIC/NAICS, listing status, delisting status, corporate actions, security identifiers, ticker changes, name changes, mergers, bankruptcies, and index membership.
- Benchmark data for broad market and financial-sector indexes. Constituents and benchmark definitions must be point-in-time when used for sample construction or classification.

No filings or prices should be downloaded until the design artifacts are approved.

## Firm Universe Construction

The proposed universe should be constructed before text analysis and saved with inclusion and exclusion reasons. The universe must be point-in-time: a firm can enter because it was US-listed during the sample period even if it later delisted, merged, went bankrupt, changed name, changed ticker, or left an index.

Candidate inclusion logic:

- US-listed common equity or equivalent primary listed security.
- Financial-sector SIC or NAICS codes, plus fintech-related firms not captured by traditional financial-sector codes.
- Exchanges likely including NYSE, Nasdaq, and NYSE American.
- Firms with at least one 10-K filed between 2015-01-01 and 2025-12-31.
- Firms that were listed during the relevant filing year, not only firms listed or active as of 2026.

Candidate exclusion logic:

- Non-US issuers unless explicitly included.
- Funds, ETFs, closed-end funds, SPAC shells, blank-check companies, and trusts unless explicitly included.
- Duplicate share classes unless a primary security rule is chosen.
- Filings without extractable text are not excluded silently; they remain with extraction reason codes.

Index membership must not be used with current constituents unless the research question explicitly studies current-constituent survivorship. If index membership is used, membership dates and source vintage must be stored, and firm eligibility must be evaluated as of the filing date.

## Filing Collection Plan

For each issuer-year:

1. Resolve issuer identity and CIK.
2. Query 10-K filings for filing dates from 2015-01-01 through 2025-12-31.
3. Store accession number, filing date, acceptance datetime if available, fiscal year end or report period, filing URL, primary document URL, and metadata.
4. Extract text from the primary 10-K document.
5. Segment text into auditable sections where possible.
6. Record all missing, amended, duplicate, malformed, or unavailable filings with reason codes.

The primary timing variable for return measurement is the EDGAR filing date and acceptance datetime, not fiscal year end. Fiscal year end is stored for descriptive grouping and robustness checks. Any analysis by fiscal year must be labeled as such and must not be mixed silently with filing-year analysis.

## Text Identification Plan

Raw exact phrase hits must remain separate from interpreted/classified hits.

Raw hit layer:

- Deterministic phrase matching against a controlled phrase taxonomy.
- Store exact matched phrase, normalized phrase, phrase family, section, character offsets where available, and an excerpt.
- Preserve enough context to audit the match without reprocessing the full filing.
- Track known false-positive risk flags such as generic "market access", risk-factor hypotheticals, litigation language, customer quotes, boilerplate, negative statements, and unrelated infrastructure usage.

Interpreted/classified layer:

- Classify whether each raw hit appears to describe access expansion, inclusion, barrier reduction, democratization, broadening, affordability, or availability.
- Classification may be rule-based, model-assisted, or human-coded, but every classification requires method, version, label, confidence or score, and audit fields.
- The interpreted layer cannot overwrite or replace the raw hit layer.
- Interpreted classifications must include a label for non-access or ambiguous usage. Absence of that label is not evidence of access expansion.

## Return Measurement Plan

Returns are measured after the filing date for 1-, 3-, and 5-year windows.

Window observability as of 2026-06-27:

- 1-year return is observable only when the target date is on or before 2026-06-27.
- 3-year return is observable only when the target date is on or before 2026-06-27.
- 5-year return is observable only when the target date is on or before 2026-06-27.
- Unobservable windows remain in the dataset with reason code `WINDOW_NOT_MATURE_AS_OF_DATE`.
- Right-censored windows must be reported as right-censored, not as poor performance, zero returns, or missing-at-random observations.

Price measurement details to resolve:

- Use filing date close, next trading day close, or event-time convention using EDGAR acceptance datetime.
- Use adjusted close, total return, CRSP returns, or another source.
- Handle ticker changes, delistings, mergers, bankruptcies, name changes, and exchange changes consistently through security-identifier histories and corporate-action tables.
- Validate adjusted price quality against splits, dividends, stale prices, missing trading days, extreme returns, and provider restatements.
- Pre-specify broad market and financial-sector benchmark choices before comparing excess returns.
- Keep price-source metadata attached to each return observation.

## Bias And Validity Risks

Survivorship bias:

- Include delisted, merged, bankrupt, renamed, and ticker-changed firms if they were listed and filed during the sample period.
- Do not construct the universe from current index members, current tickers, or currently active listings unless explicitly labeled as a survivorship-biased sensitivity analysis.
- Record missing market data, delisting events, merger outcomes, bankruptcy events, and unresolved security links instead of dropping affected observations.

Selection bias:

- Save firm-universe construction rules and all inclusion/exclusion reason codes.
- Maintain a candidate universe table separate from the final included universe.
- Store index membership and industry classification as dated attributes. Do not use future index membership or future industry classification to determine filing-date eligibility.

Look-ahead bias:

- Use only information available on or before each filing date for classification features that are intended to be contemporaneous.
- Return-window eligibility must be evaluated against the fixed as-of date, 2026-06-27.
- Do not let later stock performance, later litigation, later press coverage, later index changes, or later firm outcomes influence text classification.
- Keep EDGAR filing date, acceptance datetime, report period, and fiscal year end as separate fields.

Measurement bias:

- Keep raw phrase hits separate from interpreted classifications.
- Version phrase dictionaries and classification rules.
- Record extraction failures and section-parsing uncertainty.
- Report phrase-level false positive rates from manual audit samples before interpreting classified access language.
- Do not treat failed section extraction as evidence that a phrase is absent from a section.

Semantic overreach:

- Treat filing language as disclosure text, not proof of actual product availability, customer impact, or managerial intent.
- Require excerpt-level evidence before describing the language as access-expansion language.
- Use neutral terms such as "access-related wording" until classification and validation support a stronger description.

Multiple testing and narrative risk:

- Pre-specify primary phrase families, classification labels, return windows, benchmark returns, and subgroup comparisons before analysis.
- Label exploratory tests clearly.
- Report the full tested family of outcomes and comparisons, not only statistically significant or narratively convenient results.
- Use multiple-testing adjustments or false-discovery controls for families of related tests.

## Claims We Are Not Allowed To Make

- We are not allowed to claim that access-expansion language causes later stock returns without a separate causal design.
- We are not allowed to claim management intent, sincerity, or actual operational access expansion beyond what the filing text states.
- We are not allowed to claim a return window exists when its target end date is after 2026-06-27.
- We are not allowed to treat right-censored return windows, delistings, mergers, bankruptcies, or missing prices as ordinary complete observations.
- We are not allowed to infer that absence of a raw phrase hit means absence of access-related strategy or practice.
- We are not allowed to infer that a raw phrase hit is substantively about expanding access without classification or audit evidence.
- We are not allowed to compare returns to a benchmark selected after looking at results without labeling the comparison exploratory.
- We are not allowed to present cherry-picked phrase families, sections, subperiods, or return horizons as confirmatory evidence.

## Minimum Evidence Required Before Interpretation

Before interpreting any relation between filing language and later stock performance, the project must have:

- A point-in-time firm universe with counts of included, excluded, delisted, merged, bankrupt, renamed, and unresolved firms.
- Filing metadata tied to CIK, accession number, filing date, acceptance datetime where available, fiscal year end or report period, and filing URL.
- A documented security-link history that handles ticker changes, name changes, delistings, mergers, bankruptcies, and unresolved links.
- A reason-code summary proving that no filing, extraction, price, or return-window row was silently dropped.
- Raw phrase hits stored separately from interpreted classifications, with taxonomy and matcher versions.
- Manual or otherwise validated evidence on false positives and ambiguous contexts before relying on interpreted access-language labels.
- Section-extraction status and confidence, including explicit treatment of section failures.
- Price-source documentation, adjusted-price validation checks, and corporate-action handling.
- Pre-specified benchmark definitions and benchmark-source provenance.
- A multiple-testing plan and a list of all tested primary and exploratory comparisons.

## Deliverables After Design Approval

Later implementation should produce:

- Raw metadata tables.
- Raw filing text and/or deterministic text extraction artifacts.
- Phrase-hit tables.
- Classification tables.
- Price and return-window tables.
- Reproducible logs and reason-code summaries.
- Descriptive analysis notebooks or scripts.

These later deliverables should not be created during the current planning step.
