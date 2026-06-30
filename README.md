# Access-Expansion Narratives in Financial-Firm 10-Ks

This repository contains a working-paper research pipeline studying whether validated “access-expansion” narratives in U.S. financial and fintech-related firms’ 10-K filings are associated with subsequent stock performance.

The project began from a deliberately cautious research question:

> Can we identify substantive access-expansion language in 10-K filings and evaluate subsequent 1-, 3-, and 5-year stock performance where those return windows are observable?

The current evidence is observational. The project does **not** claim that disclosure language causes later returns.

## Research Design

- Universe: U.S.-listed financial and fintech-related firms.
- Filing years: 2015-2025.
- Documents: annual 10-K filings from SEC EDGAR.
- Text scope: Item 1 Business, Item 1A Risk Factors, and Item 7 MD&A.
- Treatment: validated conservative filing-level access-expansion language.
- Event date: SEC 10-K filing date.
- Outcomes: 1-, 3-, and 5-year forward compounded stock returns.
- Primary outcome: issuer return minus CRSP value-weighted market return with dividends (`vwretd`), winsorized within horizon at p01/p99.
- Baseline model: separate horizon-level regressions with filing-year fixed effects and issuer-clustered standard errors.

## Methodological Guardrails

The workflow is designed to avoid common empirical-finance failure modes:

- Raw phrase hits are not treated as evidence.
- Failed classifiers are rejected rather than scaled into treatment variables.
- Missing, censored, link-failed, and non-computed observations receive explicit status codes.
- Raw returns are preserved; winsorized variables are separate.
- Benchmark-adjusted returns are primary.
- Long-horizon results are treated cautiously because buy-and-hold abnormal returns are noisy and skewed.
- Baseline results are interpreted as conditional associations, not causal estimates.

## Current Baseline Result

The validated conservative treatment is not clearly associated with different subsequent benchmark-adjusted returns in the baseline year-fixed-effect models.

| Horizon | Estimate | Cluster SE | p-value | 95% CI |
| --- | ---: | ---: | ---: | --- |
| 1y | 0.009 | 0.035 | 0.788 | [-0.059, 0.078] |
| 3y | 0.040 | 0.119 | 0.735 | [-0.193, 0.274] |
| 5y | 0.191 | 0.373 | 0.609 | [-0.541, 0.923] |

Inference diagnostics clarify the strength of this null:

- The 1-year estimate is relatively informative. The approximate 80%-power MDE is about 9.7 percentage points.
- The 3-year estimate is less informative. The approximate MDE is about 33.4 percentage points.
- The 5-year estimate is low-information. The approximate MDE is about 104.6 percentage points.
- The increasing point estimates across horizons should not be narrated as a trend because uncertainty grows sharply with horizon.

Wild-cluster-bootstrap inference did not materially alter the baseline interpretation.

## Repository Structure

- `scripts/`: data construction, validation, classification, return computation, and estimation scripts.
- `config/`: phrase and classification guidelines.
- `methodology/`: research design, econometric design, pre-analysis plans, and paper-ready draft components.
- `quality_reports/`: checkpoint reports and validation summaries.
- `CHECKPOINT_*.md`: auditable stage-by-stage project checkpoints.
- `data/analysis/`: aggregate, publication-safe summary tables only.

Raw SEC filings, WRDS/CRSP data, and row-level return panels are intentionally excluded from Git.

## Reproducibility Notes

This repository is a working-paper code and documentation archive. Full regeneration requires:

- SEC EDGAR access with a compliant user-agent.
- WRDS/CRSP access for security links, daily stock returns, market returns, and delisting/corporate-action data.
- Python 3.

The currently published aggregate tables are sufficient to audit the baseline model outputs and inference diagnostics, but not to reconstruct licensed row-level CRSP data.

## Current Limitations

- The baseline design is observational and not causal.
- 3-year and 5-year horizons are less informative because treated clusters thin out and long-horizon returns are noisy.
- M&A versus failure/delisting attrition is not yet fully classified. That requires a separate CRSP delisting-code and corporate-action checkpoint.
- Factor-model or matched-firm benchmarks remain future robustness work.

## Status

Current checkpoint: `CHECKPOINT_34_BASELINE_WRITEUP_COMPONENTS.md`.
