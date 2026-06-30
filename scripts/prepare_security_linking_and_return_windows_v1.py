"""Prepare security-linking and return-window scaffolds.

This stage is deliberately pre-return. It records identifier-linking status
and creates one row per filing-window horizon without fetching prices,
benchmarks, SEC data, or computing returns.
"""

from __future__ import annotations

import csv
import hashlib
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AS_OF_DATE = date(2026, 6, 29)
HORIZONS = (1, 3, 5)

TREATMENTS = ROOT / "data" / "treatments" / "validated_conservative_filing_treatments_v1.csv"
FIRM_UNIVERSE = ROOT / "config" / "firm_universe.csv"
FILING_INDEX = ROOT / "data" / "metadata" / "filing_index.csv"

LINKING_DIR = ROOT / "data" / "linking"
RETURNS_DIR = ROOT / "data" / "returns"
REPORT_DIR = ROOT / "quality_reports"

SECURITY_LINK_CANDIDATES = LINKING_DIR / "security_link_candidates_v1.csv"
FILING_LINK_SCAFFOLD = LINKING_DIR / "filing_security_link_scaffold_v1.csv"
RETURN_WINDOW_SCAFFOLD = RETURNS_DIR / "return_window_scaffold_v1.csv"
REPORT_OUT = REPORT_DIR / "security_linking_and_return_window_prep_v1_report.md"
CHECKPOINT_OUT = ROOT / "CHECKPOINT_24_SECURITY_LINKING_AND_RETURN_WINDOW_PREP.md"

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


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def add_years(value: date, years: int) -> date:
    try:
        return value.replace(year=value.year + years)
    except ValueError:
        return value.replace(month=2, day=28, year=value.year + years)


