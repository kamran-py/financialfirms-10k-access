import csv
import hashlib
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_ROOT / "data" / "analysis" / "regression_modeling_dataset_v1.csv"
ESTIMATES_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_year_fe_estimates_v1.csv"
DIAGNOSTICS_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_year_fe_model_diagnostics_v1.csv"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "baseline_year_fe_estimation_v1_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_31_BASELINE_YEAR_FE_ESTIMATION.md"

OUTCOME = "outcome_primary_excess_vwretd_winsor_p01_p99"
TREATMENT = "treatment_main"
CLUSTER = "cluster_issuer"
YEAR = "filing_year"
HORIZON = "horizon_years"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_float(value):
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def normal_two_sided_pvalue(t_stat):
    if t_stat is None or not math.isfinite(t_stat):
        return ""
    return math.erfc(abs(t_stat) / math.sqrt(2.0))


def fmt(value, digits=10):
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    if not math.isfinite(float(value)):
        return ""
    return f"{float(value):.{digits}f}"


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def fit_horizon(rows, horizon):
    model_rows = [row for row in rows if row[HORIZON] == horizon]
    clean = []
    dropped = Counter()
    for row in model_rows:
        y = parse_float(row.get(OUTCOME))
        treatment = parse_float(row.get(TREATMENT))
        year = str(row.get(YEAR, "")).strip()
        cluster = str(row.get(CLUSTER, "")).strip()
        if y is None:
            dropped["missing_outcome"] += 1
            continue
        if treatment is None:
            dropped["missing_treatment"] += 1
            continue
        if not year:
            dropped["missing_year"] += 1
            continue
        if not cluster:
            dropped["missing_cluster"] += 1
            continue
        clean.append((row, y, treatment, year, cluster))

    years = sorted({item[3] for item in clean})
    if len(years) < 2:
        year_dummies = []
    else:
        year_dummies = years[1:]

    variable_names = ["intercept", "treatment_main"] + [f"filing_year_{year}" for year in year_dummies]
    y_values = []
    x_rows = []
    clusters = []

    for _, y, treatment, year, cluster in clean:
        x = [1.0, treatment]
        x.extend(1.0 if year == dummy_year else 0.0 for dummy_year in year_dummies)
        y_values.append(y)
        x_rows.append(x)
        clusters.append(cluster)

    y = np.asarray(y_values, dtype=float)
    x = np.asarray(x_rows, dtype=float)
    n, k = x.shape
    unique_clusters = sorted(set(clusters))
    g = len(unique_clusters)

    xtx = x.T @ x
    rank = int(np.linalg.matrix_rank(xtx))
    used_pinv = rank < k
    xtx_inv = np.linalg.pinv(xtx)
    beta = xtx_inv @ (x.T @ y)
    residuals = y - x @ beta

    meat = np.zeros((k, k), dtype=float)
    cluster_indices = defaultdict(list)
    for index, cluster in enumerate(clusters):
        cluster_indices[cluster].append(index)
    for indices in cluster_indices.values():
        xg = x[indices, :]
        ug = residuals[indices].reshape(-1, 1)
        score = xg.T @ ug
        meat += score @ score.T

    vcov = xtx_inv @ meat @ xtx_inv
    if g > 1 and n > k:
        vcov *= (g / (g - 1)) * ((n - 1) / (n - k))
    se = np.sqrt(np.maximum(np.diag(vcov), 0.0))
    t_stats = np.divide(beta, se, out=np.full_like(beta, np.nan), where=se > 0)

    y_mean = float(np.mean(y))
    ss_total = float(np.sum((y - y_mean) ** 2))
    ss_resid = float(np.sum(residuals**2))
    r2 = "" if ss_total == 0 else 1.0 - (ss_resid / ss_total)

    estimates = []
    for idx, name in enumerate(variable_names):
        t_stat = float(t_stats[idx]) if math.isfinite(float(t_stats[idx])) else None
        p_value = normal_two_sided_pvalue(t_stat)
        estimates.append(
            {
                "model_id": f"baseline_year_fe_h{horizon}",
                "horizon_years": horizon,
                "outcome": OUTCOME,
                "term": name,
                "estimate": fmt(beta[idx]),
                "cluster_se": fmt(se[idx]),
                "t_stat_normal_approx": fmt(t_stat),
                "p_value_normal_approx": fmt(p_value),
                "ci95_low_normal_approx": fmt(beta[idx] - 1.96 * se[idx]),
                "ci95_high_normal_approx": fmt(beta[idx] + 1.96 * se[idx]),
                "n": str(n),
                "clusters": str(g),
                "fixed_effects": "filing_year",
                "cluster_variable": CLUSTER,
                "interpretation_boundary": "association_only_not_causal",
            }
        )

    diagnostics = {
        "model_id": f"baseline_year_fe_h{horizon}",
        "horizon_years": horizon,
        "input_rows_for_horizon": str(len(model_rows)),
        "estimation_rows": str(n),
        "dropped_rows": str(sum(dropped.values())),
        "dropped_reason_counts": ";".join(f"{key}:{value}" for key, value in sorted(dropped.items())),
        "treated_rows": str(sum(1 for item in clean if item[2] == 1.0)),
        "control_rows": str(sum(1 for item in clean if item[2] == 0.0)),
        "unique_issuers": str(g),
        "filing_years": ",".join(years),
        "k_parameters": str(k),
        "matrix_rank": str(rank),
        "used_pseudoinverse": "yes" if used_pinv else "no",
        "r_squared": fmt(r2),
        "mean_outcome": fmt(y_mean),
    }
    return estimates, diagnostics


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(INPUT_PATH)

    input_hash_before = sha256_file(INPUT_PATH)
    rows = read_rows(INPUT_PATH)
    if not rows:
        raise ValueError("Modeling dataset has no rows.")

    horizons = sorted({row[HORIZON] for row in rows}, key=lambda value: int(value))
    all_estimates = []
    diagnostics = []
    for horizon in horizons:
        estimates, diag = fit_horizon(rows, horizon)
        all_estimates.extend(estimates)
        diagnostics.append(diag)

    estimate_fields = [
        "model_id",
        "horizon_years",
        "outcome",
        "term",
        "estimate",
        "cluster_se",
        "t_stat_normal_approx",
        "p_value_normal_approx",
        "ci95_low_normal_approx",
        "ci95_high_normal_approx",
        "n",
        "clusters",
        "fixed_effects",
        "cluster_variable",
        "interpretation_boundary",
    ]
    ESTIMATES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ESTIMATES_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=estimate_fields)
        writer.writeheader()
        writer.writerows(all_estimates)

    diagnostic_fields = [
        "model_id",
        "horizon_years",
        "input_rows_for_horizon",
        "estimation_rows",
        "dropped_rows",
        "dropped_reason_counts",
        "treated_rows",
        "control_rows",
        "unique_issuers",
        "filing_years",
        "k_parameters",
        "matrix_rank",
        "used_pseudoinverse",
        "r_squared",
        "mean_outcome",
    ]
    with DIAGNOSTICS_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=diagnostic_fields)
        writer.writeheader()
        writer.writerows(diagnostics)

    treatment_rows = [row for row in all_estimates if row["term"] == "treatment_main"]
    input_hash_after = sha256_file(INPUT_PATH)

    report = "\n".join(
        [
            "# Baseline Year-FE Estimation V1 Report",
            "",
            "## Guardrails",
            "",
            "- This checkpoint runs only the pre-specified baseline association models.",
            "- Estimates are conditional associations, not causal effects.",
            "- No claim is made that disclosure language caused later stock returns.",
            "- No additional controls were introduced after viewing results.",
            "- The upstream modeling dataset was preserved unchanged.",
            "",
            "## Model",
            "",
            "Separate models were estimated for each horizon:",
            "",
            "```text",
            "outcome_primary_excess_vwretd_winsor_p01_p99 = alpha + beta * treatment_main + filing_year_fixed_effects + error",
            "```",
            "",
            "- Standard errors are clustered by issuer.",
            "- P-values and confidence intervals use a normal approximation to the cluster-robust t-statistic.",
            "- Outcome is winsorized excess return versus CRSP value-weighted market return with dividends.",
            "",
            "## Treatment Coefficients",
            "",
            markdown_table(
                [
                    "Horizon",
                    "Estimate",
                    "Cluster SE",
                    "t-stat",
                    "p-value",
                    "95% CI low",
                    "95% CI high",
                    "N",
                    "Clusters",
                ],
                [
                    [
                        row["horizon_years"],
                        row["estimate"],
                        row["cluster_se"],
                        row["t_stat_normal_approx"],
                        row["p_value_normal_approx"],
                        row["ci95_low_normal_approx"],
                        row["ci95_high_normal_approx"],
                        row["n"],
                        row["clusters"],
                    ]
                    for row in treatment_rows
                ],
            ),
            "",
            "## Model Diagnostics",
            "",
            markdown_table(
                [
                    "Horizon",
                    "Rows",
                    "Treated",
                    "Controls",
                    "Issuers",
                    "Years",
                    "Rank",
                    "K",
                    "R-squared",
                ],
                [
                    [
                        row["horizon_years"],
                        row["estimation_rows"],
                        row["treated_rows"],
                        row["control_rows"],
                        row["unique_issuers"],
                        row["filing_years"],
                        row["matrix_rank"],
                        row["k_parameters"],
                        row["r_squared"],
                    ]
                    for row in diagnostics
                ],
            ),
            "",
            "## Interpretation Boundary",
            "",
            "These estimates describe whether validated conservative access-oriented disclosure filings are associated with different later benchmark-adjusted returns within filing-year cells. They do not identify a causal effect of the narrative, management policy, or any access-oriented disclosure action.",
            "",
            "## Outputs",
            "",
            "- `data/analysis/baseline_year_fe_estimates_v1.csv`",
            "- `data/analysis/baseline_year_fe_model_diagnostics_v1.csv`",
            "",
            "## Input Integrity",
            "",
            f"- `regression_modeling_dataset_v1.csv` before: `{input_hash_before}`",
            f"- `regression_modeling_dataset_v1.csv` after: `{input_hash_after}`",
            f"- `regression_modeling_dataset_v1.csv` unchanged: {'yes' if input_hash_before == input_hash_after else 'no'}",
            "",
        ]
    )
    REPORT_PATH.write_text(report, encoding="utf-8")

    checkpoint = "\n".join(
        [
            "# CHECKPOINT 31: Baseline Year-FE Estimation",
            "",
            "## Status",
            "",
            "Completed baseline filing-year fixed-effect association models.",
            "",
            "## Created",
            "",
            "- `scripts/run_baseline_year_fe_models_v1.py`",
            "- `data/analysis/baseline_year_fe_estimates_v1.csv`",
            "- `data/analysis/baseline_year_fe_model_diagnostics_v1.csv`",
            "- `quality_reports/baseline_year_fe_estimation_v1_report.md`",
            "- `CHECKPOINT_31_BASELINE_YEAR_FE_ESTIMATION.md`",
            "",
            "## Validation",
            "",
            f"- Horizons estimated: {', '.join(horizons)}",
            f"- Treatment coefficient rows: {len(treatment_rows)}",
            f"- Upstream modeling dataset unchanged: {'yes' if input_hash_before == input_hash_after else 'no'}",
            "",
            "## Guardrails",
            "",
            "- Baseline estimates are association-only.",
            "- No causal claims made.",
            "- No post-result controls added.",
            "- Firm fixed effects, raw-return sensitivity, and alternative benchmarks remain future robustness checkpoints.",
            "",
        ]
    )
    CHECKPOINT_PATH.write_text(checkpoint, encoding="utf-8")

    print(f"Wrote {ESTIMATES_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {DIAGNOSTICS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    for row in treatment_rows:
        print(
            "horizon",
            row["horizon_years"],
            "estimate",
            row["estimate"],
            "se",
            row["cluster_se"],
            "p",
            row["p_value_normal_approx"],
        )


if __name__ == "__main__":
    main()
