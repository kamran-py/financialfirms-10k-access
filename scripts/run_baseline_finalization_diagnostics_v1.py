import csv
import hashlib
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCAFFOLD_PATH = PROJECT_ROOT / "data" / "returns" / "return_window_scaffold_v1.csv"
LINK_PATH = PROJECT_ROOT / "data" / "linking" / "wrds_crsp_link_resolved_v1.csv"
RETURN_PANEL_PATH = PROJECT_ROOT / "data" / "analysis" / "return_analysis_panel_v1.csv"
MODELING_PATH = PROJECT_ROOT / "data" / "analysis" / "regression_modeling_dataset_v1.csv"
ESTIMATES_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_year_fe_estimates_v1.csv"
LINKED_REQUEST_PATH = PROJECT_ROOT / "data" / "returns" / "wrds_crsp_return_windows_linked_request_v1.csv"

ATTRITION_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_differential_attrition_v1.csv"
TRANSITION_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_horizon_transition_attrition_v1.csv"
BOOTSTRAP_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_wild_cluster_bootstrap_v1.csv"
EQUIVALENCE_PATH = PROJECT_ROOT / "data" / "analysis" / "baseline_equivalence_diagnostics_v1.csv"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "baseline_finalization_diagnostics_v1_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_33_BASELINE_FINALIZATION_DIAGNOSTICS.md"

OUTCOME = "outcome_primary_excess_vwretd_winsor_p01_p99"
TREATMENT = "treatment_main"
CLUSTER = "cluster_issuer"
YEAR = "filing_year"
HORIZON = "horizon_years"
BOOTSTRAP_REPS = 999
BOOTSTRAP_SEED = 20260629


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


def key_from(row):
    return (
        row.get("firm_id", ""),
        row.get("accession_number", ""),
        row.get("event_date", row.get("filing_date", "")),
    )


def parse_float(value):
    try:
        out = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(out):
        return None
    return out


def fmt(value, digits=10):
    if value is None:
        return ""
    return f"{float(value):.{digits}f}"


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def build_design(rows):
    clean = []
    for row in rows:
        y = parse_float(row.get(OUTCOME))
        treatment = parse_float(row.get(TREATMENT))
        year = str(row.get(YEAR, "")).strip()
        cluster = str(row.get(CLUSTER, "")).strip()
        if y is None or treatment is None or not year or not cluster:
            continue
        clean.append((row, y, treatment, year, cluster))

    years = sorted({item[3] for item in clean})
    year_dummies = years[1:] if len(years) > 1 else []
    variable_names = ["intercept", "treatment_main"] + [f"filing_year_{year}" for year in year_dummies]

    y_values = []
    x_rows = []
    clusters = []
    for _, y, treatment, year, cluster in clean:
        x = [1.0, treatment]
        x.extend(1.0 if year == dummy else 0.0 for dummy in year_dummies)
        y_values.append(y)
        x_rows.append(x)
        clusters.append(cluster)
    return np.asarray(y_values, dtype=float), np.asarray(x_rows, dtype=float), clusters, variable_names


def ols_cluster(y, x, clusters):
    n, k = x.shape
    xtx_inv = np.linalg.pinv(x.T @ x)
    beta = xtx_inv @ (x.T @ y)
    residuals = y - x @ beta
    meat = np.zeros((k, k), dtype=float)
    cluster_indices = defaultdict(list)
    for idx, cluster in enumerate(clusters):
        cluster_indices[cluster].append(idx)
    for indices in cluster_indices.values():
        xg = x[indices, :]
        ug = residuals[indices].reshape(-1, 1)
        score = xg.T @ ug
        meat += score @ score.T
    vcov = xtx_inv @ meat @ xtx_inv
    g = len(cluster_indices)
    if g > 1 and n > k:
        vcov *= (g / (g - 1)) * ((n - 1) / (n - k))
    se = np.sqrt(np.maximum(np.diag(vcov), 0.0))
    return beta, se, residuals, x @ beta


