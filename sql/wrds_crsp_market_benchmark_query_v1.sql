-- WRDS CRSP market benchmark query template v1
--
-- Purpose:
--   Pull CRSP value-weighted market return with dividends for the date range
--   needed by event windows.
--
-- Usage:
--   Set the date bounds to the min window start search date and max target
--   calendar end date plus a trading-day buffer from the local request file.
--   Export results to data/returns/wrds_crsp_market_benchmark_raw_v1.csv.

select
    date,
    vwretd,
    vwretx,
    ewretd,
    ewretx,
    sprtrn
from crsp.dsi
where date >= DATE '2015-01-01'
  and date <= DATE '2026-07-15'
order by date;
