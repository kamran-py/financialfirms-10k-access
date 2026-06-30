"""Import and validate WRDS CRSP/Compustat link output.

This stage reconciles the WRDS link export against the original filing-event
list and resolves one CRSP PERMNO per filing event only when the
pre-specified common-share rule leaves a single eligible security.

It does not fetch prices, compute returns, load benchmarks, make SEC requests,
or make empirical claims.
"""

from __future__ import annotations

import csv
import hashlib
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CRSP_DAILY_MAX_DATE = "2024-12-31"

LINK_INPUT = ROOT / "data" / "linking" / "wrds_crsp_link_input_v1.csv"
LINK_RAW = ROOT / "data" / "linking" / "wrds_crsp_link_output_v1.csv"
WINDOW_REQUEST = ROOT / "data" / "returns" / "wrds_crsp_return_windows_request_v1.csv"
SOURCE_PLAN = ROOT / "methodology" / "market_data_source_plan.md"

RESOLVED_LINKS = ROOT / "data" / "linking" / "wrds_crsp_link_resolved_v1.csv"
LINKED_WINDOW_REQUEST = ROOT / "data" / "returns" / "wrds_crsp_return_windows_linked_request_v1.csv"
REPORT_OUT = ROOT / "quality_reports" / "wrds_crsp_link_import_validation_v1_report.md"
CHECKPOINT_OUT = ROOT / "CHECKPOINT_26_WRDS_CRSP_LINK_IMPORT_VALIDATION.md"

csv.field_size_limit(sys.maxsize)


