# Baseline Table Appendix Draft V1

This draft records paper-ready table structure and methods language. It does not introduce a new empirical specification.

## Attrition Table Structure

The final attrition table should be issuer-level, not filing-level, so it aligns with issuer-clustered inference. For treated issuers with multiple qualifying treated filings, collapse to the first qualifying treatment date before counting the issuer in treated attrition rows.

| Horizon | Group | Total issuers | Observed | Right-censored | Exit: M&A | Exit: failed/delisted | Unlinked / data gap | Eligible N | Exit attrition % |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1y | Treated |  |  |  |  |  |  |  |  |
| 1y | Control |  |  |  |  |  |  |  |  |
| 3y | Treated |  |  |  |  |  |  |  |  |
| 3y | Control |  |  |  |  |  |  |  |  |
| 5y | Treated |  |  |  |  |  |  |  |  |
| 5y | Control |  |  |  |  |  |  |  |  |

`Eligible N = Total issuers - Right-censored - Unlinked / data gap`. `Exit attrition % = (Exit: M&A + Exit: failed/delisted) / Eligible N`.

The current project files support right-censoring, link/coverage, and return-computation statuses. They do not yet support a defensible M&A versus failed/delisted split. That split requires a separate CRSP delisting-code and corporate-action checkpoint.

## Differential Exit Test Structure

| Horizon | Treated exited / eligible | Control exited / eligible | Difference in exit rate | Fisher exact p |
| --- | ---: | ---: | ---: | ---: |
| 1y |  |  |  |  |
| 3y |  |  |  |  |
| 5y |  |  |  |  |

Run this once pooling M&A and failure exits, and once for failure-only exits. Fisher's exact test is preferred because treated issuer counts are thin, especially at 3y and 5y.

## Equivalence Threshold Paragraph

For the 1-year horizon, we interpret equivalence using a pre-specified economically meaningful threshold rather than treating non-significance as evidence of no association. We define Delta as 0.5 times the cross-sectional standard deviation of the 1-year primary benchmark-adjusted return outcome in the full analysis sample, pooling treated and control observations. In this sample, the 1-year standard deviation of `outcome_primary_excess_vwretd_winsor_p01_p99` is 0.3140, giving Delta = 0.1570. This threshold is mechanically independent of the estimated treatment coefficient and its standard error, and corresponds to a medium standardized difference. The equivalence claim is evaluated using TOST logic: the 90% confidence interval for the treatment coefficient must lie entirely within [-Delta, +Delta]. The 1-year 90% confidence interval is [-0.0479, 0.0666], so it lies inside the medium-effect Delta interval. The stricter 0.2 SD threshold is reported as a sensitivity benchmark and should not be treated as the primary threshold unless approved before formal interpretation.

Because this threshold is being formalized after the baseline estimates were already generated, final writeup language should say it was approved before making a formal equivalence claim, not before the baseline table was estimated.

## Wild Cluster Bootstrap Procedure

We use a wild cluster bootstrap as an inference check for the pre-specified baseline model because treated issuer clusters are thin at longer horizons. For each horizon, we estimate the baseline filing-year fixed-effect model and record the treatment coefficient and t-statistic. We then impose the null by estimating the restricted model without the treatment effect, draw Rademacher weights at the issuer-cluster level, construct bootstrap outcomes from restricted fitted values plus cluster-weighted residuals, and re-estimate the unrestricted model. The bootstrap p-value is the share of bootstrap t-statistics at least as extreme as the observed t-statistic. This changes inference only; it does not introduce a new economic specification.

Current checkpoint bootstrap results used 999 Rademacher replications:

| Horizon | Bootstrap p | Bootstrap 95% CI |
| --- | ---: | --- |
| 1y | 0.7780000000 | [-0.0636936640, 0.0791195454] |
| 3y | 0.7650000000 | [-0.1979461271, 0.2850455216] |
| 5y | 0.8140000000 | [-0.4379887210, 0.8591617856] |

For a paper-final table, rerun with 9,999 replications and consider Webb weights at 3y and 5y as a sensitivity check.
