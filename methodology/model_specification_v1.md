# Model Specification V1

This specification is locked before running regressions or event-study estimates.

## Analysis Unit

- Unit: issuer-filing-window.
- Event date: SEC 10-K filing date.
- Horizons: 1-year, 3-year, and 5-year forward windows.
- Main analysis sample: rows with `model_sample_main == 1` in `data/analysis/regression_modeling_dataset_v1.csv`.

## Treatment

- Main treatment: `treatment_main`, equal to the validated conservative filing-level access-expansion treatment.
- This is the V3 conservative treatment that passed manual validation.
- Raw phrase hits, failed V2 labels, and tiered V1 labels are not main treatments.

## Primary Outcome

- `outcome_primary_excess_vwretd_winsor_p01_p99`: issuer compounded return minus CRSP value-weighted market return with dividends, winsorized within horizon at p01/p99.
- Raw non-winsorized `outcome_primary_excess_vwretd_raw` must be reported as a sensitivity check.

## Secondary Outcomes

- `outcome_secondary_raw_return_winsor_p01_p99` for unadjusted return comparisons.
- Alternative benchmark-adjusted outcomes using `vwretx`, `ewretd`, and `sprtrn` only as robustness checks.

## Baseline Estimation Plan

Estimate separate cross-sectional panel models by horizon:

```text
Y_{i,f,h} = alpha_h + beta_h * Treatment_{i,f} + FilingYearFE_f + epsilon_{i,f,h}
```

- Run this separately for 1-year, 3-year, and 5-year horizons.
- Cluster standard errors by issuer using `cluster_issuer`.
- Interpret estimates as conditional associations, not causal effects.

## Secondary Pooled Specification

A pooled horizon specification may be used only as a compact summary:

```text
Y_{i,f,h} = alpha + beta * Treatment_{i,f} + HorizonFE_h + FilingYearFE_f + epsilon_{i,f,h}
```

- Cluster by issuer.
- Do not use pooled results as the sole headline because horizons have different censoring and return distributions.

## Firm Fixed Effects

- Firm fixed-effects models are exploratory unless within-issuer treatment variation is sufficient.
- Support must be reported from `data/analysis/model_sample_support_v1.csv` before any firm-FE result is interpreted.
- If support is limited, firm-FE estimates should be described as low-power diagnostics.

## Controls

- Baseline controls are filing-year fixed effects only, because point-in-time accounting controls have not yet been imported.
- Size, book-to-market, leverage, profitability, prior returns, and volatility require a separate WRDS/Compustat/CRSP control-import checkpoint before use.
- No control should be added after viewing regression results unless labeled exploratory.

## Prohibited Claims

- Do not claim treatment caused later returns.
- Do not claim disclosure language proves actual product expansion, customer outcomes, or management intent.
- Do not treat right-censored, link-failed, or non-computed windows as ordinary complete observations.

## Required Reporting

- Report sample size by horizon and treatment.
- Report filing-year treatment support.
- Report raw and winsorized primary outcomes.
- Report missing/non-computed status counts inherited from prior checkpoints.
- Report long-horizon caution for 3-year and 5-year windows.