RAW_REQUIRED_FIELDS = {
    "event_id",
    "firm_id",
    "cik",
    "ticker_from_project",
    "company_name",
    "accession_number",
    "filing_date",
    "event_date",
    "validated_conservative_treatment",
    "primary_narrative_subcategory",
    "gvkey",
    "compustat_company_name",
    "compustat_ticker",
    "permno",
    "permco",
    "linktype",
    "linkprim",
    "linkdt",
    "linkenddt",
    "crsp_ticker",
    "crsp_company_name",
    "shrcd",
    "exchcd",
    "namedt",
    "nameendt",
    "raw_link_status",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def csv_headers(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle)
        return next(reader)


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


def clean_number(value: str) -> str:
    value = (value or "").strip()
    if value.endswith(".0"):
        return value[:-2]
    return value


def parse_ymd(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def is_common_candidate(row: dict[str, str]) -> bool:
    return (
        row.get("raw_link_status") == "candidate_link"
        and bool(clean_number(row.get("permno", "")))
        and clean_number(row.get("shrcd", "")) in {"10", "11"}
    )


def sort_candidate(row: dict[str, str]) -> tuple[int, int, str]:
    linkprim_rank = {"P": 0, "C": 1}.get(row.get("linkprim", ""), 9)
    linktype_rank = {"LC": 0, "LU": 1, "LS": 2}.get(row.get("linktype", ""), 9)
    return (linkprim_rank, linktype_rank, clean_number(row.get("permno", "")))


def summarize_statuses(rows: list[dict[str, str]]) -> str:
    counts = Counter(row.get("raw_link_status", "missing_raw_link_status") or "blank_raw_link_status" for row in rows)
    return "; ".join(f"{status}:{count}" for status, count in sorted(counts.items()))


def choose_unresolved_status(base: dict[str, str], rows: list[dict[str, str]]) -> tuple[str, str]:
    if not rows and base.get("event_date", "") > CRSP_DAILY_MAX_DATE:
        return "crsp_source_coverage_unavailable_after_2024_12_31", (
            "No WRDS link row was returned because the available WRDS/CRSP stocknames "
            "and daily stock files end on 2024-12-31, before this filing event date."
        )
    if not rows:
        return "no_wrds_link_row", "No row was returned by the WRDS link export for this filing event."

    statuses = Counter(row.get("raw_link_status", "") for row in rows)
    if statuses.get("no_permno_link"):
        return "no_permno_link", "WRDS matched the filing event but did not return an eligible active PERMNO link."
    if statuses.get("permno_without_active_name_at_event_date"):
        return (
            "permno_without_active_name_at_event_date",
            "WRDS returned a PERMNO link, but no CRSP stock-name row was active on the event date.",
        )
    if statuses.get("non_common_share_code"):
        return (
            "non_common_share_code",
            "WRDS returned linked securities, but the active CRSP share code was not ordinary common equity.",
        )
    return "unresolved_link_status", "No eligible ordinary common-share PERMNO survived the pre-specified filters."


def resolve_event(base: dict[str, str], rows: list[dict[str, str]]) -> dict[str, str]:
    eligible = [row for row in rows if is_common_candidate(row)]
    unique_permnos = sorted({clean_number(row["permno"]) for row in eligible})

    resolved: dict[str, str] = {
        **base,
        "gvkey": "",
        "compustat_company_name": "",
        "compustat_ticker": "",
        "permno": "",
        "permco": "",
        "linktype": "",
        "linkprim": "",
        "linkdt": "",
        "linkenddt": "",
        "crsp_ticker": "",
        "crsp_company_name": "",
        "shrcd": "",
        "exchcd": "",
        "namedt": "",
        "nameendt": "",
        "security_link_status": "",
        "security_link_status_reason": "",
        "price_identifier": "",
        "price_identifier_type": "",
        "price_identifier_source": "",
        "link_confidence": "",
        "multiple_share_class_status": "",
        "eligible_candidate_row_count": str(len(eligible)),
        "unique_eligible_permno_count": str(len(unique_permnos)),
        "raw_wrds_row_count": str(len(rows)),
        "raw_link_statuses": summarize_statuses(rows),
        "primary_security_rule": (
            "Resolved only when WRDS CIK-GVKEY-CCM link active at filing date "
            "left exactly one CRSP ordinary common-share PERMNO."
        ),
    }

    if len(unique_permnos) == 1:
        chosen_permno = unique_permnos[0]
        chosen_rows = [row for row in eligible if clean_number(row["permno"]) == chosen_permno]
        chosen = sorted(chosen_rows, key=sort_candidate)[0]
        for field in [
            "gvkey",
            "compustat_company_name",
            "compustat_ticker",
            "permco",
            "linktype",
            "linkprim",
            "linkdt",
            "linkenddt",
            "crsp_ticker",
            "crsp_company_name",
            "shrcd",
            "exchcd",
            "namedt",
            "nameendt",
        ]:
            resolved[field] = chosen.get(field, "")
        resolved["permno"] = chosen_permno
        resolved["permco"] = clean_number(chosen.get("permco", ""))
        resolved["security_link_status"] = "resolved_common_share_permno"
        resolved["security_link_status_reason"] = "Exactly one eligible ordinary common-share PERMNO survived WRDS/CRSP filters."
        resolved["price_identifier"] = chosen_permno
        resolved["price_identifier_type"] = "CRSP_PERMNO"
        resolved["price_identifier_source"] = "WRDS_CRSP_CCM_LINKTABLE_AND_STOCKNAMES"
        resolved["link_confidence"] = "high"
        resolved["multiple_share_class_status"] = "single_eligible_common_share_permno"
        return resolved

    if len(unique_permnos) > 1:
        best = sorted(eligible, key=sort_candidate)[0]
        for field in [
            "gvkey",
            "compustat_company_name",
            "compustat_ticker",
            "linktype",
            "linkprim",
            "linkdt",
            "linkenddt",
            "shrcd",
            "exchcd",
            "namedt",
            "nameendt",
        ]:
            resolved[field] = best.get(field, "")
        resolved["security_link_status"] = "multiple_share_class_ambiguous"
        resolved["security_link_status_reason"] = (
            f"Multiple eligible ordinary common-share PERMNOs survived filters: {', '.join(unique_permnos)}."
        )
        resolved["link_confidence"] = "failed_ambiguous"
        resolved["multiple_share_class_status"] = "multiple_eligible_common_share_permnos"
        return resolved

    status, reason = choose_unresolved_status(base, rows)
    resolved["security_link_status"] = status
    resolved["security_link_status_reason"] = reason
    resolved["link_confidence"] = "failed"
    resolved["multiple_share_class_status"] = "not_applicable"
    if rows:
        row = rows[0]
        for field in [
            "gvkey",
            "compustat_company_name",
            "compustat_ticker",
            "permno",
            "permco",
            "linktype",
            "linkprim",
            "linkdt",
            "linkenddt",
            "crsp_ticker",
            "crsp_company_name",
            "shrcd",
            "exchcd",
            "namedt",
            "nameendt",
        ]:
            resolved[field] = clean_number(row.get(field, "")) if field in {"permno", "permco", "shrcd", "exchcd"} else row.get(field, "")
    return resolved


def main() -> None:
    required = [LINK_INPUT, LINK_RAW, WINDOW_REQUEST, SOURCE_PLAN]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")

    raw_headers = set(csv_headers(LINK_RAW))
    missing_raw_fields = sorted(RAW_REQUIRED_FIELDS - raw_headers)
    if missing_raw_fields:
        raise ValueError(f"WRDS link output is missing required fields: {missing_raw_fields}")

    hashes_before = {path.name: sha256(path) for path in required}

    link_input_rows = read_csv(LINK_INPUT)
    raw_rows = read_csv(LINK_RAW)
    window_rows = read_csv(WINDOW_REQUEST)

    event_ids = [row["event_id"] for row in link_input_rows]
    duplicate_input_ids = [event_id for event_id, count in Counter(event_ids).items() if count > 1]
    if duplicate_input_ids:
        raise ValueError(f"Duplicate event_id values in link input: {duplicate_input_ids[:10]}")

    input_by_event = {row["event_id"]: row for row in link_input_rows}
    raw_by_event: dict[str, list[dict[str, str]]] = defaultdict(list)
    raw_unknown_event_ids: list[str] = []
    for row in raw_rows:
        event_id = row["event_id"]
        if event_id not in input_by_event:
            raw_unknown_event_ids.append(event_id)
            continue
        raw_by_event[event_id].append(row)

    resolved_rows = [resolve_event(row, raw_by_event.get(row["event_id"], [])) for row in link_input_rows]
    resolved_by_event = {row["event_id"]: row for row in resolved_rows}

    linked_window_rows: list[dict[str, str]] = []
    for row in window_rows:
        link = resolved_by_event[row["event_id"]]
        if link["security_link_status"] != "resolved_common_share_permno":
            post_status = link["security_link_status"]
        elif parse_ymd(row["target_calendar_end_date"]) > parse_ymd(CRSP_DAILY_MAX_DATE):
            post_status = "crsp_return_window_exceeds_available_daily_coverage"
        else:
            post_status = "ready_for_wrds_daily_return_request"
        linked_window_rows.append(
            {
                **row,
                "post_link_return_window_status": post_status,
                "permno": link["permno"],
                "permco": link["permco"],
                "price_identifier": link["price_identifier"],
                "price_identifier_type": link["price_identifier_type"],
                "price_identifier_source": link["price_identifier_source"],
                "security_link_status": link["security_link_status"],
                "security_link_status_reason": link["security_link_status_reason"],
                "crsp_ticker": link["crsp_ticker"],
                "crsp_company_name": link["crsp_company_name"],
                "shrcd": link["shrcd"],
                "exchcd": link["exchcd"],
                "link_confidence": link["link_confidence"],
            }
        )

    link_fields = [
        "event_id",
        "firm_id",
        "cik",
        "ticker_from_project",
        "company_name",
        "accession_number",
        "filing_date",
        "event_date",
        "validated_conservative_treatment",
        "primary_narrative_subcategory",
        "gvkey",
        "compustat_company_name",
        "compustat_ticker",
        "permno",
        "permco",
        "linktype",
        "linkprim",
        "linkdt",
        "linkenddt",
        "crsp_ticker",
        "crsp_company_name",
        "shrcd",
        "exchcd",
        "namedt",
        "nameendt",
        "security_link_status",
        "security_link_status_reason",
        "price_identifier",
        "price_identifier_type",
        "price_identifier_source",
        "link_confidence",
        "multiple_share_class_status",
        "eligible_candidate_row_count",
        "unique_eligible_permno_count",
        "raw_wrds_row_count",
        "raw_link_statuses",
        "primary_security_rule",
    ]
    window_fields = list(window_rows[0].keys()) + [
        "post_link_return_window_status",
        "permno",
        "permco",
        "price_identifier",
        "price_identifier_type",
        "price_identifier_source",
        "security_link_status",
        "security_link_status_reason",
        "crsp_ticker",
        "crsp_company_name",
        "shrcd",
        "exchcd",
        "link_confidence",
    ]

    write_csv(RESOLVED_LINKS, link_fields, resolved_rows)
    write_csv(LINKED_WINDOW_REQUEST, window_fields, linked_window_rows)

    hashes_after = {path.name: sha256(path) for path in required}

    raw_status_counts = Counter(row["raw_link_status"] for row in raw_rows)
    status_counts = Counter(row["security_link_status"] for row in resolved_rows)
    treated_status_counts = Counter(
        row["security_link_status"] for row in resolved_rows if row["validated_conservative_treatment"] == "1"
    )
    untreated_status_counts = Counter(
        row["security_link_status"] for row in resolved_rows if row["validated_conservative_treatment"] == "0"
    )
    year_status_counts = Counter((row["event_date"][:4], row["security_link_status"]) for row in resolved_rows)
    ready_window_counts = Counter(
        row["horizon_years"]
        for row in linked_window_rows
        if row["post_link_return_window_status"] == "ready_for_wrds_daily_return_request"
    )
    treated_ready_window_counts = Counter(
        row["horizon_years"]
        for row in linked_window_rows
        if row["post_link_return_window_status"] == "ready_for_wrds_daily_return_request"
        and row["validated_conservative_treatment"] == "1"
    )
    link_confidence_counts = Counter(row["link_confidence"] for row in resolved_rows)
    year_totals = Counter(row["event_date"][:4] for row in resolved_rows)
    resolved_by_year = Counter(
        row["event_date"][:4]
        for row in resolved_rows
        if row["security_link_status"] == "resolved_common_share_permno"
    )
    zero_resolved_years = sorted(
        year for year, total in year_totals.items() if total and resolved_by_year.get(year, 0) == 0
    )
    unexplained_zero_resolved_years = [year for year in zero_resolved_years if year <= CRSP_DAILY_MAX_DATE[:4]]
    validation_decision = (
        "blocked_pending_investigation"
        if unexplained_zero_resolved_years
        else "passed_with_crsp_source_coverage_limit"
    )
    validation_warning = (
        "The WRDS link export has no resolved common-share PERMNOs for filing year(s) "
        + ", ".join(unexplained_zero_resolved_years)
        + ". This is not explained by the documented WRDS/CRSP coverage limit and requires investigation before return pulls."
        if unexplained_zero_resolved_years
        else (
            f"WRDS diagnostics supplied on 2026-06-29 show `crsp.stocknames` and `crsp.dsf` both end on "
            f"{CRSP_DAILY_MAX_DATE}. Filing years after that date are source-coverage limited, not silently dropped."
        )
    )

    report = [
        "# WRDS CRSP Link Import Validation V1 Report",
        "",
        "## Guardrails",
        "",
        "- Raw WRDS link output was preserved unchanged.",
        "- No prices were fetched.",
        "- No returns were computed.",
        "- No benchmark data were loaded.",
        "- No SEC requests were made.",
        "- No empirical performance claims were made.",
        "",
        "## Inputs",
        "",
        "- `data/linking/wrds_crsp_link_input_v1.csv`",
        "- `data/linking/wrds_crsp_link_output_v1.csv`",
        "- `data/returns/wrds_crsp_return_windows_request_v1.csv`",
        "- `methodology/market_data_source_plan.md`",
        "",
        "## Outputs",
        "",
        "- `data/linking/wrds_crsp_link_resolved_v1.csv`",
        "- `data/returns/wrds_crsp_return_windows_linked_request_v1.csv`",
        "",
        "## Resolution Rule",
        "",
        "A filing event is marked `resolved_common_share_permno` only when the WRDS CIK-GVKEY-CCM link and CRSP stock-name filters leave exactly one active ordinary common-share PERMNO at the filing date. Ordinary common shares require `shrcd in (10, 11)`. If multiple eligible PERMNOs survive, the filing is marked `multiple_share_class_ambiguous` rather than force-resolved.",
        "",
        "## WRDS/CRSP Coverage Limit",
        "",
        f"WRDS diagnostics supplied from the project notebook on 2026-06-29 show `crsp.stocknames` max `nameenddt` = `{CRSP_DAILY_MAX_DATE}` and `crsp.dsf` max `date` = `{CRSP_DAILY_MAX_DATE}`. Return-window rows whose target calendar end date exceeds this coverage date are not marked ready for daily-return requests.",
        "",
        "## Reconciliation Counts",
        "",
        f"- Original filing events: {len(link_input_rows):,}",
        f"- Raw WRDS output rows: {len(raw_rows):,}",
        f"- Raw WRDS unique event IDs: {len({row['event_id'] for row in raw_rows}):,}",
        f"- Resolved output rows: {len(resolved_rows):,}",
        f"- Raw rows with unknown event IDs: {len(raw_unknown_event_ids):,}",
        f"- Validation decision: `{validation_decision}`",
        f"- Validation warning: {validation_warning}",
        "",
        "## Raw WRDS Link Status Counts",
        "",
        markdown_table(["Raw link status", "Rows"], [[k, v] for k, v in sorted(raw_status_counts.items())]),
        "",
        "## Final Security Link Status Counts",
        "",
        markdown_table(["Security link status", "Filing events"], [[k, v] for k, v in sorted(status_counts.items())]),
        "",
        "## Link Confidence Counts",
        "",
        markdown_table(["Link confidence", "Filing events"], [[k, v] for k, v in sorted(link_confidence_counts.items())]),
        "",
        "## Treatment Balance By Link Status",
        "",
        markdown_table(
            ["Security link status", "Treated filings", "Untreated/control filings"],
            [
                [status, treated_status_counts.get(status, 0), untreated_status_counts.get(status, 0)]
                for status in sorted(status_counts)
            ],
        ),
        "",
        "## Ready Mature Return Windows By Horizon",
        "",
        markdown_table(["Horizon years", "Ready windows"], [[k, v] for k, v in sorted(ready_window_counts.items())]),
        "",
        "## Ready Treated Mature Return Windows By Horizon",
        "",
        markdown_table(
            ["Horizon years", "Ready treated windows"],
            [[k, v] for k, v in sorted(treated_ready_window_counts.items())],
        ),
        "",
        "## Link Status By Filing Year",
        "",
        markdown_table(
            ["Filing year", "Security link status", "Filing events"],
            [[year, status, count] for (year, status), count in sorted(year_status_counts.items())],
        ),
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
        "# CHECKPOINT 26: WRDS CRSP Link Import Validation",
        "",
        "## Completed",
        "",
        "- Imported WRDS CRSP/Compustat link output.",
        "- Reconciled raw WRDS rows against the original 5,954 filing events.",
        "- Resolved one CRSP PERMNO per event only when exactly one active ordinary common-share PERMNO survived the pre-specified rule.",
        "- Flagged unresolved, non-common-share, no-PERMNO, and ambiguous link cases.",
        "- Created a linked return-window request scaffold for the next WRDS daily-return pull.",
        f"- Validation decision: `{validation_decision}`.",
        "- Did not fetch prices, compute returns, load benchmarks, make SEC requests, or make empirical claims.",
        "",
        "## Files Created",
        "",
        "- `scripts/import_validate_wrds_crsp_links_v1.py`",
        "- `data/linking/wrds_crsp_link_resolved_v1.csv`",
        "- `data/returns/wrds_crsp_return_windows_linked_request_v1.csv`",
        "- `quality_reports/wrds_crsp_link_import_validation_v1_report.md`",
        "- `CHECKPOINT_26_WRDS_CRSP_LINK_IMPORT_VALIDATION.md`",
        "",
        "## Counts",
        "",
        f"- Original filing events: {len(link_input_rows):,}",
        f"- Raw WRDS output rows: {len(raw_rows):,}",
        f"- Resolved common-share PERMNO events: {status_counts.get('resolved_common_share_permno', 0):,}",
        f"- Multiple-share-class ambiguous events: {status_counts.get('multiple_share_class_ambiguous', 0):,}",
        f"- No WRDS link row events: {status_counts.get('no_wrds_link_row', 0):,}",
        f"- Non-common-share events: {status_counts.get('non_common_share_code', 0):,}",
        f"- No-PERMNO events: {status_counts.get('no_permno_link', 0):,}",
        f"- Ready mature return-window rows: {sum(ready_window_counts.values()):,}",
        f"- Ready treated 1-year windows: {treated_ready_window_counts.get('1', 0):,}",
        f"- Ready treated 3-year windows: {treated_ready_window_counts.get('3', 0):,}",
        f"- Ready treated 5-year windows: {treated_ready_window_counts.get('5', 0):,}",
        "",
        "## Next",
        "",
        (
            "Investigate unexplained zero-resolved filing years before any daily-return pull."
            if unexplained_zero_resolved_years
            else "Use `data/returns/wrds_crsp_return_windows_linked_request_v1.csv` to request CRSP daily returns only for rows with `post_link_return_window_status == ready_for_wrds_daily_return_request`. Validate raw return coverage before computing any 1-, 3-, or 5-year outcomes."
        ),
        "",
    ]
    CHECKPOINT_OUT.write_text("\n".join(checkpoint), encoding="utf-8")

    print(f"Wrote {RESOLVED_LINKS.relative_to(ROOT)} ({len(resolved_rows)} rows)")
    print(f"Wrote {LINKED_WINDOW_REQUEST.relative_to(ROOT)} ({len(linked_window_rows)} rows)")
    print(f"Wrote {REPORT_OUT.relative_to(ROOT)}")
    print(f"Wrote {CHECKPOINT_OUT.relative_to(ROOT)}")
    print("Final security link statuses:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")


if __name__ == "__main__":
    main()
