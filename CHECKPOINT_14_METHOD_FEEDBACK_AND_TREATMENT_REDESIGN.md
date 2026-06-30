# CHECKPOINT 14: Method Feedback And Treatment Redesign

Generated at: 2026-06-29T15:48:17.5385957-04:00

## Completed

- Incorporated external methodological feedback into the research design.
- Incorporated the failed full-corpus V2 spot check into treatment-definition planning.
- Created construct-validity addendum.
- Created stricter treatment-definition plan.
- Created return-methodology addendum.
- Created censoring and linking protocol.
- Updated the pre-analysis plan to block treatment construction until revised classification passes validation.
- Preserved raw and classified data files unchanged.

## Files Created

- `methodology/construct_validity_addendum.md`
- `methodology/treatment_definition_plan.md`
- `methodology/return_methodology_addendum.md`
- `methodology/censoring_and_linking_protocol.md`
- `CHECKPOINT_14_METHOD_FEEDBACK_AND_TREATMENT_REDESIGN.md`

## Files Modified

- `methodology/pre_analysis_plan.md`

## Explicit Non-Actions

- No prices fetched.
- No returns computed.
- No return analysis run.
- No benchmark outcomes loaded.
- No SEC requests made.
- No empirical performance claims made.
- No modification of `data/extracted/phrase_hits.csv`.
- No final treatment variables constructed.
- No classifier revision performed in this stage.

## Data File Integrity

- Raw `data/extracted/phrase_hits.csv` SHA256: `ba511bf32939b78c7d15b6518c7fba78cee3e7e6357b49bfef21f90d18288054`
- Classified `data/classified/phrase_hits_classified_v2.csv` SHA256: `7a7dff2df2b59e6d4655729db9ac6e49c8bc2a68577dc8ccfa5d765b17334898`
- Raw file unchanged: yes
- Classified file unchanged: yes

## Professor Feedback Points Incorporated

- Raw keyword hits are candidate signals, not evidence.
- The `access-expansion narrative` is not a single homogeneous construct.
- Access language must be separated into economically distinct narrative subcategories before return analysis.
- Phrase meaning can drift across the 2015-2025 sample, especially around 2020-2021 retail trading, crypto, and fintech language.
- Calendar-time and vintage confounding must be addressed before interpreting return comparisons.
- Raw returns alone are insufficient; benchmark-adjusted or excess returns should be primary.
- Sector, subsector, and size matching or controls are needed where point-in-time data support them.
- Long-horizon 3-year and 5-year BHARs require caution because of skewness, overlapping windows, cross-correlation, and inflated naive test statistics.
- Barber & Lyon 1997 and Mitchell & Stafford 2000 should be cited later as methodological cautions for long-horizon abnormal-return inference.
- Identifier linking from CIK/ticker to PERMNO or equivalent must be auditable.
- Delistings, acquisitions, failures, missing prices, and right-censored windows must be status-coded rather than dropped silently.
- Claims should remain descriptive or associational unless a separate identification strategy is established.

## Failed V2 Spot-Check Implications

Full-corpus V2 failed the pre-specified precision threshold:

- Spot-check sample: 150 rows.
- Sampled V2 positives: 100.
- Confirmed positives: 55.
- Positive precision: 55.0%.
- Required precision threshold: 85.0%.
- Disagreements: 59 / 150.
- False-negative rate among sampled V2 non-positives: 12.0%.

Implications:

- Full-corpus V2 must not be used as the treatment variable.
- Full-corpus V2 remains only a candidate and diagnostic classification layer.
- Treatment construction must wait for stricter classification rules, reclassification or filtering, and successful post-revision validation.
- The main revision need is reducing over-called positives, especially in high-risk phrase families.

## Updated Treatment-Tier Framework

Tier 1: Conservative Main Treatment

- High-confidence true positives only.
- Must identify an external beneficiary.
- Must identify a direct financial-access mechanism.
- Must assign a narrative subcategory.
- Excludes high-risk phrases unless context rules explicitly validate them.
- Excludes generic regulatory boilerplate unless issuer action or substantive access mechanism is clear.
- Intended as the main treatment only after revised validation passes.

Tier 2: Broader Validated Treatment

- Includes high- and medium-confidence true positives from a revised, validated classifier.
- Includes validated CRA/regulatory language when beneficiary and access mechanism are clear.
- Includes repeated mission language only when a financial-access mechanism is explicit.
- Intended as a secondary or robustness treatment.

Tier 3: Exploratory Raw-Signal Treatment

- Includes raw phrase hits or broad classifier positives.
- Used only for robustness or sensitivity analysis.
- Never used for main conclusions or described as substantive access-expansion evidence.

## Narrative Subcategories Added

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

## High-Risk Phrase Families Requiring Stricter Handling

- `affordable housing`
- `fractional share`
- `market access`
- `access to markets`
- `capital markets access`
- `institutional quality`
- `institutional-grade`
- `institutional caliber`
- `institutional level`
- `access to credit`
- `lower barriers`
- `reduce barriers`
- `reduced barriers`
- `removing barriers`
- `eliminate barriers`

## Open Methodological Risks

- Revised classification may still have phrase-family-specific false positives unless high-risk rules are tightened and revalidated.
- Narrative subcategories may have limited sample support after conservative filtering.
- 2020-2021 language vintage may remain correlated with fintech, crypto, retail-trading, and rate-cycle exposure.
- Public price data may have incomplete delisting returns, ticker histories, and multiple-share-class resolution if CRSP/WRDS or equivalent data are unavailable.
- Long-horizon returns may remain sensitive to benchmark choice, overlapping windows, censoring, and delisting assumptions.
- Treatment and link failures may be differentially distributed by issuer type, filing year, or narrative subcategory.

## Updated Return-Methodology Requirements

- Benchmark-adjusted or excess returns are primary; raw returns are descriptive.
- Filing-year and calendar-time controls are required.
- 2020-2021 vintage effects must be reported.
- Sector, subsector, and size-matched benchmarks or controls should be used where point-in-time data permit.
- Event-time returns should be supplemented with calendar-time portfolio methods where feasible.
- 3-year and 5-year BHARs require explicit long-horizon-return cautions.
- Language must remain `associated with`, `conditional on`, or `followed by`; do not use `caused by` or `led to`.

## Censoring And Linking Requirements Added

Return-window status flags:

- `observed`
- `right_censored`
- `delisted_acquired`
- `delisted_failure`
- `delisted_unknown`
- `ticker_or_cik_link_failed`
- `price_unavailable`
- `IPO_too_recent`
- `multiple_share_class_ambiguous`
- `benchmark_unavailable`

Required preserved identifiers:

- CIK.
- Ticker at filing date where available.
- Accession number.
- Filing date.
- Price identifier used.
- CIK/ticker/PERMNO or equivalent link status and failures.

## Next Recommended Stage

Revise the classification rules and treatment-candidate construction logic before building treatment variables. The next stage should:

- Convert the treatment-definition plan into revised classification rules.
- Apply stricter high-risk phrase handling.
- Add narrative subcategory assignment.
- Reclassify or filter full-corpus V2 candidate positives under the revised rules.
- Produce a new validation sample that oversamples high-risk phrase positives, all sections, high-count firms, and filing years.
- Require at least 85% sampled positive precision before treatment construction proceeds.

## Guardrail Reminder

Returns, prices, benchmark outcomes, and empirical performance analysis remain off-limits until treatment classification is revised, revalidated, and approved, and until treatment construction is complete under the updated methodology.
