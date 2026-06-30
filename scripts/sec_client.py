#!/usr/bin/env python3
"""
Shared SEC EDGAR client utilities.

The client uses SEC public endpoints, enforces a descriptive User-Agent, respects
the SEC fair-access ceiling of 10 requests per second, and caches every response
that the pipeline requests.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import tempfile
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_SEC_DIR = PROJECT_ROOT / "data" / "raw" / "sec"
SEC_SUBMISSIONS_DIR = RAW_SEC_DIR / "submissions"
SEC_HISTORICAL_SUBMISSIONS_DIR = RAW_SEC_DIR / "submissions_historical"
SEC_FILING_DOCUMENTS_DIR = RAW_SEC_DIR / "filings"
LEGACY_REFERENCE_SUBMISSIONS_DIR = PROJECT_ROOT / "data" / "raw" / "reference" / "sec_submissions_metadata"

SEC_SUBMISSION_URL = "https://data.sec.gov/submissions/CIK{cik10}.json"
SEC_HISTORICAL_SUBMISSION_URL = "https://data.sec.gov/submissions/{name}"
SEC_ARCHIVES_DOCUMENT_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_nodash}/{primary_document}"
SEC_ARCHIVES_INDEX_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession_nodash}/{accession_number}-index.html"

MAX_SEC_REQUESTS_PER_SECOND = 10.0


class SecClientError(RuntimeError):
    pass


@dataclass
class FetchResult:
    url: str
    local_path: Path
    status: str
    http_status: int | None
    error_reason: str
    bytes_written: int
    sha256: str
    from_cache: bool


class RateLimiter:
    def __init__(self, requests_per_second: float) -> None:
        if requests_per_second <= 0:
            raise ValueError("requests_per_second must be positive")
        if requests_per_second > MAX_SEC_REQUESTS_PER_SECOND:
            raise ValueError("SEC fair-access limit is max 10 requests/second")
        self.interval = 1.0 / requests_per_second
        self.lock = threading.Lock()
        self.next_allowed = 0.0

    def wait(self) -> None:
        with self.lock:
            now = time.monotonic()
            if now < self.next_allowed:
                time.sleep(self.next_allowed - now)
            self.next_allowed = time.monotonic() + self.interval


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_sec_user_agent(user_agent: str | None = None) -> str:
    value = (user_agent or os.environ.get("SEC_USER_AGENT") or "").strip()
    if len(value) < 25:
        raise SecClientError(
            "SEC_USER_AGENT is required and must be descriptive, for example "
            "'FinancialFirms10KAccess/0.1 contact: name@example.com'."
        )
    if not (re.search(r"@", value) or re.search(r"\bcontact\b", value, re.I)):
        raise SecClientError("SEC_USER_AGENT must include contact information.")
    return value


def ensure_dirs() -> None:
    for path in [SEC_SUBMISSIONS_DIR, SEC_HISTORICAL_SUBMISSIONS_DIR, SEC_FILING_DOCUMENTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def cik10(cik: str) -> str:
    digits = re.sub(r"\D", "", cik or "")
    if not digits:
        return ""
    return digits.zfill(10)


def cik_int(cik: str) -> str:
    normalized = cik10(cik)
    return str(int(normalized)) if normalized else ""


def accession_nodash(accession_number: str) -> str:
    return (accession_number or "").replace("-", "")


def filing_url(cik: str, accession_number: str) -> str:
    return SEC_ARCHIVES_INDEX_URL.format(
        cik_int=cik_int(cik),
        accession_nodash=accession_nodash(accession_number),
        accession_number=accession_number,
    )


def primary_document_url(cik: str, accession_number: str, primary_document: str) -> str:
    return SEC_ARCHIVES_DOCUMENT_URL.format(
        cik_int=cik_int(cik),
        accession_nodash=accession_nodash(accession_number),
        primary_document=primary_document,
    )


def raw_filing_path(cik: str, accession_number: str, primary_document: str) -> Path:
    clean_doc = Path(primary_document).name
    return SEC_FILING_DOCUMENTS_DIR / cik10(cik) / accession_nodash(accession_number) / clean_doc


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def decode_response(raw: bytes) -> bytes:
    if raw[:2] == b"\x1f\x8b":
        return gzip.decompress(raw)
    return raw


def atomic_write(path: Path, payload: bytes, overwrite: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(str(path))
    with tempfile.NamedTemporaryFile(delete=False, dir=str(path.parent)) as tmp:
        tmp.write(payload)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


class SecClient:
    def __init__(self, user_agent: str | None = None, requests_per_second: float = 9.0) -> None:
        ensure_dirs()
        self.user_agent = ensure_sec_user_agent(user_agent)
        self.rate_limiter = RateLimiter(requests_per_second)

    def request_bytes(self, url: str, timeout: int = 60) -> tuple[bytes, int]:
        self.rate_limiter.wait()
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept-Encoding": "gzip",
                "Accept": "*/*",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = int(getattr(response, "status", 200))
            raw = response.read()
        return decode_response(raw), status

    def fetch_to_cache(self, url: str, path: Path, overwrite: bool = False, timeout: int = 60) -> FetchResult:
        if path.exists() and not overwrite:
            return FetchResult(
                url=url,
                local_path=path,
                status="SKIPPED_DUPLICATE",
                http_status=None,
                error_reason="SKIPPED_DUPLICATE",
                bytes_written=path.stat().st_size,
                sha256=sha256_path(path),
                from_cache=True,
            )
        try:
            payload, http_status = self.request_bytes(url, timeout=timeout)
            atomic_write(path, payload, overwrite=overwrite)
            return FetchResult(
                url=url,
                local_path=path,
                status="DOWNLOADED",
                http_status=http_status,
                error_reason="",
                bytes_written=len(payload),
                sha256=sha256_bytes(payload),
                from_cache=False,
            )
        except urllib.error.HTTPError as exc:
            return FetchResult(url, path, "HTTP_FAILURE", exc.code, f"HTTP_{exc.code}: {exc.reason}", 0, "", False)
        except urllib.error.URLError as exc:
            return FetchResult(url, path, "HTTP_FAILURE", None, f"URL_ERROR: {exc.reason}", 0, "", False)
        except FileExistsError:
            return FetchResult(
                url=url,
                local_path=path,
                status="SKIPPED_DUPLICATE",
                http_status=None,
                error_reason="SKIPPED_DUPLICATE",
                bytes_written=path.stat().st_size if path.exists() else 0,
                sha256=sha256_path(path) if path.exists() else "",
                from_cache=True,
            )
        except Exception as exc:  # noqa: BLE001 - captured for audit
            return FetchResult(url, path, "DOWNLOAD_FAILED", None, f"{type(exc).__name__}: {exc}", 0, "", False)

    def get_json(self, url: str, path: Path, overwrite: bool = False) -> tuple[dict[str, Any] | None, FetchResult]:
        result = self.fetch_to_cache(url, path, overwrite=overwrite)
        if result.status in {"DOWNLOADED", "SKIPPED_DUPLICATE"} and path.exists():
            try:
                with path.open("r", encoding="utf-8") as f:
                    return json.load(f), result
            except json.JSONDecodeError as exc:
                result.status = "MALFORMED_METADATA"
                result.error_reason = f"JSONDecodeError: {exc}"
                return None, result
        return None, result

    def get_company_submissions(self, cik: str, refresh: bool = False) -> tuple[dict[str, Any] | None, FetchResult]:
        normalized = cik10(cik)
        path = SEC_SUBMISSIONS_DIR / f"CIK{normalized}.json"
        legacy = LEGACY_REFERENCE_SUBMISSIONS_DIR / f"CIK{normalized}.json"
        if not refresh and not path.exists() and legacy.exists():
            payload = legacy.read_bytes()
            atomic_write(path, payload, overwrite=False)
        return self.get_json(SEC_SUBMISSION_URL.format(cik10=normalized), path, overwrite=refresh)

    def get_historical_submissions(self, name: str, refresh: bool = False) -> tuple[dict[str, Any] | None, FetchResult]:
        safe_name = Path(name).name
        path = SEC_HISTORICAL_SUBMISSIONS_DIR / safe_name
        return self.get_json(SEC_HISTORICAL_SUBMISSION_URL.format(name=safe_name), path, overwrite=refresh)

    def download_primary_document(
        self,
        cik: str,
        accession_number: str,
        primary_document: str,
        overwrite: bool = False,
    ) -> FetchResult:
        url = primary_document_url(cik, accession_number, primary_document)
        path = raw_filing_path(cik, accession_number, primary_document)
        return self.fetch_to_cache(url, path, overwrite=overwrite, timeout=120)

