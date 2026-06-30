# Market Data Source Plan

Version: `market_data_source_plan_v1`

Date: 2026-06-29

## Source Decision

Primary return/security source: WRDS CRSP, with Compustat/CRSP linking where available.

Fallback/cross-check source: FactSet, if WRDS linking or delisting coverage is incomplete for specific issuers.

Public web price sources should not be used as the primary source for the main research design because historical ticker changes, delisting returns, share-class resolution, and survivorship controls are weaker.

## Why WRDS/CRSP Is Primary

WRDS/CRSP is preferred because it supports:

- point-in-time PERMNO security identifiers
- CRSP share codes and exchange codes
- dated Compustat-CRSP links through GVKEY/PERMNO
- daily returns
- delisting returns where available
- clear return-status and missingness accounting
- benchmark series through CRSP market indexes

This better matches the project's econometric requirements than using current tickers alone.

## Primary Linking Rule

Preferred linking path:

1. Use filing CIK to identify Compustat `gvkey`.
2. Use the CRSP/Compustat link table to identify `permno` active at the 10-K filing date.
3. Keep links with common accepted link types and primary-link flags.
4. Join to CRSP names at the filing date and prefer ordinary common shares.
5. Mark unresolved or multiple plausible securities explicitly rather than dropping them.

Candidate filters:

- `linktype in ('LC', 'LU', 'LS')`
- `linkprim in ('P', 'C')`
- filing date between `linkdt` and `linkenddt`, treating missing `linkenddt` as open-ended
- CRSP share code `shrcd in (10, 11)` when available

If multiple securities survive the rule, mark `multiple_share_class_ambiguous` unless a documented primary-security rule resolves the case.

## Return Convention

Event date: 10-K filing date.

Window start: nearest CRSP trading day on or after the filing date.

Window end: nearest CRSP trading day on or after the 1-, 3-, or 5-year calendar anniversary, if the window is mature as of 2026-06-29.

Issuer return: compounded CRSP daily return over the window, incorporating delisting return where CRSP provides it.

Delisting handling:

- If CRSP `dlret` is present on a date, combine it with `ret` as `(1 + ret) * (1 + dlret) - 1`.
- If `ret` is missing but `dlret` is present, use `dlret`.
- If a security delists before the target end date and no delisting return is available, status must not be `observed`; it must be a documented delisting or price-unavailable status.

## Benchmark Convention

Primary benchmark for first implementation: CRSP value-weighted market return with dividends, matched to the same trading-date window.

Secondary benchmark to develop after the first successful WRDS pull: financial-sector benchmark or matched portfolio, depending on available CRSP/Compustat fields and support.

Raw returns may be retained as descriptive outcomes, but benchmark-adjusted returns should be the primary outcome family.

## Guardrails

- Do not use current ticker alone as a resolved price identifier.
- Do not drop failed links, delistings, unavailable prices, or right-censored windows.
- Do not compute or inspect returns before the WRDS input, linking output, and status reports are created.
- Do not use FactSet or public sources to patch failed WRDS links without recording source and reason.
- Do not make causal claims from return outcomes unless a separate identification strategy is later established.
