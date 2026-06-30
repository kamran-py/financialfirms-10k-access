# Project Tasks

## Phase 0: Design Lock

- [ ] Confirm firm-universe definition for "financial and fintech-related."
- [ ] Confirm whether filing year means SEC filing-date year or fiscal year-end year.
- [ ] Confirm whether 10-K/A amendments are included, excluded, or separately flagged.
- [ ] Select market data source and return convention.
- [ ] Select broad market and financial-sector benchmarks before analysis.
- [ ] Define point-in-time treatment for index membership and industry classification.
- [ ] Define handling rules for ticker changes, name changes, exchange changes, delistings, mergers, bankruptcies, and duplicate share classes.
- [ ] Define right-censoring rules for unobservable return windows as of 2026-06-27.
- [ ] Approve reason-code taxonomy.
- [ ] Approve raw phrase taxonomy and classification labels.
- [ ] Decide whether interpreted classifications will be rule-based, human-coded, model-assisted, or hybrid.
- [ ] Freeze primary hypotheses, phrase families, return windows, benchmarks, subgroup cuts, and multiple-testing plan.

## Phase 1: Repository And Reproducibility Setup

- [ ] Create directory structure after approval.
- [ ] Add environment specification.
- [ ] Add configuration files for sample period, as-of date, and source endpoints.
- [ ] Add logging conventions.
- [ ] Add data dictionary.
- [ ] Add claims-control checklist covering prohibited claims and minimum evidence thresholds.
- [ ] Add test inventory template to separate confirmatory and exploratory tests.
- [ ] Add test fixture policy using small synthetic or public-domain examples.

## Phase 2: Universe Construction

- [ ] Build candidate issuer universe.
- [ ] Resolve CIK, historical ticker, current ticker, company names, exchange, security identifier, SIC/NAICS, and listing-period metadata.
- [ ] Collect or import dated ticker changes, name changes, exchange changes, delistings, mergers, bankruptcies, and security identifier changes.
- [ ] Collect point-in-time index membership if index membership is used anywhere in sample construction or analysis.
- [ ] Assign inclusion/exclusion flags and reason codes.
- [ ] Preserve candidate universe before filtering.
- [ ] Verify the universe is not constructed from current tickers, current active listings, or current index constituents unless explicitly labeled as a sensitivity analysis.
- [ ] Produce a universe audit report with counts by inclusion reason and exclusion reason.
- [ ] Produce counts for delisted, merged, bankrupt, renamed, ticker-changed, and unresolved-security firms.

## Phase 3: Filing Metadata Collection

- [ ] Query SEC metadata for all candidate CIKs.
- [ ] Identify 10-K filings with filing dates from 2015-01-01 through 2025-12-31.
- [ ] Store filing metadata, accession numbers, URLs, EDGAR filing dates, acceptance datetimes, fiscal year ends or report periods, and primary documents.
- [ ] Record missing filings by issuer-year with reason codes.
- [ ] Detect duplicates, amendments, and document-type ambiguity.
- [ ] Keep EDGAR filing date, acceptance datetime, fiscal year end, and filing year as separate fields.

## Phase 4: Filing Text Extraction

- [ ] Download filings only after design approval.
- [ ] Save raw source document metadata and checksums.
- [ ] Extract text from HTML or text filing documents.
- [ ] Segment filings into sections where feasible.
- [ ] Store extraction method, version, status, and failure reason.
- [ ] Preserve failed extraction rows.
- [ ] Store section confidence, unknown-section buckets, and section-failure reason codes.
- [ ] Add tests for section parsing failures, malformed filings, tables, exhibits, and repeated navigation text.

## Phase 5: Raw Phrase Matching

- [ ] Implement exact phrase taxonomy with versioning.
- [ ] Match phrases deterministically against filing text.
- [ ] Store every raw match with phrase, section, excerpt, offsets, accession number, and filing URL.
- [ ] Store zero-hit filings explicitly.
- [ ] Add tests for phrase matching, casing, punctuation, and boundary behavior.
- [ ] Add false-positive flags for generic, negative, boilerplate, quote, risk-factor, litigation, historical, and unrelated-access contexts.
- [ ] Build an audit sample of raw hits and non-hits before interpreting access-language prevalence.

## Phase 6: Interpreted Classification

- [ ] Define classification labels and codebook.
- [ ] Include non-access, ambiguous, negative-context, and boilerplate labels in the codebook.
- [ ] Classify raw phrase hits without modifying raw hit records.
- [ ] Store method, version, label, confidence/score, and reviewer/model metadata.
- [ ] Support multiple classification runs per raw hit.
- [ ] Audit ambiguous and negative-context examples.
- [ ] Validate false-positive and ambiguous-use rates by phrase family and section.
- [ ] Freeze primary classification run before looking at return results.

## Phase 7: Price And Return Data

- [ ] Load price/security metadata from selected provider.
- [ ] Map issuer filings to tradable securities at filing date.
- [ ] Resolve historical security links through ticker changes, name changes, exchange changes, delistings, mergers, bankruptcies, and duplicate share classes.
- [ ] Fetch or import adjusted prices or returns.
- [ ] Fetch or import selected broad market and financial-sector benchmark returns.
- [ ] Validate adjusted price data for split continuity, dividend or total-return treatment, stale prices, duplicate prices, missing dates, currency issues, delisting returns, and extreme returns.
- [ ] Compute 1-, 3-, and 5-year windows only where observable as of 2026-06-27.
- [ ] Preserve right-censored windows, unobservable windows, unresolved security links, delistings, mergers, bankruptcies, and missing-price cases with reason codes.
- [ ] Compute raw and pre-specified benchmark-adjusted returns separately.
- [ ] Record price source, source version, retrieval date, adjustment policy, and corporate-action handling.

## Phase 8: Quality Assurance

- [ ] Verify no silent row dropping from candidate universe through final return table.
- [ ] Reconcile issuer-year counts at every stage.
- [ ] Randomly audit filing URLs, extracted sections, excerpts, and phrase matches.
- [ ] Validate return calculations against provider examples or hand calculations.
- [ ] Check survivorship, selection, index-membership timing, and look-ahead bias risks.
- [ ] Verify no current index membership, current ticker list, or post-filing firm outcome enters filing-date eligibility.
- [ ] Verify right-censored windows are reported and not treated as complete returns.
- [ ] Verify section-restricted analyses disclose section extraction failures and unknown-section counts.
- [ ] Verify claims-control checklist before drafting interpretation.

## Phase 9: Descriptive Analysis

- [ ] Produce counts of filings, hits, and classifications by year and firm category.
- [ ] Produce return summary tables by raw hit status and interpreted class.
- [ ] Clearly mark unobservable windows.
- [ ] Clearly mark right-censored windows and separate them from missing-price failures.
- [ ] Report raw returns and benchmark-adjusted returns using pre-specified benchmarks.
- [ ] Report complete test inventory, including null and unfavorable comparisons.
- [ ] Apply multiple-testing adjustments or false-discovery controls for related test families.
- [ ] Label exploratory analyses separately from frozen primary analyses.
- [ ] Avoid causal language unless a separate design is added.
- [ ] Include robustness checks based on phrase families and section filters.

## Phase 10: Documentation And Archive

- [ ] Freeze schema and data dictionary.
- [ ] Archive source manifests, checksums, and logs.
- [ ] Produce provenance report.
- [ ] Produce limitations section.
- [ ] Produce "Claims We Are Not Allowed To Make" compliance check.
- [ ] Produce "Minimum Evidence Required Before Interpretation" checklist.
- [ ] Package reproducible scripts after implementation is complete.
