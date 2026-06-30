# Project History and Checkpoint Summary

This document summarizes the main design choices, validation gates, and current findings. The project should be read as a pilot research archive unless and until the sample universe is rebuilt from point-in-time market data.

## 1. Research Question

The project asks whether substantive access-oriented disclosure language in financial and fintech-related firms’ 10-K filings is associated with later stock performance.

The project is observational. It does not claim causation.

## 2. Document Ingestion

The pipeline indexed and downloaded 10-K filings for filing years 2015-2025.

Key artifacts:

- `CHECKPOINT_04_EXTRACTION.md`
- `data/extracted/filing_sections.csv` (excluded from Git)

Core extraction scope:

- Item 1 Business
- Item 1A Risk Factors
- Item 7 MD&A

Extraction output:

- 5,954 discovered 10-K filings.
- 17,862 extracted section rows.

## 3. Phrase Matching

The initial phrase taxonomy searched for language around democratized access, financial inclusion, underserved or underbanked users, retail/institutional access, housing access, credit access, and reduced barriers.

Key artifact:

- `CHECKPOINT_05_PHRASE_MATCHING.md`

Phrase matching output:

- 9,400 raw phrase-hit rows.
- 3,042 unique filings with at least one raw hit.

Raw phrase hits were treated only as candidate signals, not evidence.

## 4. Classification and Treatment Validation

Several broad classifiers were tested and rejected.

Important failed or limited stages:

- V2 full-corpus classification failed post-scale validation.
- Tiered V1 classification failed precision thresholds.

The accepted treatment layer is the validated conservative filing-level treatment from the V3 rule set.

Key artifacts:

- `CHECKPOINT_13_FULL_CORPUS_V2_SPOTCHECK.md`
- `CHECKPOINT_16_TIERED_CLASSIFICATION_AUDIT.md`
- `CHECKPOINT_22_CONSERVATIVE_FILING_TREATMENT_V3_AUDIT.md`
- `CHECKPOINT_23_VALIDATED_CONSERVATIVE_TREATMENTS.md`

Treatment validation:

- Manual audit sample: 150 rows.
- Positive precision: 92%.
- False-negative rate in audit: 0%.
- Final validated conservative treated filings: 182.

## 5. Security Linking and Return Windows

The project used WRDS/CRSP as the primary return source. Filing dates were matched to 1-, 3-, and 5-year forward windows using CRSP trading dates.

Key artifacts:

- `CHECKPOINT_24_SECURITY_LINKING_AND_RETURN_WINDOW_PREP.md`
- `CHECKPOINT_25_WRDS_CRSP_DATA_REQUEST_PLAN.md`
- `CHECKPOINT_26_WRDS_CRSP_LINK_IMPORT_VALIDATION.md`

Security-link validation:

- 5,954 filing events reconciled.
- 4,259 events resolved to ordinary common-share CRSP PERMNOs.
- Link failures and CRSP source-coverage limits were retained with explicit statuses.

## 6. Return Construction

WRDS/CRSP daily returns and benchmark returns were imported locally. Return windows were computed only where coverage checks passed.

Primary return outcome:

- Issuer compounded return minus CRSP value-weighted market return with dividends (`vwretd`).

Key artifacts:

- `CHECKPOINT_27_WRDS_CRSP_RAW_RETURN_IMPORT_VALIDATION.md`
- `CHECKPOINT_28_WRDS_CRSP_WINDOW_RETURNS.md`
- `CHECKPOINT_29_RETURN_ANALYSIS_PANEL_PREP.md`

Return computation:

- 8,291 linked return-window rows carried forward.
- 8,238 computed successfully.
- 53 retained as non-computed with explicit statuses.
- Computed treated windows: 138 one-year, 93 three-year, 63 five-year.

## 7. Baseline Model Specification

The baseline model was locked before estimation.

Model:

```text
Y_{i,f,h} = alpha + beta * Treatment_{i,f} + FilingYearFE_f + error
```

Where:

- `Y` is winsorized benchmark-adjusted return.
- `Treatment` is the validated conservative treatment.
- Standard errors are clustered by issuer.
- Models are estimated separately for 1-, 3-, and 5-year horizons.

Key artifact:

- `CHECKPOINT_30_MODELING_DATASET_AND_SPEC.md`

## 8. Baseline Estimates

Key artifact:

- `CHECKPOINT_31_BASELINE_YEAR_FE_ESTIMATION.md`

| Horizon | Estimate | Cluster SE | p-value | 95% CI |
| --- | ---: | ---: | ---: | --- |
| 1y | 0.009 | 0.035 | 0.788 | [-0.059, 0.078] |
| 3y | 0.040 | 0.119 | 0.735 | [-0.193, 0.274] |
| 5y | 0.191 | 0.373 | 0.609 | [-0.541, 0.923] |

Baseline interpretation:

- No clear conditional association is detected.
- This is not causal evidence.
- Non-significance is not interpreted as proof of no association.

## 9. Power, Inference, and Attrition Diagnostics

Key artifacts:

- `CHECKPOINT_32_POWER_AND_INFERENCE_DIAGNOSTICS.md`
- `CHECKPOINT_33_BASELINE_FINALIZATION_DIAGNOSTICS.md`
- `CHECKPOINT_34_BASELINE_WRITEUP_COMPONENTS.md`

MDE diagnostics:

| Horizon | Approx. MDE | Interpretation |
| --- | ---: | --- |
| 1y | 0.097 | relatively informative |
| 3y | 0.334 | lower power |
| 5y | 1.046 | low-information |

Wild-cluster-bootstrap p-values:

| Horizon | Bootstrap p |
| --- | ---: |
| 1y | 0.778 |
| 3y | 0.765 |
| 5y | 0.814 |

Equivalence:

- The 1-year 90% CI lies inside a medium-effect threshold defined as 0.5 times the 1-year primary-outcome standard deviation.
- The stricter 0.2 SD threshold does not pass.
- 3-year and 5-year equivalence claims remain weak or inappropriate because those horizons are underpowered.

## 10. Current Conclusion

The strongest current conclusion is:

> In this pilot sample and baseline specification, we do not find informative evidence that validated access-oriented disclosure language predicts benchmark-adjusted returns. The 1-year result is the most interpretable and suggests no large short-run association under the pilot design, but the 3-year and 5-year estimates are too imprecise for strong conclusions.

This should be framed as a cautious observational result, not as a causal claim.

## 11. Remaining Work

Recommended next stages:

- Rebuild the firm universe from point-in-time CRSP/Compustat/security-master data.
- Add CRSP delisting-code and corporate-action data to classify M&A versus failed/delisted attrition.
- Run 9,999-replication wild-cluster bootstrap for final tables.
- Consider Webb weights for 3-year and 5-year few-treated-cluster inference.
- Add factor-model or matched-firm benchmark robustness.
- Add point-in-time accounting controls only through a separate validated data-import checkpoint.

Without the point-in-time universe rebuild, this project should not be treated as a publication-ready empirical finance paper.
