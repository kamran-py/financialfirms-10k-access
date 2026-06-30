# Return Analysis Panel Validation V1 Report

## Guardrails

- This step prepared an analysis-ready panel and diagnostics only.
- No regressions, hypothesis tests, event-study estimates, or empirical claims were made.
- Upstream computed return-window data were preserved unchanged.

## Inputs

- `data/returns/wrds_crsp_window_returns_v1.csv`

## Outputs

- `data/analysis/return_analysis_panel_v1.csv`
- `data/analysis/return_winsorization_thresholds_v1.csv`
- `data/analysis/return_outlier_tail_diagnostics_v1.csv`
- `methodology/return_outlier_winsorization_policy_v1.md`

## Reconciliation

- Input return-window rows: 8,291
- Expected rows from checkpoint 28: 8,291
- Output analysis panel rows: 8,291
- Computed rows: 8,238
- Expected computed rows from checkpoint 28: 8,238
- Computed treated rows: 294
- Expected computed treated rows from checkpoint 28: 294

## Uniqueness Checks

- Duplicate `event_window_id` values: 0
- Duplicate `event_id` plus `horizon_years` combinations: 0

## Return Computation Status Counts

| Return computation status | Rows |
| --- | --- |
| computed | 8,238 |
| not_computed_missing_issuer_return_inside_window | 26 |
| not_computed_raw_coverage_incomplete | 27 |

## Treatment And Status Counts

| Treatment | Return computation status | Rows |
| --- | --- | --- |
| 0 | computed | 7,944 |
| 0 | not_computed_missing_issuer_return_inside_window | 26 |
| 0 | not_computed_raw_coverage_incomplete | 27 |
| 1 | computed | 294 |

## Analysis Sample Coverage By Horizon And Treatment

| Horizon years | Treatment | Analysis sample status | Rows |
| --- | --- | --- | --- |
| 1 | 0 | analysis_ready_computed_return | 3,580 |
| 1 | 0 | not_analysis_ready_not_computed_missing_issuer_return_inside_window | 7 |
| 1 | 0 | not_analysis_ready_not_computed_raw_coverage_incomplete | 7 |
| 1 | 1 | analysis_ready_computed_return | 138 |
| 3 | 0 | analysis_ready_computed_return | 2,605 |
| 3 | 0 | not_analysis_ready_not_computed_missing_issuer_return_inside_window | 10 |
| 3 | 0 | not_analysis_ready_not_computed_raw_coverage_incomplete | 10 |
| 3 | 1 | analysis_ready_computed_return | 93 |
| 5 | 0 | analysis_ready_computed_return | 1,759 |
| 5 | 0 | not_analysis_ready_not_computed_missing_issuer_return_inside_window | 9 |
| 5 | 0 | not_analysis_ready_not_computed_raw_coverage_incomplete | 10 |
| 5 | 1 | analysis_ready_computed_return | 63 |

## Numeric Field Checks For Computed Rows

| Outcome field | Computed rows with missing/non-numeric value |
| --- | --- |
| issuer_raw_return_compounded | 0 |
| excess_return_vs_vwretd | 0 |
| excess_return_vs_vwretx | 0 |
| excess_return_vs_ewretd | 0 |
| excess_return_vs_ewretx | 0 |
| excess_return_vs_sprtrn | 0 |

## Diagnostics By Horizon

| Horizon years | Outcome | N | Mean | SD | P01 | P50 | P99 | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | issuer_raw_return_compounded | 3718 | 0.1339168712 | 1.6137758747 | -0.8012105744 | 0.0513961785 | 1.4467440491 | -0.9975532119 | 74.6437725523 |
| 1 | excess_return_vs_vwretd | 3718 | 0.0127353935 | 1.5907121502 | -0.8479286600 | -0.0412219654 | 1.1130019511 | -1.2509129934 | 73.8172410752 |
| 3 | issuer_raw_return_compounded | 2698 | 0.3739284632 | 0.8748981788 | -0.8946484957 | 0.2530338568 | 2.8685584734 | -0.9991765656 | 16.3552083248 |
| 3 | excess_return_vs_vwretd | 2698 | -0.0197990182 | 0.8569370958 | -1.2502939409 | -0.1418336824 | 2.4207979388 | -1.4819857336 | 15.5548508402 |
| 5 | issuer_raw_return_compounded | 1822 | 0.6245270252 | 1.2803382839 | -0.9291347307 | 0.3792228826 | 5.3254540111 | -0.9998404987 | 21.7697428720 |
| 5 | excess_return_vs_vwretd | 1822 | -0.1395434065 | 1.2516302082 | -1.7230815285 | -0.3360820815 | 4.2679141550 | -2.1353824536 | 20.6954865403 |

