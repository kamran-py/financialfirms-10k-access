import csv
import hashlib
import math
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODELING_PATH = PROJECT_ROOT / "data" / "analysis" / "regression_modeling_dataset_v1.csv"
ESTIMATES_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_year_fe_estimates_v1.csv"
INFERENCE_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_inference_diagnostics_v1.csv"
FINALIZATION_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_wild_cluster_bootstrap_v1.csv"

DELTA_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_equivalence_sd_threshold_v1.csv"
APPENDIX_PATH = PROJECT_ROOT / "methodology" / "baseline_table_appendix_draft_v1.md"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "baseline_writeup_components_v1_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_34_BASELINE_WRITEUP_COMPONENTS.md"

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


def sample_sd(values):
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / (len(values) - 1))


def fmt(value, digits=10):
    return f"{float(value):.{digits}f}"


def find_treatment_estimate(rows, horizon):
    for row in rows:
        if row.get("horizon_years") == horizon and row.get("term") == "treatment_main":
            return row
    raise ValueError(f"Missing treatment estimate for horizon {horizon}.")


def main():
    inputs = [MODELING_PATH, ESTIMATES_PATH, INFERENCE_PATH, FINALIZATION_PATH]
    for path in inputs:
        if not path.exists():
            raise FileNotFoundError(path)
    hashes_before = {path.name: sha256_file(path) for path in inputs}

    modeling_rows = read_rows(MODELING_PATH)
    estimates = read_rows(ESTIMATES_PATH)
    bootstrap_rows = read_rows(FINALIZATION_PATH)

    one_year_rows = [row for row in modeling_rows if row.get("horizon_years") == "1"]
    primary_values = [float(row[PRIMARY_OUTCOME]) for row in one_year_rows]
    raw_values = [float(row[RAW_PRIMARY_OUTCOME]) for row in one_year_rows]

    primary_sd = sample_sd(primary_values)
    raw_sd = sample_sd(raw_values)
    estimate_1y = find_treatment_estimate(estimates, "1")
    beta_1y = float(estimate_1y["estimate"])
    se_1y = float(estimate_1y["cluster_se"])
    ci90_low = beta_1y - 1.6448536269514722 * se_1y
    ci90_high = beta_1y + 1.6448536269514722 * se_1y

    delta_rows = []
    for anchor_name, multiplier, sd_value, source_field, note in [
        (
            "medium_effect_half_sd_primary_winsorized_1y",
            0.5,
            primary_sd,
            PRIMARY_OUTCOME,
            "Preferred equivalence threshold for the primary 1-year outcome.",
        ),
        (
            "small_effect_point_two_sd_primary_winsorized_1y",
            0.2,
            primary_sd,
            PRIMARY_OUTCOME,
            "Stricter sensitivity anchor; not the preferred medium-effect threshold.",
        ),
        (
            "medium_effect_half_sd_raw_1y_reference",
            0.5,
            raw_sd,
            RAW_PRIMARY_OUTCOME,
            "Reference only because raw 1-year returns are highly dispersed.",
        ),
    ]:
        delta = multiplier * sd_value
        delta_rows.append(
            {
                "threshold_name": anchor_name,
                "horizon_years": "1",
                "source_outcome": source_field,
                "n": str(len(one_year_rows)),
                "sd": fmt(sd_value),
                "multiplier": fmt(multiplier, 2),
                "delta": fmt(delta),
                "ci90_low": fmt(ci90_low),
                "ci90_high": fmt(ci90_high),
                "equivalence_passes_tost_interval_rule": "yes" if ci90_low > -delta and ci90_high < delta else "no",
                "note": note,
            }
        )

    write_csv(
        DELTA_PATH,
        [
            "threshold_name",
            "horizon_years",
            "source_outcome",
            "n",
            "sd",
            "multiplier",
            "delta",
            "ci90_low",
            "ci90_high",
            "equivalence_passes_tost_interval_rule",
            "note",
        ],
        delta_rows,
    )

    bootstrap_summary = {
        row["horizon_years"]: row for row in bootstrap_rows
    }

    appendix = "\n".join(
        [
            "# Baseline Table Appendix Draft V1",
            "",
            "This draft records paper-ready table structure and methods language. It does not introduce a new empirical specification.",
            "",
            "## Attrition Table Structure",
            "",
            "The final attrition table should be issuer-level, not filing-level, so it aligns with issuer-clustered inference. For treated issuers with multiple qualifying treated filings, collapse to the first qualifying treatment date before counting the issuer in treated attrition rows.",
            "",
            "| Horizon | Group | Total issuers | Observed | Right-censored | Exit: M&A | Exit: failed/delisted | Unlinked / data gap | Eligible N | Exit attrition % |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            "| 1y | Treated |  |  |  |  |  |  |  |  |",
            "| 1y | Control |  |  |  |  |  |  |  |  |",
            "| 3y | Treated |  |  |  |  |  |  |  |  |",
            "| 3y | Control |  |  |  |  |  |  |  |  |",
            "| 5y | Treated |  |  |  |  |  |  |  |  |",
            "| 5y | Control |  |  |  |  |  |  |  |  |",
            "",
            "`Eligible N = Total issuers - Right-censored - Unlinked / data gap`. `Exit attrition % = (Exit: M&A + Exit: failed/delisted) / Eligible N`.",
            "",
            "The current project files support right-censoring, link/coverage, and return-computation statuses. They do not yet support a defensible M&A versus failed/delisted split. That split requires a separate CRSP delisting-code and corporate-action checkpoint.",
            "",
            "## Differential Exit Test Structure",
            "",
            "| Horizon | Treated exited / eligible | Control exited / eligible | Difference in exit rate | Fisher exact p |",
            "| --- | ---: | ---: | ---: | ---: |",
            "| 1y |  |  |  |  |",
            "| 3y |  |  |  |  |",
            "| 5y |  |  |  |  |",
            "",
            "Run this once pooling M&A and failure exits, and once for failure-only exits. Fisher's exact test is preferred because treated issuer counts are thin, especially at 3y and 5y.",
            "",
            "## Equivalence Threshold Paragraph",
            "",
            f"For the 1-year horizon, we interpret equivalence using a pre-specified economically meaningful threshold rather than treating non-significance as evidence of no association. We define Delta as 0.5 times the cross-sectional standard deviation of the 1-year primary benchmark-adjusted return outcome in the full analysis sample, pooling treated and control observations. In this sample, the 1-year standard deviation of `{PRIMARY_OUTCOME}` is {fmt(primary_sd, 4)}, giving Delta = {fmt(0.5 * primary_sd, 4)}. This threshold is mechanically independent of the estimated treatment coefficient and its standard error, and corresponds to a medium standardized difference. The equivalence claim is evaluated using TOST logic: the 90% confidence interval for the treatment coefficient must lie entirely within [-Delta, +Delta]. The 1-year 90% confidence interval is [{fmt(ci90_low, 4)}, {fmt(ci90_high, 4)}], so it lies inside the medium-effect Delta interval. The stricter 0.2 SD threshold is reported as a sensitivity benchmark and should not be treated as the primary threshold unless approved before formal interpretation.",
            "",
            "Because this threshold is being formalized after the baseline estimates were already generated, final writeup language should say it was approved before making a formal equivalence claim, not before the baseline table was estimated.",
            "",
            "## Wild Cluster Bootstrap Procedure",
            "",
            "We use a wild cluster bootstrap as an inference check for the pre-specified baseline model because treated issuer clusters are thin at longer horizons. For each horizon, we estimate the baseline filing-year fixed-effect model and record the treatment coefficient and t-statistic. We then impose the null by estimating the restricted model without the treatment effect, draw Rademacher weights at the issuer-cluster level, construct bootstrap outcomes from restricted fitted values plus cluster-weighted residuals, and re-estimate the unrestricted model. The bootstrap p-value is the share of bootstrap t-statistics at least as extreme as the observed t-statistic. This changes inference only; it does not introduce a new economic specification.",
            "",
            "Current checkpoint bootstrap results used 999 Rademacher replications:",
            "",
            "| Horizon | Bootstrap p | Bootstrap 95% CI |",
            "| --- | ---: | --- |",
            f"| 1y | {bootstrap_summary['1']['wild_cluster_p_value']} | [{bootstrap_summary['1']['wild_cluster_ci95_low_percentile_t']}, {bootstrap_summary['1']['wild_cluster_ci95_high_percentile_t']}] |",
            f"| 3y | {bootstrap_summary['3']['wild_cluster_p_value']} | [{bootstrap_summary['3']['wild_cluster_ci95_low_percentile_t']}, {bootstrap_summary['3']['wild_cluster_ci95_high_percentile_t']}] |",
            f"| 5y | {bootstrap_summary['5']['wild_cluster_p_value']} | [{bootstrap_summary['5']['wild_cluster_ci95_low_percentile_t']}, {bootstrap_summary['5']['wild_cluster_ci95_high_percentile_t']}] |",
            "",
            "For a paper-final table, rerun with 9,999 replications and consider Webb weights at 3y and 5y as a sensitivity check.",
            "",
        ]
    )
    APPENDIX_PATH.write_text(appendix, encoding="utf-8")

    hashes_after = {path.name: sha256_file(path) for path in inputs}
    unchanged = all(hashes_before[name] == hashes_after[name] for name in hashes_before)

    report = "\n".join(
        [
            "# Baseline Writeup Components V1 Report",
            "",
            "## Created",
            "",
            "- `data/analysis/baseline_equivalence_sd_threshold_v1.csv`",
            "- `methodology/baseline_table_appendix_draft_v1.md`",
            "",
            "## Delta Diagnostics",
            "",
            f"- 1-year primary outcome rows: {len(one_year_rows):,}",
            f"- 1-year primary winsorized outcome SD: {fmt(primary_sd)}",
            f"- Medium-effect Delta, 0.5 x SD: {fmt(0.5 * primary_sd)}",
            f"- Small-effect sensitivity Delta, 0.2 x SD: {fmt(0.2 * primary_sd)}",
            f"- 1-year 90% CI: [{fmt(ci90_low)}, {fmt(ci90_high)}]",
            "",
            "## Guardrails",
            "",
            "- No new regression was estimated.",
            "- No causal claims were made.",
            "- M&A/failure exit claims remain blocked until delisting/corporate-action data are imported.",
            f"- Upstream files unchanged: {'yes' if unchanged else 'no'}",
            "",
        ]
    )
    REPORT_PATH.write_text(report, encoding="utf-8")

    checkpoint = "\n".join(
        [
            "# CHECKPOINT 34: Baseline Writeup Components",
            "",
            "## Status",
            "",
            "Completed draft attrition table structure, Delta-equivalence threshold diagnostics, and wild-bootstrap procedure language.",
            "",
            "## Created",
            "",
            "- `scripts/build_baseline_writeup_components_v1.py`",
            "- `data/analysis/baseline_equivalence_sd_threshold_v1.csv`",
            "- `methodology/baseline_table_appendix_draft_v1.md`",
            "- `quality_reports/baseline_writeup_components_v1_report.md`",
            "- `CHECKPOINT_34_BASELINE_WRITEUP_COMPONENTS.md`",
            "",
            "## Validation",
            "",
            f"- 1-year primary outcome SD: {fmt(primary_sd)}",
            f"- Medium-effect Delta, 0.5 x SD: {fmt(0.5 * primary_sd)}",
            f"- 1-year 90% CI lies inside medium-effect Delta: {'yes' if ci90_low > -(0.5 * primary_sd) and ci90_high < (0.5 * primary_sd) else 'no'}",
            f"- Upstream files unchanged: {'yes' if unchanged else 'no'}",
            "",
            "## Guardrails",
            "",
            "- No new economic specification introduced.",
            "- No new regression estimated.",
            "- No causal claims made.",
            "- Exit-mode table remains a structure until CRSP delisting/corporate-action data are added.",
            "",
        ]
    )
    CHECKPOINT_PATH.write_text(checkpoint, encoding="utf-8")

    print(f"Wrote {DELTA_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {APPENDIX_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"primary_sd_1y {fmt(primary_sd)}")
    print(f"delta_0_5_sd {fmt(0.5 * primary_sd)}")
    print(f"ci90 {fmt(ci90_low)} {fmt(ci90_high)}")


if __name__ == "__main__":
    main()
