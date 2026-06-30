"""Build validated conservative filing-level treatment dataset from V3.

This stage converts the V3 candidate layer into a validated treatment file
after the V3 manual audit passed the pre-specified precision gate. It does not
fetch prices, compute returns, make SEC requests, or make empirical claims.
"""

from __future__ import annotations

import csv
import hashlib
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AS_OF_DATE = date(2026, 6, 29)
TREATMENT_ID = "validated_conservative_filing_v1_from_v3_20260629"
AUDIT_PRECISION = "0.920"
AUDIT_FALSE_NEGATIVE_RATE = "0.000"

CANDIDATES_V3 = ROOT / "data" / "treatments" / "conservative_filing_treatment_candidates_v3.csv"
EVIDENCE_V3 = ROOT / "data" / "treatments" / "conservative_filing_treatment_evidence_v3.csv"
AUDITED_SAMPLE_V3 = ROOT / "data" / "review" / "conservative_filing_treatment_v3_audit_sample_audited_20260629.csv"
FILING_INDEX = ROOT / "data" / "metadata" / "filing_index.csv"
FIRM_UNIVERSE = ROOT / "config" / "firm_universe.csv"
RAW_PHRASE_HITS = ROOT / "data" / "extracted" / "phrase_hits.csv"

TREATMENT_OUT = ROOT / "data" / "treatments" / "validated_conservative_filing_treatments_v1.csv"
EVIDENCE_OUT = ROOT / "data" / "treatments" / "validated_conservative_filing_treatment_evidence_v1.csv"
REPORT_OUT = ROOT / "quality_reports" / "validated_conservative_filing_treatments_v1_report.md"
CHECKPOINT_OUT = ROOT / "CHECKPOINT_23_VALIDATED_CONSERVATIVE_TREATMENTS.md"

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


def parse_date(value: str) -> date | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def add_years(value: date, years: int) -> date:
    try:
        return value.replace(year=value.year + years)
    except ValueError:
        return value.replace(month=2, day=28, year=value.year + years)


def matured_flag(filing_date: str, years: int) -> tuple[str, str]:
    parsed = parse_date(filing_date)
    if parsed is None:
        return "no", "missing_filing_date"
    anniversary = add_years(parsed, years)
    if anniversary <= AS_OF_DATE:
        return "yes", anniversary.isoformat()
    return "no", f"right_censored_as_of_{AS_OF_DATE.isoformat()}"


