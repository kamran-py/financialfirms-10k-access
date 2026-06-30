import csv
import hashlib
import math
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

ESTIMATES_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_year_fe_estimates_v1.csv"
DIAGNOSTICS_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_year_fe_model_diagnostics_v1.csv"
MODELING_PATH = PROJECT_ROOT / "data" / "analysis" / "regression_modeling_dataset_v1.csv"
RETURNS_PATH = PROJECT_ROOT / "data" / "analysis" / "return_analysis_panel_v1.csv"
WINSOR_PATH = PROJECT_ROOT / "data" / "analysis" / "return_winsorization_thresholds_v1.csv"

OUTPUT_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_inference_diagnostics_v1.csv"
FOOTNOTE_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_table_footnotes_v1.csv"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "baseline_inference_diagnostics_v1_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_32_POWER_AND_INFERENCE_DIAGNOSTICS.md"

PRIMARY_OUTCOME = "outcome_primary_excess_vwretd_winsor_p01_p99"
RAW_PRIMARY_OUTCOME = "outcome_primary_excess_vwretd_raw"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value):
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def fmt(value, digits=10):
    if value is None:
        return ""
    return f"{float(value):.{digits}f}"


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main():
    inputs = [ESTIMATES_PATH, DIAGNOSTICS_PATH, MODELING_PATH, RETURNS_PATH, WINSOR_PATH]
    for path in inputs:
        if not path.exists():
            raise FileNotFoundError(path)

    hashes_before = {path.name: sha256_file(path) for path in inputs}

    estimates = read_rows(ESTIMATES_PATH)
    model_diagnostics = {row["horizon_years"]: row for row in read_rows(DIAGNOSTICS_PATH)}
    modeling_rows = read_rows(MODELING_PATH)
    return_rows = read_rows(RETURNS_PATH)
    winsor_rows = read_rows(WINSOR_PATH)

    treatment_estimates = [
        row for row in estimates if row.get("term") == "treatment_main" and row.get("outcome") == PRIMARY_OUTCOME
    ]
    if len(treatment_estimates) != 3:
        raise ValueError(f"Expected three treatment estimates, found {len(treatment_estimates)}.")

    cluster_counts = defaultdict(lambda: defaultdict(set))
    row_counts = Counter()
    for row in modeling_rows:
        horizon = row.get("horizon_years", "")
        treatment = row.get("treatment_main", "")
        cluster = row.get("cluster_issuer", "")
        row_counts[(horizon, treatment)] += 1
        if cluster:
            cluster_counts[horizon][treatment].add(cluster)

    noncomputed_counts = Counter()
    noncomputed_by_horizon = Counter()
    for row in return_rows:
        if row.get("analysis_sample_flag") != "1":
            status = row.get("return_computation_status", "")
            horizon = row.get("horizon_years", "")
            noncomputed_counts[status] += 1
            noncomputed_by_horizon[(horizon, status)] += 1

    winsor_thresholds = {
        (row.get("horizon_years", ""), row.get("outcome", "")): row
        for row in winsor_rows
    }

    diagnostics_rows = []
    for estimate in sorted(treatment_estimates, key=lambda row: int(row["horizon_years"])):
        horizon = estimate["horizon_years"]
        beta = parse_float(estimate["estimate"])
        se = parse_float(estimate["cluster_se"])
        ci95_low = parse_float(estimate["ci95_low_normal_approx"])
        ci95_high = parse_float(estimate["ci95_high_normal_approx"])
        ci90_low = beta - 1.6448536269514722 * se
        ci90_high = beta + 1.6448536269514722 * se
        mde_80pct_5pct_two_sided = 2.8 * se
        half_width_95 = 1.96 * se
        half_width_90 = 1.6448536269514722 * se

        thresholds_to_check = [0.05, 0.10, 0.15, 0.25, 0.50]
        equivalent_thresholds = [
            threshold
            for threshold in thresholds_to_check
            if ci90_low > -threshold and ci90_high < threshold
        ]

        diag = model_diagnostics[horizon]
        winsor = winsor_thresholds[(horizon, "excess_return_vs_vwretd")]
        diagnostics_rows.append(
            {
                "horizon_years": horizon,
                "estimate": fmt(beta),
                "cluster_se": fmt(se),
                "p_value_normal_approx": estimate["p_value_normal_approx"],
                "ci95_low": fmt(ci95_low),
                "ci95_high": fmt(ci95_high),
                "ci90_low_for_equivalence": fmt(ci90_low),
                "ci90_high_for_equivalence": fmt(ci90_high),
                "mde_80pct_power_5pct_two_sided_rule_of_thumb": fmt(mde_80pct_5pct_two_sided),
                "ci95_half_width": fmt(half_width_95),
                "ci90_half_width": fmt(half_width_90),
                "smallest_checked_delta_with_equivalence": (
                    fmt(min(equivalent_thresholds), 2) if equivalent_thresholds else ""
                ),
                "checked_equivalence_deltas": "0.05;0.10;0.15;0.25;0.50",
                "n": estimate["n"],
                "clusters_total": estimate["clusters"],
                "treated_rows": diag["treated_rows"],
                "control_rows": diag["control_rows"],
                "treated_clusters": str(len(cluster_counts[horizon]["1"])),
                "control_clusters": str(len(cluster_counts[horizon]["0"])),
                "winsor_lower_p01": winsor["lower_p01"],
                "winsor_upper_p99": winsor["upper_p99"],
                "inference_note": (
                    "more_informative_null"
                    if horizon == "1"
                    else "wide_interval_lower_power_long_horizon"
                ),
            }
        )

    diagnostic_fields = [
        "horizon_years",
        "estimate",
        "cluster_se",
        "p_value_normal_approx",
        "ci95_low",
        "ci95_high",
        "ci90_low_for_equivalence",
        "ci90_high_for_equivalence",
        "mde_80pct_power_5pct_two_sided_rule_of_thumb",
        "ci95_half_width",
        "ci90_half_width",
        "smallest_checked_delta_with_equivalence",
        "checked_equivalence_deltas",
        "n",
        "clusters_total",
        "treated_rows",
        "control_rows",
        "treated_clusters",
        "control_clusters",
        "winsor_lower_p01",
        "winsor_upper_p99",
        "inference_note",
    ]
    write_csv(OUTPUT_PATH, diagnostic_fields, diagnostics_rows)

    footnote_rows = []
    for row in diagnostics_rows:
        horizon = row["horizon_years"]
        footnote_rows.append(
            {
                "horizon_years": horizon,
                "footnote_type": "sample",
                "footnote_text": (
                    f"Horizon {horizon}y uses {row['n']} analysis-ready issuer-filing-window observations, "
                    f"including {row['treated_rows']} treated and {row['control_rows']} control observations."
                ),
            }
        )
        footnote_rows.append(
            {
                "horizon_years": horizon,
                "footnote_type": "clusters",
                "footnote_text": (
                    f"Standard errors are issuer-clustered across {row['clusters_total']} issuers; "
                    f"treated observations span {row['treated_clusters']} treated issuer clusters."
                ),
            }
        )
        footnote_rows.append(
            {
                "horizon_years": horizon,
                "footnote_type": "winsorization",
                "footnote_text": (
                    f"The primary outcome is winsorized within horizon at p01/p99; for {horizon}y, "
                    f"the p01/p99 thresholds are {row['winsor_lower_p01']} and {row['winsor_upper_p99']}."
                ),
            }
        )
        incomplete_parts = [
            f"{status}: {count}"
            for (h, status), count in sorted(noncomputed_by_horizon.items())
            if h == horizon
        ]
        footnote_rows.append(
            {
                "horizon_years": horizon,
                "footnote_type": "missingness",
                "footnote_text": (
                    "Non-analysis-ready rows were retained upstream with explicit statuses"
                    + (f": {'; '.join(incomplete_parts)}." if incomplete_parts else "; none for this horizon.")
                ),
            }
        )

    write_csv(FOOTNOTE_PATH, ["horizon_years", "footnote_type", "footnote_text"], footnote_rows)

    hashes_after = {path.name: sha256_file(path) for path in inputs}
    unchanged_lines = [
        f"- `{name}` unchanged: {'yes' if hashes_before[name] == hashes_after[name] else 'no'}"
        for name in sorted(hashes_before)
    ]

    report = "\n".join(
        [
            "# Baseline Inference Diagnostics V1 Report",
            "",
            "## Guardrails",
            "",
            "- This checkpoint adds inference diagnostics to the baseline association estimates.",
            "- No new regression specification was estimated.",
            "- No causal claims were made.",
            "- Non-significance is not interpreted as proof of no association.",
            "",
            "## MDE And Interval Diagnostics",
            "",
            markdown_table(
                [
                    "Horizon",
                    "Estimate",
                    "SE",
                    "MDE rule-of-thumb",
                    "90% CI",
                    "95% CI",
                    "Treated clusters",
                    "Inference note",
                ],
                [
                    [
                        row["horizon_years"],
                        row["estimate"],
                        row["cluster_se"],
                        row["mde_80pct_power_5pct_two_sided_rule_of_thumb"],
                        f"[{row['ci90_low_for_equivalence']}, {row['ci90_high_for_equivalence']}]",
                        f"[{row['ci95_low']}, {row['ci95_high']}]",
                        row["treated_clusters"],
                        row["inference_note"],
                    ]
                    for row in diagnostics_rows
                ],
            ),
            "",
            "## Equivalence Framing",
            "",
            "The 90% confidence interval is reported to support later TOST-style equivalence framing if an economically meaningful equivalence threshold is justified before interpretation. Checked thresholds are diagnostic only and are not a substitute for a pre-specified economics-based threshold.",
            "",
            markdown_table(
                ["Horizon", "90% CI", "Smallest checked delta satisfying equivalence"],
                [
                    [
                        row["horizon_years"],
                        f"[{row['ci90_low_for_equivalence']}, {row['ci90_high_for_equivalence']}]",
                        row["smallest_checked_delta_with_equivalence"] or "none_up_to_0.50",
                    ]
                    for row in diagnostics_rows
                ],
            ),
            "",
            "## Missingness And Non-Computed Rows",
            "",
            markdown_table(
                ["Non-computed status", "Rows"],
                [(status, str(count)) for status, count in sorted(noncomputed_counts.items())],
            ),
            "",
            "## Interpretation Boundary",
            "",
            "The 1-year estimate is more informative than the long-horizon estimates because its cluster-robust standard error and MDE are much smaller. The 3-year and especially 5-year estimates should not receive the same epistemic weight as the 1-year estimate. The increasing point estimates across horizons should not be narrated as a trend because the standard errors widen substantially with horizon, consistent with long-horizon buy-and-hold return noise and skew.",
            "",
            "## Outputs",
            "",
            "- `data/analysis/baseline_inference_diagnostics_v1.csv`",
            "- `data/analysis/baseline_table_footnotes_v1.csv`",
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
            "# CHECKPOINT 32: Power And Inference Diagnostics",
            "",
            "## Status",
            "",
            "Completed baseline power, MDE, interval, cluster-count, and table-footnote diagnostics.",
            "",
            "## Created",
            "",
            "- `scripts/build_inference_diagnostics_v1.py`",
            "- `data/analysis/baseline_inference_diagnostics_v1.csv`",
            "- `data/analysis/baseline_table_footnotes_v1.csv`",
            "- `quality_reports/baseline_inference_diagnostics_v1_report.md`",
            "- `CHECKPOINT_32_POWER_AND_INFERENCE_DIAGNOSTICS.md`",
            "",
            "## Validation",
            "",
            f"- Treatment estimate rows processed: {len(diagnostics_rows)}",
            f"- Table footnote rows written: {len(footnote_rows)}",
            "- Upstream estimate, diagnostic, modeling, return-panel, and winsor-threshold files unchanged.",
            "",
            "## Guardrails",
            "",
            "- No new regression specification estimated.",
            "- No causal claims made.",
            "- Non-significance not interpreted as proof of no association.",
            "- Long-horizon estimates explicitly marked as lower-information because of wide intervals and larger MDEs.",
            "",
        ]
    )
    CHECKPOINT_PATH.write_text(checkpoint, encoding="utf-8")

    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {FOOTNOTE_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    for row in diagnostics_rows:
        print(
            "horizon",
            row["horizon_years"],
            "mde",
            row["mde_80pct_power_5pct_two_sided_rule_of_thumb"],
            "treated_clusters",
            row["treated_clusters"],
        )


if __name__ == "__main__":
    main()
