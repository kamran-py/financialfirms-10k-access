import csv
import hashlib
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "returns" / "wrds_crsp_window_returns_v1.csv"
PANEL_PATH = PROJECT_ROOT / "data" / "analysis" / "return_analysis_panel_v1.csv"
THRESHOLDS_PATH = PROJECT_ROOT / "data" / "analysis" / "return_winsorization_thresholds_v1.csv"
TAILS_PATH = PROJECT_ROOT / "data" / "analysis" / "return_outlier_tail_diagnostics_v1.csv"
POLICY_PATH = PROJECT_ROOT / "methodology" / "return_outlier_winsorization_policy_v1.md"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "return_analysis_panel_validation_v1_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_29_RETURN_ANALYSIS_PANEL_PREP.md"

COMPUTED_STATUS = "computed"
EXPECTED_ROWS = 8291
EXPECTED_COMPUTED_ROWS = 8238
EXPECTED_COMPUTED_TREATED_ROWS = 294

OUTCOME_FIELDS = [
    "issuer_raw_return_compounded",
    "excess_return_vs_vwretd",
    "excess_return_vs_vwretx",
    "excess_return_vs_ewretd",
    "excess_return_vs_ewretx",
    "excess_return_vs_sprtrn",
]

PRIMARY_DIAGNOSTIC_FIELDS = [
    "issuer_raw_return_compounded",
    "excess_return_vs_vwretd",
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


def parse_year(date_text):
    text = str(date_text or "").strip()
    if not text:
        return ""
    try:
        return str(datetime.strptime(text, "%Y-%m-%d").year)
    except ValueError:
        return ""


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def quantile(sorted_values, q):
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = (len(sorted_values) - 1) * q
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return sorted_values[int(pos)]
    fraction = pos - lower
    return sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction


def describe(values):
    clean = sorted(v for v in values if v is not None and math.isfinite(v))
    n = len(clean)
    if n == 0:
        return {
            "n": 0,
            "mean": None,
            "sd": None,
            "min": None,
            "p01": None,
            "p05": None,
            "p25": None,
            "p50": None,
            "p75": None,
            "p95": None,
            "p99": None,
            "max": None,
        }
    mean = sum(clean) / n
    sd = None
    if n > 1:
        sd = math.sqrt(sum((value - mean) ** 2 for value in clean) / (n - 1))
    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "min": clean[0],
        "p01": quantile(clean, 0.01),
        "p05": quantile(clean, 0.05),
        "p25": quantile(clean, 0.25),
        "p50": quantile(clean, 0.50),
        "p75": quantile(clean, 0.75),
        "p95": quantile(clean, 0.95),
        "p99": quantile(clean, 0.99),
        "max": clean[-1],
    }