## Diagnostics By Horizon And Treatment

| Horizon years | Treatment | Outcome | N | Mean | SD | P01 | P50 | P99 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | issuer_raw_return_compounded | 3580 | 0.1349306698 | 1.6411426597 | -0.7980989142 | 0.0536414817 | 1.4278476361 |
| 1 | 0 | excess_return_vs_vwretd | 3580 | 0.0137770718 | 1.6179859643 | -0.8486906323 | -0.0399458745 | 1.0813099697 |
| 1 | 1 | issuer_raw_return_compounded | 138 | 0.1076168766 | 0.5436100737 | -0.7799869246 | 0.0018324932 | 1.7992839681 |
| 1 | 1 | excess_return_vs_vwretd | 138 | -0.0142878558 | 0.5117248851 | -0.7371739237 | -0.0867609959 | 1.6343373669 |
| 3 | 0 | issuer_raw_return_compounded | 2605 | 0.3659131654 | 0.7999557883 | -0.9007860445 | 0.2538701400 | 2.8506483118 |
| 3 | 0 | excess_return_vs_vwretd | 2605 | -0.0275886420 | 0.7834068959 | -1.2617453657 | -0.1402727659 | 2.3461145377 |
| 3 | 1 | issuer_raw_return_compounded | 93 | 0.5984429864 | 2.0672894802 | -0.7786135905 | 0.2018411274 | 12.9440765388 |
| 3 | 1 | excess_return_vs_vwretd | 93 | 0.1983942096 | 2.0264261984 | -1.1762306159 | -0.2512045146 | 12.3382350131 |
| 5 | 0 | issuer_raw_return_compounded | 1759 | 0.6059120627 | 1.1580028281 | -0.9356047292 | 0.3823002142 | 4.6606923155 |
| 5 | 0 | excess_return_vs_vwretd | 1759 | -0.1591071151 | 1.1270561543 | -1.6947377560 | -0.3349848969 | 3.9629316621 |
| 5 | 1 | issuer_raw_return_compounded | 63 | 1.1442685964 | 3.1367992343 | -0.8592250998 | 0.2879454636 | 14.6294153992 |
| 5 | 1 | excess_return_vs_vwretd | 63 | 0.4066877608 | 3.1112675293 | -1.8449168910 | -0.4033843021 | 13.9162973692 |

## Filing-Year Diagnostics

Filing-year diagnostics were generated in memory for validation coverage. Detailed year-level returns should be used as diagnostics only until formal specifications are approved.

