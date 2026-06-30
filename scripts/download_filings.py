#!/usr/bin/env python3
"""
Download primary SEC 10-K filing documents from data/metadata/filing_index.csv.

The downloader is resumable:
- existing raw filing documents are skipped unless --overwrite is supplied
- every attempted row is appended to data/metadata/download_attempts.csv
- each failed download records an error reason
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from build_filing_index import (
    DOWNLOAD_ATTEMPT_FIELDS,
    DOWNLOAD_ATTEMPTS_PATH,
    FILING_INDEX_PATH,
    PROJECT_ROOT,
    REPORT_PATH,
    read_csv,
    write_report,
)
from sec_client import SecClient, raw_filing_path, utc_now_iso


def append_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


def next_attempt_id(existing_attempts: list[dict[str, str]]) -> int:
    values = []
    for row in existing_attempts:
        value = row.get("attempt_id", "")
        if value.isdigit():
            values.append(int(value))
    return max(values, default=0) + 1


def selected_index_rows(index_rows: list[dict[str, str]], retry_failed_only: bool) -> list[dict[str, str]]:
    rows = [row for row in index_rows if row.get("expected_status") == "FOUND"]
    if not retry_failed_only:
        return rows
    attempts = read_csv(DOWNLOAD_ATTEMPTS_PATH) if DOWNLOAD_ATTEMPTS_PATH.exists() else []
    failed_accessions = {
        row.get("accession_number", "")
        for row in attempts
        if row.get("status") in {"HTTP_FAILURE", "DOWNLOAD_FAILED", "MALFORMED_METADATA"}
    }
    return [row for row in rows if row.get("accession_number", "") in failed_accessions]


def make_attempt_row(
    attempt_id: int,
    index_row: dict[str, str],
    status: str,
    error_reason: str,
    http_status: str,
    local_path: Path,
    bytes_written: int,
    sha256: str,
    overwrite: bool,
    notes: str = "",
) -> dict[str, str]:
    return {
        "attempt_id": str(attempt_id),
        "attempted_at_utc": utc_now_iso(),
        "firm_id": index_row.get("firm_id", ""),
        "company_name": index_row.get("company_name", ""),
        "ticker": index_row.get("ticker", ""),
        "cik": index_row.get("cik", ""),
        "filing_year": index_row.get("filing_year", ""),
        "accession_number": index_row.get("accession_number", ""),
        "filing_date": index_row.get("filing_date", ""),
        "report_date": index_row.get("report_date", ""),
        "form": index_row.get("form", ""),
        "primary_document": index_row.get("primary_document", ""),
        "primary_document_url": index_row.get("primary_document_url", ""),
        "local_path": str(local_path.relative_to(PROJECT_ROOT)) if local_path.is_absolute() else str(local_path),
        "status": status,
        "error_reason": error_reason,
        "http_status": http_status,
        "bytes": str(bytes_written),
        "sha256": sha256,
        "overwrite": str(overwrite),
        "notes": notes,
    }


def download_filings(
    client: SecClient,
    index_rows: list[dict[str, str]],
    overwrite: bool,
    limit: int | None,
    retry_failed_only: bool,
) -> list[dict[str, str]]:
    rows = selected_index_rows(index_rows, retry_failed_only)
    if limit is not None:
        rows = rows[:limit]

    existing_attempts = read_csv(DOWNLOAD_ATTEMPTS_PATH) if DOWNLOAD_ATTEMPTS_PATH.exists() else []
    attempt_id = next_attempt_id(existing_attempts)
    new_attempts: list[dict[str, str]] = []

    for idx, row in enumerate(rows, start=1):
        primary_doc = row.get("primary_document", "")
        accession = row.get("accession_number", "")
        cik = row.get("cik", "")
        local_path = raw_filing_path(cik, accession, primary_doc) if primary_doc else Path("")

        if not primary_doc or not accession or not cik:
            attempt = make_attempt_row(
                attempt_id,
                row,
                "MALFORMED_METADATA",
                "Missing CIK, accession number, or primary document.",
                "",
                local_path,
                0,
                "",
                overwrite,
            )
        else:
            result = client.download_primary_document(cik, accession, primary_doc, overwrite=overwrite)
            attempt = make_attempt_row(
                attempt_id,
                row,
                result.status,
                result.error_reason,
                str(result.http_status or ""),
                result.local_path,
                result.bytes_written,
                result.sha256,
                overwrite,
                "Existing cached filing preserved." if result.status == "SKIPPED_DUPLICATE" else "",
            )

        new_attempts.append(attempt)
        append_csv(DOWNLOAD_ATTEMPTS_PATH, [attempt], DOWNLOAD_ATTEMPT_FIELDS)
        attempt_id += 1
        if idx % 100 == 0 or idx == len(rows):
            print(f"Processed filing downloads {idx}/{len(rows)}")

    return new_attempts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download SEC primary 10-K documents from filing_index.csv.")
    parser.add_argument("--filing-index", default=str(FILING_INDEX_PATH), help="Input filing index CSV.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing raw filings.")
    parser.add_argument("--limit", type=int, default=None, help="Optional max number of found filing rows to process.")
    parser.add_argument("--retry-failed-only", action="store_true", help="Only retry filings with prior failed attempts.")
    parser.add_argument("--requests-per-second", type=float, default=9.0, help="SEC request rate, max 10/sec.")
    parser.add_argument("--sec-user-agent", default=None, help="SEC User-Agent; otherwise SEC_USER_AGENT env var.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    index_rows = read_csv(Path(args.filing_index))
    client = SecClient(user_agent=args.sec_user_agent, requests_per_second=args.requests_per_second)
    new_attempts = download_filings(
        client,
        index_rows,
        overwrite=args.overwrite,
        limit=args.limit,
        retry_failed_only=args.retry_failed_only,
    )
    all_attempts = read_csv(DOWNLOAD_ATTEMPTS_PATH) if DOWNLOAD_ATTEMPTS_PATH.exists() else new_attempts
    write_report(index_rows, all_attempts)
    print(f"Logged {len(new_attempts)} attempts to {DOWNLOAD_ATTEMPTS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
