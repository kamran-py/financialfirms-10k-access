# Security Linking And Return Window Prep V1 Report

Generated as of 2026-06-29.

## Guardrails

- No prices were fetched.
- No returns were computed.
- No benchmark data were loaded.
- No SEC requests were made.
- No empirical performance claims were made.

## Purpose

This stage prepares identifier-linking and return-window scaffolds after validated treatment construction. It does not assign a final price identifier. Current ticker and CIK are preserved, but all securities remain `pending_price_identifier` until a point-in-time security master or price source is selected.

## Outputs

- `data/linking/security_link_candidates_v1.csv`
- `data/linking/filing_security_link_scaffold_v1.csv`
- `data/returns/return_window_scaffold_v1.csv`

## Counts

- Unique firm link candidates: 655
- Filing link rows: 5,954
- Return-window scaffold rows: 17,862
- Treated filing rows: 182
- Untreated/control filing rows: 5,772

## Filing Link Status Counts

| Security link status | Filing rows |
| --- | --- |
| pending_price_identifier | 5954 |

## Return Window Status Counts

| Horizon years | Pre-price return-window status | Rows |
| --- | --- | --- |
| 1 | pending_security_link_and_price_data | 5901 |
| 1 | right_censored_as_of_2026-06-29 | 53 |
| 3 | pending_security_link_and_price_data | 4627 |
| 3 | right_censored_as_of_2026-06-29 | 1327 |
| 5 | pending_security_link_and_price_data | 3417 |
| 5 | right_censored_as_of_2026-06-29 | 2537 |

## Treated Return Window Status Counts

| Horizon years | Pre-price return-window status | Treated rows |
| --- | --- | --- |
| 1 | pending_security_link_and_price_data | 180 |
| 1 | right_censored_as_of_2026-06-29 | 2 |
| 3 | pending_security_link_and_price_data | 139 |
| 3 | right_censored_as_of_2026-06-29 | 43 |
| 5 | pending_security_link_and_price_data | 94 |
| 5 | right_censored_as_of_2026-06-29 | 88 |

## Link Status By Filing Year

| Filing year | Security link status | Filing rows |
| --- | --- | --- |
| 2015 | pending_price_identifier | 451 |
| 2016 | pending_price_identifier | 460 |
| 2017 | pending_price_identifier | 472 |
| 2018 | pending_price_identifier | 488 |
| 2019 | pending_price_identifier | 507 |
| 2020 | pending_price_identifier | 526 |
| 2021 | pending_price_identifier | 557 |
| 2022 | pending_price_identifier | 600 |
| 2023 | pending_price_identifier | 616 |
| 2024 | pending_price_identifier | 629 |
| 2025 | pending_price_identifier | 648 |

## Methodological Notes

- Ticker alone is not treated as a resolved return-security identifier.
- The project still needs a price/security source decision before fetching returns.
- Primary security rule is not final until the selected data source exposes share class, delisting, corporate-action, and adjusted-return fields.
- Right-censored rows are retained in the scaffold and must not be treated as observed returns.

## Input Integrity

- `filing_index.csv` before: `1396bd2909f1020a9d50cef996b079f865c15c4daef5f7d0660e3262d04a476d`
- `filing_index.csv` after: `1396bd2909f1020a9d50cef996b079f865c15c4daef5f7d0660e3262d04a476d`
- `filing_index.csv` unchanged: yes
- `firm_universe.csv` before: `3eaaf45d0fd487a2c405ffc11f8972670dfc0440e3cbb5b171bf9e6905539d2a`
- `firm_universe.csv` after: `3eaaf45d0fd487a2c405ffc11f8972670dfc0440e3cbb5b171bf9e6905539d2a`
- `firm_universe.csv` unchanged: yes
- `validated_conservative_filing_treatments_v1.csv` before: `35665f1470c476837b2da9f863ba87941fbd253884309bf968ca74aae5049308`
- `validated_conservative_filing_treatments_v1.csv` after: `35665f1470c476837b2da9f863ba87941fbd253884309bf968ca74aae5049308`
- `validated_conservative_filing_treatments_v1.csv` unchanged: yes

## Next Gate

Select the return/security data source and benchmark source. If the next step requires SEC requests, use the approved SEC user-agent. If the next step uses a market-data provider, first document its identifier, corporate-action, delisting, adjusted-price, and benchmark limitations.
