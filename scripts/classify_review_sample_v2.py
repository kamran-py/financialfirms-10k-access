#!/usr/bin/env python3
"""
Reclassify the 600-row review sample using v3 guidance and audit labels.

This script is text-treatment validation only. It does not fetch prices, run
return analysis, make SEC requests, scale classification to all raw hits, or
modify data/extracted/phrase_hits.csv.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLASSIFIED_V1_PATH = PROJECT_ROOT / "data" / "review" / "phrase_hit_review_sample_classified_v1.csv"
MANUAL_LABELS_PATH = PROJECT_ROOT / "data" / "review" / "manual_calibration_labels_20260629.csv"
AUDIT_LABELS_PATH = PROJECT_ROOT / "data" / "review" / "codex_assisted_label_audit_sample_audited_20260629.csv"
CLASSIFIED_V2_PATH = PROJECT_ROOT / "data" / "review" / "phrase_hit_review_sample_classified_v2.csv"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "review_sample_classification_v2_report.md"
RAW_PHRASE_HITS_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"
GUIDELINES_V3_PATH = PROJECT_ROOT / "config" / "classification_guidelines_v3.md"

SCRIPT_VERSION = "classify_review_sample_v2"

ALLOWED_LABELS = {
    "true_positive_access_expansion",
    "generic_marketing",
    "risk_disclosure_only",
    "customer_access_unrelated_to_finance",
    "operational_access_or_platform_language",
    "ambiguous",
    "false_positive",
}

V2_FIELDS = [
    "final_label_v2",
    "final_confidence_v2",
    "label_source_v2",
    "codex_assisted_label_v2",
    "codex_assisted_confidence_v2",
    "codex_assisted_notes_v2",
]


@dataclass(frozen=True)
class Decision:
    label: str
    confidence: str
    notes: str


def field_size_limit() -> None:
    csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def read_csv_with_fields(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_label(label: str, context: str) -> None:
    if label not in ALLOWED_LABELS:
        raise ValueError(f"invalid label in {context}: {label!r}")


def normalize(row: dict[str, str]) -> str:
    return re.sub(
        r"\s+",
        " ",
        " ".join(
            [
                row.get("phrase", ""),
                row.get("category", ""),
                row.get("section_name", ""),
                row.get("matched_text", ""),
                row.get("excerpt", ""),
            ]
        ).lower(),
    ).strip()


def has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def beneficiary(text: str) -> bool:
    return has_any(
        text,
        [
            "consumer",
            "consumers",
            "customer",
            "customers",
            "member",
            "members",
            "borrower",
            "borrowers",
            "investor",
            "investors",
            "retail",
            "individual",
            "individuals",
            "underserved",
            "underbanked",
            "unbanked",
            "low- and moderate-income",
            "low and moderate income",
            "lmi",
            "community",
            "communities",
            "small business",
            "small businesses",
            "smb",
            "smbs",
            "merchant",
            "merchants",
            "homeowner",
            "homeowners",
            "homebuyer",
            "homebuyers",
            "renters",
            "residents",
            "families",
            "households",
            "clients",
            "users",
            "smaller issuers",
            "emerging companies",
        ],
    )


def mechanism(text: str) -> bool:
    return has_any(
        text,
        [
            "credit",
            "loan",
            "loans",
            "lending",
            "mortgage",
            "mortgages",
            "banking",
            "bank",
            "financial services",
            "financial products",
            "payments",
            "payment",
            "money movement",
            "commerce",
            "investment",
            "investing",
            "brokerage",
            "capital markets",
            "markets",
            "homeownership",
            "housing",
            "insurance",
            "savings",
            "wealth",
            "affordable",
            "low-cost",
            "low cost",
            "finance",
            "financing",
        ],
    )


def explicit_positive(text: str) -> bool:
    return has_any(
        text,
        [
            "expand access",
            "expanded access",
            "expanding access",
            "broaden access",
            "broader access",
            "democratize",
            "democratizing",
            "democratized",
            "lower barriers",
            "lowering barriers",
            "reduce barriers",
            "remove barriers",
            "financial inclusion",
            "inclusive finance",
            "access to affordable",
            "provide access",
            "provides access",
            "providing access",
            "make available",
            "available to retail",
            "available to individual",
            "serve underserved",
            "serving underserved",
            "reach underserved",
            "empower small businesses",
            "small businesses access",
        ],
    )


def risk_context(text: str, section: str) -> bool:
    return "risk" in section or has_any(
        text,
        [
            "could adversely",
            "would adversely",
            "may adversely",
            "adverse effect",
            "material adverse",
            "unable to access",
            "inability to access",
            "loss of access",
            "deterioration",
            "market volatility",
            "liquidity",
            "funding",
            "capital resources",
            "debt markets",
            "credit markets",
            "our ability to access",
            "ability to access capital",
            "access to capital",
            "access to credit markets",
            "access to financing",
            "access to funding",
            "economic conditions",
        ],
    )


def accounting_or_table(text: str) -> bool:
    return has_any(
        text,
        [
            "tax credit",
            "low income housing tax credit",
            "limited partnership",
            "partnership investment",
            "equity investment",
            "investment income",
            "community development investment",
            "portfolio",
            "commitments table",
            "table",
            "fair value",
            "amortized cost",
            "accounting",
            "asset quality",
            "carrying value",
            "tax benefits",
            "unfunded commitments",
            "cra commitments",
        ],
    )


def non_financial_context(text: str) -> bool:
    return has_any(
        text,
        [
            "healthcare",
            "health care",
            "patient",
            "patients",
            "sports",
            "stadium",
            "education",
            "hr",
            "human resources",
            "employee inclusion",
            "employees",
            "ai innovation",
            "artificial intelligence",
            "internal inclusion",
            "website access",
            "data access",
        ],
    )


def classify(row: dict[str, str]) -> Decision:
    phrase = row.get("phrase", "").strip().lower()
    category = row.get("category", "").strip().lower()
    section = row.get("section_name", "").strip().lower()
    text = normalize(row)
    has_beneficiary = beneficiary(text)
    has_mechanism = mechanism(text)
    positive = explicit_positive(text)
    risky = risk_context(text, section)

    if non_financial_context(text) and not has_any(text, ["financial", "credit", "loan", "bank", "payments", "invest"]):
        return Decision("customer_access_unrelated_to_finance", "high", "Non-financial ESG, HR, healthcare, sports, AI, internal, website, or data-access context.")

    if has_beneficiary and has_mechanism and positive:
        explicit_note = "External beneficiary plus financial-access mechanism and explicit access/mission wording."
    else:
        explicit_note = ""

    if phrase == "fractional share":
        if has_any(text, ["fractional investing", "fractional investment", "fractional shares through", "buy fractional", "invest in fractional"]) and has_beneficiary:
            return Decision("true_positive_access_expansion", "medium", "Fractional-share wording clearly concerns fractional investing access.")
        return Decision("false_positive", "high", "Fractional-share wording defaults to stock, merger, issuance, conversion, exchange-ratio, or cash-in-lieu mechanics.")

    if phrase == "affordable housing" or "affordable housing" in phrase:
        if accounting_or_table(text) and not has_any(text, ["homeowner", "homebuyer", "renters", "residents", "mortgage access", "housing access"]):
            return Decision("false_positive", "high", "Affordable-housing wording appears in tax-credit, partnership, portfolio, investment-income, commitment-table, or accounting context.")
        if has_beneficiary and has_any(text, ["housing finance", "mortgage", "homeownership", "renters", "residents", "community housing", "housing access", "loan", "lending"]):
            return Decision("true_positive_access_expansion", "medium", "Affordable-housing wording is tied to housing finance, mortgage, homeownership, residents, or community access.")
        return Decision("false_positive", "medium", "Affordable-housing wording lacks clear housing-finance or external access mechanism.")

    institutional_family = {
        "institutional caliber",
        "institutional quality",
        "institutional level",
        "institutional-grade",
        "institutional grade",
        "institutional-level",
    }
    if phrase in institutional_family:
        if has_beneficiary and has_mechanism and has_any(text, ["access", "available", "retail", "individual", "consumer", "small business", "underserved"]):
            return Decision("true_positive_access_expansion", "medium", "Institutional-quality capability is explicitly made available to external users.")
        if has_any(text, ["api", "platform", "custodian", "analytics", "advisor", "analyst", "process", "infrastructure", "security", "technology", "property", "real estate", "portfolio", "quality"]):
            return Decision("operational_access_or_platform_language", "high", "Institutional-quality wording describes platform, API, custodian, analyst, advisor analytics, property, or internal quality.")
        return Decision("false_positive", "high", "Institutional-quality wording lacks external access mechanism.")

    if phrase in {"market access", "access to markets", "capital markets access"}:
        if has_beneficiary and has_mechanism and has_any(text, ["smaller issuers", "customers", "investors", "borrowers", "communities", "small businesses", "access to capital markets for"]):
            return Decision("true_positive_access_expansion", "medium", "Market-access wording identifies external beneficiaries gaining financial-market access.")
        if risky:
            return Decision("risk_disclosure_only", "high", "Market-access wording defaults to risk/issuer-financing context without external beneficiary.")
        return Decision("operational_access_or_platform_language", "high", "Market-access wording defaults to operational, regulatory, competitive, distribution, or infrastructure context.")

    credit_phrases = {
        "access to credit",
        "credit access",
        "affordable credit",
        "access to affordable credit",
        "expand access to credit",
        "expanded access to credit",
        "expanding access to credit",
        "broaden access to credit",
        "broader access to credit",
    }
    if phrase in credit_phrases:
        if risky and not has_beneficiary:
            return Decision("risk_disclosure_only", "high", "Credit-access wording in risk/liquidity context defaults to issuer risk.")
        if has_beneficiary and has_any(text, ["credit", "loan", "lending", "borrower", "borrowers", "customers", "members", "lmi", "underserved", "small business"]):
            return Decision("true_positive_access_expansion", "high" if positive else "medium", "Credit-access wording identifies external borrowers, consumers, members, customers, LMI communities, underserved groups, or small businesses.")
        if risky:
            return Decision("risk_disclosure_only", "medium", "Credit-access wording appears in a risk section without clear external beneficiary.")
        return Decision("ambiguous", "low", "Credit-access wording lacks clear beneficiary.")

    if has_any(text, ["community reinvestment act", "cra", "regulatory", "agency", "agencies", "compliance"]):
        if has_beneficiary and has_mechanism and has_any(text, ["lend", "lending", "credit", "banking", "investment", "housing", "low- and moderate-income", "lmi", "underserved"]):
            return Decision("true_positive_access_expansion", "medium", "CRA/regulatory wording substantively describes financial access for LMI, underserved, or external communities.")
        return Decision("operational_access_or_platform_language", "medium", "CRA/regulatory wording is compliance background, agency authority, or obligation language without external access mechanism.")

    if category == "underserved / underbanked / unbanked":
        if has_mechanism:
            return Decision("true_positive_access_expansion", "high", "Underserved, underbanked, or unbanked wording appears in financial-services context.")
        if non_financial_context(text):
            return Decision("customer_access_unrelated_to_finance", "high", "Underserved wording appears outside financial access.")
        return Decision("ambiguous", "medium", "Underserved wording lacks clear financial-access mechanism.")

    if category == "financial inclusion":
        if has_mechanism or positive:
            return Decision("true_positive_access_expansion", "medium", "Financial-inclusion wording is tied to financial access.")
        return Decision("generic_marketing", "medium", "Financial-inclusion wording lacks specific beneficiary/mechanism.")

    if category == "democratized access":
        if has_beneficiary and has_mechanism:
            return Decision("true_positive_access_expansion", "high" if positive else "medium", explicit_note or "Democratized wording includes external beneficiary and financial mechanism.")
        if has_mechanism and has_any(text, ["mission", "customers", "small businesses", "payments", "money movement", "commerce"]):
            return Decision("true_positive_access_expansion", "medium", "Explicit financial-access mission language with sufficient external orientation.")
        return Decision("generic_marketing", "medium", "Democratized wording lacks beneficiary or mechanism.")

    if category == "retail access to investing":
        if phrase in {"retail investors", "individual investors"}:
            if has_any(text, ["available to", "access", "offering", "platform", "product", "minimum", "fractional", "democrat", "expand"]) and has_mechanism:
                return Decision("true_positive_access_expansion", "medium", "Retail/individual investor wording is tied to investment access or availability.")
            return Decision("false_positive", "medium", "Retail/individual investor wording appears generic or investor-relations related.")
        if has_beneficiary and has_mechanism:
            return Decision("true_positive_access_expansion", "medium", "Investing-access wording identifies external investor beneficiaries.")
        return Decision("ambiguous", "low", "Investing-access wording lacks clear access mechanism.")

    if category == "homeownership access":
        if accounting_or_table(text) and not has_any(text, ["homeowner", "homebuyer", "renters", "residents", "mortgage", "housing access"]):
            return Decision("false_positive", "medium", "Housing wording appears in investment, accounting, tax-credit, portfolio, or commitments context.")
        if has_beneficiary and has_any(text, ["homeownership", "housing", "mortgage", "loan", "lending", "residents", "renters", "community"]):
            return Decision("true_positive_access_expansion", "medium", "Housing wording is tied to external housing, lending, homeownership, resident, or community access.")
        return Decision("ambiguous", "low", "Housing wording lacks beneficiary/mechanism detail.")

    if category == "affordable financial products":
        if has_beneficiary and has_mechanism:
            return Decision("true_positive_access_expansion", "medium", "Affordable or low-cost financial-services wording identifies external beneficiary and mechanism.")
        if has_mechanism and has_any(text, ["affordable credit", "affordable loans", "low-cost financial services", "low cost financial services"]):
            return Decision("true_positive_access_expansion", "medium", "Explicit affordable/low-cost financial-access language.")
        return Decision("generic_marketing", "medium", "Affordability wording lacks specific external beneficiary.")

    if category == "lower barriers / level playing field":
        if has_beneficiary and has_mechanism:
            return Decision("true_positive_access_expansion", "medium", "Barrier-reduction wording includes beneficiary and financial mechanism.")
        if has_any(text, ["competition", "competitors", "regulatory", "operations", "technology", "platform", "employee", "sports", "ai"]):
            return Decision("operational_access_or_platform_language", "medium", "Barrier or level-playing-field wording is operational, competitive, regulatory, or non-financial.")
        return Decision("generic_marketing", "medium", "Barrier-reduction wording lacks financial beneficiary.")

    if category == "broader market participation":
        if has_beneficiary and has_mechanism and positive:
            return Decision("true_positive_access_expansion", "medium", "Market-participation wording identifies external financial beneficiaries.")
        if risky:
            return Decision("risk_disclosure_only", "medium", "Market wording appears in risk or issuer-financing context.")
        return Decision("operational_access_or_platform_language", "medium", "Market wording appears operational or generic without beneficiary.")

    if has_beneficiary and has_mechanism and positive:
        return Decision("true_positive_access_expansion", "medium", explicit_note)
    if risky and not has_beneficiary:
        return Decision("risk_disclosure_only", "medium", "Risk or issuer-financing context without external beneficiary.")
    if has_beneficiary and not has_mechanism:
        return Decision("customer_access_unrelated_to_finance", "medium", "Beneficiary/access context lacks financial-access mechanism.")
    return Decision("ambiguous", "low", "Insufficient context for a more specific label.")


def load_manual(path: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        hit_id = row.get("hit_id", "").strip()
        label = row.get("human_label", "").strip()
        validate_label(label, f"manual calibration hit_id {hit_id}")
        out[hit_id] = {
            "label": label,
            "confidence": row.get("confidence", "").strip(),
            "notes": row.get("reviewer_notes", ""),
        }
    return out


def load_audit(path: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        hit_id = row.get("hit_id", "").strip()
        label = row.get("audit_label", "").strip()
        validate_label(label, f"manual audit hit_id {hit_id}")
        out[hit_id] = {
            "label": label,
            "confidence": row.get("audit_confidence", "").strip(),
            "notes": row.get("audit_notes", ""),
        }
    return out


def reclassify(rows: list[dict[str, str]], manual: dict[str, dict[str, str]], audit: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    sample_ids = {row.get("hit_id", "") for row in rows}
    missing_manual = sorted(set(manual) - sample_ids, key=int)
    missing_audit = sorted(set(audit) - sample_ids, key=int)
    if missing_manual:
        raise ValueError(f"manual calibration hit_ids not in sample: {missing_manual[:10]}")
    if missing_audit:
        raise ValueError(f"manual audit hit_ids not in sample: {missing_audit[:10]}")

    output: list[dict[str, str]] = []
    for row in rows:
        item = dict(row)
        hit_id = item.get("hit_id", "")
        for field in V2_FIELDS:
            item[field] = ""
        if hit_id in manual:
            item["final_label_v2"] = manual[hit_id]["label"]
            item["final_confidence_v2"] = manual[hit_id]["confidence"]
            item["label_source_v2"] = "manual_calibration"
        elif hit_id in audit:
            item["final_label_v2"] = audit[hit_id]["label"]
            item["final_confidence_v2"] = audit[hit_id]["confidence"]
            item["label_source_v2"] = "manual_audit"
        else:
            decision = classify(item)
            validate_label(decision.label, f"codex v2 hit_id {hit_id}")
            item["codex_assisted_label_v2"] = decision.label
            item["codex_assisted_confidence_v2"] = decision.confidence
            item["codex_assisted_notes_v2"] = decision.notes
            item["final_label_v2"] = decision.label
            item["final_confidence_v2"] = decision.confidence
            item["label_source_v2"] = "codex_assisted_v2"
        output.append(item)
    return output


def counter_by(rows: list[dict[str, str]], *fields: str) -> Counter[tuple[str, ...]]:
    return Counter(tuple(row.get(field, "") for field in fields) for row in rows)


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return lines


def label_rows(counter: Counter[str]) -> list[list[str]]:
    return [[label, str(counter.get(label, 0))] for label in sorted(ALLOWED_LABELS)]


def true_positive_rate_by_category(rows: list[dict[str, str]]) -> list[list[str]]:
    by_cat: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        by_cat[row.get("category", "")][row.get("final_label_v2", "")] += 1
    out: list[list[str]] = []
    for category in sorted(by_cat):
        total = sum(by_cat[category].values())
        tp = by_cat[category]["true_positive_access_expansion"]
        out.append([category, str(total), str(tp), f"{tp / total:.1%}" if total else "0.0%"])
    return out


def changes_by(rows: list[dict[str, str]], field: str) -> list[list[str]]:
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        if row.get("final_label") != row.get("final_label_v2"):
            counts[row.get(field, "")][f"{row.get('final_label')} -> {row.get('final_label_v2')}"] += 1
    out: list[list[str]] = []
    for key in sorted(counts):
        total = sum(counts[key].values())
        top = "; ".join(f"{transition}: {count}" for transition, count in counts[key].most_common(5))
        out.append([key or "(blank)", str(total), top])
    return sorted(out, key=lambda row: (-int(row[1]), row[0]))


def high_risk_phrases(rows: list[dict[str, str]]) -> list[list[str]]:
    risk_phrases = {
        "institutional caliber",
        "institutional quality",
        "institutional level",
        "institutional-grade",
        "institutional grade",
        "market access",
        "access to markets",
        "capital markets access",
        "fractional share",
        "affordable housing",
        "access to credit",
    }
    by_phrase: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        phrase = row.get("phrase", "")
        if phrase in risk_phrases:
            by_phrase[phrase][row.get("final_label_v2", "")] += 1
    out: list[list[str]] = []
    for phrase in sorted(by_phrase):
        total = sum(by_phrase[phrase].values())
        tp = by_phrase[phrase]["true_positive_access_expansion"]
        out.append([phrase, str(total), str(tp), f"{tp / total:.1%}" if total else "0.0%", dict(by_phrase[phrase])])
    return out


def write_report(rows: list[dict[str, str]], manual: dict[str, dict[str, str]], audit: dict[str, dict[str, str]], raw_before: str, raw_after: str) -> None:
    v1_counts = Counter(row.get("final_label", "") for row in rows)
    v2_counts = Counter(row.get("final_label_v2", "") for row in rows)
    source_counts = Counter(row.get("label_source_v2", "") for row in rows)
    changed = [row for row in rows if row.get("final_label") != row.get("final_label_v2")]
    inst_market_rows = [
        row for row in rows if row.get("phrase", "") in {
            "institutional caliber",
            "institutional quality",
            "institutional level",
            "institutional-grade",
            "institutional grade",
            "market access",
            "access to markets",
            "capital markets access",
        }
    ]
    inst_market_v1_tp = sum(1 for row in inst_market_rows if row.get("final_label") == "true_positive_access_expansion")
    inst_market_v2_tp = sum(1 for row in inst_market_rows if row.get("final_label_v2") == "true_positive_access_expansion")
    explicit_mission_phrases = {"democratize access", "democratize finance", "democratizing financial services", "affordable loans", "affordable financial services", "low-cost financial services"}
    mission_rows = [row for row in rows if row.get("phrase", "") in explicit_mission_phrases]
    mission_v1_tp = sum(1 for row in mission_rows if row.get("final_label") == "true_positive_access_expansion")
    mission_v2_tp = sum(1 for row in mission_rows if row.get("final_label_v2") == "true_positive_access_expansion")

    lines = [
        "# Review Sample Classification V2 Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "- Reclassified the 600-row review sample using `classification_guidelines_v3.md`.",
        "- Preserved v1 labels for comparison.",
        "- Preserved manual calibration and manual audit labels as ground truth.",
        "- Did not fetch prices, compute returns, make SEC requests, make empirical claims, scale to all 9,400 hits, or modify raw `phrase_hits.csv`.",
        f"- Script version: `{SCRIPT_VERSION}`.",
        "",
        "## Row Counts",
        "",
        f"- Total rows: {len(rows)}",
        f"- Manual calibration rows: {len(manual)}",
        f"- Manual audit rows: {len(audit)}",
        f"- Codex-assisted v2 rows: {source_counts.get('codex_assisted_v2', 0)}",
        f"- Label source counts v2: {dict(source_counts)}",
        f"- Raw `phrase_hits.csv` SHA256 before: `{raw_before}`",
        f"- Raw `phrase_hits.csv` SHA256 after: `{raw_after}`",
        f"- Raw file unchanged by this stage: {'yes' if raw_before == raw_after else 'no'}",
        "",
        "## V1 Label Distribution",
        "",
    ]
    lines.extend(markdown_table(["V1 label", "Count"], label_rows(v1_counts)))
    lines.extend(["", "## V2 Label Distribution", ""])
    lines.extend(markdown_table(["V2 label", "Count"], label_rows(v2_counts)))
    lines.extend(["", "## V1 To V2 Change Summary", ""])
    lines.append(f"- Rows changed from v1 to v2: {len(changed)}")
    transition_counts = Counter((row.get("final_label", ""), row.get("final_label_v2", "")) for row in changed)
    transition_rows = [[old, new, str(count)] for (old, new), count in transition_counts.most_common()]
    lines.extend(markdown_table(["V1 label", "V2 label", "Rows"], transition_rows) if transition_rows else ["- No changes."])
    lines.extend(["", "## Changes By Category", ""])
    cat_changes = changes_by(rows, "category")
    lines.extend(markdown_table(["Category", "Changed rows", "Top transitions"], cat_changes) if cat_changes else ["- No changes."])
    lines.extend(["", "## Changes By Phrase", ""])
    phrase_changes = changes_by(rows, "phrase")
    lines.extend(markdown_table(["Phrase", "Changed rows", "Top transitions"], phrase_changes) if phrase_changes else ["- No changes."])
    lines.extend(["", "## True-Positive Rate By Category Under V2", ""])
    lines.extend(markdown_table(["Category", "Rows", "V2 true positives", "V2 TP rate"], true_positive_rate_by_category(rows)))
    lines.extend(["", "## High-Risk Phrases Still Requiring Caution", ""])
    risk_rows = [[phrase, total, tp, rate, str(dist)] for phrase, total, tp, rate, dist in high_risk_phrases(rows)]
    lines.extend(markdown_table(["Phrase", "Rows", "V2 true positives", "V2 TP rate", "V2 labels"], risk_rows))
    lines.extend(
        [
            "",
            "## Directional Checks",
            "",
            f"- Institutional/platform/market-access phrase rows: {len(inst_market_rows)}",
            f"- V1 true positives in those rows: {inst_market_v1_tp}",
            f"- V2 true positives in those rows: {inst_market_v2_tp}",
            f"- V2 appears more conservative on institutional/platform/market-access language: {'yes' if inst_market_v2_tp < inst_market_v1_tp else 'no'}",
            f"- Explicit financial-access mission phrase rows: {len(mission_rows)}",
            f"- V1 true positives in those rows: {mission_v1_tp}",
            f"- V2 true positives in those rows: {mission_v2_tp}",
            f"- V2 recovers under-called explicit financial-access mission language: {'yes' if mission_v2_tp > mission_v1_tp else 'mixed/no'}",
            "",
            "## Recommendation",
            "",
            "Run a second smaller audit before full-corpus scaling. The revised rules incorporate audit lessons, but v2 still depends on Codex-assisted labels for rows without manual calibration or audit coverage. A targeted 75-100 row audit should oversample changed rows, high-risk phrases, and newly positive mission-language cases before classifying all 9,400 raw hits.",
            "",
            "## Guardrail Reminder",
            "",
            "Treatment construction is not finalized. Returns, prices, benchmark outcomes, and empirical performance analysis remain off-limits until post-revision classification quality is checked and approved.",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def validate(rows: list[dict[str, str]], manual: dict[str, dict[str, str]], audit: dict[str, dict[str, str]]) -> None:
    if len(rows) != 600:
        raise ValueError(f"expected 600 rows, found {len(rows)}")
    for row in rows:
        hit_id = row.get("hit_id", "")
        for field in ["final_label_v2", "final_confidence_v2", "label_source_v2"]:
            if not row.get(field):
                raise ValueError(f"hit_id {hit_id} missing {field}")
        validate_label(row["final_label_v2"], f"final v2 hit_id {hit_id}")
        if hit_id in manual and row["final_label_v2"] != manual[hit_id]["label"]:
            raise ValueError(f"manual calibration mismatch hit_id {hit_id}")
        if hit_id not in manual and hit_id in audit and row["final_label_v2"] != audit[hit_id]["label"]:
            raise ValueError(f"manual audit mismatch hit_id {hit_id}")
    source_counts = Counter(row.get("label_source_v2", "") for row in rows)
    if source_counts.get("manual_calibration", 0) != len(manual):
        raise ValueError("manual calibration source count mismatch")
    expected_audit = len(set(audit) - set(manual))
    if source_counts.get("manual_audit", 0) != expected_audit:
        raise ValueError("manual audit source count mismatch")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reclassify 600-row review sample with v3 guidance.")
    parser.add_argument("--input", default=str(CLASSIFIED_V1_PATH))
    parser.add_argument("--manual-labels", default=str(MANUAL_LABELS_PATH))
    parser.add_argument("--audit-labels", default=str(AUDIT_LABELS_PATH))
    parser.add_argument("--output", default=str(CLASSIFIED_V2_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    field_size_limit()
    if not GUIDELINES_V3_PATH.exists():
        raise FileNotFoundError(GUIDELINES_V3_PATH)
    raw_before = file_sha256(RAW_PHRASE_HITS_PATH)
    rows, fields = read_csv_with_fields(Path(args.input))
    manual = load_manual(Path(args.manual_labels))
    audit = load_audit(Path(args.audit_labels))
    reclassified = reclassify(rows, manual, audit)
    validate(reclassified, manual, audit)
    output_fields = fields + [field for field in V2_FIELDS if field not in fields]
    write_csv(Path(args.output), reclassified, output_fields)
    raw_after = file_sha256(RAW_PHRASE_HITS_PATH)
    write_report(reclassified, manual, audit, raw_before, raw_after)
    changed = sum(1 for row in reclassified if row.get("final_label") != row.get("final_label_v2"))
    source_counts = Counter(row.get("label_source_v2", "") for row in reclassified)
    print(
        "Reclassified review sample v2: "
        f"rows={len(reclassified)}, changed={changed}, sources={dict(source_counts)}"
    )
    print(f"Wrote {Path(args.output).resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