def compact(value: str, limit: int = 420) -> str:
    text = " ".join((value or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def residual_risk(row: dict[str, str], excerpts: str) -> tuple[str, str]:
    if row["validated_conservative_treatment"] != "1":
        return "no", ""
    text = f"{row.get('strongest_evidence_phrase', '')} {row.get('narrative_subcategories_present', '')} {excerpts}".lower()
    reasons: list[str] = []
    if "cra" in text or "community reinvestment act" in text or "final rules" in text or "regulatory" in text:
        reasons.append("CRA/regulatory-policy access language")
    if "gain on sale of affordable housing" in text or "residential mortgage loans" in text:
        reasons.append("affordable-housing sale/accounting context")
    if "risk factors" in text:
        reasons.append("risk-section evidence")
    if reasons:
        return "yes", "; ".join(sorted(set(reasons)))
    return "no", ""


def markdown_table(headers: list[str], rows: list[list[str | int]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main() -> None:
    required = [CANDIDATES_V3, EVIDENCE_V3, AUDITED_SAMPLE_V3, FILING_INDEX, FIRM_UNIVERSE, RAW_PHRASE_HITS]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")

    hashes_before = {path.name: sha256(path) for path in required}

    candidate_rows = read_csv(CANDIDATES_V3)
    evidence_rows = read_csv(EVIDENCE_V3)
    filing_rows = read_csv(FILING_INDEX)
    firm_rows = read_csv(FIRM_UNIVERSE)

    filing_lookup = {row.get("accession_number", ""): row for row in filing_rows if row.get("accession_number")}
    firm_lookup = {row.get("firm_id", ""): row for row in firm_rows if row.get("firm_id")}

    evidence_by_accession: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in evidence_rows:
        evidence_by_accession[row["accession_number"]].append(row)

    treatment_rows: list[dict[str, str]] = []
    for row in candidate_rows:
        accession = row["accession_number"]
        filing = filing_lookup.get(accession, {})
        firm = firm_lookup.get(row["firm_id"], {})
        is_treated = row["conservative_candidate_flag"] == "yes"
        evidence = evidence_by_accession.get(accession, [])
        primary_evidence = sorted(
            evidence,
            key=lambda ev: (
                0 if ev.get("evidence_confidence") == "high" else 1,
                ev.get("section_name", ""),
                ev.get("phrase", ""),
            ),
        )
        representative_excerpt = compact(primary_evidence[0].get("excerpt", "") if primary_evidence else "")
        subcategories = row.get("narrative_subcategories_present", "")
        flag_1y, date_1y = matured_flag(row["filing_date"], 1)
        flag_3y, date_3y = matured_flag(row["filing_date"], 3)
        flag_5y, date_5y = matured_flag(row["filing_date"], 5)

        out = {
            "treatment_definition_id": TREATMENT_ID,
            "validation_source": "CHECKPOINT_22_CONSERVATIVE_FILING_TREATMENT_V3_AUDIT",
            "validation_precision_estimate": AUDIT_PRECISION,
            "validation_false_negative_rate_estimate": AUDIT_FALSE_NEGATIVE_RATE,
            "firm_id": row["firm_id"],
            "ticker": row["ticker"],
            "company_name": row.get("company_name") or filing.get("company_name") or firm.get("company_name", ""),
            "cik": row["cik"],
            "accession_number": accession,
            "filing_year": row["filing_year"],
            "filing_date": row["filing_date"],
            "event_date": row["filing_date"],
            "report_date": filing.get("report_date", ""),
            "form": filing.get("form", ""),
            "filing_url": filing.get("filing_url", ""),
            "primary_document_url": filing.get("primary_document_url", ""),
            "validated_conservative_treatment": "1" if is_treated else "0",
            "treatment_status": "validated_conservative_treated" if is_treated else "validated_control_or_untreated",
            "narrative_subcategories_present": subcategories,
            "primary_narrative_subcategory": subcategories.split("; ")[0] if subcategories else "",
            "evidence_hit_count": row["evidence_hit_count"],
            "evidence_section_count": row["evidence_section_count"],
            "strongest_evidence_phrase": row["strongest_evidence_phrase"],
            "high_risk_evidence_flag": row["high_risk_evidence_flag"],
            "candidate_confidence": row["candidate_confidence"],
            "exclusion_or_no_treatment_reason": "" if is_treated else row["exclusion_or_no_candidate_reason"],
            "representative_evidence_excerpt": representative_excerpt,
            "one_year_window_matured_as_of_2026_06_29": flag_1y,
            "one_year_anniversary_or_status": date_1y,
            "three_year_window_matured_as_of_2026_06_29": flag_3y,
            "three_year_anniversary_or_status": date_3y,
            "five_year_window_matured_as_of_2026_06_29": flag_5y,
            "five_year_anniversary_or_status": date_5y,
        }
        risk_flag, risk_reason = residual_risk(out, representative_excerpt)
        out["residual_false_positive_risk_flag"] = risk_flag
        out["residual_false_positive_risk_reason"] = risk_reason
        treatment_rows.append(out)

    treatment_fields = [
        "treatment_definition_id",
        "validation_source",
        "validation_precision_estimate",
        "validation_false_negative_rate_estimate",
        "firm_id",
        "ticker",
        "company_name",
        "cik",
        "accession_number",
        "filing_year",
        "filing_date",
        "event_date",
        "report_date",
        "form",
        "filing_url",
        "primary_document_url",
        "validated_conservative_treatment",
        "treatment_status",
        "narrative_subcategories_present",
        "primary_narrative_subcategory",
        "evidence_hit_count",
        "evidence_section_count",
        "strongest_evidence_phrase",
        "high_risk_evidence_flag",
        "candidate_confidence",
        "exclusion_or_no_treatment_reason",
        "representative_evidence_excerpt",
        "residual_false_positive_risk_flag",
        "residual_false_positive_risk_reason",
        "one_year_window_matured_as_of_2026_06_29",
        "one_year_anniversary_or_status",
        "three_year_window_matured_as_of_2026_06_29",
        "three_year_anniversary_or_status",
        "five_year_window_matured_as_of_2026_06_29",
        "five_year_anniversary_or_status",
    ]
    write_csv(TREATMENT_OUT, treatment_fields, treatment_rows)

    evidence_out_rows: list[dict[str, str]] = []
    treated_accessions = {row["accession_number"] for row in treatment_rows if row["validated_conservative_treatment"] == "1"}
    for row in evidence_rows:
        if row["accession_number"] not in treated_accessions:
            continue
        evidence_out_rows.append(
            {
                "treatment_definition_id": TREATMENT_ID,
                "validation_source": "CHECKPOINT_22_CONSERVATIVE_FILING_TREATMENT_V3_AUDIT",
                **row,
            }
        )

    evidence_fields = [
        "treatment_definition_id",
        "validation_source",
        "firm_id",
        "ticker",
        "company_name",
        "cik",
        "accession_number",
        "filing_date",
        "filing_year",
        "section_name",
        "phrase",
        "category",
        "narrative_subcategory",
        "excerpt",
        "evidence_rule",
        "evidence_confidence",
        "high_risk_phrase_flag",
        "evidence_notes",
    ]
    write_csv(EVIDENCE_OUT, evidence_fields, evidence_out_rows)

    hashes_after = {path.name: sha256(path) for path in required}

    treated = [row for row in treatment_rows if row["validated_conservative_treatment"] == "1"]
    controls = [row for row in treatment_rows if row["validated_conservative_treatment"] == "0"]
    year_counts = Counter(row["filing_year"] for row in treated)
    subcat_counts = Counter(row["primary_narrative_subcategory"] for row in treated)
    firm_counts = Counter(f"{row['ticker']} ({row['firm_id']})" for row in treated)
    maturity_counts = Counter(
        (
            row["one_year_window_matured_as_of_2026_06_29"],
            row["three_year_window_matured_as_of_2026_06_29"],
            row["five_year_window_matured_as_of_2026_06_29"],
        )
        for row in treated
    )
    residual_risk_counts = Counter(row["residual_false_positive_risk_flag"] for row in treated)

    report_lines = [
        "# Validated Conservative Filing Treatments V1 Report",
        "",
        f"Generated from V3 candidate layer and CHECKPOINT_22 audit on {AS_OF_DATE.isoformat()}.",
        "",
        "## Guardrails",
        "",
        "- This stage constructs a validated text-treatment dataset only.",
        "- No prices were fetched.",
        "- No returns were computed.",
        "- No benchmark data were loaded.",
        "- No SEC requests were made.",
        "- No empirical performance claims were made.",
        "",
        "## Validation Basis",
        "",
        "- Source candidate layer: `data/treatments/conservative_filing_treatment_candidates_v3.csv`.",
        "- Source evidence layer: `data/treatments/conservative_filing_treatment_evidence_v3.csv`.",
        "- Manual audit checkpoint: `CHECKPOINT_22_CONSERVATIVE_FILING_TREATMENT_V3_AUDIT.md`.",
        "- Candidate-positive precision estimate: 92.0%.",
        "- Candidate-negative false-negative estimate: 0.0%.",
        "",
        "## Treatment Counts",
        "",
        f"- Filing rows in treatment panel: {len(treatment_rows):,}",
        f"- Validated conservative treated filings: {len(treated):,}",
        f"- Untreated/control filings: {len(controls):,}",
        f"- Validated evidence rows retained for treated filings: {len(evidence_out_rows):,}",
        "",
        "## Treated Filings By Filing Year",
        "",
        markdown_table(["Filing year", "Treated filings"], [[k, v] for k, v in sorted(year_counts.items())]),
        "",
        "## Treated Filings By Primary Narrative Subcategory",
        "",
        markdown_table(["Primary narrative subcategory", "Treated filings"], subcat_counts.most_common()),
        "",
        "## Top Treated Firms",
        "",
        markdown_table(["Firm", "Treated filings"], firm_counts.most_common(25)),
        "",
        "## Calendar Window Observability For Treated Filings",
        "",
        "These are date-maturity flags only, not return availability checks.",
        "",
        markdown_table(
            ["1Y matured", "3Y matured", "5Y matured", "Treated filings"],
            [[a, b, c, n] for (a, b, c), n in sorted(maturity_counts.items())],
        ),
        "",
        "## Residual Construct-Validity Risk Flags",
        "",
        markdown_table(["Residual risk flag", "Treated filings"], residual_risk_counts.most_common()),
        "",
        "## Input Integrity",
        "",
    ]
    for name, before_hash in sorted(hashes_before.items()):
        report_lines.append(f"- `{name}` before: `{before_hash}`")
        report_lines.append(f"- `{name}` after: `{hashes_after[name]}`")
        report_lines.append(f"- `{name}` unchanged: {'yes' if before_hash == hashes_after[name] else 'no'}")
    report_lines += [
        "",
        "## Next Gate",
        "",
        "The next methodological step is linking/security-return preparation. That step should first audit ticker/CIK/security identifiers, delisting and corporate-action handling, benchmark definitions, and return-window status codes. SEC requests, if needed, should wait until that stage and must use a valid SEC user-agent.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(report_lines), encoding="utf-8")

    checkpoint_lines = [
        "# CHECKPOINT 23: Validated Conservative Filing Treatments",
        "",
        f"Generated at: {AS_OF_DATE.isoformat()}",
        "",
        "## Completed",
        "",
        "- Converted V3 candidate layer into a validated conservative filing-level treatment dataset.",
        "- Preserved validation metadata from CHECKPOINT_22.",
        "- Added event dates based on 10-K filing dates.",
        "- Added calendar-only 1-year, 3-year, and 5-year window maturity flags.",
        "- Retained evidence excerpts for treated filings.",
        "- Did not fetch prices, compute returns, load benchmarks, make SEC requests, or make empirical claims.",
        "",
        "## Files Created",
        "",
        "- `scripts/build_validated_conservative_treatments_v1.py`",
        "- `data/treatments/validated_conservative_filing_treatments_v1.csv`",
        "- `data/treatments/validated_conservative_filing_treatment_evidence_v1.csv`",
        "- `quality_reports/validated_conservative_filing_treatments_v1_report.md`",
        "- `CHECKPOINT_23_VALIDATED_CONSERVATIVE_TREATMENTS.md`",
        "",
        "## Counts",
        "",
        f"- Treatment panel filings: {len(treatment_rows):,}",
        f"- Validated conservative treated filings: {len(treated):,}",
        f"- Untreated/control filings: {len(controls):,}",
        f"- Treated evidence rows: {len(evidence_out_rows):,}",
        "",
        "## Validation Metadata",
        "",
        "- Candidate-positive precision estimate: 92.0%.",
        "- Candidate-negative false-negative estimate: 0.0%.",
        "- Validation source: `CHECKPOINT_22_CONSERVATIVE_FILING_TREATMENT_V3_AUDIT.md`.",
        "",
        "## Guardrails",
        "",
        "- No prices fetched.",
        "- No returns computed.",
        "- No benchmarks loaded.",
        "- No SEC requests made.",
        "- No empirical performance claims made.",
        "",
        "## Next",
        "",
        "Proceed to security-linking and return-data preparation only after reviewing the validated treatment output. Ask for the SEC user-agent before any future SEC request stage.",
        "",
    ]
    CHECKPOINT_OUT.write_text("\n".join(checkpoint_lines), encoding="utf-8")

    print(f"Wrote {TREATMENT_OUT.relative_to(ROOT)} ({len(treatment_rows)} rows)")
    print(f"Wrote {EVIDENCE_OUT.relative_to(ROOT)} ({len(evidence_out_rows)} rows)")
    print(f"Wrote {REPORT_OUT.relative_to(ROOT)}")
    print(f"Wrote {CHECKPOINT_OUT.relative_to(ROOT)}")
    print(f"treated_filings {len(treated)}")
    print(f"control_filings {len(controls)}")


if __name__ == "__main__":
    main()