def fit_restricted_without_treatment(y, x):
    xr = np.column_stack([x[:, 0], x[:, 2:]]) if x.shape[1] > 2 else x[:, [0]]
    beta_r = np.linalg.pinv(xr.T @ xr) @ (xr.T @ y)
    fitted = xr @ beta_r
    residuals = y - fitted
    return fitted, residuals


def wild_cluster_bootstrap(rows, horizon, reps=BOOTSTRAP_REPS):
    horizon_rows = [row for row in rows if row.get(HORIZON) == horizon]
    y, x, clusters, variable_names = build_design(horizon_rows)
    if "treatment_main" not in variable_names:
        raise ValueError("Treatment variable not found in design.")
    treatment_idx = variable_names.index("treatment_main")
    beta_hat, se_hat, _, _ = ols_cluster(y, x, clusters)
    beta = beta_hat[treatment_idx]
    se = se_hat[treatment_idx]
    t_obs = beta / se if se > 0 else float("nan")
    fitted_r, resid_r = fit_restricted_without_treatment(y, x)

    unique_clusters = sorted(set(clusters))
    cluster_to_indices = defaultdict(list)
    for idx, cluster in enumerate(clusters):
        cluster_to_indices[cluster].append(idx)

    rng = np.random.default_rng(BOOTSTRAP_SEED + int(horizon))
    t_boot = []
    beta_boot = []
    for _ in range(reps):
        weights = {cluster: rng.choice([-1.0, 1.0]) for cluster in unique_clusters}
        y_star = fitted_r.copy()
        for cluster, indices in cluster_to_indices.items():
            y_star[indices] += resid_r[indices] * weights[cluster]
        beta_star, se_star, _, _ = ols_cluster(y_star, x, clusters)
        if se_star[treatment_idx] > 0:
            beta_boot.append(float(beta_star[treatment_idx]))
            t_boot.append(float(beta_star[treatment_idx] / se_star[treatment_idx]))

    t_boot = np.asarray(t_boot, dtype=float)
    beta_boot = np.asarray(beta_boot, dtype=float)
    p_value = float((np.sum(np.abs(t_boot) >= abs(t_obs)) + 1) / (len(t_boot) + 1))
    q_low, q_high = np.quantile(t_boot, [0.975, 0.025])
    ci_low = beta - q_low * se
    ci_high = beta - q_high * se
    return {
        "horizon_years": horizon,
        "bootstrap_reps_requested": str(reps),
        "bootstrap_reps_used": str(len(t_boot)),
        "seed": str(BOOTSTRAP_SEED + int(horizon)),
        "estimate": fmt(beta),
        "cluster_se_cr1": fmt(se),
        "t_stat_cr1": fmt(t_obs),
        "wild_cluster_p_value": fmt(p_value),
        "wild_cluster_ci95_low_percentile_t": fmt(ci_low),
        "wild_cluster_ci95_high_percentile_t": fmt(ci_high),
        "clusters_total": str(len(unique_clusters)),
        "inference_note": "wild_cluster_bootstrap_rademacher_restricted_null",
    }


