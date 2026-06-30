# Next Steps for a Publication-Grade Version

This document lists the major upgrades required before the project could credibly become a publishable empirical finance paper.

## 1. Rebuild the Firm Universe

Replace the current-listed SEC ticker universe with a point-in-time security universe.

Requirements:

- Use CRSP/Compustat/security-master data.
- Include firms active at any point from 2015-2025.
- Preserve delisted, merged, acquired, bankrupt, renamed, and ticker-changed firms.
- Maintain point-in-time CIK, ticker, GVKEY, PERMNO, and PERMCO links where available.
- Rebuild the 10-K filing index from this corrected universe.
- Compare old versus new universe coverage.

This is the highest-priority fix.

## 2. Recompute Treatment and Return Windows

After rebuilding the universe:

- rerun EDGAR filing discovery,
- rerun section extraction,
- rerun phrase matching,
- rerun conservative treatment construction,
- rerun manual validation checks if the distribution shifts materially,
- rebuild CRSP/WRDS return windows.

Do not reuse old treatment counts as final if the universe changes.

## 3. Classify Exit Modes

Add CRSP delisting and corporate-action data to distinguish:

- observed active windows,
- M&A exits,
- performance-related delistings,
- bankruptcy/liquidation,
- other delistings,
- unresolved data gaps.

Run differential-exit diagnostics by treatment status.

## 4. Upgrade Benchmarks and Controls

Add robustness beyond broad-market excess returns:

- Fama-French factor-adjusted returns,
- size/style matched benchmarks,
- industry or subindustry benchmarks,
- prior-return and volatility controls,
- point-in-time accounting controls where feasible.

Controls must be imported and documented before model estimation.

## 5. Add Stronger Empirical Designs

Potential specifications:

- filing-year fixed effects,
- firm fixed effects where treatment variation supports them,
- industry-year fixed effects,
- first-treatment event-time designs,
- placebo text categories,
- pre-trend checks,
- matched-control designs.

Any causal language would still require a credible identification strategy beyond these observational designs.

## 6. Improve Inference

For final tables:

- rerun wild-cluster-bootstrap inference with 9,999 replications,
- consider Webb weights for few-treated-cluster horizons,
- report treated and control issuer-cluster counts,
- report minimum detectable effects,
- report equivalence-test thresholds only where justified before formal interpretation.

## 7. Write a Real Manuscript

A publication-grade version needs:

- literature review,
- positioning relative to textual disclosure and return-predictability research,
- construct-validity discussion,
- sample construction section,
- data appendix,
- treatment-validation appendix,
- return-methodology appendix,
- limitations section.

## Publication Readiness Assessment

Current version:

- auditability: strong,
- treatment-construction discipline: strong,
- empirical-finance identification: preliminary,
- sample-frame quality: insufficient for publication,
- publishable-paper readiness: not yet.

The next publication-grade version should start with the point-in-time universe rebuild.
