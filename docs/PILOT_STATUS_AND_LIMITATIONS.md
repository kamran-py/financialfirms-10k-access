# Pilot Status and Limitations

This repository should be interpreted as a pilot research archive, not as a publication-ready empirical finance paper.

## What This Project Establishes

The current version demonstrates that the workflow is feasible:

- SEC 10-K filings can be ingested and sectioned at scale.
- Access-expansion language can be identified with phrase matching and then filtered through stricter validation.
- Broad or weak classifiers can be rejected when audit evidence does not support them.
- A conservative filing-level treatment can be constructed and manually validated.
- WRDS/CRSP links and return windows can be built with explicit missingness and coverage statuses.
- Baseline association models can be estimated without making causal claims.

The project is strongest as an auditable methodological prototype.

## Main Empirical Limitation

The largest limitation is sample construction.

The original firm universe was built from a current-listed SEC ticker feed as of 2026-06-27 rather than from a point-in-time 2015-2025 CRSP/Compustat/security-master universe. That creates survivorship risk because firms that delisted, merged, failed, or otherwise disappeared before 2026 may be missing or underrepresented.

For a return study, this is a serious limitation. It affects both:

- treatment/control sample construction, and
- interpretation of subsequent stock returns.

The current baseline estimates should therefore be treated as pilot evidence only.

## Current Baseline Result

The baseline year fixed-effect models do not show a statistically clear association between validated conservative access-expansion filings and later benchmark-adjusted stock returns.

| Horizon | Estimate | Cluster SE | p-value | Interpretation |
| --- | ---: | ---: | ---: | --- |
| 1y | 0.009 | 0.035 | 0.788 | relatively informative null |
| 3y | 0.040 | 0.119 | 0.735 | imprecise |
| 5y | 0.191 | 0.373 | 0.609 | low-information |

The 1-year result is the most informative. The 3-year and 5-year estimates have wide confidence intervals, thin treated-cluster support, and long-horizon return noise.

These results are not causal.

## Why This Is Not Yet a Working Paper

This project should not yet be framed as a publication-ready empirical finance paper because:

- the sample universe is not point-in-time,
- the baseline has year fixed effects only,
- firm and industry-year fixed-effect support remains limited,
- factor-model and matched-firm robustness are not yet implemented,
- M&A versus failed/delisted exit modes are not classified,
- treated issuer clusters are thin at 3-year and 5-year horizons,
- the baseline p-values and confidence intervals are not strong enough to motivate a standalone return-predictability claim.

The current evidence is useful, but it is not strong enough to support a broad empirical-finance contribution.

## Appropriate Use

Appropriate uses of this repository:

- research design archive,
- pilot study,
- reproducible pipeline template,
- audit trail for text-treatment construction,
- foundation for a future publication-grade version.

Inappropriate uses:

- claiming access-expansion language causes later returns,
- claiming the null result is definitive,
- treating the 2015-2025 sample as free of survivorship bias,
- presenting the current baseline estimates as a final empirical finance result.

## Bottom Line

The project succeeded as a careful pilot. It should pause here unless the sample frame is rebuilt from point-in-time market data.
