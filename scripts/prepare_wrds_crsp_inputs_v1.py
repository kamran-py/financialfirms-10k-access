"""Prepare WRDS/CRSP input files for security linking and return pulls.

This script does not connect to WRDS, fetch prices, compute returns, make SEC
requests, or make empirical claims. It creates reproducible input CSVs and a
data-request report for the WRDS stage.
"""

from __future__ import annotations

import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_SCAFFOLD = ROOT / "data" / "linking" / "filing_security_link_scaffold_v1.csv"
WINDOW_SCAFFOLD = ROOT / "data" / "returns" / "return_window_scaffold_v1.csv"
SOURCE_PLAN = ROOT / "methodology" / "market_data_source_plan.md"

LINK_INPUT = ROOT / "data" / "linking" / "wrds_crsp_link_input_v1.csv"
WINDOW_REQUEST = ROOT / "data" / "returns" / "wrds_crsp_return_windows_request_v1.csv"
REPORT_OUT = ROOT / "quality_reports" / "wrds_crsp_data_request_plan_v1_report.md"
CHECKPOINT_OUT = ROOT / "CHECKPOINT_25_WRDS_CRSP_DATA_REQUEST_PLAN.md"

csv.field_size_limit(sys.maxsize)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def markdown_table(headers: list[str], rows: list[list[str | int]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main() -> None:
    required = [LINK_SCAFFOLD, WINDOW_SCAFFOLD, SOURCE_PLAN]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")

    hashes_before = {path.name: sha256(path) for path in required}
    link_rows = read_csv(LINK_SCAFFOLD)
    window_rows = read_csv(WINDOW_SCAFFOLD)

    link_input_rows: list[dict[str, str]] = []
    for idx, row in enumerate(link_rows, start=1):
        link_input_rows.append(
            {
                "event_id": f"event_{idx:06d}",
                "firm_id": row["firm_id"],
                "cik": row["cik"],
                "ticker_from_project": row["ticker_from_project"],
                "company_name": row["company_name"],
                "accession_number": row["accession_number"],
                "filing_date": row["filing_date"],
                "event_date": row["event_date"],
                "validated_conservative_treatment": row["validated_conservative_treatment"],
                "primary_narrative_subcategory": row["primary_narrative_subcategory"],
            }
        )

    event_id_by_accession = {row["accession_number"]: row["event_id"] for row in link_input_rows}
    mature_windows = [
        row
        for row in window_rows
        if row["pre_price_return_window_status"] == "pending_security_link_and_price_data"
    ]
    window_request_rows: list[dict[str, str]] = []
    for idx, row in enumerate(mature_windows, start=1):
        event_id = event_id_by_accession[row["accession_number"]]
        window_request_rows.append(
            {
                "event_window_id": f"window_{idx:06d}",
                "event_id": event_id,
                "firm_id": row["firm_id"],
                "cik": row["cik"],
                "ticker_from_project": row["ticker_from_project"],
                "company_name": row["company_name"],
                "accession_number": row["accession_number"],
                "event_date": row["event_date"],
                "window_start_search_date": row["event_date"],
                "target_calendar_end_date": row["target_calendar_end_date"],
                "horizon_years": row["horizon_years"],
                "validated_conservative_treatment": row["validated_conservative_treatment"],
                "primary_narrative_subcategory": row["primary_narrative_subcategory"],
                "pre_price_return_window_status": row["pre_price_return_window_status"],
            }
        )

    link_fields = list(link_input_rows[0].keys())
    window_fields = list(window_request_rows[0].keys())
    write_csv(LINK_INPUT, link_fields, link_input_rows)
    write_csv(WINDOW_REQUEST, window_fields, window_request_rows)

    hashes_after = {path.name: sha256(path) for path in required}

    link_treatment_counts = Counter(row["validated_conservative_treatment"] for row in link_input_rows)
    window_horizon_counts = Counter(row["horizon_years"] for row in window_request_rows)
    treated_window_horizon_counts = Counter(
        row["horizon_years"] for row in window_request_rows if row["validated_conservative_treatment"] == "1"
    )
    year_counts = Counter(row["event_date"][:4] for row in link_input_rows)

    report = [
        "# WRDS CRSP Data Request Plan V1 Report",
        "",
        "## Guardrails",
        "",
        "- No WRDS connection was opened.",
        "- No prices were fetched.",
        "- No returns were computed.",
        "- No benchmark data were loaded.",
        "- No SEC requests were made.",
        "- No empirical performance claims were made.",
        "",
        "## Source Decision",
        "",
        "Primary source: WRDS CRSP with Compustat/CRSP linking. FactSet remains a fallback/cross-check source.",
        "",
        "## Files Created",
        "",
        "- `methodology/market_data_source_plan.md`",
        "- `sql/wrds_crsp_linking_query_v1.sql`",
        "- `sql/wrds_crsp_daily_returns_query_v1.sql`",
        "- `sql/wrds_crsp_market_benchmark_query_v1.sql`",
        "- `data/linking/wrds_crsp_link_input_v1.csv`",
        "- `data/returns/wrds_crsp_return_windows_request_v1.csv`",
        "",
        "## Request Counts",
        "",
        f"- Filing events for WRDS linking: {len(link_input_rows):,}",
        f"- Mature filing-window rows requesting returns after link resolution: {len(window_request_rows):,}",
        f"- Treated filing events: {link_treatment_counts.get('1', 0):,}",
        f"- Untreated/control filing events: {link_treatment_counts.get('0', 0):,}",
        "",
        "## Mature Window Requests By Horizon",
        "",
        markdown_table(["Horizon years", "Mature window requests"], [[k, v] for k, v in sorted(window_horizon_counts.items())]),
        "",
        "## Treated Mature Window Requests By Horizon",
        "",
        markdown_table(
            ["Horizon years", "Treated mature window requests"],
            [[k, v] for k, v in sorted(treated_window_horizon_counts.items())],
        ),
        "",
        "## Filing Events By Event Year",
        "",
        markdown_table(["Event year", "Filing events"], [[k, v] for k, v in sorted(year_counts.items())]),
        "",
        "## Export / Import Contract",
        "",
        "- Export WRDS link results to `data/linking/wrds_crsp_link_output_v1.csv`.",
        "- Export WRDS daily security returns to `data/returns/wrds_crsp_daily_returns_raw_v1.csv`.",
        "- Export WRDS market benchmark returns to `data/returns/wrds_crsp_market_benchmark_raw_v1.csv`.",
        "- Do not compute returns until these files are imported, validated, and status counts are reported.",
        "",
        "## Input Integrity",
        "",
    ]
    for name, before_hash in sorted(hashes_before.items()):
        report.append(f"- `{name}` before: `{before_hash}`")
        report.append(f"- `{name}` after: `{hashes_after[name]}`")
        report.append(f"- `{name}` unchanged: {'yes' if before_hash == hashes_after[name] else 'no'}")
    REPORT_OUT.write_text("\n".join(report), encoding="utf-8")

    checkpoint = [
        "# CHECKPOINT 25: WRDS CRSP Data Request Plan",
        "",
        "## Completed",
        "",
        "- Documented WRDS/CRSP as the primary market/security data source.",
        "- Created WRDS link input file.",
        "- Created mature return-window request file.",
        "- Created WRDS SQL templates for linking, daily returns, and market benchmark pulls.",
        "- Did not connect to WRDS, fetch prices, compute returns, load benchmarks, make SEC requests, or make empirical claims.",
        "",
        "## Files Created",
        "",
        "- `methodology/market_data_source_plan.md`",
        "- `sql/wrds_crsp_linking_query_v1.sql`",
        "- `sql/wrds_crsp_daily_returns_query_v1.sql`",
        "- `sql/wrds_crsp_market_benchmark_query_v1.sql`",
        "- `scripts/prepare_wrds_crsp_inputs_v1.py`",
        "- `data/linking/wrds_crsp_link_input_v1.csv`",
        "- `data/returns/wrds_crsp_return_windows_request_v1.csv`",
        "- `quality_reports/wrds_crsp_data_request_plan_v1_report.md`",
        "- `CHECKPOINT_25_WRDS_CRSP_DATA_REQUEST_PLAN.md`",
        "",
        "## Counts",
        "",
        f"- Filing events for WRDS linking: {len(link_input_rows):,}",
        f"- Mature return-window requests: {len(window_request_rows):,}",
        f"- Treated mature 1-year windows: {treated_window_horizon_counts.get('1', 0):,}",
        f"- Treated mature 3-year windows: {treated_window_horizon_counts.get('3', 0):,}",
        f"- Treated mature 5-year windows: {treated_window_horizon_counts.get('5', 0):,}",
        "",
        "## Next",
        "",
        "Run the WRDS linking query using `data/linking/wrds_crsp_link_input_v1.csv`, export the link output, and import/validate it before pulling daily returns.",
        "",
    ]
    CHECKPOINT_OUT.write_text("\n".join(checkpoint), encoding="utf-8")

    print(f"Wrote {LINK_INPUT.relative_to(ROOT)} ({len(link_input_rows)} rows)")
    print(f"Wrote {WINDOW_REQUEST.relative_to(ROOT)} ({len(window_request_rows)} rows)")
    print(f"Wrote {REPORT_OUT.relative_to(ROOT)}")
    print(f"Wrote {CHECKPOINT_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