| Filing year | Horizon years | Outcome | N | Mean | P50 |
| --- | --- | --- | --- | --- | --- |
| 2015 | 1 | issuer_raw_return_compounded | 340 | -0.0106460763 | 0.0159284098 |
| 2015 | 1 | excess_return_vs_vwretd | 340 | 0.0473300754 | 0.0752469460 |
| 2015 | 3 | issuer_raw_return_compounded | 337 | 0.6269516195 | 0.5925337776 |
| 2015 | 3 | excess_return_vs_vwretd | 337 | 0.2867513239 | 0.2517310935 |
| 2015 | 5 | issuer_raw_return_compounded | 337 | 0.5235966071 | 0.3998674628 |
| 2015 | 5 | excess_return_vs_vwretd | 337 | 0.0593757015 | -0.0624142165 |
| 2016 | 1 | issuer_raw_return_compounded | 356 | 0.4300104905 | 0.4247596347 |
| 2016 | 1 | excess_return_vs_vwretd | 356 | 0.1905909329 | 0.1949465420 |
| 2016 | 3 | issuer_raw_return_compounded | 356 | 0.6654755161 | 0.5872029760 |
| 2016 | 3 | excess_return_vs_vwretd | 356 | 0.1730461658 | 0.0980271225 |
| 2016 | 5 | issuer_raw_return_compounded | 355 | 1.1972598774 | 0.8795369902 |
| 2016 | 5 | excess_return_vs_vwretd | 355 | 0.0166349637 | -0.2914618200 |
| 2017 | 1 | issuer_raw_return_compounded | 364 | 0.1522585691 | 0.1061630250 |
| 2017 | 1 | excess_return_vs_vwretd | 364 | -0.0034037306 | -0.0492016126 |
| 2017 | 3 | issuer_raw_return_compounded | 364 | 0.1114102008 | -0.0428022795 |
| 2017 | 3 | excess_return_vs_vwretd | 364 | -0.1601599959 | -0.3075446172 |
| 2017 | 5 | issuer_raw_return_compounded | 363 | 0.6715280127 | 0.3747247634 |
| 2017 | 5 | excess_return_vs_vwretd | 363 | -0.1724612258 | -0.4650175135 |
| 2018 | 1 | issuer_raw_return_compounded | 376 | 0.0063511559 | -0.0297089984 |
| 2018 | 1 | excess_return_vs_vwretd | 376 | -0.0386985993 | -0.0676828014 |
| 2018 | 3 | issuer_raw_return_compounded | 375 | 0.3396988135 | 0.1441072147 |
| 2018 | 3 | excess_return_vs_vwretd | 375 | -0.1938715898 | -0.3757625303 |
| 2018 | 5 | issuer_raw_return_compounded | 373 | 0.3238062950 | 0.1854535936 |
| 2018 | 5 | excess_return_vs_vwretd | 373 | -0.1808295826 | -0.3160758938 |
| 2019 | 1 | issuer_raw_return_compounded | 399 | -0.0608938163 | -0.0799218056 |
| 2019 | 1 | excess_return_vs_vwretd | 399 | -0.1135930678 | -0.1430683940 |
| 2019 | 3 | issuer_raw_return_compounded | 398 | 0.4675556431 | 0.2841474172 |
| 2019 | 3 | excess_return_vs_vwretd | 398 | -0.0669213047 | -0.2411539259 |
| 2019 | 5 | issuer_raw_return_compounded | 394 | 0.4362043406 | 0.1489081951 |
| 2019 | 5 | excess_return_vs_vwretd | 394 | -0.3809904843 | -0.6667946809 |
| 2020 | 1 | issuer_raw_return_compounded | 426 | 0.6969958858 | 0.2690950802 |
| 2020 | 1 | excess_return_vs_vwretd | 426 | 0.3121611018 | -0.1181002198 |
| 2020 | 3 | issuer_raw_return_compounded | 424 | 0.4252841185 | 0.3017806467 |
| 2020 | 3 | excess_return_vs_vwretd | 424 | 0.0674411066 | -0.0444411007 |
| 2021 | 1 | issuer_raw_return_compounded | 449 | 0.0890860655 | 0.1131103288 |
| 2021 | 1 | excess_return_vs_vwretd | 449 | 0.0346344246 | 0.0463367649 |
| 2021 | 3 | issuer_raw_return_compounded | 444 | 0.0592771033 | 0.0273060303 |
| 2021 | 3 | excess_return_vs_vwretd | 444 | -0.1860757825 | -0.2246237864 |
| 2022 | 1 | issuer_raw_return_compounded | 497 | -0.1098892136 | -0.0715823424 |
| 2022 | 1 | excess_return_vs_vwretd | 497 | -0.0484953105 | -0.0143525391 |
| 2023 | 1 | issuer_raw_return_compounded | 511 | 0.0638363710 | 0.0030258100 |
| 2023 | 1 | excess_return_vs_vwretd | 511 | -0.1955155699 | -0.2617834463 |

## Input Integrity

- `wrds_crsp_window_returns_v1.csv` before: `001f897f6250e8afe808637df89718a2645ec8ee1726608bd0582ec8b9609312`
- `wrds_crsp_window_returns_v1.csv` after: `001f897f6250e8afe808637df89718a2645ec8ee1726608bd0582ec8b9609312`
- `wrds_crsp_window_returns_v1.csv` unchanged: yes
