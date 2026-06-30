"""WRDS/Jupyter script: pull CRSP daily returns and market benchmark.

Run this inside WRDS JupyterHub after uploading:

- wrds_crsp_return_windows_linked_request_v1.csv
- this script

Outputs:

- wrds_crsp_daily_returns_raw_v1.csv
- wrds_crsp_market_benchmark_raw_v1.csv
- wrds_crsp_return_pull_manifest_v1.txt

This script only pulls raw WRDS data. It does not compute event-window
returns or make empirical claims.
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pandas as pd
import wrds


REQUEST_FILE = Path("wrds_crsp_return_windows_linked_request_v1.csv")
DAILY_OUT = Path("wrds_crsp_daily_returns_raw_v1.csv")
BENCHMARK_OUT = Path("wrds_crsp_market_benchmark_raw_v1.csv")
MANIFEST_OUT = Path("wrds_crsp_return_pull_manifest_v1.txt")

CRSP_DAILY_MAX_DATE = pd.Timestamp("2024-12-31")
PERMNO_CHUNK_SIZE = 500


def sql_int_list(values: list[int]) -> str:
    return ",".join(str(int(value)) for value in values)


def main() -> None:
    if not REQUEST_FILE.exists():
        raise FileNotFoundError(f"Missing {REQUEST_FILE}. Upload it to this Jupyter directory first.")

    windows = pd.read_csv(REQUEST_FILE, dtype=str)
    ready = windows[windows["post_link_return_window_status"] == "ready_for_wrds_daily_return_request"].copy()
    if ready.empty:
        raise ValueError("No ready windows found in request file.")

    ready["permno_int"] = ready["permno"].astype(float).astype(int)
    ready["window_start_search_date_dt"] = pd.to_datetime(ready["window_start_search_date"])
    ready["target_calendar_end_date_dt"] = pd.to_datetime(ready["target_calendar_end_date"])

    min_date = ready["window_start_search_date_dt"].min()
    max_date = ready["target_calendar_end_date_dt"].max() + timedelta(days=10)
    max_date = min(max_date, CRSP_DAILY_MAX_DATE)
    permnos = sorted(ready["permno_int"].dropna().unique().tolist())

    print(f"Ready windows: {len(ready):,}")
    print(f"Unique PERMNOs: {len(permnos):,}")
    print(f"Daily return query range: {min_date.date()} to {max_date.date()}")

    db = wrds.Connection()

    daily_parts = []
    for idx in range(0, len(permnos), PERMNO_CHUNK_SIZE):
        chunk = permnos[idx : idx + PERMNO_CHUNK_SIZE]
        query = f"""
            select permno, date, ret, prc, shrout, vol, cfacpr, cfacshr
            from crsp.dsf
            where permno in ({sql_int_list(chunk)})
              and date >= DATE '{min_date.date()}'
              and date <= DATE '{max_date.date()}'
            order by permno, date
        """
        part = db.raw_sql(query, date_cols=["date"])
        daily_parts.append(part)
        print(f"Pulled PERMNO chunk {idx // PERMNO_CHUNK_SIZE + 1}: {len(part):,} rows")

    daily = pd.concat(daily_parts, ignore_index=True).drop_duplicates()
    daily["dlret"] = pd.NA

    delist_parts = []
    for idx in range(0, len(permnos), PERMNO_CHUNK_SIZE):
        chunk = permnos[idx : idx + PERMNO_CHUNK_SIZE]
        query = f"""
            select permno, dlstdt as date, dlret
            from crsp.dsedelist
            where permno in ({sql_int_list(chunk)})
              and dlstdt >= DATE '{min_date.date()}'
              and dlstdt <= DATE '{max_date.date()}'
            order by permno, dlstdt
        """
        try:
            part = db.raw_sql(query, date_cols=["date"])
        except Exception as exc:
            print(f"Delisting-return query failed on chunk {idx // PERMNO_CHUNK_SIZE + 1}: {exc}")
            part = pd.DataFrame(columns=["permno", "date", "dlret"])
        delist_parts.append(part)

    delist = pd.concat(delist_parts, ignore_index=True).drop_duplicates()
    if not delist.empty:
        daily = daily.merge(delist, on=["permno", "date"], how="outer", suffixes=("", "_from_delist"))
        daily["dlret"] = daily["dlret_from_delist"].combine_first(daily["dlret"])
        daily = daily.drop(columns=["dlret_from_delist"])

    daily["ret_with_delisting"] = daily["ret"]
    both = daily["ret"].notna() & daily["dlret"].notna()
    dl_only = daily["ret"].isna() & daily["dlret"].notna()
    daily.loc[both, "ret_with_delisting"] = (1 + daily.loc[both, "ret"]) * (1 + daily.loc[both, "dlret"]) - 1
    daily.loc[dl_only, "ret_with_delisting"] = daily.loc[dl_only, "dlret"]
    daily.to_csv(DAILY_OUT, index=False)
    print(f"Saved {DAILY_OUT}: {len(daily):,} rows")

    benchmark_query = f"""
        select date, vwretd, vwretx, ewretd, ewretx, sprtrn
        from crsp.dsi
        where date >= DATE '{min_date.date()}'
          and date <= DATE '{max_date.date()}'
        order by date
    """
    benchmark = db.raw_sql(benchmark_query, date_cols=["date"])
    benchmark.to_csv(BENCHMARK_OUT, index=False)
    print(f"Saved {BENCHMARK_OUT}: {len(benchmark):,} rows")

    manifest = [
        "WRDS CRSP Return Pull Manifest V1",
        "",
        "Guardrails:",
        "- Raw WRDS daily returns pulled only for windows marked ready_for_wrds_daily_return_request.",
        "- No event-window returns computed.",
        "- No empirical claims made.",
        "",
        f"Input request file: {REQUEST_FILE}",
        f"Ready windows: {len(ready):,}",
        f"Unique PERMNOs: {len(permnos):,}",
        f"Min query date: {min_date.date()}",
        f"Max query date: {max_date.date()}",
        f"Daily return rows: {len(daily):,}",
        f"Delisting return rows: {len(delist):,}",
        f"Benchmark rows: {len(benchmark):,}",
        f"Daily output: {DAILY_OUT}",
        f"Benchmark output: {BENCHMARK_OUT}",
    ]
    MANIFEST_OUT.write_text("\n".join(manifest), encoding="utf-8")
    print(f"Saved {MANIFEST_OUT}")


if __name__ == "__main__":
    main()
