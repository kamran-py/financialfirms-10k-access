import bisect
import csv
import hashlib
import math
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

COVERAGE_PATH = PROJECT_ROOT / "data" / "returns" / "wrds_crsp_return_window_raw_coverage_v1.csv"
ISSUER_RETURNS_PATH = PROJECT_ROOT / "data" / "returns" / "wrds_crsp_daily_returns_raw_v1.csv"
BENCHMARK_RETURNS_PATH = PROJECT_ROOT / "data" / "returns" / "wrds_crsp_market_benchmark_raw_v1.csv"

OUTPUT_PATH = PROJECT_ROOT / "data" / "returns" / "wrds_crsp_window_returns_v1.csv"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "wrds_crsp_window_return_computation_v1_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_28_WRDS_CRSP_WINDOW_RETURNS.md"

READY_STATUS = "raw_coverage_ready_for_return_computation"
COMPUTED_STATUS = "computed"
INCOMPLETE_STATUS = "not_computed_raw_coverage_incomplete"

BENCHMARK_FIELDS = ("vwretd", "vwretx", "ewretd", "ewretx", "sprtrn")
RETURN_FIELDS = [
    "issuer_trading_days",
    "benchmark_trading_days",
    "issuer_raw_return_compounded",
    "benchmark_vwretd_compounded",
    "benchmark_vwretx_compounded",
    "benchmark_ewretd_compounded",
    "benchmark_ewretx_compounded",
    "benchmark_sprtrn_compounded",
    "excess_return_vs_vwretd",
    "excess_return_vs_vwretx",
    "excess_return_vs_ewretd",
    "excess_return_vs_ewretx",
    "excess_return_vs_sprtrn",
    "return_computation_status",
    "return_computation_reason",
]


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_float(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def fmt_float(value):
    if value is None:
        return ""
    return f"{value:.10f}"


def compound(returns):
    total = 1.0
    for value in returns:
        total *= 1.0 + value
    return total - 1.0


def read_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_issuer_returns(path):
    by_permno = defaultdict(list)
    duplicate_count = 0
    seen = set()
    nonnumeric_ret_count = 0

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            permno = str(row.get("permno", "")).strip()
            date = str(row.get("date", "")).strip()
            if not permno or not date:
                continue
            key = (permno, date)
            if key in seen:
                duplicate_count += 1
                continue
            seen.add(key)
            ret = parse_float(row.get("ret_with_delisting"))
            if ret is None:
                nonnumeric_ret_count += 1
            by_permno[permno].append((date, ret))

    indexed = {}
    for permno, observations in by_permno.items():
        observations.sort(key=lambda item: item[0])
        indexed[permno] = {
            "dates": [item[0] for item in observations],
            "returns": [item[1] for item in observations],
        }

    return indexed, {
        "issuer_duplicate_permno_date_rows": duplicate_count,
        "issuer_nonnumeric_ret_with_delisting_rows": nonnumeric_ret_count,
        "issuer_unique_permnos": len(indexed),
        "issuer_rows": sum(len(v["dates"]) for v in indexed.values()),
    }


def load_benchmark_returns(path):
    dates = []
    by_date = {}
    duplicate_count = 0
    missing_field_counts = Counter()
    seen = set()

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = str(row.get("date", "")).strip()
            if not date:
                continue
            if date in seen:
                duplicate_count += 1
                continue
            seen.add(date)
            parsed = {}
            for field in BENCHMARK_FIELDS:
                parsed[field] = parse_float(row.get(field))
                if parsed[field] is None:
                    missing_field_counts[field] += 1
            dates.append(date)
            by_date[date] = parsed

    dates.sort()
    return {"dates": dates, "by_date": by_date}, {
        "benchmark_duplicate_date_rows": duplicate_count,
        "benchmark_rows": len(dates),
        "benchmark_missing_field_counts": dict(missing_field_counts),
    }


def slice_by_date(dates, values, start_date, end_date):
    left = bisect.bisect_left(dates, start_date)
    right = bisect.bisect_right(dates, end_date)
    return dates[left:right], values[left:right]


def compute_row(row, issuer_index, benchmark_index):
    output = {field: "" for field in RETURN_FIELDS}

    if row.get("raw_return_coverage_status") != READY_STATUS:
        output["return_computation_status"] = INCOMPLETE_STATUS
        output["return_computation_reason"] = row.get("raw_return_coverage_reason", "raw_coverage_not_ready")
        return output

    permno = str(row.get("permno", "")).strip()
    issuer_start = str(row.get("issuer_start_trading_date", "")).strip()
    issuer_end = str(row.get("issuer_end_trading_date", "")).strip()
    bench_start = str(row.get("benchmark_start_trading_date", "")).strip()
    bench_end = str(row.get("benchmark_end_trading_date", "")).strip()

    if not permno or not issuer_start or not issuer_end or not bench_start or not bench_end:
        output["return_computation_status"] = "not_computed_missing_window_dates"
        output["return_computation_reason"] = "required_permno_or_trading_window_date_missing"
        return output

    issuer_data = issuer_index.get(permno)
    if issuer_data is None:
        output["return_computation_status"] = "not_computed_missing_permno_in_raw_returns"
        output["return_computation_reason"] = "permno_absent_from_raw_issuer_return_file"
        return output

    issuer_dates, issuer_returns = slice_by_date(
        issuer_data["dates"],
        issuer_data["returns"],
        issuer_start,
        issuer_end,
    )
    if not issuer_dates:
        output["return_computation_status"] = "not_computed_no_issuer_rows_inside_window"
        output["return_computation_reason"] = "no_raw_issuer_return_rows_between_start_and_end_trading_dates"
        return output
    if any(value is None for value in issuer_returns):
        output["return_computation_status"] = "not_computed_missing_issuer_return_inside_window"
        output["return_computation_reason"] = "at_least_one_issuer_trading_day_has_blank_or_non_numeric_return"
        output["issuer_trading_days"] = str(len(issuer_returns))
        return output

    bench_dates = benchmark_index["dates"]
    left = bisect.bisect_left(bench_dates, bench_start)
    right = bisect.bisect_right(bench_dates, bench_end)
    selected_bench_dates = bench_dates[left:right]
    if not selected_bench_dates:
        output["return_computation_status"] = "not_computed_no_benchmark_rows_inside_window"
        output["return_computation_reason"] = "no_raw_benchmark_return_rows_between_start_and_end_trading_dates"
        output["issuer_trading_days"] = str(len(issuer_returns))
        return output

    benchmark_returns = {}
    missing_benchmark_fields = []
    for field in BENCHMARK_FIELDS:
        values = [benchmark_index["by_date"][date][field] for date in selected_bench_dates]
        if any(value is None for value in values):
            missing_benchmark_fields.append(field)
        benchmark_returns[field] = values
    if missing_benchmark_fields:
        output["return_computation_status"] = "not_computed_missing_benchmark_return_inside_window"
        output["return_computation_reason"] = "missing_benchmark_fields:" + ",".join(missing_benchmark_fields)
        output["issuer_trading_days"] = str(len(issuer_returns))
        output["benchmark_trading_days"] = str(len(selected_bench_dates))
        return output

    issuer_return = compound(issuer_returns)
    benchmark_compounded = {field: compound(values) for field, values in benchmark_returns.items()}

    output["issuer_trading_days"] = str(len(issuer_returns))
    output["benchmark_trading_days"] = str(len(selected_bench_dates))
    output["issuer_raw_return_compounded"] = fmt_float(issuer_return)
    for field in BENCHMARK_FIELDS:
        output[f"benchmark_{field}_compounded"] = fmt_float(benchmark_compounded[field])
        output[f"excess_return_vs_{field}"] = fmt_float(issuer_return - benchmark_compounded[field])
    output["return_computation_status"] = COMPUTED_STATUS
    output["return_computation_reason"] = "issuer_and_benchmark_returns_compounded_successfully"
    return output


def count_by(rows, *fields):
    counts = Counter(tuple(row.get(field, "") for field in fields) for row in rows)
    return sorted(counts.items(), key=lambda item: item[0])


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main():
    for path in (COVERAGE_PATH, ISSUER_RETURNS_PATH, BENCHMARK_RETURNS_PATH):
        if not path.exists():
            raise FileNotFoundError(path)

    hashes_before = {
        str(COVERAGE_PATH): sha256_file(COVERAGE_PATH),
        str(ISSUER_RETURNS_PATH): sha256_file(ISSUER_RETURNS_PATH),
        str(BENCHMARK_RETURNS_PATH): sha256_file(BENCHMARK_RETURNS_PATH),
    }

    coverage_rows = read_csv_rows(COVERAGE_PATH)
    issuer_index, issuer_stats = load_issuer_returns(ISSUER_RETURNS_PATH)
    benchmark_index, benchmark_stats = load_benchmark_returns(BENCHMARK_RETURNS_PATH)

    if not coverage_rows:
        raise ValueError("Coverage input has no rows.")

    input_fieldnames = list(coverage_rows[0].keys())
    fieldnames = input_fieldnames + [field for field in RETURN_FIELDS if field not in input_fieldnames]

    output_rows = []
    for row in coverage_rows:
        computed = compute_row(row, issuer_index, benchmark_index)
        out = dict(row)
        out.update(computed)
        output_rows.append(out)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    hashes_after = {
        str(COVERAGE_PATH): sha256_file(COVERAGE_PATH),
        str(ISSUER_RETURNS_PATH): sha256_file(ISSUER_RETURNS_PATH),
        str(BENCHMARK_RETURNS_PATH): sha256_file(BENCHMARK_RETURNS_PATH),
    }

    status_counts = Counter(row["return_computation_status"] for row in output_rows)
    reason_counts = Counter(row["return_computation_reason"] for row in output_rows)
    computed_rows = [row for row in output_rows if row["return_computation_status"] == COMPUTED_STATUS]
    computed_treated_rows = [
        row
        for row in computed_rows
        if str(row.get("validated_conservative_treatment", "")).strip() == "1"
    ]

    horizon_rows = [
        (key[0], key[1], count)
        for key, count in count_by(output_rows, "horizon_years", "return_computation_status")
    ]
    treated_horizon_rows = [
        (key[0], key[1], count)
        for key, count in count_by(
            [row for row in output_rows if str(row.get("validated_conservative_treatment", "")).strip() == "1"],
            "horizon_years",
            "return_computation_status",
        )
    ]

    unchanged_lines = []
    for path_text, before_hash in hashes_before.items():
        after_hash = hashes_after[path_text]
        unchanged_lines.append(f"- `{Path(path_text).name}` before: `{before_hash}`")
        unchanged_lines.append(f"- `{Path(path_text).name}` after: `{after_hash}`")
        unchanged_lines.append(f"- `{Path(path_text).name}` unchanged: {'yes' if before_hash == after_hash else 'no'}")

    report = "\n".join(
        [
            "# WRDS CRSP Window Return Computation V1 Report",
            "",
            "## Guardrails",
            "",
            "- Returns were computed only for rows marked `raw_coverage_ready_for_return_computation`.",
            "- Rows without raw coverage were retained with explicit non-computed statuses.",
            "- Issuer returns use compounded `ret_with_delisting` from the WRDS raw daily file.",
            "- Primary benchmark-adjusted return is issuer compounded return minus compounded CRSP `vwretd`.",
            "- No regressions, hypothesis tests, causal claims, or performance conclusions were made.",
            "",
            "## Inputs",
            "",
            "- `data/returns/wrds_crsp_return_window_raw_coverage_v1.csv`",
            "- `data/returns/wrds_crsp_daily_returns_raw_v1.csv`",
            "- `data/returns/wrds_crsp_market_benchmark_raw_v1.csv`",
            "",
            "## Output",
            "",
            "- `data/returns/wrds_crsp_window_returns_v1.csv`",
            "",
            "## Source File Counts",
            "",
            f"- Coverage input rows: {len(coverage_rows):,}",
            f"- Issuer daily rows indexed: {issuer_stats['issuer_rows']:,}",
            f"- Issuer unique PERMNOs indexed: {issuer_stats['issuer_unique_permnos']:,}",
            f"- Issuer duplicate PERMNO-date rows skipped: {issuer_stats['issuer_duplicate_permno_date_rows']:,}",
            f"- Issuer rows with blank/non-numeric `ret_with_delisting`: {issuer_stats['issuer_nonnumeric_ret_with_delisting_rows']:,}",
            f"- Benchmark rows indexed: {benchmark_stats['benchmark_rows']:,}",
            f"- Benchmark duplicate date rows skipped: {benchmark_stats['benchmark_duplicate_date_rows']:,}",
            "",
            "## Return Computation Status Counts",
            "",
            markdown_table(
                ["Return computation status", "Window rows"],
                [(status, f"{count:,}") for status, count in sorted(status_counts.items())],
            ),
            "",
            "## Return Computation Reason Counts",
            "",
            markdown_table(
                ["Return computation reason", "Window rows"],
                [(reason, f"{count:,}") for reason, count in sorted(reason_counts.items())],
            ),
            "",
            "## Return Computation By Horizon",
            "",
            markdown_table(["Horizon years", "Return computation status", "Window rows"], horizon_rows),
            "",
            "## Treated Return Computation By Horizon",
            "",
            markdown_table(["Horizon years", "Return computation status", "Treated window rows"], treated_horizon_rows),
            "",
            "## Computed Row Counts",
            "",
            f"- Computed window rows: {len(computed_rows):,}",
            f"- Computed treated window rows: {len(computed_treated_rows):,}",
            "",
            "## Input Integrity",
            "",
            *unchanged_lines,
            "",
        ]
    )
    REPORT_PATH.write_text(report, encoding="utf-8")

    checkpoint = "\n".join(
        [
            "# CHECKPOINT 28: WRDS CRSP Window Returns",
            "",
            "## Status",
            "",
            "Completed WRDS CRSP window-return computation V1.",
            "",
            "## Created",
            "",
            "- `scripts/compute_wrds_crsp_window_returns_v1.py`",
            "- `data/returns/wrds_crsp_window_returns_v1.csv`",
            "- `quality_reports/wrds_crsp_window_return_computation_v1_report.md`",
            "- `CHECKPOINT_28_WRDS_CRSP_WINDOW_RETURNS.md`",
            "",
            "## Validation",
            "",
            f"- Coverage input rows: {len(coverage_rows):,}",
            f"- Output return-window rows: {len(output_rows):,}",
            f"- Computed rows: {len(computed_rows):,}",
            f"- Non-computed rows retained: {len(output_rows) - len(computed_rows):,}",
            f"- Computed treated rows: {len(computed_treated_rows):,}",
            "- Raw WRDS daily issuer returns file unchanged.",
            "- Raw WRDS market benchmark file unchanged.",
            "- Coverage input file unchanged.",
            "",
            "## Guardrails",
            "",
            "- No prices fetched.",
            "- No SEC requests made.",
            "- No regressions or event-study estimates run.",
            "- No empirical performance or causal claims made.",
            "",
        ]
    )
    CHECKPOINT_PATH.write_text(checkpoint, encoding="utf-8")

    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"computed_rows {len(computed_rows)}")
    print(f"noncomputed_rows {len(output_rows) - len(computed_rows)}")
    print(f"computed_treated_rows {len(computed_treated_rows)}")


if __name__ == "__main__":
    main()
