#!/usr/bin/env python3
"""
Build a firm-year SEC 10-K filing index for filing years 2015-2025.

The output contains one row per discovered 10-K filing and one explicit missing
row per firm-year where no 10-K is found or metadata cannot be used.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sec_client import (
    PROJECT_ROOT,
    SecClient,
    cik10,
    filing_url,
    primary_document_url,
    utc_now_iso,
)


FILING_YEARS = list(range(2015, 2026))
FIRM_UNIVERSE_PATH = PROJECT_ROOT / "config" / "firm_universe.csv"
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"
FILING_INDEX_PATH = METADATA_DIR / "filing_index.csv"
QUALITY_REPORT_DIR = PROJECT_ROOT / "quality_reports"
REPORT_PATH = QUALITY_REPORT_DIR / "filing_ingestion_report.md"
DOWNLOAD_ATTEMPTS_PATH = METADATA_DIR / "download_attempts.csv"

FILING_INDEX_FIELDS = [
    "firm_id",
    "company_name",
    "ticker",
    "cik",
    "filing_year",
    "expected_status",
    "missing_reason",
    "accession_number",
    "filing_date",
    "report_date",
    "form",
    "primary_document",
    "filing_url",
    "primary_document_url",
    "metadata_source",
    "metadata_status",
    "notes",
]

DOWNLOAD_ATTEMPT_FIELDS = [
    "attempt_id",
    "attempted_at_utc",
    "firm_id",
    "company_name",
    "ticker",
    "cik",
    "filing_year",
    "accession_number",
    "filing_date",
    "report_date",
    "form",
    "primary_document",
    "primary_document_url",
    "local_path",
    "status",
    "error_reason",
    "http_status",
    "bytes",
    "sha256",
    "overwrite",
    "notes",
]


def ensure_dirs() -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    QUALITY_REPORT_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def ensure_download_attempts_file() -> None:
    if not DOWNLOAD_ATTEMPTS_PATH.exists():
        write_csv(DOWNLOAD_ATTEMPTS_PATH, [], DOWNLOAD_ATTEMPT_FIELDS)


def recent_rows(payload: dict[str, Any]) -> list[dict[str, str]]:
    recent = payload.get("filings", {}).get("recent")
    if not isinstance(recent, dict):
        return []
    keys = list(recent.keys())
    n = max((len(v) for v in recent.values() if isinstance(v, list)), default=0)
    rows: list[dict[str, str]] = []
    for idx in range(n):
        row = {}
        for key in keys:
            values = recent.get(key)
            row[key] = str(values[idx]) if isinstance(values, list) and idx < len(values) and values[idx] is not None else ""
        rows.append(row)
    return rows


def historical_rows(payload: dict[str, Any]) -> list[dict[str, str]]:
    if not isinstance(payload, dict):
        return []
    keys = list(payload.keys())
    n = max((len(v) for v in payload.values() if isinstance(v, list)), default=0)
    rows: list[dict[str, str]] = []
    for idx in range(n):
        row = {}
        for key in keys:
            values = payload.get(key)
            row[key] = str(values[idx]) if isinstance(values, list) and idx < len(values) and values[idx] is not None else ""
        rows.append(row)
    return rows


def relevant_history_files(company_payload: dict[str, Any]) -> list[str]:
    files = company_payload.get("filings", {}).get("files", [])
    names: list[str] = []
    if not isinstance(files, list):
        return names
    for item in files:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "")
        filing_from = str(item.get("filingFrom") or "")
        filing_to = str(item.get("filingTo") or "")
        if not name:
            continue
        if filing_to and filing_to[:4].isdigit() and int(filing_to[:4]) < min(FILING_YEARS):
            continue
        if filing_from and filing_from[:4].isdigit() and int(filing_from[:4]) > max(FILING_YEARS):
            continue
        names.append(name)
    return names


def is_target_10k(row: dict[str, str]) -> bool:
    return row.get("form", "").strip().upper() == "10-K"


def filing_year(row: dict[str, str]) -> int | None:
    filing_date = row.get("filingDate", "")
    if len(filing_date) >= 4 and filing_date[:4].isdigit():
        return int(filing_date[:4])
    return None


def normalize_accession(accession_number: str) -> str:
    return accession_number.strip()


def make_found_row(firm: dict[str, str], filing: dict[str, str], source: str, metadata_status: str) -> dict[str, str]:
    cik = cik10(firm.get("cik", ""))
    accession = normalize_accession(filing.get("accessionNumber", ""))
    primary_doc = filing.get("primaryDocument", "").strip()
    year = filing_year(filing)
    return {
        "firm_id": firm.get("firm_id", ""),
        "company_name": firm.get("company_name", ""),
        "ticker": firm.get("ticker", ""),
        "cik": cik,
        "filing_year": str(year) if year else "",
        "expected_status": "FOUND",
        "missing_reason": "",
        "accession_number": accession,
        "filing_date": filing.get("filingDate", ""),
        "report_date": filing.get("reportDate", ""),
        "form": filing.get("form", ""),
        "primary_document": primary_doc,
        "filing_url": filing_url(cik, accession) if accession else "",
        "primary_document_url": primary_document_url(cik, accession, primary_doc) if accession and primary_doc else "",
        "metadata_source": source,
        "metadata_status": metadata_status,
        "notes": "",
    }


def make_missing_row(
    firm: dict[str, str],
    year: int,
    reason: str,
    metadata_source: str = "",
    metadata_status: str = "",
    notes: str = "",
) -> dict[str, str]:
    return {
        "firm_id": firm.get("firm_id", ""),
        "company_name": firm.get("company_name", ""),
        "ticker": firm.get("ticker", ""),
        "cik": cik10(firm.get("cik", "")),
        "filing_year": str(year),
        "expected_status": "MISSING",
        "missing_reason": reason,
        "accession_number": "",
        "filing_date": "",
        "report_date": "",
        "form": "",
        "primary_document": "",
        "filing_url": "",
        "primary_document_url": "",
        "metadata_source": metadata_source,
        "metadata_status": metadata_status,
        "notes": notes,
    }


def make_metadata_error_rows(firm: dict[str, str], reason: str, status: str, notes: str) -> list[dict[str, str]]:
    return [make_missing_row(firm, year, reason, metadata_status=status, notes=notes) for year in FILING_YEARS]


def build_index(client: SecClient, firms: list[dict[str, str]], refresh_metadata: bool = False) -> list[dict[str, str]]:
    index_rows: list[dict[str, str]] = []
    for idx, firm in enumerate(firms, start=1):
        cik = cik10(firm.get("cik", ""))
        if not cik:
            index_rows.extend(make_metadata_error_rows(firm, "CIK_MISSING", "CIK_MISSING", "Firm universe row has no CIK."))
            continue

        payload, result = client.get_company_submissions(cik, refresh=refresh_metadata)
        if payload is None:
            reason = "MALFORMED_METADATA" if result.status == "MALFORMED_METADATA" else "HTTP_FAILURE"
            index_rows.extend(make_metadata_error_rows(firm, reason, result.status, result.error_reason))
            continue

        all_filings: list[tuple[dict[str, str], str, str]] = [
            (row, str(result.local_path.relative_to(PROJECT_ROOT)), result.status) for row in recent_rows(payload)
        ]
        for history_name in relevant_history_files(payload):
            history_payload, history_result = client.get_historical_submissions(history_name, refresh=refresh_metadata)
            if history_payload is None:
                continue
            all_filings.extend(
                (row, str(history_result.local_path.relative_to(PROJECT_ROOT)), history_result.status)
                for row in historical_rows(history_payload)
            )

        seen_accessions: set[str] = set()
        found_by_year: dict[int, list[dict[str, str]]] = defaultdict(list)
        malformed_count = 0
        for filing, source, metadata_status in all_filings:
            if not is_target_10k(filing):
                continue
            year = filing_year(filing)
            if year not in FILING_YEARS:
                continue
            accession = normalize_accession(filing.get("accessionNumber", ""))
            if not accession:
                malformed_count += 1
                continue
            if accession in seen_accessions:
                continue
            seen_accessions.add(accession)
            found_by_year[year].append(make_found_row(firm, filing, source, metadata_status))

        for year in FILING_YEARS:
            if found_by_year.get(year):
                index_rows.extend(sorted(found_by_year[year], key=lambda row: row["filing_date"]))
            else:
                notes = f"Malformed target 10-K metadata rows skipped: {malformed_count}" if malformed_count else ""
                index_rows.append(make_missing_row(firm, year, "NO_FILING_FOUND", metadata_status=result.status, notes=notes))

        if idx % 100 == 0 or idx == len(firms):
            print(f"Indexed filings for {idx}/{len(firms)} firms")
    return index_rows


def read_download_attempts() -> list[dict[str, str]]:
    if not DOWNLOAD_ATTEMPTS_PATH.exists():
        return []
    return read_csv(DOWNLOAD_ATTEMPTS_PATH)


def write_report(index_rows: list[dict[str, str]], attempt_rows: list[dict[str, str]]) -> None:
    firm_ids = {row["firm_id"] for row in index_rows if row.get("firm_id")}
    found_rows = [row for row in index_rows if row.get("expected_status") == "FOUND"]
    missing_rows = [row for row in index_rows if row.get("expected_status") == "MISSING"]
    missing_reasons = Counter(row.get("missing_reason", "") for row in missing_rows)
    metadata_status = Counter(row.get("metadata_status", "") for row in index_rows)
    attempt_status = Counter(row.get("status", "") for row in attempt_rows)
    attempt_errors = Counter(row.get("error_reason", "") for row in attempt_rows if row.get("error_reason"))
    found_by_year = Counter(row.get("filing_year", "") for row in found_rows)
    missing_firm_years = len(missing_rows)

    lines = [
        "# Filing Ingestion Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "- Filing form: exact `10-K`.",
        "- Filing years: 2015-2025 based on SEC filing date.",
        "- SEC endpoints: `data.sec.gov/submissions` and `www.sec.gov/Archives`.",
        "- SEC fair-access limit: scripts reject rates above 10 requests/second.",
        "",
        "## Filing Index Counts",
        "",
        f"- Firms represented in index: {len(firm_ids)}",
        f"- Firm-year rows with no 10-K found or metadata issue: {missing_firm_years}",
        f"- 10-K filing rows found: {len(found_rows)}",
        "",
        "## Found 10-K Filings By Filing Year",
        "",
    ]
    for year in FILING_YEARS:
        lines.append(f"- {year}: {found_by_year.get(str(year), 0)}")
    lines.extend(["", "## Missing Or Metadata Reasons", ""])
    for reason, count in sorted(missing_reasons.items()):
        lines.append(f"- {reason or 'NONE'}: {count}")
    lines.extend(["", "## Metadata Status Counts", ""])
    for status, count in sorted(metadata_status.items()):
        lines.append(f"- {status or 'NONE'}: {count}")
    lines.extend(["", "## Download Attempt Status Counts", ""])
    if attempt_status:
        for status, count in sorted(attempt_status.items()):
            lines.append(f"- {status or 'NONE'}: {count}")
    else:
        lines.append("- No filing document download attempts logged yet.")
    lines.extend(["", "## Download Error Reasons", ""])
    if attempt_errors:
        for reason, count in sorted(attempt_errors.items()):
            lines.append(f"- {reason}: {count}")
    else:
        lines.append("- No download errors logged yet.")
    lines.extend(
        [
            "",
            "## Required Distinctions",
            "",
            f"- No filing found: {missing_reasons.get('NO_FILING_FOUND', 0)}",
            f"- CIK missing: {missing_reasons.get('CIK_MISSING', 0)}",
            f"- HTTP failure: {missing_reasons.get('HTTP_FAILURE', 0) + attempt_status.get('HTTP_FAILURE', 0)}",
            f"- Malformed metadata: {missing_reasons.get('MALFORMED_METADATA', 0) + attempt_status.get('MALFORMED_METADATA', 0)}",
            f"- Skipped duplicate: {attempt_status.get('SKIPPED_DUPLICATE', 0)}",
            "",
            "## Output Files",
            "",
            f"- `{FILING_INDEX_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{DOWNLOAD_ATTEMPTS_PATH.relative_to(PROJECT_ROOT)}`",
            "",
            "Every firm-year appears either as a discovered filing row or as an explicit missing row with a reason.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build SEC 10-K filing index for the firm universe.")
    parser.add_argument("--firm-universe", default=str(FIRM_UNIVERSE_PATH), help="Input firm universe CSV.")
    parser.add_argument("--output", default=str(FILING_INDEX_PATH), help="Output filing index CSV.")
    parser.add_argument("--refresh-metadata", action="store_true", help="Refresh SEC submissions metadata cache.")
    parser.add_argument("--requests-per-second", type=float, default=9.0, help="SEC request rate, max 10/sec.")
    parser.add_argument("--sec-user-agent", default=None, help="SEC User-Agent; otherwise SEC_USER_AGENT env var.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    ensure_download_attempts_file()
    firms = read_csv(Path(args.firm_universe))
    client = SecClient(user_agent=args.sec_user_agent, requests_per_second=args.requests_per_second)
    rows = build_index(client, firms, refresh_metadata=args.refresh_metadata)
    write_csv(Path(args.output), rows, FILING_INDEX_FIELDS)
    write_report(rows, read_download_attempts())
    print(f"Wrote {Path(args.output).relative_to(PROJECT_ROOT)} with {len(rows)} rows")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Download attempts initialized at {DOWNLOAD_ATTEMPTS_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

