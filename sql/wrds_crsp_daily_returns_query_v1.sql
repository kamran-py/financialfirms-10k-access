-- WRDS CRSP daily returns query template v1
--
-- Purpose:
--   Pull daily CRSP returns for resolved event-window PERMNOs.
--
-- Usage:
--   1. After resolving links locally, load mature resolved window rows into a
--      WRDS temporary table named project_resolved_windows.
--   2. Required columns:
--      event_window_id, event_id, permno, window_start_search_date,
--      target_calendar_end_date, horizon_years.
--   3. Export results to data/returns/wrds_crsp_daily_returns_raw_v1.csv.

select
    w.event_window_id,
    w.event_id,
    w.horizon_years,
    w.permno,
    w.window_start_search_date::date as window_start_search_date,
    w.target_calendar_end_date::date as target_calendar_end_date,
    d.date,
    d.ret,
    d.dlret,
    d.prc,
    d.shrout,
    d.vol,
    d.cfacpr,
    d.cfacshr,
    case
        when d.ret is not null and d.dlret is not null then ((1 + d.ret) * (1 + d.dlret) - 1)
        when d.ret is null and d.dlret is not null then d.dlret
        else d.ret
    end as ret_with_delisting
from project_resolved_windows w
join crsp.dsf d
    on d.permno = w.permno
   and d.date >= w.window_start_search_date::date
   and d.date <= w.target_calendar_end_date::date + interval '10 days'
order by w.event_window_id, d.date;
