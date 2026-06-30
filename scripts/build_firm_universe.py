#!/usr/bin/env python3
"""
Build the firm-universe layer for the 10-K access-language project.

This script intentionally downloads only issuer/reference metadata:
- SEC current listed ticker feed
- SEC company submissions metadata for SIC, SIC description, names, and current tickers

It does not download filing documents.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
RAW_REFERENCE_DIR = PROJECT_ROOT / "data" / "raw" / "reference"
SEC_SUBMISSIONS_META_DIR = RAW_REFERENCE_DIR / "sec_submissions_metadata"
QUALITY_DIR = PROJECT_ROOT / "data" / "quality"
MANIFEST_DIR = PROJECT_ROOT / "data" / "manifests" / "source_manifests"

SEC_TICKERS_EXCHANGE_URL = "https://www.sec.gov/files/company_tickers_exchange.json"
SEC_SUBMISSION_URL = "https://data.sec.gov/submissions/CIK{cik10}.json"

UNIVERSE_PATH = CONFIG_DIR / "firm_universe.csv"
MANIFEST_PATH = MANIFEST_DIR / "firm_universe_sources.json"
QUALITY_REPORT_PATH = QUALITY_DIR / "firm_universe_quality_report.md"
MISSING_CIKS_PATH = QUALITY_DIR / "firm_universe_missing_ciks.csv"
DUPLICATE_TICKERS_PATH = QUALITY_DIR / "firm_universe_duplicate_tickers.csv"
TICKER_CHANGES_PATH = QUALITY_DIR / "firm_universe_ticker_changes.csv"
AMBIGUOUS_FIRMS_PATH = QUALITY_DIR / "firm_universe_ambiguous_firms.csv"
IDENTIFIER_CROSSWALK_PATH = QUALITY_DIR / "firm_identifier_crosswalk.csv"

UNIVERSE_SOURCE_LABEL = "SEC_CURRENT_LISTED_WITH_SEC_SIC"
SURVIVORSHIP_NOTE = (
    "Current-listed SEC ticker universe as of source_date; not point-in-time for 2015-2025. "
    "Delisted, merged, bankrupt, and formerly listed firms are not fully represented."
)
ELIGIBLE_EXCHANGES = {"Nasdaq", "NYSE", "CBOE"}

FIRM_UNIVERSE_FIELDS = [
    "firm_id",
    "company_name",
    "ticker",
    "cik",
    "sic",
    "sic_description",
    "sector",
    "industry",
    "exchange",
    "source",
    "source_date",
    "inclusion_reason",
    "notes",
]

FINANCIAL_SIC_GROUPS = {
    "602": ("Financials", "Commercial Banks"),
    "603": ("Financials", "Savings Institutions"),
    "606": ("Financials", "Credit Unions"),
    "608": ("Financials", "Foreign Banking Organizations"),
    "609": ("Financials", "Banking Services"),
    "611": ("Financials", "Credit Agencies"),
    "614": ("Financials", "Consumer Finance"),
    "615": ("Financials", "Business Finance"),
    "616": ("Financials", "Mortgage Finance"),
    "617": ("Financials", "Finance Leasing"),
    "619": ("Financials", "Finance Services"),
    "621": ("Financials", "Brokers and Dealers"),
    "622": ("Financials", "Commodity Contracts"),
    "628": ("Financials", "Asset Management and Investment Advice"),
    "631": ("Financials", "Life Insurance"),
    "632": ("Financials", "Health and Accident Insurance"),
    "633": ("Financials", "Property and Casualty Insurance"),
    "635": ("Financials", "Surety Insurance"),
    "636": ("Financials", "Title Insurance"),
    "639": ("Financials", "Insurance Carriers"),
    "641": ("Financials", "Insurance Agents and Brokers"),
}

SELECTED_INVESTMENT_SICS = {
    "6798": ("Financials", "Mortgage REIT or Selected Investment Vehicle"),
    "6799": ("Financials", "Selected Investment and Capital Markets"),
}

FINTECH_NAME_PATTERNS = [
    (re.compile(r"\bPAYMENTS?\b|\bPAYMENT\b|\bPAYPAL\b|\bFISERV\b|\bPAYONEER\b|\bSHIFT4\b|\bMARQETA\b", re.I), "Payments"),
    (re.compile(r"\bBLOCK,\s*INC\.?\b|\bSQUARE\b|\bSTRIPE\b|\bTOAST,\s*INC\.?\b", re.I), "Payments Platform"),
    (re.compile(r"\bVISA\b|\bMASTERCARD\b|\bDISCOVER\b|\bAMERICAN EXPRESS\b", re.I), "Card Network or Payments"),
    (re.compile(r"\bFINTECH\b|\bDIGITAL BANK\b|\bNEOBANK\b", re.I), "Fintech Platform"),
    (re.compile(r"\bSOFI\b|\bUPSTART\b|\bAFFIRM\b|\bLENDINGCLUB\b|\bLENDINGTREE\b|\bENOVA\b", re.I), "Digital Lending"),
    (re.compile(r"\bROCKET COMPANIES\b|\bLOANDEPOT\b|\bMORTGAGE\b", re.I), "Mortgage Finance"),
    (re.compile(r"\bROBINHOOD\b|\bCOINBASE\b|\bBROKERAGE\b|\bTRADING\b", re.I), "Brokerage or Crypto Platform"),
    (re.compile(r"\bNASDAQ\b|\bCBOE\b|\bCME\b|\bINTERCONTINENTAL EXCHANGE\b|\bICE\b", re.I), "Exchange or Market Infrastructure"),
    (re.compile(r"\bFACTSET\b|\bMORNINGSTAR\b|\bMSCI\b|\bS&P GLOBAL\b|\bMOODYS\b", re.I), "Capital Markets Data"),
    (re.compile(r"\bLEMONADE\b|\bROOT\b|\bINSURTECH\b|\bOSCAR HEALTH\b", re.I), "Insurance Technology"),
]

EXCLUDE_NAME_PATTERN = re.compile(
    r"\bETF\b|\bETN\b|\bCLOSED[- ]END\b|\bSPAC\b|\bACQUISITION CORP\b|"
    r"\bACQUISITION CORPORATION\b|\bBLANK CHECK\b|\bSPECIAL PURPOSE\b|"
    r"\bTRUST\b.*\bSERIES\b|\bFUND\b|\bPORTFOLIO\b",
    re.I,
)

MORTGAGE_OR_CAPITAL_MARKETS_PATTERN = re.compile(
    r"\bMORTGAGE\b|\bCAPITAL\b|\bFINANCE\b|\bFINANCIAL\b|\bCREDIT\b|"
    r"\bLOAN\b|\bLENDING\b|\bASSET\b|\bINVESTMENT\b|\bMARKETS\b",
    re.I,
)


@dataclass
class TickerRecord:
    cik: str
    company_name: str
    ticker: str
    exchange: str


@dataclass
class CompanyMetadata:
    cik: str
    name: str
    sic: str
    sic_description: str
    tickers: list[str]
    exchanges: list[str]
    former_names: list[str]
    fetch_status: str
    fetch_error: str = ""


class RateLimiter:
    def __init__(self, per_second: float) -> None:
        self.interval = 1.0 / per_second
        self.lock = threading.Lock()
        self.next_allowed = 0.0

    def wait(self) -> None:
        with self.lock:
            now = time.monotonic()
            if now < self.next_allowed:
                time.sleep(self.next_allowed - now)
            self.next_allowed = time.monotonic() + self.interval


def ensure_dirs() -> None:
    for path in [CONFIG_DIR, RAW_REFERENCE_DIR, SEC_SUBMISSIONS_META_DIR, QUALITY_DIR, MANIFEST_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json_url(url: str, user_agent: str, timeout: int = 60) -> Any:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")


def load_sec_ticker_feed(user_agent: str, refresh: bool) -> list[TickerRecord]:
    path = RAW_REFERENCE_DIR / "sec_company_tickers_exchange.json"
    if refresh or not path.exists():
        payload = read_json_url(SEC_TICKERS_EXCHANGE_URL, user_agent)
        write_json(path, payload)
    else:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

    fields = payload["fields"]
    rows: list[TickerRecord] = []
    for item in payload["data"]:
        row = dict(zip(fields, item, strict=True))
        rows.append(
            TickerRecord(
                cik=str(row["cik"]).zfill(10),
                company_name=str(row["name"]).strip(),
                ticker=str(row["ticker"]).strip().upper(),
                exchange=str(row["exchange"]).strip(),
            )
        )
    return rows


def parse_company_metadata(cik: str, payload: dict[str, Any], status: str, error: str = "") -> CompanyMetadata:
    former_names = []
    for item in payload.get("formerNames") or []:
        name = item.get("name")
        if name:
            former_names.append(str(name).strip())
    return CompanyMetadata(
        cik=cik,
        name=str(payload.get("name") or "").strip(),
        sic=str(payload.get("sic") or "").strip(),
        sic_description=str(payload.get("sicDescription") or "").strip(),
        tickers=[str(x).strip().upper() for x in payload.get("tickers") or [] if str(x).strip()],
        exchanges=[str(x).strip() for x in payload.get("exchanges") or [] if str(x).strip()],
        former_names=former_names,
        fetch_status=status,
        fetch_error=error,
    )


def fetch_company_metadata(cik: str, user_agent: str, refresh: bool, limiter: RateLimiter) -> CompanyMetadata:
    path = SEC_SUBMISSIONS_META_DIR / f"CIK{cik}.json"
    if not refresh and path.exists():
        try:
            with path.open("r", encoding="utf-8") as f:
                return parse_company_metadata(cik, json.load(f), "cached")
        except (json.JSONDecodeError, OSError) as exc:
            return CompanyMetadata(cik, "", "", "", [], [], [], "cache_error", str(exc))

    limiter.wait()
    try:
        payload = read_json_url(SEC_SUBMISSION_URL.format(cik10=cik), user_agent)
        write_json(path, payload)
        return parse_company_metadata(cik, payload, "fetched")
    except urllib.error.HTTPError as exc:
        return CompanyMetadata(cik, "", "", "", [], [], [], f"http_{exc.code}", str(exc))
    except Exception as exc:  # noqa: BLE001 - recorded in QA output
        return CompanyMetadata(cik, "", "", "", [], [], [], "fetch_error", str(exc))


def fetch_all_company_metadata(
    ciks: list[str],
    user_agent: str,
    refresh: bool,
    max_workers: int,
    requests_per_second: float,
) -> dict[str, CompanyMetadata]:
    limiter = RateLimiter(requests_per_second)
    metadata: dict[str, CompanyMetadata] = {}
    total = len(ciks)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fetch_company_metadata, cik, user_agent, refresh, limiter): cik
            for cik in ciks
        }
        for idx, future in enumerate(as_completed(futures), start=1):
            cik = futures[future]
            try:
                metadata[cik] = future.result()
            except Exception as exc:  # noqa: BLE001
                metadata[cik] = CompanyMetadata(cik, "", "", "", [], [], [], "worker_error", str(exc))
            if idx % 500 == 0 or idx == total:
                print(f"Fetched SEC company metadata {idx}/{total}", file=sys.stderr)
    return metadata


def common_ticker_score(ticker: str, exchange: str = "") -> tuple[int, int, int, str]:
    t = ticker.upper()
    preferred_or_debt = bool(re.search(r"[-./]P[A-Z]?$|[-./]PR|[-./]WS$|[-./]WT$|[-./]U$|[-./]R$", t))
    has_separator = bool(re.search(r"[-./]", t))
    ineligible_exchange = exchange not in ELIGIBLE_EXCHANGES
    return (1 if ineligible_exchange else 0, 1 if preferred_or_debt else 0, 1 if has_separator else 0, t)


def select_primary_ticker(feed_records: list[TickerRecord], metadata: CompanyMetadata) -> tuple[str, str]:
    exchange_by_ticker = {r.ticker: r.exchange for r in feed_records}
    candidates = [r.ticker for r in feed_records]
    if metadata.tickers:
        ordered = metadata.tickers + [t for t in candidates if t not in metadata.tickers]
    else:
        ordered = candidates
    selected = sorted(ordered, key=lambda t: common_ticker_score(t, exchange_by_ticker.get(t, "")))[0] if ordered else ""
    exchange = ""
    for record in feed_records:
        if record.ticker == selected:
            exchange = record.exchange
            break
    if not exchange and metadata.exchanges:
        exchange = metadata.exchanges[0]
    return selected, exchange


def sic_group(sic: str) -> tuple[str, str, str]:
    if len(sic) >= 3 and sic[:3] in FINANCIAL_SIC_GROUPS:
        sector, industry = FINANCIAL_SIC_GROUPS[sic[:3]]
        return sector, industry, f"financial_sic_{sic[:3]}"
    if sic in SELECTED_INVESTMENT_SICS:
        sector, industry = SELECTED_INVESTMENT_SICS[sic]
        return sector, industry, f"selected_investment_sic_{sic}"
    return "", "", ""


def fintech_name_group(name: str) -> tuple[str, str, str]:
    for pattern, industry in FINTECH_NAME_PATTERNS:
        if pattern.search(name):
            return "Financial Technology", industry, f"fintech_name_keyword_{industry.lower().replace(' ', '_')}"
    return "", "", ""


def should_exclude_name(name: str) -> bool:
    return bool(EXCLUDE_NAME_PATTERN.search(name))


def classify_firm(record_name: str, metadata: CompanyMetadata) -> tuple[bool, str, str, str, list[str], bool]:
    name = metadata.name or record_name
    notes: list[str] = [SURVIVORSHIP_NOTE]
    ambiguous = False

    if not metadata.sic:
        notes.append("Missing SEC SIC in company submissions metadata.")
        ambiguous = True

    excluded_by_name = should_exclude_name(name)
    sector, industry, reason = sic_group(metadata.sic)

    if reason.startswith("selected_investment_sic") and not MORTGAGE_OR_CAPITAL_MARKETS_PATTERN.search(name):
        notes.append("Selected investment SIC without mortgage/capital-markets name signal; excluded as ambiguous investment vehicle.")
        return False, "", "", "", notes, True

    if sector and not excluded_by_name:
        return True, sector, industry, reason, notes, ambiguous

    fintech_sector, fintech_industry, fintech_reason = fintech_name_group(name)
    if fintech_sector and not excluded_by_name:
        if not sector:
            notes.append("Included by fintech/capital-markets name keyword outside core financial SIC groups.")
            ambiguous = True
        return True, fintech_sector, fintech_industry, fintech_reason, notes, ambiguous

    if sector and excluded_by_name:
        notes.append("Financial SIC but excluded by fund/SPAC/trust/security-name pattern.")
        return False, "", "", "", notes, True

    return False, "", "", "", notes, ambiguous


def build_universe(
    ticker_records: list[TickerRecord],
    metadata_by_cik: dict[str, CompanyMetadata],
    source_date: str,
) -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]]]]:
    records_by_cik: dict[str, list[TickerRecord]] = {}
    for record in ticker_records:
        records_by_cik.setdefault(record.cik, []).append(record)

    universe: list[dict[str, str]] = []
    missing_ciks: list[dict[str, str]] = []
    ticker_change_risks: list[dict[str, str]] = []
    ambiguous_firms: list[dict[str, str]] = []
    identifier_crosswalk: list[dict[str, str]] = []

    for cik, records in sorted(records_by_cik.items()):
        metadata = metadata_by_cik.get(cik) or CompanyMetadata(cik, "", "", "", [], [], [], "not_fetched")
        if metadata.fetch_status not in {"cached", "fetched"}:
            missing_ciks.append(
                {
                    "cik": cik,
                    "company_name": records[0].company_name,
                    "ticker": records[0].ticker,
                    "exchange": records[0].exchange,
                    "status": metadata.fetch_status,
                    "reason": metadata.fetch_error,
                }
            )

        ticker, exchange = select_primary_ticker(records, metadata)
        company_name = metadata.name or records[0].company_name
        included, sector, industry, reason, notes, ambiguous = classify_firm(company_name, metadata)
        firm_id = f"CIK{cik}"

        for rec in records:
            identifier_crosswalk.append(
                {
                    "firm_id": firm_id,
                    "identifier_type": "ticker",
                    "identifier_value": rec.ticker,
                    "exchange": rec.exchange,
                    "source": UNIVERSE_SOURCE_LABEL,
                    "source_date": source_date,
                }
            )
        identifier_crosswalk.append(
            {
                "firm_id": firm_id,
                "identifier_type": "cik",
                "identifier_value": cik,
                "exchange": "",
                "source": UNIVERSE_SOURCE_LABEL,
                "source_date": source_date,
            }
        )

        if len(records) > 1 or metadata.former_names:
            ticker_change_risks.append(
                {
                    "firm_id": firm_id,
                    "cik": cik,
                    "company_name": company_name,
                    "selected_ticker": ticker,
                    "current_sec_tickers": "|".join(sorted({r.ticker for r in records})),
                    "former_names": "|".join(metadata.former_names),
                    "status": "review_required",
                    "notes": "SEC current feeds do not provide point-in-time historical ticker changes.",
                }
            )

        if included and exchange not in ELIGIBLE_EXCHANGES:
            notes.append(
                f"Excluded from firm_universe.csv because selected exchange `{exchange or 'UNKNOWN'}` is not in "
                f"eligible exchange-listed venues: {', '.join(sorted(ELIGIBLE_EXCHANGES))}."
            )
            included = False
            ambiguous = True

        if ambiguous:
            ambiguous_firms.append(
                {
                    "firm_id": firm_id,
                    "cik": cik,
                    "company_name": company_name,
                    "ticker": ticker,
                    "sic": metadata.sic,
                    "sic_description": metadata.sic_description,
                    "classification_status": "ambiguous_or_manual_review",
                    "notes": " ".join(notes),
                }
            )

        if included:
            universe.append(
                {
                    "firm_id": firm_id,
                    "company_name": company_name,
                    "ticker": ticker,
                    "cik": cik,
                    "sic": metadata.sic,
                    "sic_description": metadata.sic_description,
                    "sector": sector,
                    "industry": industry,
                    "exchange": exchange,
                    "source": UNIVERSE_SOURCE_LABEL,
                    "source_date": source_date,
                    "inclusion_reason": reason,
                    "notes": " ".join(notes),
                }
            )

    duplicate_tickers = find_duplicate_tickers(universe)
    quality = {
        "missing_ciks": missing_ciks,
        "duplicate_tickers": duplicate_tickers,
        "ticker_changes": ticker_change_risks,
        "ambiguous_firms": ambiguous_firms,
        "identifier_crosswalk": identifier_crosswalk,
    }
    return sorted(universe, key=lambda row: (row["company_name"].upper(), row["ticker"])), quality


def find_duplicate_tickers(universe: list[dict[str, str]]) -> list[dict[str, str]]:
    by_ticker: dict[str, list[dict[str, str]]] = {}
    for row in universe:
        by_ticker.setdefault(row["ticker"], []).append(row)
    duplicates: list[dict[str, str]] = []
    for ticker, rows in sorted(by_ticker.items()):
        if ticker and len(rows) > 1:
            for row in rows:
                duplicates.append(
                    {
                        "ticker": ticker,
                        "firm_id": row["firm_id"],
                        "cik": row["cik"],
                        "company_name": row["company_name"],
                        "exchange": row["exchange"],
                        "notes": "Duplicate selected ticker in firm universe; requires manual review.",
                    }
                )
    return duplicates


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_quality_report(
    universe: list[dict[str, str]],
    quality: dict[str, list[dict[str, str]]],
    source_date: str,
    ticker_feed_count: int,
    unique_cik_count: int,
) -> None:
    by_industry: dict[str, int] = {}
    by_reason: dict[str, int] = {}
    by_exchange: dict[str, int] = {}
    for row in universe:
        by_industry[row["industry"]] = by_industry.get(row["industry"], 0) + 1
        by_reason[row["inclusion_reason"]] = by_reason.get(row["inclusion_reason"], 0) + 1
        by_exchange[row["exchange"]] = by_exchange.get(row["exchange"], 0) + 1

    lines = [
        "# Firm Universe Quality Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        f"Source date: {source_date}",
        f"Universe source label: `{UNIVERSE_SOURCE_LABEL}`",
        "",
        "## Scope Warning",
        "",
        SURVIVORSHIP_NOTE,
        f"Eligible exchange-listed venues in this build: {', '.join(sorted(ELIGIBLE_EXCHANGES))}. "
        "OTC and unknown-exchange firms are retained for review in QA outputs but excluded from firm_universe.csv.",
        "",
        "This quality report must exist before any filing downloads are started.",
        "",
        "## Counts",
        "",
        f"- SEC current ticker rows read: {ticker_feed_count}",
        f"- Unique CIKs in SEC current ticker feed: {unique_cik_count}",
        f"- Included firms: {len(universe)}",
        f"- Missing or failed CIK metadata rows: {len(quality['missing_ciks'])}",
        f"- Duplicate selected tickers: {len(quality['duplicate_tickers'])}",
        f"- Ticker-change or multi-ticker review rows: {len(quality['ticker_changes'])}",
        f"- Ambiguous/manual-review firms: {len(quality['ambiguous_firms'])}",
        "",
        "## Included Firms By Industry",
        "",
    ]
    for key, value in sorted(by_industry.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Included Firms By Inclusion Reason", ""])
    for key, value in sorted(by_reason.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Included Firms By Exchange", ""])
    for key, value in sorted(by_exchange.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {key or 'UNKNOWN'}: {value}")
    lines.extend(
        [
            "",
            "## Quality Output Files",
            "",
            f"- `{MISSING_CIKS_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{DUPLICATE_TICKERS_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{TICKER_CHANGES_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{AMBIGUOUS_FIRMS_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{IDENTIFIER_CROSSWALK_PATH.relative_to(PROJECT_ROOT)}`",
            "",
            "## Ticker Change Limitation",
            "",
            "The SEC current listed ticker feed and current submissions metadata do not provide complete point-in-time ticker histories. "
            "The ticker-change output therefore lists multi-ticker issuers and issuers with former company names as review candidates, "
            "not a complete ticker-change history.",
            "",
            "## Next Required Upgrade",
            "",
            "For a historical 2015-2025 research sample, augment this layer with CRSP, Compustat, FactSet, Refinitiv, "
            "or another point-in-time security master that covers delisted, merged, bankrupt, and renamed issuers.",
            "",
        ]
    )
    QUALITY_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def write_manifest(source_date: str) -> None:
    paths = [
        RAW_REFERENCE_DIR / "sec_company_tickers_exchange.json",
        UNIVERSE_PATH,
        QUALITY_REPORT_PATH,
        MISSING_CIKS_PATH,
        DUPLICATE_TICKERS_PATH,
        TICKER_CHANGES_PATH,
        AMBIGUOUS_FIRMS_PATH,
        IDENTIFIER_CROSSWALK_PATH,
    ]
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_date": source_date,
        "source_label": UNIVERSE_SOURCE_LABEL,
        "source_urls": [
            SEC_TICKERS_EXCHANGE_URL,
            "https://data.sec.gov/submissions/CIK##########.json",
        ],
        "filing_downloads_performed": False,
        "survivorship_bias_note": SURVIVORSHIP_NOTE,
        "files": [
            {
                "path": str(path.relative_to(PROJECT_ROOT)),
                "sha256": sha256_path(path) if path.exists() else "",
            }
            for path in paths
        ],
    }
    write_json(MANIFEST_PATH, manifest)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build current-listed SEC financial/fintech firm universe.")
    parser.add_argument("--refresh", action="store_true", help="Refresh SEC reference metadata instead of using cache.")
    parser.add_argument("--max-workers", type=int, default=8, help="Concurrent SEC metadata workers.")
    parser.add_argument("--requests-per-second", type=float, default=8.0, help="Global SEC metadata request rate.")
    parser.add_argument(
        "--source-date",
        default=date.today().isoformat(),
        help="Date to record in firm_universe.csv source_date.",
    )
    parser.add_argument(
        "--user-agent",
        default="financialfirms_10K_access research admin@example.com",
        help="SEC-compliant User-Agent with contact information.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    ticker_records = load_sec_ticker_feed(args.user_agent, args.refresh)
    ciks = sorted({record.cik for record in ticker_records})
    metadata_by_cik = fetch_all_company_metadata(
        ciks,
        args.user_agent,
        args.refresh,
        max_workers=args.max_workers,
        requests_per_second=args.requests_per_second,
    )
    universe, quality = build_universe(ticker_records, metadata_by_cik, args.source_date)

    write_csv(UNIVERSE_PATH, universe, FIRM_UNIVERSE_FIELDS)
    write_csv(
        MISSING_CIKS_PATH,
        quality["missing_ciks"],
        ["cik", "company_name", "ticker", "exchange", "status", "reason"],
    )
    write_csv(
        DUPLICATE_TICKERS_PATH,
        quality["duplicate_tickers"],
        ["ticker", "firm_id", "cik", "company_name", "exchange", "notes"],
    )
    write_csv(
        TICKER_CHANGES_PATH,
        quality["ticker_changes"],
        ["firm_id", "cik", "company_name", "selected_ticker", "current_sec_tickers", "former_names", "status", "notes"],
    )
    write_csv(
        AMBIGUOUS_FIRMS_PATH,
        quality["ambiguous_firms"],
        ["firm_id", "cik", "company_name", "ticker", "sic", "sic_description", "classification_status", "notes"],
    )
    write_csv(
        IDENTIFIER_CROSSWALK_PATH,
        quality["identifier_crosswalk"],
        ["firm_id", "identifier_type", "identifier_value", "exchange", "source", "source_date"],
    )
    write_quality_report(universe, quality, args.source_date, len(ticker_records), len(ciks))
    write_manifest(args.source_date)

    print(f"Wrote {UNIVERSE_PATH.relative_to(PROJECT_ROOT)} with {len(universe)} firms")
    print(f"Wrote {QUALITY_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
