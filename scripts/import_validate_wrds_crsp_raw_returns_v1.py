"""Validate raw WRDS CRSP daily-return and benchmark pulls.

This stage checks whether raw issuer and benchmark rows are available for
previously linked return windows. It records coverage status and candidate
start/end trading dates, but it does not compound returns, compute abnormal
returns, run regressions, or make empirical claims.
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from bisect import bisect_left
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WINDOW_REQUEST = ROOT / "data" / "returns" / "wrds_crsp_return_windows_linked_request_v1.csv"
DAILY_RAW = ROOT / "data" / "returns" / "wrds_crsp_daily_returns_raw_v1.csv"
BENCHMARK_RAW = ROOT / "data" / "returns" / "wrds_crsp_market_benchmark_raw_v1.csv"
MANIFEST = ROOT / "quality_reports" / "wrds_crsp_return_pull_manifest_v1.txt"

COVERAGE_OUT = ROOT / "data" / "returns" / "wrds_crsp_return_window_raw_coverage_v1.csv"
REPORT_OUT = ROOT / "quality_reports" / "wrds_crsp_raw_return_import_validation_v1_report.md"
CHECKPOINT_OUT = ROOT / "CHECKPOINT_27_WRDS_CRSP_RAW_RETURN_IMPORT_VALIDATION.md"

TRADING_DAY_BUFFER_DAYS = 10

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


def parse_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def clean_int(value: str) -> str:
    value = (value or "").strip()
    if value.endswith(".0"):
        return value[:-2]
    return value


def manifest_count(text: str, label: str) -> int | None:
    match = re.search(rf"^{re.escape(label)}:\s*([0-9,]+)\s*$", text, flags=re.MULTILINE)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def markdown_table(headers: list[str], rows: list[list[str | int]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def first_on_or_after(dates: list, target, max_date):
    idx = bisect_left(dates, target)
    if idx >= len(dates):
        return None
    candidate = dates[idx]
    if candidate > max_date:
        return None
    return candidate


def load_daily_index() -> tuple[dict[str, list], dict[str, Counter], int, int]:
    dates_by_permno: dict[str, set] = defaultdict(set)
    stats_by_permno: dict[str, Counter] = defaultdict(Counter)
    row_count = 0
    duplicate_count = 0
    seen_keys: set[tuple[str, str]] = set()

    with DAILY_RAW.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"permno", "date", "ret", "dlret", "ret_with_delisting"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Daily raw file missing fields: {sorted(missing)}")

        for row in reader:
            row_count += 1
            permno = clean_int(row["permno"])
            date_text = row["date"]
            key = (permno, date_text)
            if key in seen_keys:
                duplicate_count += 1
            seen_keys.add(key)

            date_value = parse_date(date_text)
            dates_by_permno[permno].add(date_value)
            stats = stats_by_permno[permno]
            stats["rows"] += 1
            if row.get("ret", "") in {"", "nan", "NaN"}:
                stats["missing_ret_rows"] += 1
            if row.get("dlret", "") not in {"", "nan", "NaN"}:
                stats["dlret_rows"] += 1
            if row.get("ret_with_delisting", "") in {"", "nan", "NaN"}:
                stats["missing_ret_with_delisting_rows"] += 1

    sorted_dates = {permno: sorted(dates) for permno, dates in dates_by_permno.items()}
    return sorted_dates, stats_by_permno, row_count, duplicate_count


def load_benchmark_dates() -> tuple[list, int, int, Counter]:
    dates: list = []
    seen: set[str] = set()
    duplicate_count = 0
    stats: Counter = Counter()
    with BENCHMARK_RAW.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"date", "vwretd", "vwretx", "ewretd", "ewretx", "sprtrn"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Benchmark raw file missing fields: {sorted(missing)}")
        for row in reader:
            stats["rows"] += 1
            date_text = row["date"]
            if date_text in seen:
                duplicate_count += 1
            seen.add(date_text)
            dates.append(parse_date(date_text))
            for field in ["vwretd", "vwretx", "ewretd", "ewretx", "sprtrn"]:
                if row.get(field, "") in {"", "nan", "NaN"}:
                    stats[f"missing_{field}"] += 1
    return sorted(dates), len(dates), duplicate_count, stats


def classify_window(row: dict[str, str], dates_by_permno: dict[str, list], benchmark_dates: list) -> dict[str, str]:
    permno = clean_int(row["permno"])
    start_search = parse_date(row["window_start_search_date"])
    target_end = parse_date(row["target_calendar_end_date"])
    buffered_end = target_end + timedelta(days=TRADING_DAY_BUFFER_DAYS)

    issuer_dates = dates_by_permno.get(permno, [])
    issuer_start = first_on_or_after(issuer_dates, start_search, buffered_end)
    issuer_end = first_on_or_after(issuer_dates, target_end, buffered_end)
    benchmark_start = first_on_or_after(benchmark_dates, start_search, buffered_end)
    benchmark_end = first_on_or_after(benchmark_dates, target_end, buffered_end)

    reasons: list[str] = []
    if not issuer_dates:
        reasons.append("no_issuer_daily_rows_for_permno")
    elif issuer_start is None:
        reasons.append("issuer_start_trading_date_unavailable_within_buffer")
    elif issuer_end is None:
        reasons.append("issuer_end_trading_date_unavailable_within_buffer")

    if not benchmark_dates:
        reasons.append("no_benchmark_daily_rows")
    elif benchmark_start is None:
        reasons.append("benchmark_start_trading_date_unavailable_within_buffer")
    elif benchmark_end is None:
        reasons.append("benchmark_end_trading_date_unavailable_within_buffer")

    status = "raw_coverage_ready_for_return_computation" if not reasons else "raw_coverage_incomplete"

    return {
        **row,
        "issuer_start_trading_date": issuer_start.isoformat() if issuer_start else "",
        "issuer_end_trading_date": issuer_end.isoformat() if issuer_end else "",
        "benchmark_start_trading_date": benchmark_start.isoformat() if benchmark_start else "",
        "benchmark_end_trading_date": benchmark_end.isoformat() if benchmark_end else "",
        "raw_return_coverage_status": status,
        "raw_return_coverage_reason": "; ".join(reasons) if reasons else "issuer_and_benchmark_raw_rows_available",
        "trading_day_buffer_days": str(TRADING_DAY_BUFFER_DAYS),
        "return_computation_status": "not_computed",
    }


def main() -> None:
    required = [WINDOW_REQUEST, DAILY_RAW, BENCHMARK_RAW, MANIFEST]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")

    hashes_before = {path.name: sha256(path) for path in required}
    manifest_text = MANIFEST.read_text(encoding="utf-8")

    window_rows = read_csv(WINDOW_REQUEST)
    ready_windows = [
        row
        for row in window_rows
        if row["post_link_return_window_status"] == "ready_for_wrds_daily_return_request"
    ]

    dates_by_permno, stats_by_permno, daily_row_count, daily_duplicate_count = load_daily_index()
    benchmark_dates, benchmark_row_count, benchmark_duplicate_count, benchmark_stats = load_benchmark_dates()

    coverage_rows = [classify_window(row, dates_by_permno, benchmark_dates) for row in ready_windows]
    coverage_fields = list(coverage_rows[0].keys()) if coverage_rows else []
    write_csv(COVERAGE_OUT, coverage_fields, coverage_rows)

    hashes_after = {path.name: sha256(path) for path in required}

    manifest_ready = manifest_count(manifest_text, "Ready windows")
    manifest_permnos = manifest_count(manifest_text, "Unique PERMNOs")
    manifest_daily = manifest_count(manifest_text, "Daily return rows")
    manifest_delist = manifest_count(manifest_text, "Delisting return rows")
    manifest_benchmark = manifest_count(manifest_text, "Benchmark rows")

    coverage_counts = Counter(row["raw_return_coverage_status"] for row in coverage_rows)
    coverage_reasons = Counter(row["raw_return_coverage_reason"] for row in coverage_rows)
    horizon_counts = Counter(
        (row["horizon_years"], row["raw_return_coverage_status"]) for row in coverage_rows
    )
    treated_horizon_counts = Counter(
        (row["horizon_years"], row["raw_return_coverage_status"])
        for row in coverage_rows
        if row["validated_conservative_treatment"] == "1"
    )
    unique_permnos_in_request = {clean_int(row["permno"]) for row in ready_windows}
    unique_permnos_in_daily = set(dates_by_permno)

    manifest_checks = [
        ["Ready windows", manifest_ready, len(ready_windows), manifest_ready == len(ready_windows)],
        ["Unique PERMNOs", manifest_permnos, len(unique_permnos_in_request), manifest_permnos == len(unique_permnos_in_request)],
        ["Daily return rows", manifest_daily, daily_row_count, manifest_daily == daily_row_count],
        ["Benchmark rows", manifest_benchmark, benchmark_row_count, manifest_benchmark == benchmark_row_count],
    ]

    report = [
        "# WRDS CRSP Raw Return Import Validation V1 Report",
        "",
        "## Guardrails",
        "",
        "- Raw WRDS daily issuer returns were imported and validated for coverage only.",
        "- Raw CRSP market benchmark rows were imported and validated for coverage only.",
        "- No 1-year, 3-year, or 5-year issuer returns were computed.",
        "- No benchmark-adjusted returns were computed.",
        "- No regressions, tests, or empirical performance claims were made.",
        "",
        "## Inputs",
        "",
        "- `data/returns/wrds_crsp_return_windows_linked_request_v1.csv`",
        "- `data/returns/wrds_crsp_daily_returns_raw_v1.csv`",
        "- `data/returns/wrds_crsp_market_benchmark_raw_v1.csv`",
        "- `quality_reports/wrds_crsp_return_pull_manifest_v1.txt`",
        "",
        "## Output",
        "",
        "- `data/returns/wrds_crsp_return_window_raw_coverage_v1.csv`",
        "",
        "## Manifest Reconciliation",
        "",
        markdown_table(
            ["Metric", "Manifest count", "Local count", "Matches"],
            manifest_checks,
        ),
        "",
        "## Raw File Counts",
        "",
        f"- Ready return-window rows checked: {len(ready_windows):,}",
        f"- Daily issuer rows: {daily_row_count:,}",
        f"- Daily issuer duplicate PERMNO-date rows: {daily_duplicate_count:,}",
        f"- Unique PERMNOs in request: {len(unique_permnos_in_request):,}",
        f"- Unique PERMNOs in raw daily file: {len(unique_permnos_in_daily):,}",
        f"- Requested PERMNOs missing from raw daily file: {len(unique_permnos_in_request - unique_permnos_in_daily):,}",
        f"- Delisting-return rows reported in manifest: {manifest_delist:,}" if manifest_delist is not None else "- Delisting-return rows reported in manifest: not_found",
        f"- Raw daily rows with nonblank `dlret`: {sum(stats.get('dlret_rows', 0) for stats in stats_by_permno.values()):,}",
        f"- Benchmark rows: {benchmark_row_count:,}",
        f"- Benchmark duplicate date rows: {benchmark_duplicate_count:,}",
        "",
        "## Raw Coverage Status Counts",
        "",
        markdown_table(["Coverage status", "Window rows"], [[k, v] for k, v in sorted(coverage_counts.items())]),
        "",
        "## Raw Coverage Reason Counts",
        "",
        markdown_table(["Coverage reason", "Window rows"], [[k, v] for k, v in sorted(coverage_reasons.items())]),
        "",
        "## Coverage By Horizon",
        "",
        markdown_table(
            ["Horizon years", "Coverage status", "Window rows"],
            [[h, status, count] for (h, status), count in sorted(horizon_counts.items())],
        ),
        "",
        "## Treated Coverage By Horizon",
        "",
        markdown_table(
            ["Horizon years", "Coverage status", "Treated window rows"],
            [[h, status, count] for (h, status), count in sorted(treated_horizon_counts.items())],
        ),
        "",
        "## Benchmark Missingness",
        "",
        markdown_table(["Benchmark field", "Missing rows"], [[k, v] for k, v in sorted(benchmark_stats.items()) if k.startswith("missing_")]),
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
        "# CHECKPOINT 27: WRDS CRSP Raw Return Import Validation",
        "",
        "## Completed",
        "",
        "- Imported the WRDS raw daily issuer return file.",
        "- Imported the WRDS raw CRSP market benchmark file.",
        "- Reconciled raw files against the WRDS pull manifest.",
        "- Validated issuer and benchmark raw date coverage for ready return windows.",
        "- Created a per-window raw coverage table with candidate start/end trading dates.",
        "- Did not compute issuer returns, benchmark-adjusted returns, regressions, tests, or empirical claims.",
        "",
        "## Files Created",
        "",
        "- `scripts/import_validate_wrds_crsp_raw_returns_v1.py`",
        "- `data/returns/wrds_crsp_return_window_raw_coverage_v1.csv`",
        "- `quality_reports/wrds_crsp_raw_return_import_validation_v1_report.md`",
        "- `CHECKPOINT_27_WRDS_CRSP_RAW_RETURN_IMPORT_VALIDATION.md`",
        "",
        "## Counts",
        "",
        f"- Ready return-window rows checked: {len(ready_windows):,}",
        f"- Daily issuer rows: {daily_row_count:,}",
        f"- Benchmark rows: {benchmark_row_count:,}",
        f"- Raw coverage ready windows: {coverage_counts.get('raw_coverage_ready_for_return_computation', 0):,}",
        f"- Raw coverage incomplete windows: {coverage_counts.get('raw_coverage_incomplete', 0):,}",
        f"- Ready treated 1-year windows with raw coverage: {treated_horizon_counts.get(('1', 'raw_coverage_ready_for_return_computation'), 0):,}",
        f"- Ready treated 3-year windows with raw coverage: {treated_horizon_counts.get(('3', 'raw_coverage_ready_for_return_computation'), 0):,}",
        f"- Ready treated 5-year windows with raw coverage: {treated_horizon_counts.get(('5', 'raw_coverage_ready_for_return_computation'), 0):,}",
        "",
        "## Next",
        "",
        "Use `data/returns/wrds_crsp_return_window_raw_coverage_v1.csv` to compute raw and benchmark-matched window returns only for rows with `raw_return_coverage_status == raw_coverage_ready_for_return_computation`, preserving incomplete windows as explicit missingness statuses.",
        "",
    ]
    CHECKPOINT_OUT.write_text("\n".join(checkpoint), encoding="utf-8")

    print(f"Wrote {COVERAGE_OUT.relative_to(ROOT)} ({len(coverage_rows)} rows)")
    print(f"Wrote {REPORT_OUT.relative_to(ROOT)}")
    print(f"Wrote {CHECKPOINT_OUT.relative_to(ROOT)}")
    print("Coverage statuses:")
    for status, count in sorted(coverage_counts.items()):
        print(f"  {status}: {count}")


if __name__ == "__main__":
    main()
