import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PANEL_PATH = PROJECT_ROOT / "data" / "analysis" / "return_analysis_panel_v1.csv"
MODELING_PATH = PROJECT_ROOT / "data" / "analysis" / "regression_modeling_dataset_v1.csv"
SUPPORT_PATH = PROJECT_ROOT / "data" / "analysis" / "model_sample_support_v1.csv"
SPEC_PATH = PROJECT_ROOT / "methodology" / "model_specification_v1.md"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "modeling_dataset_pre_estimation_validation_v1_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_30_MODELING_DATASET_AND_SPEC.md"

ANALYSIS_READY = "analysis_ready_computed_return"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def is_float_text(value):
    text = str(value or "").strip()
    if not text:
        return False
    try:
        float(text)
    except ValueError:
        return False
    return True


def markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    if not PANEL_PATH.exists():
        raise FileNotFoundError(PANEL_PATH)

    panel_hash_before = sha256_file(PANEL_PATH)
    rows = read_rows(PANEL_PATH)
    if not rows:
        raise ValueError("Analysis panel has no rows.")

    modeling_rows = []
    missing_required = Counter()

    for row in rows:
        if row.get("analysis_sample_status") != ANALYSIS_READY:
            continue

        treatment = str(row.get("validated_conservative_treatment", "")).strip()
        horizon = str(row.get("horizon_years", "")).strip()
        filing_year = str(row.get("filing_year", "")).strip()
        issuer_cluster_id = str(row.get("firm_id") or row.get("cik") or "").strip()

        required = {
            "event_window_id": row.get("event_window_id", ""),
            "event_id": row.get("event_id", ""),
            "issuer_cluster_id": issuer_cluster_id,
            "filing_year": filing_year,
            "horizon_years": horizon,
            "treatment_main": treatment,
            "outcome_primary_excess_vwretd_raw": row.get("excess_return_vs_vwretd", ""),
            "outcome_primary_excess_vwretd_winsor_p01_p99": row.get(
                "excess_return_vs_vwretd_winsor_p01_p99_by_horizon", ""
            ),
            "outcome_secondary_raw_return": row.get("issuer_raw_return_compounded", ""),
            "outcome_secondary_raw_return_winsor_p01_p99": row.get(
                "issuer_raw_return_compounded_winsor_p01_p99_by_horizon", ""
            ),
        }

        for key, value in required.items():
            if not str(value).strip():
                missing_required[key] += 1
        for key in [
            "outcome_primary_excess_vwretd_raw",
            "outcome_primary_excess_vwretd_winsor_p01_p99",
            "outcome_secondary_raw_return",
            "outcome_secondary_raw_return_winsor_p01_p99",
        ]:
            if not is_float_text(required[key]):
                missing_required[key + "_non_numeric"] += 1

        modeling_rows.append(
            {
                "event_window_id": row.get("event_window_id", ""),
                "event_id": row.get("event_id", ""),
                "firm_id": row.get("firm_id", ""),
                "cik": row.get("cik", ""),
                "issuer_cluster_id": issuer_cluster_id,
                "ticker_from_project": row.get("ticker_from_project", ""),
                "company_name": row.get("company_name", ""),
                "accession_number": row.get("accession_number", ""),
                "event_date": row.get("event_date", ""),
                "filing_year": filing_year,
                "horizon_years": horizon,
                "permno": row.get("permno", ""),
                "validated_conservative_treatment": treatment,
                "treatment_main": treatment,
                "primary_narrative_subcategory": row.get("primary_narrative_subcategory", ""),
                "model_sample_main": "1",
                "model_sample_reason": "analysis_ready_computed_return",
                "outcome_primary_excess_vwretd_raw": row.get("excess_return_vs_vwretd", ""),
                "outcome_primary_excess_vwretd_winsor_p01_p99": row.get(
                    "excess_return_vs_vwretd_winsor_p01_p99_by_horizon", ""
                ),
                "outcome_secondary_raw_return": row.get("issuer_raw_return_compounded", ""),
                "outcome_secondary_raw_return_winsor_p01_p99": row.get(
                    "issuer_raw_return_compounded_winsor_p01_p99_by_horizon", ""
                ),
                "outcome_alt_excess_vwretx_winsor_p01_p99": row.get(
                    "excess_return_vs_vwretx_winsor_p01_p99_by_horizon", ""
                ),
                "outcome_alt_excess_ewretd_winsor_p01_p99": row.get(
                    "excess_return_vs_ewretd_winsor_p01_p99_by_horizon", ""
                ),
                "outcome_alt_excess_sprtrn_winsor_p01_p99": row.get(
                    "excess_return_vs_sprtrn_winsor_p01_p99_by_horizon", ""
                ),
                "fixed_effect_filing_year": filing_year,
                "fixed_effect_horizon": horizon,
                "cluster_issuer": issuer_cluster_id,
            }
        )

    modeling_fieldnames = [
        "event_window_id",
        "event_id",
        "firm_id",
        "cik",
        "issuer_cluster_id",
        "ticker_from_project",
        "company_name",
        "accession_number",
        "event_date",
        "filing_year",
        "horizon_years",
        "permno",
        "validated_conservative_treatment",
        "treatment_main",
        "primary_narrative_subcategory",
        "model_sample_main",
        "model_sample_reason",
        "outcome_primary_excess_vwretd_raw",
        "outcome_primary_excess_vwretd_winsor_p01_p99",
        "outcome_secondary_raw_return",
        "outcome_secondary_raw_return_winsor_p01_p99",
        "outcome_alt_excess_vwretx_winsor_p01_p99",
        "outcome_alt_excess_ewretd_winsor_p01_p99",
        "outcome_alt_excess_sprtrn_winsor_p01_p99",
        "fixed_effect_filing_year",
        "fixed_effect_horizon",
        "cluster_issuer",
    ]
    write_csv(MODELING_PATH, modeling_fieldnames, modeling_rows)

    support_rows = []
    horizon_counts = Counter(row["horizon_years"] for row in modeling_rows)
    horizon_treatment_counts = Counter((row["horizon_years"], row["treatment_main"]) for row in modeling_rows)
    year_horizon_treatment_counts = Counter(
        (row["filing_year"], row["horizon_years"], row["treatment_main"]) for row in modeling_rows
    )

    issuer_horizon_treatments = defaultdict(set)
    issuer_horizon_counts = Counter()
    for row in modeling_rows:
        key = (row["issuer_cluster_id"], row["horizon_years"])
        issuer_horizon_treatments[key].add(row["treatment_main"])
        issuer_horizon_counts[key] += 1

    for horizon in sorted(horizon_counts):
        total = horizon_counts[horizon]
        treated = horizon_treatment_counts[(horizon, "1")]
        control = horizon_treatment_counts[(horizon, "0")]
        firms = {row["issuer_cluster_id"] for row in modeling_rows if row["horizon_years"] == horizon}
        treated_firms = {
            row["issuer_cluster_id"]
            for row in modeling_rows
            if row["horizon_years"] == horizon and row["treatment_main"] == "1"
        }
        within_var_firms = {
            firm
            for (firm, h), treatments in issuer_horizon_treatments.items()
            if h == horizon and treatments == {"0", "1"}
        }
        support_rows.append(
            {
                "support_type": "horizon_summary",
                "filing_year": "",
                "horizon_years": horizon,
                "treatment": "",
                "rows": str(total),
                "treated_rows": str(treated),
                "control_rows": str(control),
                "unique_issuers": str(len(firms)),
                "treated_issuers": str(len(treated_firms)),
                "within_issuer_variation_issuers": str(len(within_var_firms)),
                "support_note": "baseline_year_FE_specification_support",
            }
        )

    for (year, horizon, treatment), count in sorted(year_horizon_treatment_counts.items()):
        support_rows.append(
            {
                "support_type": "filing_year_horizon_treatment",
                "filing_year": year,
                "horizon_years": horizon,
                "treatment": treatment,
                "rows": str(count),
                "treated_rows": str(count if treatment == "1" else 0),
                "control_rows": str(count if treatment == "0" else 0),
                "unique_issuers": "",
                "treated_issuers": "",
                "within_issuer_variation_issuers": "",
                "support_note": "cell_count_only_no_estimation",
            }
        )

    support_fieldnames = [
        "support_type",
        "filing_year",
        "horizon_years",
        "treatment",
        "rows",
        "treated_rows",
        "control_rows",
        "unique_issuers",
        "treated_issuers",
        "within_issuer_variation_issuers",
        "support_note",
    ]
    write_csv(SUPPORT_PATH, support_fieldnames, support_rows)

    panel_hash_after = sha256_file(PANEL_PATH)

    horizon_summary_rows = [
        [
            row["horizon_years"],
            row["rows"],
            row["treated_rows"],
            row["control_rows"],
            row["unique_issuers"],
            row["treated_issuers"],
            row["within_issuer_variation_issuers"],
        ]
        for row in support_rows
        if row["support_type"] == "horizon_summary"
    ]

    year_treated_rows = [
        [year, horizon, count]
        for (year, horizon, treatment), count in sorted(year_horizon_treatment_counts.items())
        if treatment == "1"
    ]

    spec = "\n".join(
        [
            "# Model Specification V1",
            "",
            "This specification is locked before running regressions or event-study estimates.",
            "",
            "## Analysis Unit",
            "",
            "- Unit: issuer-filing-window.",
            "- Event date: SEC 10-K filing date.",
            "- Horizons: 1-year, 3-year, and 5-year forward windows.",
            "- Main analysis sample: rows with `model_sample_main == 1` in `data/analysis/regression_modeling_dataset_v1.csv`.",
            "",
            "## Treatment",
            "",
            "- Main treatment: `treatment_main`, equal to the validated conservative filing-level access-oriented disclosure treatment.",
            "- This is the V3 conservative treatment that passed manual validation.",
            "- Raw phrase hits, failed V2 labels, and tiered V1 labels are not main treatments.",
            "",
            "## Primary Outcome",
            "",
            "- `outcome_primary_excess_vwretd_winsor_p01_p99`: issuer compounded return minus CRSP value-weighted market return with dividends, winsorized within horizon at p01/p99.",
            "- Raw non-winsorized `outcome_primary_excess_vwretd_raw` must be reported as a sensitivity check.",
            "",
            "## Secondary Outcomes",
            "",
            "- `outcome_secondary_raw_return_winsor_p01_p99` for unadjusted return comparisons.",
            "- Alternative benchmark-adjusted outcomes using `vwretx`, `ewretd`, and `sprtrn` only as robustness checks.",
            "",
            "## Baseline Estimation Plan",
            "",
            "Estimate separate cross-sectional panel models by horizon:",
            "",
            "```text",
            "Y_{i,f,h} = alpha_h + beta_h * Treatment_{i,f} + FilingYearFE_f + epsilon_{i,f,h}",
            "```",
            "",
            "- Run this separately for 1-year, 3-year, and 5-year horizons.",
            "- Cluster standard errors by issuer using `cluster_issuer`.",
            "- Interpret estimates as conditional associations, not causal effects.",
            "",
            "## Secondary Pooled Specification",
            "",
            "A pooled horizon specification may be used only as a compact summary:",
            "",
            "```text",
            "Y_{i,f,h} = alpha + beta * Treatment_{i,f} + HorizonFE_h + FilingYearFE_f + epsilon_{i,f,h}",
            "```",
            "",
            "- Cluster by issuer.",
            "- Do not use pooled results as the sole headline because horizons have different censoring and return distributions.",
            "",
            "## Firm Fixed Effects",
            "",
            "- Firm fixed-effects models are exploratory unless within-issuer treatment variation is sufficient.",
            "- Support must be reported from `data/analysis/model_sample_support_v1.csv` before any firm-FE result is interpreted.",
            "- If support is limited, firm-FE estimates should be described as low-power diagnostics.",
            "",
            "## Controls",
            "",
            "- Baseline controls are filing-year fixed effects only, because point-in-time accounting controls have not yet been imported.",
            "- Size, book-to-market, leverage, profitability, prior returns, and volatility require a separate WRDS/Compustat/CRSP control-import checkpoint before use.",
            "- No control should be added after viewing regression results unless labeled exploratory.",
            "",
            "## Prohibited Claims",
            "",
            "- Do not claim treatment caused later returns.",
            "- Do not claim disclosure language proves actual product expansion, customer outcomes, or management intent.",
            "- Do not treat right-censored, link-failed, or non-computed windows as ordinary complete observations.",
            "",
            "## Required Reporting",
            "",
            "- Report sample size by horizon and treatment.",
            "- Report filing-year treatment support.",
            "- Report raw and winsorized primary outcomes.",
            "- Report missing/non-computed status counts inherited from prior checkpoints.",
            "- Report long-horizon caution for 3-year and 5-year windows.",
            "",
        ]
    )
    SPEC_PATH.write_text(spec, encoding="utf-8")

    report = "\n".join(
        [
            "# Modeling Dataset Pre-Estimation Validation V1 Report",
            "",
            "## Guardrails",
            "",
            "- This step built modeling inputs and locked the first model specification.",
            "- No regressions, event-study estimates, p-values, or empirical claims were produced.",
            "- The upstream analysis panel was preserved unchanged.",
            "",
            "## Inputs",
            "",
            "- `data/analysis/return_analysis_panel_v1.csv`",
            "",
            "## Outputs",
            "",
            "- `data/analysis/regression_modeling_dataset_v1.csv`",
            "- `data/analysis/model_sample_support_v1.csv`",
            "- `methodology/model_specification_v1.md`",
            "",
            "## Reconciliation",
            "",
            f"- Analysis panel rows read: {len(rows):,}",
            f"- Regression modeling rows written: {len(modeling_rows):,}",
            f"- Non-analysis-ready rows excluded from modeling dataset: {len(rows) - len(modeling_rows):,}",
            "",
            "## Required Field Checks",
            "",
            markdown_table(
                ["Field issue", "Rows"],
                [(issue, f"{count:,}") for issue, count in sorted(missing_required.items())] or [["none", "0"]],
            ),
            "",
            "## Horizon Support",
            "",
            markdown_table(
                [
                    "Horizon years",
                    "Rows",
                    "Treated rows",
                    "Control rows",
                    "Unique issuers",
                    "Treated issuers",
                    "Within-issuer variation issuers",
                ],
                horizon_summary_rows,
            ),
            "",
            "## Treated Filing-Year Support",
            "",
            markdown_table(["Filing year", "Horizon years", "Treated rows"], year_treated_rows),
            "",
            "## Input Integrity",
            "",
            f"- `return_analysis_panel_v1.csv` before: `{panel_hash_before}`",
            f"- `return_analysis_panel_v1.csv` after: `{panel_hash_after}`",
            f"- `return_analysis_panel_v1.csv` unchanged: {'yes' if panel_hash_before == panel_hash_after else 'no'}",
            "",
        ]
    )
    REPORT_PATH.write_text(report, encoding="utf-8")

    checkpoint = "\n".join(
        [
            "# CHECKPOINT 30: Modeling Dataset And Specification",
            "",
            "## Status",
            "",
            "Completed regression-modeling dataset construction and pre-estimation model specification.",
            "",
            "## Created",
            "",
            "- `scripts/prepare_modeling_specification_v1.py`",
            "- `data/analysis/regression_modeling_dataset_v1.csv`",
            "- `data/analysis/model_sample_support_v1.csv`",
            "- `methodology/model_specification_v1.md`",
            "- `quality_reports/modeling_dataset_pre_estimation_validation_v1_report.md`",
            "- `CHECKPOINT_30_MODELING_DATASET_AND_SPEC.md`",
            "",
            "## Validation",
            "",
            f"- Modeling rows: {len(modeling_rows):,}",
            f"- Non-analysis-ready rows excluded: {len(rows) - len(modeling_rows):,}",
            f"- Required field issue types: {len(missing_required):,}",
            f"- Upstream analysis panel unchanged: {'yes' if panel_hash_before == panel_hash_after else 'no'}",
            "",
            "## Guardrails",
            "",
            "- No regressions run.",
            "- No event-study estimates run.",
            "- No p-values, coefficients, or empirical claims produced.",
            "- Controls beyond filing-year fixed effects remain blocked until a separate point-in-time control-import checkpoint.",
            "",
        ]
    )
    CHECKPOINT_PATH.write_text(checkpoint, encoding="utf-8")

    print(f"Wrote {MODELING_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {SUPPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {SPEC_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"modeling_rows {len(modeling_rows)}")
    print(f"required_field_issue_types {len(missing_required)}")


if __name__ == "__main__":
    main()