def main():
    inputs = [SCAFFOLD_PATH, LINK_PATH, LINKED_REQUEST_PATH, RETURN_PANEL_PATH, MODELING_PATH, ESTIMATES_PATH]
    for path in inputs:
        if not path.exists():
            raise FileNotFoundError(path)

    hashes_before = {path.name: sha256_file(path) for path in inputs}
    scaffold = read_rows(SCAFFOLD_PATH)
    link_rows = read_rows(LINK_PATH)
    linked_request_rows = read_rows(LINKED_REQUEST_PATH)
    return_panel = read_rows(RETURN_PANEL_PATH)
    modeling_rows = read_rows(MODELING_PATH)
    estimates = read_rows(ESTIMATES_PATH)

    link_by_event = {key_from(row): row for row in link_rows}
    linked_request_by_event_horizon = {
        (key_from(row), row.get("horizon_years", "")): row for row in linked_request_rows
    }
    panel_by_event_horizon = {(key_from(row), row.get("horizon_years", "")): row for row in return_panel}
    modeling_by_event_horizon = {(key_from(row), row.get("horizon_years", "")): row for row in modeling_rows}

    attrition_records = []
    event_horizon_status = {}
    for row in scaffold:
        event_key = key_from(row)
        horizon = row.get("horizon_years", "")
        treatment = row.get("validated_conservative_treatment", "")
        cluster = row.get("firm_id", "")
        maturity = row.get("calendar_maturity_status_as_of_2026_06_29", "")
        link = link_by_event.get(event_key)
        linked_request = linked_request_by_event_horizon.get((event_key, horizon))
        panel = panel_by_event_horizon.get((event_key, horizon))
        model = modeling_by_event_horizon.get((event_key, horizon))

        if maturity != "mature":
            status = "calendar_right_censored_not_mature"
        elif link is None:
            status = "security_link_row_missing"
        elif link.get("security_link_status") != "resolved_common_share_permno":
            status = "security_link_" + link.get("security_link_status", "unknown")
        elif model is not None:
            status = "analysis_ready"
        elif panel is not None:
            status = "return_noncomputed_" + panel.get("return_computation_status", "unknown")
        elif linked_request is not None:
            status = "post_link_" + linked_request.get("post_link_return_window_status", "unknown")
        else:
            status = "resolved_link_but_not_in_return_request_or_panel"

        event_horizon_status[(event_key, horizon)] = {
            "status": status,
            "treatment": treatment,
            "cluster": cluster,
            "filing_year": row.get("filing_year", ""),
            "company_name": row.get("company_name", ""),
            "ticker": row.get("ticker_from_project", ""),
        }
        attrition_records.append(
            {
                "horizon_years": horizon,
                "validated_conservative_treatment": treatment,
                "issuer_cluster_id": cluster,
                "attrition_status": status,
            }
        )

    summary = {}
    for record in attrition_records:
        key = (record["horizon_years"], record["validated_conservative_treatment"], record["attrition_status"])
        if key not in summary:
            summary[key] = {"rows": 0, "issuers": set()}
        summary[key]["rows"] += 1
        summary[key]["issuers"].add(record["issuer_cluster_id"])

    attrition_rows = []
    for key, value in sorted(summary.items(), key=lambda item: (int(item[0][0]), item[0][1], item[0][2])):
        horizon, treatment, status = key
        attrition_rows.append(
            {
                "horizon_years": horizon,
                "validated_conservative_treatment": treatment,
                "attrition_status": status,
                "event_window_rows": str(value["rows"]),
                "unique_issuer_clusters": str(len(value["issuers"])),
            }
        )
    write_csv(
        ATTRITION_PATH,
        [
            "horizon_years",
            "validated_conservative_treatment",
            "attrition_status",
            "event_window_rows",
            "unique_issuer_clusters",
        ],
        attrition_rows,
    )

    transition_rows = []
    for from_h, to_h in [("1", "3"), ("1", "5"), ("3", "5")]:
        event_keys = {key for key, h in event_horizon_status if h == from_h}
        for treatment in ["0", "1"]:
            selected_keys = [
                key
                for key in event_keys
                if event_horizon_status.get((key, from_h), {}).get("treatment") == treatment
                and event_horizon_status.get((key, from_h), {}).get("status") == "analysis_ready"
            ]
            reason_counts = Counter()
            issuer_sets = defaultdict(set)
            for key in selected_keys:
                to_status = event_horizon_status.get((key, to_h), {}).get("status", "missing_target_horizon_row")
                reason_counts[to_status] += 1
                issuer_sets[to_status].add(event_horizon_status[(key, from_h)]["cluster"])
            for status, count in sorted(reason_counts.items()):
                transition_rows.append(
                    {
                        "from_horizon_years": from_h,
                        "to_horizon_years": to_h,
                        "validated_conservative_treatment": treatment,
                        "from_status_required": "analysis_ready",
                        "to_horizon_status": status,
                        "event_rows": str(count),
                        "unique_issuer_clusters": str(len(issuer_sets[status])),
                    }
                )
    write_csv(
        TRANSITION_PATH,
        [
            "from_horizon_years",
            "to_horizon_years",
            "validated_conservative_treatment",
            "from_status_required",
            "to_horizon_status",
            "event_rows",
            "unique_issuer_clusters",
        ],
        transition_rows,
    )

    bootstrap_rows = [wild_cluster_bootstrap(modeling_rows, horizon) for horizon in ["1", "3", "5"]]
    write_csv(
        BOOTSTRAP_PATH,
        [
            "horizon_years",
            "bootstrap_reps_requested",
            "bootstrap_reps_used",
            "seed",
            "estimate",
            "cluster_se_cr1",
            "t_stat_cr1",
            "wild_cluster_p_value",
            "wild_cluster_ci95_low_percentile_t",
            "wild_cluster_ci95_high_percentile_t",
            "clusters_total",
            "inference_note",
        ],
        bootstrap_rows,
    )

    treatment_estimates = {
        row["horizon_years"]: row
        for row in estimates
        if row.get("term") == "treatment_main" and row.get("outcome") == OUTCOME
    }
    equivalence_rows = []
    thresholds = [
        ("absolute_10pp", 0.10, "External economic threshold: +/- 10 percentage points cumulative benchmark-adjusted return."),
        ("absolute_15pp", 0.15, "External economic threshold: +/- 15 percentage points cumulative benchmark-adjusted return."),
        ("absolute_25pp", 0.25, "External economic threshold: +/- 25 percentage points cumulative benchmark-adjusted return."),
    ]
    for horizon in ["1", "3", "5"]:
        estimate = parse_float(treatment_estimates[horizon]["estimate"])
        se = parse_float(treatment_estimates[horizon]["cluster_se"])
        ci90_low = estimate - 1.6448536269514722 * se
        ci90_high = estimate + 1.6448536269514722 * se
        for threshold_name, delta, justification in thresholds:
            passed = ci90_low > -delta and ci90_high < delta
            equivalence_rows.append(
                {
                    "horizon_years": horizon,
                    "threshold_name": threshold_name,
                    "delta": fmt(delta),
                    "ci90_low": fmt(ci90_low),
                    "ci90_high": fmt(ci90_high),
                    "equivalence_passes_tost_interval_rule": "yes" if passed else "no",
                    "threshold_justification": justification,
                    "interpretation_note": (
                        "diagnostic_equivalence_only_requires_researcher_approved_threshold"
                    ),
                }
            )
    write_csv(
        EQUIVALENCE_PATH,
        [
            "horizon_years",
            "threshold_name",
            "delta",
            "ci90_low",
            "ci90_high",
            "equivalence_passes_tost_interval_rule",
            "threshold_justification",
            "interpretation_note",
        ],
        equivalence_rows,
    )

    hashes_after = {path.name: sha256_file(path) for path in inputs}
    unchanged_lines = [
        f"- `{name}` unchanged: {'yes' if hashes_before[name] == hashes_after[name] else 'no'}"
        for name in sorted(hashes_before)
    ]

    attrition_focus_rows = [
        [
            row["horizon_years"],
            row["validated_conservative_treatment"],
            row["attrition_status"],
            row["event_window_rows"],
            row["unique_issuer_clusters"],
        ]
        for row in attrition_rows
        if row["validated_conservative_treatment"] == "1"
    ]
    transition_focus_rows = [
        [
            row["from_horizon_years"] + "->" + row["to_horizon_years"],
            row["validated_conservative_treatment"],
            row["to_horizon_status"],
            row["event_rows"],
            row["unique_issuer_clusters"],
        ]
        for row in transition_rows
        if row["validated_conservative_treatment"] == "1"
    ]

    report = "\n".join(
        [
            "# Baseline Finalization Diagnostics V1 Report",
            "",
            "## Guardrails",
            "",
            "- This checkpoint adds attrition, wild-cluster-bootstrap, and equivalence diagnostics.",
            "- It does not change the baseline economic specification.",
            "- No causal claims are made.",
            "- Equivalence rows are diagnostics unless the threshold is explicitly approved as economically meaningful.",
            "",
            "## Treated Attrition Status By Horizon",
            "",
            markdown_table(
                ["Horizon", "Treatment", "Attrition status", "Event-window rows", "Issuer clusters"],
                attrition_focus_rows,
            ),
            "",
            "## Treated Horizon-Transition Attrition",
            "",
            markdown_table(
                ["Transition", "Treatment", "Target-horizon status", "Event rows", "Issuer clusters"],
                transition_focus_rows,
            ),
            "",
            "## Wild Cluster Bootstrap",
            "",
            markdown_table(
                ["Horizon", "Estimate", "CR1 SE", "CR1 t", "Bootstrap p", "Bootstrap 95% CI", "Clusters"],
                [
                    [
                        row["horizon_years"],
                        row["estimate"],
                        row["cluster_se_cr1"],
                        row["t_stat_cr1"],
                        row["wild_cluster_p_value"],
                        f"[{row['wild_cluster_ci95_low_percentile_t']}, {row['wild_cluster_ci95_high_percentile_t']}]",
                        row["clusters_total"],
                    ]
                    for row in bootstrap_rows
                ],
            ),
            "",
            "## Equivalence Diagnostics",
            "",
            markdown_table(
                ["Horizon", "Threshold", "Delta", "90% CI", "Passes interval rule"],
                [
                    [
                        row["horizon_years"],
                        row["threshold_name"],
                        row["delta"],
                        f"[{row['ci90_low']}, {row['ci90_high']}]",
                        row["equivalence_passes_tost_interval_rule"],
                    ]
                    for row in equivalence_rows
                ],
            ),
            "",
            "## Interpretation Boundary",
            "",
            "Differential attrition is now summarized from the full scaffold rather than inferred from the final model sample. Current files distinguish calendar right-censoring, CRSP/security-link limitations, CRSP daily-coverage limits, and return-computation failures, but they do not yet classify acquisition versus bankruptcy versus other delisting causes. A separate CRSP delist-code or corporate-action checkpoint would be needed before making exit-mode claims.",
            "",
            "## Outputs",
            "",
            "- `data/analysis/baseline_differential_attrition_v1.csv`",
            "- `data/analysis/baseline_horizon_transition_attrition_v1.csv`",
            "- `data/analysis/baseline_wild_cluster_bootstrap_v1.csv`",
            "- `data/analysis/baseline_equivalence_diagnostics_v1.csv`",
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
            "# CHECKPOINT 33: Baseline Finalization Diagnostics",
            "",
            "## Status",
            "",
            "Completed differential attrition, wild cluster bootstrap, and equivalence diagnostics.",
            "",
            "## Created",
            "",
            "- `scripts/run_baseline_finalization_diagnostics_v1.py`",
            "- `data/analysis/baseline_differential_attrition_v1.csv`",
            "- `data/analysis/baseline_horizon_transition_attrition_v1.csv`",
            "- `data/analysis/baseline_wild_cluster_bootstrap_v1.csv`",
            "- `data/analysis/baseline_equivalence_diagnostics_v1.csv`",
            "- `quality_reports/baseline_finalization_diagnostics_v1_report.md`",
            "- `CHECKPOINT_33_BASELINE_FINALIZATION_DIAGNOSTICS.md`",
            "",
            "## Validation",
            "",
            f"- Scaffold event-window rows processed: {len(scaffold):,}",
            f"- Wild bootstrap replications requested per horizon: {BOOTSTRAP_REPS:,}",
            "- Upstream scaffold, link, linked-request, return-panel, modeling, and estimate files unchanged.",
            "",
            "## Guardrails",
            "",
            "- No new economic specification introduced.",
            "- No causal claims made.",
            "- Exit-mode claims remain blocked until delist/acquisition reasons are separately classified.",
            "",
        ]
    )
    CHECKPOINT_PATH.write_text(checkpoint, encoding="utf-8")

    print(f"Wrote {ATTRITION_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {TRANSITION_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {BOOTSTRAP_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {EQUIVALENCE_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    for row in bootstrap_rows:
        print("bootstrap", row["horizon_years"], row["wild_cluster_p_value"], row["wild_cluster_ci95_low_percentile_t"], row["wild_cluster_ci95_high_percentile_t"])


if __name__ == "__main__":
    main()
