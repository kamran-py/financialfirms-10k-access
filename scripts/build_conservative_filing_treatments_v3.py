"""Build V3 conservative filing-level access-oriented disclosure candidates.

V3 tightens V2 based on the CHECKPOINT_20 audit. It remains a candidate
construction step only: no prices, returns, SEC requests, or empirical claims.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import build_conservative_filing_treatments_v1 as base
import build_conservative_filing_treatments_v2 as v2


ROOT = base.ROOT

base.CANDIDATE_OUT = ROOT / "data" / "treatments" / "conservative_filing_treatment_candidates_v3.csv"
base.EVIDENCE_OUT = ROOT / "data" / "treatments" / "conservative_filing_treatment_evidence_v3.csv"
base.REPORT_OUT = ROOT / "quality_reports" / "conservative_filing_treatment_candidates_v3_report.md"
base.AUDIT_SAMPLE_OUT = ROOT / "data" / "review" / "conservative_filing_treatment_v3_audit_sample.csv"
base.AUDIT_PLAN_OUT = ROOT / "quality_reports" / "conservative_filing_treatment_v3_audit_plan.md"
base.CHECKPOINT_OUT = ROOT / "CHECKPOINT_21_CONSERVATIVE_FILING_TREATMENT_CANDIDATES_V3.md"

RULES_V3 = ROOT / "config" / "conservative_filing_treatment_rules_v3.md"
AUDIT_RESULTS_V2 = ROOT / "quality_reports" / "conservative_filing_treatment_v2_audit_results_20260629.md"


def rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


ANY_FHLB = rx(r"\b(FHLB|FHLBs|Federal Home Loan Bank|Federal Home Loan Banks)\b")
CRE_PROPERTY_LIST = rx(
    r"\b(property types financed include|properties financed include|commercial real estate.*(?:office|industrial).{0,120}affordable housing|"
    r"office,\s*industrial,\s*multi[- ]family,\s*affordable housing,\s*retail)\b"
)
CRA_OR_REGULATORY_GOALS = rx(
    r"\b(CRA Rule|CRA Proposal|bank regulatory agencies described the goals|federal banking agencies described the goals|"
    r"goals of the CRA|to expand access to credit, investment, and basic banking services|"
    r"Congress finalized|legislation is focused.*improving consumer access to credit)\b"
)
SPCP_BACKGROUND = rx(r"\b(SPCPs?|special purpose credit programs?)\b")
RISK_CLAIMS_ONLY = rx(r"\b(potential claims regarding financial inclusion|claims regarding financial inclusion)\b")
CARD_INFRASTRUCTURE = rx(
    r"\b(card issuing technology|open APIs?|modern architecture|configurability|accelerated product development|"
    r"payment gateway technology|links a merchant.?s website to its processing network|democratiz(?:e|es|ed|ing) access to card issuing technology)\b"
)
PRIVATE_ACCESS_VEHICLES = rx(
    r"\b(democratized access vehicles?|investment vehicle investor base|distributed to individual investors indirectly|"
    r"private wealth|high net worth|family office|new base of individual investors)\b"
)
BROAD_MISSION_ONLY = rx(
    r"\b(vision is to create greater economic opportunities|financial inclusion for all|community impact program|"
    r"partners with organizations that provide resources|innovative products and solutions that will achieve financial inclusion|"
    r"mission has always been to democratize access to financial markets for global customers)\b"
)
CONCRETE_PRODUCT = rx(
    r"\b(loan|loans|lending|credit|banking|deposit|checking|prepaid|debit|insurance|mortgage|"
    r"money transfer|bill payment|remittance|payment services|financial services offerings|"
    r"community checking|home ownership and loan programs|affordable credit|auto refinance)\b"
)


def text_for(row: dict[str, str]) -> tuple[str, str, str, str]:
    return v2.text_for(row)


def v3_hard_exclusion_reasons(row: dict[str, str]) -> list[str]:
    text, phrase, _category, section = text_for(row)
    lower = text.lower()
    reasons = list(v2.hard_exclusion_reasons(row))

    if ("affordable housing" in phrase or "access to housing" in phrase or "housing" in lower) and ANY_FHLB.search(text):
        reasons.append("V3 hard exclusion: FHLB housing/affordable-housing boilerplate")
    if CRE_PROPERTY_LIST.search(text):
        reasons.append("V3 hard exclusion: generic CRE property-type list")
    if CRA_OR_REGULATORY_GOALS.search(text):
        reasons.append("V3 hard exclusion: CRA/regulatory/congressional policy background")
    if SPCP_BACKGROUND.search(text) and not rx(r"\b(we|our|company|bank)\b.{0,120}\b(offer|offers|offered|provide|provides|provided|launch|launched)\b").search(text):
        reasons.append("V3 hard exclusion: special-purpose-credit-program background without issuer offering")
    if RISK_CLAIMS_ONLY.search(text):
        reasons.append("V3 hard exclusion: financial-inclusion claims/risk discussion")
    if CARD_INFRASTRUCTURE.search(text):
        reasons.append("V3 hard exclusion: card/API/platform infrastructure access")
    if PRIVATE_ACCESS_VEHICLES.search(text):
        reasons.append("V3 hard exclusion: broader-only private/HNW/investor-access vehicle")
    if BROAD_MISSION_ONLY.search(text) and not CONCRETE_PRODUCT.search(text):
        reasons.append("V3 hard exclusion: broad mission/vision language without concrete product")
    if "risk factors" in section and ("financial inclusion" in lower or "democratiz" in lower) and not CONCRETE_PRODUCT.search(text):
        reasons.append("V3 hard exclusion: risk-section access language without concrete product")

    return sorted(set(reasons))


def exclusion_reasons_v3(row: dict[str, str]) -> list[str]:
    reasons = v3_hard_exclusion_reasons(row)
    if reasons:
        return reasons
    return v2.exclusion_reasons_v2(row)


def positive_rule_v3(row: dict[str, str]) -> tuple[bool, str, str, str]:
    reasons = v3_hard_exclusion_reasons(row)
    if reasons:
        return False, "", "", "; ".join(reasons)

    positive, rule, subcategory, notes = v2.positive_rule_v2(row)
    if not positive:
        return positive, rule, subcategory, notes

    text, _phrase, _category, _section = text_for(row)
    if subcategory == "financial inclusion / underbanked / underserved" and not CONCRETE_PRODUCT.search(text):
        return False, "", "", "V3 hard exclusion: financial-inclusion language lacks concrete product/program."
    if subcategory == "payments / money movement / SMB commerce access" and CARD_INFRASTRUCTURE.search(text):
        return False, "", "", "V3 hard exclusion: payments language is technology/infrastructure access."

    return True, rule.replace("V2", "V3", 1), subcategory, notes


def build_report_v3(
    candidate_rows: list[dict[str, str]],
    evidence_rows: list[dict[str, str]],
    excluded_family_counts: Counter[str],
    evidence_by_filing: dict[tuple[str, ...], list[dict[str, str]]],
    hits_by_filing: dict[tuple[str, ...], list[dict[str, str]]],
    input_hashes: dict[str, str],
) -> str:
    text = v2.build_report_v2(
        candidate_rows,
        evidence_rows,
        excluded_family_counts,
        evidence_by_filing,
        hits_by_filing,
        input_hashes,
    )
    return (
        text.replace("Conservative Filing Treatment Candidates V2 Report", "Conservative Filing Treatment Candidates V3 Report")
        .replace("scripts/build_conservative_filing_treatments_v2.py", "scripts/build_conservative_filing_treatments_v3.py")
        .replace("V2 candidate", "V3 candidate")
        .replace("V2 uses", "V3 uses")
        .replace("V2 filing-level", "V3 filing-level")
        .replace("V2 hit", "V2 hit")
        + "\n\n## V3-Specific Revision\n\nV3 applies hard exclusions from the CHECKPOINT_20 audit: FHLB housing boilerplate, CRE property-type lists, CRA/regulatory-policy background, infrastructure democratization, private/HNW access vehicles, and broad mission language without concrete products.\n"
    )


def build_audit_plan_v3(audit_rows: list[dict[str, str]], candidate_rows: list[dict[str, str]]) -> str:
    return v2.build_audit_plan_v2(audit_rows, candidate_rows).replace(
        "Conservative Filing Treatment V2 Audit Plan", "Conservative Filing Treatment V3 Audit Plan"
    ).replace("V2 filing-level", "V3 filing-level").replace("Full V2", "Full V3")


def build_checkpoint_v3(
    candidate_rows: list[dict[str, str]],
    evidence_rows: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    excluded_family_counts: Counter[str],
    hashes_before: dict[str, str],
    hashes_after: dict[str, str],
) -> str:
    yes_count = sum(1 for row in candidate_rows if row["conservative_candidate_flag"] == "yes")
    no_count = len(candidate_rows) - yes_count
    audit_counts = Counter(row["conservative_candidate_flag"] for row in audit_rows)
    subcat_counts = Counter(ev["narrative_subcategory"] for ev in evidence_rows)
    year_counts = Counter(row["filing_year"] for row in candidate_rows if row["conservative_candidate_flag"] == "yes")
    return "\n".join(
        [
            "# CHECKPOINT 21: Conservative Filing Treatment Candidates V3",
            "",
            "Generated at: 2026-06-29",
            "",
            "## Completed",
            "",
            "- Revised V2 after CHECKPOINT_20 audit failure.",
            "- Added hard exclusions for FHLB/housing boilerplate, CRE property lists, CRA/regulatory-policy background, infrastructure democratization, and broad mission language.",
            "- Built V3 filing-level candidate flags, evidence rows, report, and audit sample.",
            "- Did not fetch prices, compute returns, make SEC requests, modify raw text artifacts, or make empirical performance claims.",
            "",
            "## Files Created",
            "",
            "- `config/conservative_filing_treatment_rules_v3.md`",
            "- `scripts/build_conservative_filing_treatments_v3.py`",
            "- `data/treatments/conservative_filing_treatment_candidates_v3.csv`",
            "- `data/treatments/conservative_filing_treatment_evidence_v3.csv`",
            "- `quality_reports/conservative_filing_treatment_candidates_v3_report.md`",
            "- `data/review/conservative_filing_treatment_v3_audit_sample.csv`",
            "- `quality_reports/conservative_filing_treatment_v3_audit_plan.md`",
            "- `CHECKPOINT_21_CONSERVATIVE_FILING_TREATMENT_CANDIDATES_V3.md`",
            "",
            "## Counts",
            "",
            f"- Filings considered: {len(candidate_rows):,}",
            f"- V3 candidate-positive filings: {yes_count:,}",
            f"- V3 candidate-negative filings: {no_count:,}",
            f"- V3 evidence rows: {len(evidence_rows):,}",
            f"- V3 audit sample rows: {len(audit_rows):,}",
            f"- V3 audit sample positives: {audit_counts.get('yes', 0):,}",
            f"- V3 audit sample negatives: {audit_counts.get('no', 0):,}",
            "",
            "## Candidate Positives By Filing Year",
            "",
            base.markdown_table(["Filing year", "Candidate filings"], [[k, v] for k, v in sorted(year_counts.items())]),
            "",
            "## Evidence By Narrative Subcategory",
            "",
            base.markdown_table(["Narrative subcategory", "Evidence rows"], subcat_counts.most_common()),
            "",
            "## Excluded High-Risk Phrase Families",
            "",
            base.markdown_table(["High-risk phrase family", "Excluded raw-hit rows"], excluded_family_counts.most_common()),
            "",
            "## Integrity",
            "",
            f"- Raw phrase hits unchanged: {'yes' if hashes_before['phrase_hits'] == hashes_after['phrase_hits'] else 'no'}",
            f"- Full-corpus V2 hit labels unchanged: {'yes' if hashes_before['classified_v2'] == hashes_after['classified_v2'] else 'no'}",
            f"- Tiered V1 labels unchanged: {'yes' if hashes_before['tiered_v1'] == hashes_after['tiered_v1'] else 'no'}",
            "",
            "## Next Gate",
            "",
            "Manually audit `data/review/conservative_filing_treatment_v3_audit_sample.csv`. Do not construct final treatment variables or fetch prices until V3 passes the pre-specified precision gate.",
            "",
        ]
    )


base.positive_rule = positive_rule_v3
base.exclusion_reasons = exclusion_reasons_v3
base.build_report = build_report_v3
base.build_audit_plan = build_audit_plan_v3
base.build_checkpoint = build_checkpoint_v3


def main() -> None:
    if not RULES_V3.exists():
        raise FileNotFoundError(RULES_V3)
    if not AUDIT_RESULTS_V2.exists():
        raise FileNotFoundError(AUDIT_RESULTS_V2)
    base.main()


if __name__ == "__main__":
    main()
