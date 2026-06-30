-- WRDS CRSP/Compustat linking query template v1
--
-- Purpose:
--   Link project filing events to CRSP PERMNO using CIK -> Compustat GVKEY
--   -> CRSP/Compustat link history -> CRSP names at filing date.
--
-- Usage:
--   1. Load data/linking/wrds_crsp_link_input_v1.csv into a temporary WRDS table
--      named project_events with the columns shown below.
--   2. Run this query in WRDS PostgreSQL.
--   3. Export results to data/linking/wrds_crsp_link_output_v1.csv.
--
-- Required temp table columns:
--   event_id, firm_id, cik, ticker_from_project, company_name, accession_number,
--   filing_date, event_date, validated_conservative_treatment,
--   primary_narrative_subcategory

select
    e.event_id,
    e.firm_id,
    e.cik,
    e.ticker_from_project,
    e.company_name,
    e.accession_number,
    e.filing_date::date as filing_date,
    e.event_date::date as event_date,
    e.validated_conservative_treatment,
    e.primary_narrative_subcategory,
    c.gvkey,
    c.conm as compustat_company_name,
    c.tic as compustat_ticker,
    l.lpermno as permno,
    l.lpermco as permco,
    l.linktype,
    l.linkprim,
    l.linkdt,
    l.linkenddt,
    n.ticker as crsp_ticker,
    n.comnam as crsp_company_name,
    n.shrcd,
    n.exchcd,
    n.namedt,
    n.nameendt,
    case
        when l.lpermno is null then 'no_permno_link'
        when n.permno is null then 'permno_without_active_name_at_event_date'
        when n.shrcd not in (10, 11) then 'non_common_share_code'
        else 'candidate_link'
    end as raw_link_status
from project_events e
left join comp.company c
    on ltrim(c.cik, '0') = ltrim(e.cik, '0')
left join crsp.ccmxpf_linktable l
    on c.gvkey = l.gvkey
   and l.linktype in ('LC', 'LU', 'LS')
   and l.linkprim in ('P', 'C')
   and e.event_date::date >= l.linkdt
   and e.event_date::date <= coalesce(l.linkenddt, '2099-12-31'::date)
left join crsp.stocknames n
    on l.lpermno = n.permno
   and e.event_date::date >= n.namedt
   and e.event_date::date <= n.nameendt
order by e.event_id, l.linkprim, l.linktype, n.shrcd, l.lpermno;