def winsorize(value, lower, upper):
    if value is None or lower is None or upper is None:
        return None
    return min(max(value, lower), upper)


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def make_diagnostic_rows(rows, group_fields, outcome_fields):
    diagnostics = []
    groups = defaultdict(list)
    for row in rows:
        key = tuple(row.get(field, "") for field in group_fields)
        groups[key].append(row)

    for key in sorted(groups):
        group_rows = groups[key]
        for outcome in outcome_fields:
            stats = describe([parse_float(row.get(outcome)) for row in group_rows])
            out = {field: key[index] for index, field in enumerate(group_fields)}
            out["outcome"] = outcome
            for stat_name, value in stats.items():
                out[stat_name] = str(value) if stat_name == "n" else fmt_float(value)
            diagnostics.append(out)
    return diagnostics


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(INPUT_PATH)

    input_hash_before = sha256_file(INPUT_PATH)
    rows = read_rows(INPUT_PATH)
    if not rows:
        raise ValueError("Input return-window file has no rows.")

    input_fieldnames = list(rows[0].keys())

    uniqueness_counter = Counter()
    event_horizon_counter = Counter()
    numeric_missing = Counter()
    computed_rows = []
    output_rows = []

    for row in rows:
        uniqueness_counter[row.get("event_window_id", "")] += 1
        event_horizon_counter[(row.get("event_id", ""), row.get("horizon_years", ""))] += 1
        row["filing_year"] = parse_year(row.get("event_date"))
        row["analysis_sample_flag"] = "1" if row.get("return_computation_status") == COMPUTED_STATUS else "0"
        row["analysis_sample_status"] = (
            "analysis_ready_computed_return"
            if row["analysis_sample_flag"] == "1"
            else "not_analysis_ready_" + row.get("return_computation_status", "unknown_status")
        )

        if row["analysis_sample_flag"] == "1":
            computed_rows.append(row)
            for field in OUTCOME_FIELDS:
                if parse_float(row.get(field)) is None:
                    numeric_missing[field] += 1
        output_rows.append(row)

    duplicate_event_window_ids = sum(1 for count in uniqueness_counter.values() if count > 1)
    duplicate_event_horizons = sum(1 for count in event_horizon_counter.values() if count > 1)

    thresholds = {}
    threshold_rows = []
    for horizon in sorted({row.get("horizon_years", "") for row in computed_rows}):
        horizon_rows = [row for row in computed_rows if row.get("horizon_years", "") == horizon]
        for outcome in OUTCOME_FIELDS:
            values = sorted(
                parse_float(row.get(outcome))
                for row in horizon_rows
                if parse_float(row.get(outcome)) is not None
            )
            lower = quantile(values, 0.01)
            upper = quantile(values, 0.99)
            thresholds[(horizon, outcome)] = (lower, upper)
            threshold_rows.append(
                {
                    "horizon_years": horizon,
                    "outcome": outcome,
                    "winsorization_method": "within_horizon_p01_p99_two_sided",
                    "n": str(len(values)),
                    "lower_p01": fmt_float(lower),
                    "upper_p99": fmt_float(upper),
                }
            )

    for row in output_rows:
        for outcome in OUTCOME_FIELDS:
            raw_value = parse_float(row.get(outcome))
            lower, upper = thresholds.get((row.get("horizon_years", ""), outcome), (None, None))
            winsorized = winsorize(raw_value, lower, upper) if row["analysis_sample_flag"] == "1" else None
            row[f"{outcome}_winsor_p01_p99_by_horizon"] = fmt_float(winsorized)

    PANEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    panel_fieldnames = (
        input_fieldnames
        + ["filing_year", "analysis_sample_flag", "analysis_sample_status"]
        + [f"{field}_winsor_p01_p99_by_horizon" for field in OUTCOME_FIELDS]
    )
    with PANEL_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=panel_fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    with THRESHOLDS_PATH.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["horizon_years", "outcome", "winsorization_method", "n", "lower_p01", "upper_p99"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(threshold_rows)

    computed_for_tails = [row for row in output_rows if row["analysis_sample_flag"] == "1"]
    tail_rows = []
    for horizon in sorted({row.get("horizon_years", "") for row in computed_for_tails}):
        horizon_rows = [row for row in computed_for_tails if row.get("horizon_years", "") == horizon]
        for outcome in PRIMARY_DIAGNOSTIC_FIELDS:
            ranked = [
                (parse_float(row.get(outcome)), row)
                for row in horizon_rows
                if parse_float(row.get(outcome)) is not None
            ]
            ranked.sort(key=lambda item: item[0])
            tails = [("bottom_10", ranked[:10]), ("top_10", list(reversed(ranked[-10:])))]
            for tail_name, selected in tails:
                for rank, (value, row) in enumerate(selected, start=1):
                    tail_rows.append(
                        {
                            "horizon_years": horizon,
                            "outcome": outcome,
                            "tail": tail_name,
                            "tail_rank": str(rank),
                            "outcome_value": fmt_float(value),
                            "event_window_id": row.get("event_window_id", ""),
                            "event_id": row.get("event_id", ""),
                            "firm_id": row.get("firm_id", ""),
                            "cik": row.get("cik", ""),
                            "ticker_from_project": row.get("ticker_from_project", ""),
                            "company_name": row.get("company_name", ""),
                            "event_date": row.get("event_date", ""),
                            "validated_conservative_treatment": row.get("validated_conservative_treatment", ""),
                            "primary_narrative_subcategory": row.get("primary_narrative_subcategory", ""),
                            "return_computation_status": row.get("return_computation_status", ""),
                        }
                    )

    with TAILS_PATH.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "horizon_years",
            "outcome",
            "tail",
            "tail_rank",
            "outcome_value",
            "event_window_id",
            "event_id",
            "firm_id",
            "cik",
            "ticker_from_project",
            "company_name",
            "event_date",
            "validated_conservative_treatment",
            "primary_narrative_subcategory",
            "return_computation_status",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tail_rows)

    by_horizon = make_diagnostic_rows(computed_for_tails, ["horizon_years"], PRIMARY_DIAGNOSTIC_FIELDS)
    by_treatment_horizon = make_diagnostic_rows(
        computed_for_tails,
        ["horizon_years", "validated_conservative_treatment"],
        PRIMARY_DIAGNOSTIC_FIELDS,
    )
    by_filing_year_horizon = make_diagnostic_rows(
        computed_for_tails,
        ["filing_year", "horizon_years"],
        PRIMARY_DIAGNOSTIC_FIELDS,
    )

    status_counts = Counter(row.get("return_computation_status", "") for row in output_rows)
    treatment_status_counts = Counter(
        (row.get("validated_conservative_treatment", ""), row.get("return_computation_status", ""))
        for row in output_rows
    )
    horizon_treatment_counts = Counter(
        (
            row.get("horizon_years", ""),
            row.get("validated_conservative_treatment", ""),
            row.get("analysis_sample_status", ""),
        )
        for row in output_rows
    )

    input_hash_after = sha256_file(INPUT_PATH)

    policy = "\n".join(
        [
            "# Return Outlier and Winsorization Policy V1",
            "",
            "This policy is defined before regression or event-study estimation.",
            "",
            "## Raw Outcomes",
            "",
            "- Raw computed returns are preserved unchanged in `data/analysis/return_analysis_panel_v1.csv`.",
            "- The primary raw outcome for market-adjusted performance is `excess_return_vs_vwretd`.",
            "- `issuer_raw_return_compounded` is retained as an unadjusted descriptive outcome.",
            "",
            "## Winsorized Outcomes",
            "",
            "- Winsorization is applied only to analysis-ready computed rows.",
            "- Thresholds are calculated separately within each return horizon: 1-year, 3-year, and 5-year.",
            "- Thresholds use the pooled treated and control sample within each horizon, not treatment-specific thresholds.",
            "- The default analysis-ready winsorized variables cap each outcome at the 1st and 99th percentiles within horizon.",
            "- Winsorized variables are suffixed `_winsor_p01_p99_by_horizon`.",
            "- Raw variables remain available for sensitivity checks and are not overwritten.",
            "",
            "## Guardrails",
            "",
            "- This policy does not imply that any return is erroneous.",
            "- Outlier-tail files are diagnostic aids, not exclusion rules.",
            "- Any later alternative threshold must be documented as a robustness specification, not selected after viewing results.",
            "",
        ]
    )
    POLICY_PATH.write_text(policy, encoding="utf-8")

    report_lines = [
        "# Return Analysis Panel Validation V1 Report",
        "",
        "## Guardrails",
        "",
        "- This step prepared an analysis-ready panel and diagnostics only.",
        "- No regressions, hypothesis tests, event-study estimates, or empirical claims were made.",
        "- Upstream computed return-window data were preserved unchanged.",
        "",
        "## Inputs",
        "",
        "- `data/returns/wrds_crsp_window_returns_v1.csv`",
        "",
        "## Outputs",
        "",
        "- `data/analysis/return_analysis_panel_v1.csv`",
        "- `data/analysis/return_winsorization_thresholds_v1.csv`",
        "- `data/analysis/return_outlier_tail_diagnostics_v1.csv`",
        "- `methodology/return_outlier_winsorization_policy_v1.md`",
        "",
        "## Reconciliation",
        "",
        f"- Input return-window rows: {len(rows):,}",
        f"- Expected rows from checkpoint 28: {EXPECTED_ROWS:,}",
        f"- Output analysis panel rows: {len(output_rows):,}",
        f"- Computed rows: {len(computed_for_tails):,}",
        f"- Expected computed rows from checkpoint 28: {EXPECTED_COMPUTED_ROWS:,}",
        f"- Computed treated rows: {sum(1 for row in computed_for_tails if row.get('validated_conservative_treatment') == '1'):,}",
        f"- Expected computed treated rows from checkpoint 28: {EXPECTED_COMPUTED_TREATED_ROWS:,}",
        "",
        "## Uniqueness Checks",
        "",
        f"- Duplicate `event_window_id` values: {duplicate_event_window_ids:,}",
        f"- Duplicate `event_id` plus `horizon_years` combinations: {duplicate_event_horizons:,}",
        "",
        "## Return Computation Status Counts",
        "",
        markdown_table(
            ["Return computation status", "Rows"],
            [(status, f"{count:,}") for status, count in sorted(status_counts.items())],
        ),
        "",
        "## Treatment And Status Counts",
        "",
        markdown_table(
            ["Treatment", "Return computation status", "Rows"],
            [(key[0], key[1], f"{count:,}") for key, count in sorted(treatment_status_counts.items())],
        ),
        "",
        "## Analysis Sample Coverage By Horizon And Treatment",
        "",
        markdown_table(
            ["Horizon years", "Treatment", "Analysis sample status", "Rows"],
            [(key[0], key[1], key[2], f"{count:,}") for key, count in sorted(horizon_treatment_counts.items())],
        ),
        "",
        "## Numeric Field Checks For Computed Rows",
        "",
        markdown_table(
            ["Outcome field", "Computed rows with missing/non-numeric value"],
            [(field, f"{numeric_missing[field]:,}") for field in OUTCOME_FIELDS],
        ),
        "",
        "## Diagnostics By Horizon",
        "",
        markdown_table(
            ["Horizon years", "Outcome", "N", "Mean", "SD", "P01", "P50", "P99", "Min", "Max"],
            [
                [
                    row["horizon_years"],
                    row["outcome"],
                    row["n"],
                    row["mean"],
                    row["sd"],
                    row["p01"],
                    row["p50"],
                    row["p99"],
                    row["min"],
                    row["max"],
                ]
                for row in by_horizon
            ],
        ),
        "",
        "## Diagnostics By Horizon And Treatment",
        "",
        markdown_table(
            ["Horizon years", "Treatment", "Outcome", "N", "Mean", "SD", "P01", "P50", "P99"],
            [
                [
                    row["horizon_years"],
                    row["validated_conservative_treatment"],
                    row["outcome"],
                    row["n"],
                    row["mean"],
                    row["sd"],
                    row["p01"],
                    row["p50"],
                    row["p99"],
                ]
                for row in by_treatment_horizon
            ],
        ),
        "",
        "## Filing-Year Diagnostics",
        "",
        "Filing-year diagnostics were generated in memory for validation coverage. Detailed year-level returns should be used as diagnostics only until formal specifications are approved.",
        "",
        markdown_table(
            ["Filing year", "Horizon years", "Outcome", "N", "Mean", "P50"],
            [
                [
                    row["filing_year"],
                    row["horizon_years"],
                    row["outcome"],
                    row["n"],
                    row["mean"],
                    row["p50"],
                ]
                for row in by_filing_year_horizon
            ],
        ),
        "",
        "## Input Integrity",
        "",
        f"- `wrds_crsp_window_returns_v1.csv` before: `{input_hash_before}`",
        f"- `wrds_crsp_window_returns_v1.csv` after: `{input_hash_after}`",
        f"- `wrds_crsp_window_returns_v1.csv` unchanged: {'yes' if input_hash_before == input_hash_after else 'no'}",
        "",
    ]
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    checkpoint = "\n".join(
        [
            "# CHECKPOINT 29: Return Analysis Panel Prep",
            "",
            "## Status",
            "",
            "Completed return-output validation and analysis-panel preparation.",
            "",
            "## Created",
            "",
            "- `scripts/prepare_return_analysis_panel_v1.py`",
            "- `data/analysis/return_analysis_panel_v1.csv`",
            "- `data/analysis/return_winsorization_thresholds_v1.csv`",
            "- `data/analysis/return_outlier_tail_diagnostics_v1.csv`",
            "- `methodology/return_outlier_winsorization_policy_v1.md`",
            "- `quality_reports/return_analysis_panel_validation_v1_report.md`",
            "- `CHECKPOINT_29_RETURN_ANALYSIS_PANEL_PREP.md`",
            "",
            "## Validation",
            "",
            f"- Input rows: {len(rows):,}",
            f"- Output panel rows: {len(output_rows):,}",
            f"- Computed analysis-ready rows: {len(computed_for_tails):,}",
            f"- Computed treated rows: {sum(1 for row in computed_for_tails if row.get('validated_conservative_treatment') == '1'):,}",
            f"- Duplicate event-window IDs: {duplicate_event_window_ids:,}",
            f"- Duplicate event-horizon rows: {duplicate_event_horizons:,}",
            f"- Upstream return-window file unchanged: {'yes' if input_hash_before == input_hash_after else 'no'}",
            "",
            "## Guardrails",
            "",
            "- No SEC requests made.",
            "- No prices fetched.",
            "- No regressions, event-study estimates, hypothesis tests, or empirical claims made.",
            "- Raw returns were not overwritten; winsorized variables are separate analysis-ready columns.",
            "",
        ]
    )
    CHECKPOINT_PATH.write_text(checkpoint, encoding="utf-8")

    print(f"Wrote {PANEL_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {THRESHOLDS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {TAILS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {POLICY_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"rows {len(output_rows)}")
    print(f"computed {len(computed_for_tails)}")
    print(f"computed_treated {sum(1 for row in computed_for_tails if row.get('validated_conservative_treatment') == '1')}")
    print(f"duplicate_event_window_ids {duplicate_event_window_ids}")
    print(f"duplicate_event_horizons {duplicate_event_horizons}")


if __name__ == "__main__":
    main()
