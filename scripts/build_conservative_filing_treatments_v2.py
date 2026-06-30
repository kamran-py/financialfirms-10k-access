"""Build V2 conservative filing-level access-expansion candidates.

V2 is a precision-oriented revision after the V1 filing-level audit failed
the conservative treatment gate. It uses only local extracted text artifacts
and the V1 audit lessons. It does not fetch prices, compute returns, make SEC
requests, or create final treatment variables.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

import build_conservative_filing_treatments_v1 as base


ROOT = base.ROOT

base.CANDIDATE_OUT = ROOT / "data" / "treatments" / "conservative_filing_treatment_candidates_v2.csv"
base.EVIDENCE_OUT = ROOT / "data" / "treatments" / "conservative_filing_treatment_evidence_v2.csv"
base.REPORT_OUT = ROOT / "quality_reports" / "conservative_filing_treatment_candidates_v2_report.md"
base.AUDIT_SAMPLE_OUT = ROOT / "data" / "review" / "conservative_filing_treatment_v2_audit_sample.csv"
base.AUDIT_PLAN_OUT = ROOT / "quality_reports" / "conservative_filing_treatment_v2_audit_plan.md"
base.CHECKPOINT_OUT = ROOT / "CHECKPOINT_19_CONSERVATIVE_FILING_TREATMENT_CANDIDATES_V2.md"

AUDIT_RESULTS_V1 = ROOT / "quality_reports" / "conservative_filing_treatment_audit_results_20260629.md"
RULES_V2 = ROOT / "config" / "conservative_filing_treatment_rules_v2.md"


def rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


ISSUER_ACTION = rx(
    r"\b(we|our|us|company|corporation|bank|platform|marketplace|programs?|products?|services?)\b.{0,140}"
    r"\b(provid(?:e|es|ed|ing)|offer(?:s|ed|ing)?|enable(?:s|d|ing)?|serve(?:s|d|ing)?|"
    r"support(?:s|ed|ing)?|expand(?:s|ed|ing)?|increase(?:s|d|ing)?|facilitat(?:e|es|ed|ing)|"
    r"develop(?:s|ed|ing)?|creat(?:e|es|ed|ing)|fund(?:s|ed|ing)?|financ(?:e|es|ed|ing)|"
    r"originat(?:e|es|ed|ing)|make available|democratiz(?:e|es|ed|ing))\b|"
    r"\b(provid(?:e|es|ed|ing)|offer(?:s|ed|ing)?|enable(?:s|d|ing)?|serve(?:s|d|ing)?|"
    r"support(?:s|ed|ing)?|expand(?:s|ed|ing)?|increase(?:s|d|ing)?|facilitat(?:e|es|ed|ing)|"
    r"develop(?:s|ed|ing)?|creat(?:e|es|ed|ing)|fund(?:s|ed|ing)?|financ(?:e|es|ed|ing)|"
    r"originat(?:e|es|ed|ing)|make available|democratiz(?:e|es|ed|ing))\b.{0,140}"
    r"\b(we|our|us|company|corporation|bank|platform|marketplace|programs?|products?|services?)\b"
)

REGULATOR_BOILERPLATE = rx(
    r"\b(CFPB|Consumer Financial Protection Bureau|FIO|Federal Insurance Office|Treasury|"
    r"FHFA|Federal Housing Finance Agency|Federal Reserve|FDIC|OCC)\b.{0,180}"
    r"\b(authori[sz]ed|authority|monitor|promote|request data|track complaints|rulemaking|regulat(?:e|ion|ory))\b"
)
FHLB_BOILERPLATE = rx(
    r"\b(FHLB|Federal Home Loan Bank|Federal Home Loan Banks)\b.{0,180}"
    r"\b(required|required to acquire|required to provide|capital stock|advances?|liquidity|member institutions|"
    r"source of liquidity|affordable housing program)\b|"
    r"\b(required|required to acquire|required to provide|capital stock|advances?|liquidity|member institutions|"
    r"source of liquidity|affordable housing program)\b.{0,180}"
    r"\b(FHLB|Federal Home Loan Bank|Federal Home Loan Banks)\b"
)
AFFORDABLE_HOUSING_ACCOUNTING = rx(
    r"\b(tax[- ]credit|LIHTC|tax advantaged|tax-advantaged|proportional amortization|"
    r"qualified affordable housing projects?|partnership investments?|affordable housing partnerships?|"
    r"investment income|investment securities|portfolio|letters of credit|guarantees?|commitments? table|"
    r"unfunded commitments?|fair value|balance sheets?|in millions|tax benefits?|recover its remaining investments?)\b"
)
FRACTIONAL_OR_SHARE_MECHANICS = rx(
    r"\b(fractional shares?|stock split|reverse split|merger consideration|exchange ratio|cash in lieu|"
    r"convertible notes?|conversion|common stock|preferred stock|dividend|shareholders? equity)\b"
)
ISSUER_FUNDING = rx(
    r"\b(our|we|company|issuer|registrant)\b.{0,90}\b(access to credit|credit facilit(?:y|ies)|"
    r"liquidity|capital resources|funding|borrowings?|debt markets?|credit ratings?)\b|"
    r"\b(access to credit|credit facilit(?:y|ies)|liquidity|capital resources|funding|borrowings?|"
    r"debt markets?|credit ratings?)\b.{0,90}\b(our|we|company|issuer|registrant)\b"
)
GENERIC_MARKET_ACCESS = rx(
    r"\b(direct market access|electronic market access|exchange access|market access trading|"
    r"colocation|connectivity|trading platform|open, direct and anonymous market access|"
    r"access to markets where we do not currently have a local presence|capital market access and sophisticated technology)\b"
)
GENERIC_COMMUNITY = rx(
    r"\b(foundation|donat(?:e|ed|ions?)|charitable|philanthrop(?:y|ic)|grants?|arts|education|"
    r"youth development|health and human services|community leaders|financial literacy)\b"
)
NON_FINANCIAL = rx(
    r"\b(healthcare|health care|patients?|medical|sports|human resources|HR|schools?|education|"
    r"food security|transportation|arts and culture|legislation|Gramm-Leach-Bliley|affiliation among banks)\b"
)
COMPETITOR_OR_RISK_ONLY = rx(
    r"\b(competitors?|competition|may|could|might|risk|risks|adverse|there can be no assurances|"
    r"well-positioned to service|alternative financial services providers who)\b"
)

CREDIT_ACCESS = rx(
    r"\b(access to affordable credit|affordable credit|affordable loans?|expand(?:ed|ing)? access to credit|"
    r"increase access to credit|consumer credit alternatives|provide various credit|one-stop financing solutions|"
    r"access to capital|lacks? the capital)\b"
)
CREDIT_BENEFICIARY = rx(
    r"\b(borrowers?|consumers?|individuals?|small businesses?|small-to-medium sized companies|SMBs?|"
    r"low[- ]and[- ]moderate[- ]income|LMI|financially underserved|underserved consumer|"
    r"underserved by traditional lenders|underserved by traditional financial institutions)\b"
)
BANKING_ACCESS = rx(
    r"\b(underbanked|unbanked|financial inclusion|financially underserved|underserved industries|underserved consumers?)\b"
    r".{0,180}\b(banking services?|financial services?|bank accounts?|deposit|credit|loan|lending|products?|programs?)\b|"
    r"\b(banking services?|financial services?|bank accounts?|deposit|credit|loan|lending|products?|programs?)\b"
    r".{0,180}\b(underbanked|unbanked|financial inclusion|financially underserved|underserved industries|underserved consumers?)\b"
)
PAYMENTS_ACCESS = rx(
    r"\b(democratiz(?:e|es|ed|ing) (?:financial services|access|money movement)|"
    r"democratiz(?:e|es|ed|ing).{0,100}(?:financial services|movement of money|money movement)|"
    r"(?:money transfer|bill payment|remittance|moving money|payment services?|payment platform).{0,140}"
    r"(?:unbanked|underbanked|immigrant workers|consumers?|merchants?|people|businesses)|"
    r"(?:unbanked|underbanked|immigrant workers|consumers?|merchants?|people|businesses).{0,140}"
    r"(?:money transfer|bill payment|remittance|moving money|payment services?|payment platform))\b"
)
INSURANCE_ACCESS = rx(
    r"\b(offer products|target(?:ing)? states|program business|insurance industry that focuses|products? in areas)\b"
    r".{0,180}\b(underserved homeowners insurance markets|underserved markets|middle-income market|"
    r"underserved middle-income|high demand for property insurance|niche, underserved markets)\b|"
    r"\b(underserved homeowners insurance markets|underserved markets|middle-income market|"
    r"underserved middle-income|high demand for property insurance|niche, underserved markets)\b"
    r".{0,180}\b(offer products|target(?:ing)? states|program business|insurance industry that focuses|products? in areas)\b"
)
HOUSING_DIRECT = rx(
    r"\b(supply funds|provide funds|funds for the construction|construction and operation|construction financing|"
    r"permanent loans|provide construction and permanent loans|financing affordable housing|"
    r"loans? to developers|loans? to owners|mortgage loans?)\b.{0,180}"
    r"\b(affordable housing|low-income housing|lower family income|low[- ]and[- ]moderate[- ]income|"
    r"affordable homeownership|homeowners?|residents?|renters?)\b|"
    r"\b(affordable housing|low-income housing|lower family income|low[- ]and[- ]moderate[- ]income|"
    r"affordable homeownership|homeowners?|residents?|renters?)\b.{0,180}"
    r"\b(supply funds|provide funds|funds for the construction|construction and operation|construction financing|"
    r"permanent loans|provide construction and permanent loans|financing affordable housing|"
    r"loans? to developers|loans? to owners|mortgage loans?)\b"
)
PUBLIC_MARKET_ACCESS = rx(
    r"\b(mission is to deliver market access|deliver market access|substantial interest cost savings)\b"
    r".{0,180}\b(issuers?|municipal bonds?|public purposes?|schools|utilities|governmental functions|transportation)\b|"
    r"\b(issuers?|municipal bonds?|public purposes?|schools|utilities|governmental functions|transportation)\b"
    r".{0,180}\b(mission is to deliver market access|deliver market access|substantial interest cost savings)\b"
)


def text_for(row: dict[str, str]) -> tuple[str, str, str, str]:
    text = base.normalize(row.get("excerpt"))
    phrase = base.normalize(row.get("phrase")).lower()
    category = base.normalize(row.get("category")).lower()
    section = base.normalize(row.get("section_name")).lower()
    return text, phrase, category, section


def has_issuer_action(text: str) -> bool:
    return bool(ISSUER_ACTION.search(text))


def hard_exclusion_reasons(row: dict[str, str]) -> list[str]:
    text, phrase, _category, section = text_for(row)
    reasons: list[str] = []
    if FRACTIONAL_OR_SHARE_MECHANICS.search(text) or "fractional share" in phrase:
        reasons.append("fractional-share/share-mechanics context")
    if ISSUER_FUNDING.search(text):
        reasons.append("issuer liquidity/funding/access-to-credit context")
    if FHLB_BOILERPLATE.search(text):
        reasons.append("FHLB membership/liquidity/required-program boilerplate")
    if ("affordable housing" in phrase or "housing" in phrase) and AFFORDABLE_HOUSING_ACCOUNTING.search(text):
        reasons.append("affordable-housing accounting/tax-credit/investment-book context")
    if REGULATOR_BOILERPLATE.search(text) and not has_issuer_action(text):
        reasons.append("regulator/agency boilerplate without issuer access action")
    if GENERIC_MARKET_ACCESS.search(text):
        reasons.append("generic trading/infrastructure/geographic market-access context")
    if GENERIC_COMMUNITY.search(text) and not (HOUSING_DIRECT.search(text) or CREDIT_ACCESS.search(text)):
        reasons.append("generic philanthropy/community context")
    if NON_FINANCIAL.search(text) and not (CREDIT_ACCESS.search(text) or PAYMENTS_ACCESS.search(text)):
        reasons.append("non-financial access or barriers context")
    if "risk factors" in section and COMPETITOR_OR_RISK_ONLY.search(text) and not (
        CREDIT_ACCESS.search(text) and CREDIT_BENEFICIARY.search(text) and has_issuer_action(text)
    ):
        reasons.append("risk-only or competitor-access context")
    return sorted(set(reasons))


def exclusion_reasons_v2(row: dict[str, str]) -> list[str]:
    reasons = hard_exclusion_reasons(row)
    if reasons:
        return reasons
    text, phrase, _category, _section = text_for(row)
    if ("market access" in phrase or "access to markets" in phrase or "capital markets access" in phrase) and not PUBLIC_MARKET_ACCESS.search(text):
        reasons.append("market-access language lacks public-purpose/smaller-issuer beneficiary")
    if ("institutional" in phrase or "retail investors" in phrase or "individual investors" in phrase) and not (
        "democratiz" in text.lower() or PUBLIC_MARKET_ACCESS.search(text)
    ):
        reasons.append("retail/institutional-investor language is broader-sensitivity only")
    if not reasons:
        reasons.append("no V2 conservative positive rule satisfied")
    return sorted(set(reasons))


def positive_rule_v2(row: dict[str, str]) -> tuple[bool, str, str, str]:
    text, phrase, _category, _section = text_for(row)
    hard_reasons = hard_exclusion_reasons(row)
    if hard_reasons:
        return False, "", "", "; ".join(hard_reasons)

    issuer_action = has_issuer_action(text)

    if CREDIT_ACCESS.search(text) and CREDIT_BENEFICIARY.search(text) and issuer_action:
        return True, "V2 direct credit access with issuer action", "consumer credit access", (
            "Issuer action ties credit/lending/financing access to borrowers, consumers, small businesses, or underserved users."
        )

    if BANKING_ACCESS.search(text) and issuer_action:
        return True, "V2 financial inclusion or banking access with issuer action", (
            "financial inclusion / underbanked / underserved"
        ), "Issuer action ties banking/financial services to underbanked, unbanked, underserved, or financially excluded users."

    if PAYMENTS_ACCESS.search(text) and issuer_action:
        return True, "V2 payments or money-movement access", "payments / money movement / SMB commerce access", (
            "Issuer action ties payments, money movement, remittance, or democratized financial services to external users."
        )

    if INSURANCE_ACCESS.search(text) and issuer_action:
        return True, "V2 insurance access for underserved beneficiaries", "insurance / benefits access", (
            "Issuer action ties insurance products/programs to underserved or middle-income insurance beneficiaries."
        )

    if HOUSING_DIRECT.search(text) and not AFFORDABLE_HOUSING_ACCOUNTING.search(text):
        return True, "V2 direct affordable-housing or homeownership finance", (
            "affordable housing / homeownership access"
        ), "Evidence describes direct financing/funding/construction/operation support for affordable housing or lower-income housing beneficiaries."

    if PUBLIC_MARKET_ACCESS.search(text):
        return True, "V2 public-purpose or smaller-issuer capital-market access", (
            "smaller-issuer capital-market access"
        ), "Evidence explicitly delivers market access or financing-cost savings to public-purpose or municipal issuers."

    return False, "", "", "; ".join(exclusion_reasons_v2(row))


def build_report_v2(
    candidate_rows: list[dict[str, str]],
    evidence_rows: list[dict[str, str]],
    excluded_family_counts: Counter[str],
    evidence_by_filing: dict[tuple[str, ...], list[dict[str, str]]],
    hits_by_filing: dict[tuple[str, ...], list[dict[str, str]]],
    input_hashes: dict[str, str],
) -> str:
    yes_rows = [row for row in candidate_rows if row["conservative_candidate_flag"] == "yes"]
    no_rows = [row for row in candidate_rows if row["conservative_candidate_flag"] == "no"]
    year_counts = Counter(row["filing_year"] for row in yes_rows)
    subcat_counts = Counter(row["narrative_subcategory"] for row in evidence_rows)
    section_counts = Counter(row["section_name"] for row in evidence_rows)
    phrase_counts = Counter(row["phrase"] for row in evidence_rows)
    firm_counts = Counter(f"{row['ticker']} ({row['firm_id']})" for row in yes_rows)

    evidence_examples = sorted(evidence_rows, key=lambda r: (r["narrative_subcategory"], r["filing_year"], r["ticker"]))[:30]
    excluded_examples = []
    for row in no_rows:
        if row["exclusion_or_no_candidate_reason"] == "no_raw_phrase_hits_in_extracted_sections":
            continue
        key = tuple(row[field] for field in base.FILING_KEY)
        excluded_examples.append(
            [
                row["ticker"],
                row["filing_year"],
                row["exclusion_or_no_candidate_reason"],
                base.compact(base.make_representative_excerpt(key, evidence_by_filing, hits_by_filing), 220),
            ]
        )
        if len(excluded_examples) >= 25:
            break

    lines = [
        "# Conservative Filing Treatment Candidates V2 Report",
        "",
        "Generated by `scripts/build_conservative_filing_treatments_v2.py`.",
        "",
        "## Guardrails",
        "",
        "- These are revised filing-level candidates only, not final treatment variables.",
        "- V2 uses the CHECKPOINT_18 audit lessons to prioritize precision over recall.",
        "- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.",
        "- Raw `data/extracted/phrase_hits.csv`, full-corpus V2 hit labels, tiered V1 labels, and V1 candidate files were not modified.",
        "",
        "## Inputs",
        "",
        "- `config/conservative_filing_treatment_rules_v2.md`",
        "- `quality_reports/conservative_filing_treatment_audit_results_20260629.md`",
        "- `data/extracted/phrase_hits.csv`",
        "- `data/extracted/filing_sections.csv`",
        "",
        "## Input Integrity",
        "",
        f"- Raw phrase hits SHA256 before build: `{input_hashes['phrase_hits']}`",
        f"- Full-corpus V2 hit classification SHA256 before build: `{input_hashes['classified_v2']}`",
        f"- Tiered V1 hit classification SHA256 before build: `{input_hashes['tiered_v1']}`",
        "",
        "## Summary Counts",
        "",
        f"- Total filings considered: {len(candidate_rows):,}",
        f"- V2 candidate-positive filings: {len(yes_rows):,}",
        f"- V2 candidate-negative filings: {len(no_rows):,}",
        f"- V2 candidate evidence rows: {len(evidence_rows):,}",
        "",
        "## Candidate Count By Filing Year",
        "",
        base.markdown_table(["Filing year", "Candidate filings"], [[k, v] for k, v in sorted(year_counts.items())]),
        "",
        "## Evidence Rows By Narrative Subcategory",
        "",
        base.markdown_table(["Narrative subcategory", "Evidence rows"], subcat_counts.most_common()),
        "",
        "## Evidence Rows By Section",
        "",
        base.markdown_table(["Section", "Evidence rows"], section_counts.most_common()),
        "",
        "## Top Evidence Phrases",
        "",
        base.markdown_table(["Phrase", "Evidence rows"], phrase_counts.most_common(25)),
        "",
        "## Top Firms By Candidate Filings",
        "",
        base.markdown_table(["Firm", "Candidate filings"], firm_counts.most_common(25)),
        "",
        "## Excluded High-Risk Phrase Families",
        "",
        base.markdown_table(["High-risk phrase family", "Excluded raw-hit rows"], excluded_family_counts.most_common()),
        "",
        "## Candidate Evidence Examples",
        "",
        base.markdown_table(
            ["Ticker", "Year", "Section", "Phrase", "Rule", "Subcategory", "Excerpt"],
            [
                [
                    ev["ticker"],
                    ev["filing_year"],
                    ev["section_name"],
                    ev["phrase"],
                    ev["evidence_rule"],
                    ev["narrative_subcategory"],
                    base.compact(ev["excerpt"], 180),
                ]
                for ev in evidence_examples
            ],
        ),
        "",
        "## Excluded / No-Candidate Examples",
        "",
        base.markdown_table(["Ticker", "Year", "Reason", "Representative excerpt"], excluded_examples),
        "",
        "## Decision",
        "",
        "V2 candidate flags are not final treatment variables. They require a fresh manual audit before any return-window construction, benchmark loading, or empirical analysis.",
        "",
    ]
    return "\n".join(lines)


def build_audit_plan_v2(audit_rows: list[dict[str, str]], candidate_rows: list[dict[str, str]]) -> str:
    sample_counts = Counter(row["conservative_candidate_flag"] for row in audit_rows)
    year_counts = Counter(row["filing_year"] for row in audit_rows)
    subcat_counts = Counter(row["narrative_subcategories_present"] or row["exclusion_or_no_candidate_reason"] for row in audit_rows)
    candidate_yes = sum(1 for row in candidate_rows if row["conservative_candidate_flag"] == "yes")

    return "\n".join(
        [
            "# Conservative Filing Treatment V2 Audit Plan",
            "",
            "## Purpose",
            "",
            "This plan defines the next validation gate for V2 filing-level conservative candidates. The audit tests construct validity only and must not inspect prices, returns, benchmarks, news, or future outcomes.",
            "",
            "## Sample Design",
            "",
            f"- Total sampled filings: {len(audit_rows):,}",
            f"- Candidate-positive sampled filings: {sample_counts.get('yes', 0):,}",
            f"- Candidate-negative sampled filings: {sample_counts.get('no', 0):,}",
            f"- Full V2 candidate-positive universe: {candidate_yes:,}",
            "- The sample is deterministic and stratified across filing years, narrative subcategories or no-candidate reasons, sections, and firms.",
            "",
            "## Audit Labels",
            "",
            "- `yes_conservative_treatment`: excerpt satisfies external beneficiary, direct financial-access mechanism, and issuer attribution.",
            "- `no_not_conservative_treatment`: excerpt fails the conservative standard.",
            "- `borderline_broader_treatment_only`: access-related but not strict enough for the conservative main treatment.",
            "",
            "## Validation Gate",
            "",
            "- Candidate-positive precision must be at least 90% before V2 candidates can become conservative treatment variables.",
            "- Candidate-negative false negatives should be documented and preferably remain below 15-20%.",
            "- Borderline rows do not count as conservative positives.",
            "",
            "## Sample Count By Candidate Flag",
            "",
            base.markdown_table(["Candidate flag", "Sampled filings"], sample_counts.most_common()),
            "",
            "## Sample Count By Filing Year",
            "",
            base.markdown_table(["Filing year", "Sampled filings"], [[k, v] for k, v in sorted(year_counts.items())]),
            "",
            "## Sample Count By Subcategory Or Reason",
            "",
            base.markdown_table(["Subcategory or reason", "Sampled filings"], subcat_counts.most_common(30)),
            "",
            "No prices, returns, SEC requests, or empirical claims are part of this audit.",
            "",
        ]
    )


def build_checkpoint_v2(
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
            "# CHECKPOINT 19: Conservative Filing Treatment Candidates V2",
            "",
            "Generated at: 2026-06-29",
            "",
            "## Completed",
            "",
            "- Revised filing-level candidate construction after the CHECKPOINT_18 audit failure.",
            "- Encoded stricter exclusions for FHLB boilerplate, regulator/agency language, generic market access, affordable-housing accounting, and broader-only retail/institutional investor language.",
            "- Built V2 filing-level candidate flags and evidence rows from local extracted text.",
            "- Prepared a fresh V2 audit sample and audit plan.",
            "- Did not fetch prices, compute returns, make SEC requests, modify raw text artifacts, or make empirical performance claims.",
            "",
            "## Files Created",
            "",
            "- `config/conservative_filing_treatment_rules_v2.md`",
            "- `scripts/build_conservative_filing_treatments_v2.py`",
            "- `data/treatments/conservative_filing_treatment_candidates_v2.csv`",
            "- `data/treatments/conservative_filing_treatment_evidence_v2.csv`",
            "- `quality_reports/conservative_filing_treatment_candidates_v2_report.md`",
            "- `data/review/conservative_filing_treatment_v2_audit_sample.csv`",
            "- `quality_reports/conservative_filing_treatment_v2_audit_plan.md`",
            "- `CHECKPOINT_19_CONSERVATIVE_FILING_TREATMENT_CANDIDATES_V2.md`",
            "",
            "## Counts",
            "",
            f"- Filings considered: {len(candidate_rows):,}",
            f"- V2 candidate-positive filings: {yes_count:,}",
            f"- V2 candidate-negative filings: {no_count:,}",
            f"- V2 evidence rows: {len(evidence_rows):,}",
            f"- V2 audit sample rows: {len(audit_rows):,}",
            f"- V2 audit sample positives: {audit_counts.get('yes', 0):,}",
            f"- V2 audit sample negatives: {audit_counts.get('no', 0):,}",
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
            f"- Raw `data/extracted/phrase_hits.csv` SHA256 before: `{hashes_before['phrase_hits']}`",
            f"- Raw `data/extracted/phrase_hits.csv` SHA256 after: `{hashes_after['phrase_hits']}`",
            f"- Raw phrase hits unchanged: {'yes' if hashes_before['phrase_hits'] == hashes_after['phrase_hits'] else 'no'}",
            f"- Full-corpus V2 hit labels unchanged: {'yes' if hashes_before['classified_v2'] == hashes_after['classified_v2'] else 'no'}",
            f"- Tiered V1 labels unchanged: {'yes' if hashes_before['tiered_v1'] == hashes_after['tiered_v1'] else 'no'}",
            "",
            "## Next Gate",
            "",
            "Manually audit `data/review/conservative_filing_treatment_v2_audit_sample.csv`. Do not construct final treatment variables or fetch prices until the V2 audit passes the pre-specified precision gate.",
            "",
        ]
    )


base.positive_rule = positive_rule_v2
base.exclusion_reasons = exclusion_reasons_v2
base.build_report = build_report_v2
base.build_audit_plan = build_audit_plan_v2
base.build_checkpoint = build_checkpoint_v2


def main() -> None:
    if not RULES_V2.exists():
        raise FileNotFoundError(RULES_V2)
    if not AUDIT_RESULTS_V1.exists():
        raise FileNotFoundError(AUDIT_RESULTS_V1)
    base.main()


if __name__ == "__main__":
    main()