def markdown_table(headers: list[str], rows: list[list[str | int]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def maturity_status(event_date: str, horizon_years: int) -> tuple[str, str, str]:
    end_date = add_years(parse_date(event_date), horizon_years)
    if end_date <= AS_OF_DATE:
        return end_date.isoformat(), "mature", "pending_security_link_and_price_data"
    return end_date.isoformat(), "right_censored", f"right_censored_as_of_{AS_OF_DATE.isoformat()}"


def main() -> None:
    required = [TREATMENTS, FIRM_UNIVERSE, FILING_INDEX]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")

    hashes_before = {path.name: sha256(path) for path in required}

    treatments = read_csv(TREATMENTS)
    firm_rows = read_csv(FIRM_UNIVERSE)
    filing_rows = read_csv(FILING_INDEX)
    firm_lookup = {row["firm_id"]: row for row in firm_rows}
    filing_lookup = {row.get("accession_number", ""): row for row in filing_rows if row.get("accession_number")}

    by_firm: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in treatments:
        by_firm[row["firm_id"]].append(row)

    security_rows: list[dict[str, str]] = []
    for firm_id, rows in sorted(by_firm.items()):
        firm = firm_lookup.get(firm_id, {})
        filing_dates = sorted(row["filing_date"] for row in rows if row.get("filing_date"))
        treated_count = sum(1 for row in rows if row["validated_conservative_treatment"] == "1")
        tickers = sorted({row["ticker"] for row in rows if row.get("ticker")})
        ciks = sorted({row["cik"] for row in rows if row.get("cik")})
        exchanges = sorted({firm.get("exchange", "")} - {""})
        security_rows.append(
            {
                "firm_id": firm_id,
                "cik": "; ".join(ciks),
                "ticker_from_project": "; ".join(tickers),
                "company_name": firm.get("company_name") or rows[0].get("company_name", ""),
                "exchange_from_firm_universe": "; ".join(exchanges),
                "sic": firm.get("sic", ""),
                "sic_description": firm.get("sic_description", ""),
                "sector": firm.get("sector", ""),
                "industry": firm.get("industry", ""),
                "filing_count": str(len(rows)),
                "treated_filing_count": str(treated_count),
                "first_filing_date": filing_dates[0] if filing_dates else "",
                "last_filing_date": filing_dates[-1] if filing_dates else "",
                "security_link_status": "pending_price_identifier",
                "security_link_status_reason": "CIK and ticker are available, but no point-in-time price identifier has been assigned.",
                "price_identifier": "",
                "price_identifier_type": "",
                "price_identifier_source": "",
                "link_start_date": "",
                "link_end_date": "",
                "link_confidence": "pending",
                "primary_security_rule": "pending: primary US-listed common equity security associated with issuer at filing date",
                "known_limitation": "Current-listed SEC ticker universe is not a point-in-time security master; ticker alone is insufficient for return linking.",
            }
        )

    filing_link_rows: list[dict[str, str]] = []
    for row in treatments:
        filing = filing_lookup.get(row["accession_number"], {})
        firm = firm_lookup.get(row["firm_id"], {})
        has_ticker = bool(row.get("ticker"))
        has_cik = bool(row.get("cik"))
        if has_ticker and has_cik:
            link_status = "pending_price_identifier"
            reason = "CIK and project ticker available; point-in-time security identifier not yet assigned."
        else:
            link_status = "ticker_or_cik_link_failed"
            reason = "Missing CIK or ticker in local treatment panel before price-source linking."
        filing_link_rows.append(
            {
                "firm_id": row["firm_id"],
                "cik": row["cik"],
                "ticker_from_project": row["ticker"],
                "company_name": row["company_name"],
                "accession_number": row["accession_number"],
                "filing_year": row["filing_year"],
                "filing_date": row["filing_date"],
                "event_date": row["event_date"],
                "report_date": row.get("report_date", filing.get("report_date", "")),
                "validated_conservative_treatment": row["validated_conservative_treatment"],
                "primary_narrative_subcategory": row["primary_narrative_subcategory"],
                "exchange_from_firm_universe": firm.get("exchange", ""),
                "sic": firm.get("sic", ""),
                "industry": firm.get("industry", ""),
                "security_link_status": link_status,
                "security_link_status_reason": reason,
                "price_identifier": "",
                "price_identifier_type": "",
                "price_identifier_source": "",
                "link_confidence": "pending" if link_status == "pending_price_identifier" else "failed",
                "multiple_share_class_status": "not_evaluated",
                "delisting_status": "not_evaluated",
                "corporate_action_adjustment_status": "not_evaluated",
                "primary_security_rule": "pending: primary US-listed common equity security associated with issuer at filing date",
            }
        )

    window_rows: list[dict[str, str]] = []
    for row in filing_link_rows:
        for horizon in HORIZONS:
            target_end, calendar_status, pre_return_status = maturity_status(row["event_date"], horizon)
            if row["security_link_status"] == "ticker_or_cik_link_failed":
                pre_return_status = "ticker_or_cik_link_failed"
            window_rows.append(
                {
                    "firm_id": row["firm_id"],
                    "cik": row["cik"],
                    "ticker_from_project": row["ticker_from_project"],
                    "company_name": row["company_name"],
                    "accession_number": row["accession_number"],
                    "filing_year": row["filing_year"],
                    "filing_date": row["filing_date"],
                    "event_date": row["event_date"],
                    "validated_conservative_treatment": row["validated_conservative_treatment"],
                    "primary_narrative_subcategory": row["primary_narrative_subcategory"],
                    "horizon_years": str(horizon),
                    "window_start_convention": "nearest_trading_day_on_or_after_event_date_pending_price_source",
                    "target_calendar_end_date": target_end,
                    "calendar_maturity_status_as_of_2026_06_29": calendar_status,
                    "pre_price_return_window_status": pre_return_status,
                    "security_link_status": row["security_link_status"],
                    "price_identifier": "",
                    "price_identifier_source": "",
                    "return_data_source": "not_selected",
                    "raw_return_status": "not_computed",
                    "benchmark_return_status": "not_computed",
                    "benchmark_identifier": "not_selected",
                    "benchmark_source": "not_selected",
                    "delisting_status": "not_evaluated",
                    "corporate_action_adjustment_status": "not_evaluated",
                    "status_notes": "Scaffold row only; no prices, returns, benchmarks, delistings, or corporate actions loaded.",
                }
            )

    security_fields = list(security_rows[0].keys())
    filing_fields = list(filing_link_rows[0].keys())
    window_fields = list(window_rows[0].keys())
    write_csv(SECURITY_LINK_CANDIDATES, security_fields, security_rows)
    write_csv(FILING_LINK_SCAFFOLD, filing_fields, filing_link_rows)
    write_csv(RETURN_WINDOW_SCAFFOLD, window_fields, window_rows)

    hashes_after = {path.name: sha256(path) for path in required}

    treatment_counts = Counter(row["validated_conservative_treatment"] for row in filing_link_rows)
    link_counts = Counter(row["security_link_status"] for row in filing_link_rows)
    window_status_counts = Counter((row["horizon_years"], row["pre_price_return_window_status"]) for row in window_rows)
    treated_window_counts = Counter(
        (row["horizon_years"], row["pre_price_return_window_status"])
        for row in window_rows
        if row["validated_conservative_treatment"] == "1"
    )
    year_link_counts = Counter((row["filing_year"], row["security_link_status"]) for row in filing_link_rows)

    report = [
        "# Security Linking And Return Window Prep V1 Report",
        "",
        f"Generated as of {AS_OF_DATE.isoformat()}.",
        "",
        "## Guardrails",
        "",
        "- No prices were fetched.",
        "- No returns were computed.",
        "- No benchmark data were loaded.",
        "- No SEC requests were made.",
        "- No empirical performance claims were made.",
        "",
        "## Purpose",
        "",
        "This stage prepares identifier-linking and return-window scaffolds after validated treatment construction. It does not assign a final price identifier. Current ticker and CIK are preserved, but all securities remain `pending_price_identifier` until a point-in-time security master or price source is selected.",
        "",
        "## Outputs",
        "",
        "- `data/linking/security_link_candidates_v1.csv`",
        "- `data/linking/filing_security_link_scaffold_v1.csv`",
        "- `data/returns/return_window_scaffold_v1.csv`",
        "",
        "## Counts",
        "",
        f"- Unique firm link candidates: {len(security_rows):,}",
        f"- Filing link rows: {len(filing_link_rows):,}",
        f"- Return-window scaffold rows: {len(window_rows):,}",
        f"- Treated filing rows: {treatment_counts.get('1', 0):,}",
        f"- Untreated/control filing rows: {treatment_counts.get('0', 0):,}",
        "",
        "## Filing Link Status Counts",
        "",
        markdown_table(["Security link status", "Filing rows"], link_counts.most_common()),
        "",
        "## Return Window Status Counts",
        "",
        markdown_table(
            ["Horizon years", "Pre-price return-window status", "Rows"],
            [[horizon, status, count] for (horizon, status), count in sorted(window_status_counts.items())],
        ),
        "",
        "## Treated Return Window Status Counts",
        "",
        markdown_table(
            ["Horizon years", "Pre-price return-window status", "Treated rows"],
            [[horizon, status, count] for (horizon, status), count in sorted(treated_window_counts.items())],
        ),
        "",
        "## Link Status By Filing Year",
        "",
        markdown_table(
            ["Filing year", "Security link status", "Filing rows"],
            [[year, status, count] for (year, status), count in sorted(year_link_counts.items())],
        ),
        "",
        "## Methodological Notes",
        "",
        "- Ticker alone is not treated as a resolved return-security identifier.",
        "- The project still needs a price/security source decision before fetching returns.",
        "- Primary security rule is not final until the selected data source exposes share class, delisting, corporate-action, and adjusted-return fields.",
        "- Right-censored rows are retained in the scaffold and must not be treated as observed returns.",
        "",
        "## Input Integrity",
        "",
    ]
    for name, before_hash in sorted(hashes_before.items()):
        report.append(f"- `{name}` before: `{before_hash}`")
        report.append(f"- `{name}` after: `{hashes_after[name]}`")
        report.append(f"- `{name}` unchanged: {'yes' if before_hash == hashes_after[name] else 'no'}")
    report += [
        "",
        "## Next Gate",
        "",
        "Select the return/security data source and benchmark source. If the next step requires SEC requests, use the approved SEC user-agent. If the next step uses a market-data provider, first document its identifier, corporate-action, delisting, adjusted-price, and benchmark limitations.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(report), encoding="utf-8")

    checkpoint = [
        "# CHECKPOINT 24: Security Linking And Return Window Prep",
        "",
        f"Generated at: {AS_OF_DATE.isoformat()}",
        "",
        "## Completed",
        "",
        "- Created firm-level security link candidates.",
        "- Created filing-level security link scaffold.",
        "- Created filing-window scaffold for 1-year, 3-year, and 5-year horizons.",
        "- Preserved treatment status and event dates from the validated treatment dataset.",
        "- Marked all security links as pending price identifier assignment.",
        "- Marked right-censored windows separately from mature-but-pending windows.",
        "- Did not fetch prices, compute returns, load benchmarks, make SEC requests, or make empirical claims.",
        "",
        "## Files Created",
        "",
        "- `scripts/prepare_security_linking_and_return_windows_v1.py`",
        "- `data/linking/security_link_candidates_v1.csv`",
        "- `data/linking/filing_security_link_scaffold_v1.csv`",
        "- `data/returns/return_window_scaffold_v1.csv`",
        "- `quality_reports/security_linking_and_return_window_prep_v1_report.md`",
        "- `CHECKPOINT_24_SECURITY_LINKING_AND_RETURN_WINDOW_PREP.md`",
        "",
        "## Counts",
        "",
        f"- Unique firm link candidates: {len(security_rows):,}",
        f"- Filing link rows: {len(filing_link_rows):,}",
        f"- Return-window scaffold rows: {len(window_rows):,}",
        f"- Treated filing rows: {treatment_counts.get('1', 0):,}",
        f"- Untreated/control filing rows: {treatment_counts.get('0', 0):,}",
        "",
        "## Guardrails",
        "",
        "- No prices fetched.",
        "- No returns computed.",
        "- No benchmarks loaded.",
        "- No SEC requests made.",
        "- No empirical performance claims made.",
        "",
        "## Next",
        "",
        "Choose and document the market/security data source before assigning final price identifiers or computing returns.",
        "",
    ]
    CHECKPOINT_OUT.write_text("\n".join(checkpoint), encoding="utf-8")

    print(f"Wrote {SECURITY_LINK_CANDIDATES.relative_to(ROOT)} ({len(security_rows)} rows)")
    print(f"Wrote {FILING_LINK_SCAFFOLD.relative_to(ROOT)} ({len(filing_link_rows)} rows)")
    print(f"Wrote {RETURN_WINDOW_SCAFFOLD.relative_to(ROOT)} ({len(window_rows)} rows)")
    print(f"Wrote {REPORT_OUT.relative_to(ROOT)}")
    print(f"Wrote {CHECKPOINT_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
