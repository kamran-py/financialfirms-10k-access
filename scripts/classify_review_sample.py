#!/usr/bin/env python3
"""
Classify the 600-row phrase-hit review sample for text-signal validation.

This script preserves raw phrase hits, preserves manual labels separately from
Codex-assisted labels, and does not fetch prices, make SEC requests, run return
analysis, or use external firm events.
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
REVIEW_SAMPLE_PATH = PROJECT_ROOT / "data" / "review" / "phrase_hit_review_sample.csv"
MANUAL_LABELS_PATH = PROJECT_ROOT / "data" / "review" / "manual_calibration_labels_20260629.csv"
CLASSIFIED_OUTPUT_PATH = PROJECT_ROOT / "data" / "review" / "phrase_hit_review_sample_classified_v1.csv"
QUALITY_REPORT_PATH = PROJECT_ROOT / "quality_reports" / "review_sample_classification_report.md"
RAW_PHRASE_HITS_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"
GUIDELINES_PATH = PROJECT_ROOT / "config" / "classification_guidelines_v2.md"

SCRIPT_VERSION = "classify_review_sample_v1"

ALLOWED_LABELS = {
    "true_positive_access_expansion",
    "generic_marketing",
    "risk_disclosure_only",
    "customer_access_unrelated_to_finance",
    "operational_access_or_platform_language",
    "ambiguous",
    "false_positive",
}

REQUIRED_SAMPLE_FIELDS = [
    "hit_id",
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
    "matched_text",
    "excerpt",
    "source_file",
    "human_label",
    "reviewer_notes",
    "confidence",
]

MANUAL_FIELDS = ["hit_id", "human_label", "confidence", "reviewer_notes", "reviewer_source", "review_date"]

ADDED_FIELDS = [
    "final_label",
    "final_confidence",
    "label_source",
    "codex_assisted_label",
    "codex_assisted_confidence",
    "codex_assisted_notes",
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


def validate_fields(rows: list[dict[str, str]], required: list[str], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} has no rows")
    missing = [field for field in required if field not in rows[0]]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def validate_label(value: str, context: str) -> None:
    if value not in ALLOWED_LABELS:
        raise ValueError(f"invalid label in {context}: {value!r}")


def normalized(row: dict[str, str]) -> str:
    parts = [
        row.get("phrase", ""),
        row.get("category", ""),
        row.get("section_name", ""),
        row.get("matched_text", ""),
        row.get("excerpt", ""),
    ]
    return re.sub(r"\s+", " ", " ".join(parts).lower()).strip()


def has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def has_word(text: str, terms: list[str]) -> bool:
    return any(re.search(rf"\b{re.escape(term)}\b", text) for term in terms)


def external_beneficiary(text: str) -> bool:
    return has_any(
        text,
        [
            "consumer",
            "customer",
            "borrower",
            "investor",
            "retail",
            "individual",
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
            "homeowner",
            "homebuyer",
            "families",
            "households",
            "clients",
            "users",
            "smaller issuers",
            "emerging companies",
        ],
    )


def financial_access_mechanism(text: str) -> bool:
    return has_any(
        text,
        [
            "credit",
            "loan",
            "loans",
            "mortgage",
            "mortgages",
            "banking",
            "bank",
            "financial services",
            "financial products",
            "investment",
            "investing",
            "capital markets",
            "markets",
            "homeownership",
            "housing",
            "insurance",
            "payments",
            "savings",
            "wealth",
            "brokerage",
            "affordable",
            "finance",
            "financing",
        ],
    )


def positive_access_verb(text: str) -> bool:
    return has_any(
        text,
        [
            "expand access",
            "expanded access",
            "expanding access",
            "broaden access",
            "broader access",
            "democratize access",
            "democratizing access",
            "democratized access",
            "lower barriers",
            "lowering barriers",
            "reduce barriers",
            "remove barriers",
            "financial inclusion",
            "inclusive finance",
            "access to affordable",
            "provide access",
            "provides access",
            "make available",
            "available to retail",
            "available to individual",
            "serve underserved",
            "serving underserved",
            "reach underserved",
        ],
    )


def risk_context(text: str) -> bool:
    return has_any(
        text,
        [
            "risk factor",
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
            "capital markets",
            "debt markets",
            "credit markets",
            "our ability to access",
            "ability to access capital",
            "access to capital",
            "access to credit markets",
            "access to financing",
            "access to funding",
            "availability of credit",
            "economic conditions",
        ],
    )


def table_or_accounting_context(text: str) -> bool:
    return has_any(
        text,
        [
            "tax credit",
            "low income housing tax credit",
            "limited partnership",
            "partnership investment",
            "equity investment",
            "community development investment",
            "investment portfolio",
            "portfolio exposure",
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


def classify_codex_assisted(row: dict[str, str]) -> Decision:
    phrase = row.get("phrase", "").strip().lower()
    category = row.get("category", "").strip().lower()
    section = row.get("section_name", "").strip().lower()
    text = normalized(row)

    beneficiary = external_beneficiary(text)
    mechanism = financial_access_mechanism(text)
    positive = positive_access_verb(text)
    in_risk_section = "risk" in section
    risk = risk_context(text) or in_risk_section

    if phrase == "fractional share":
        if has_any(text, ["cash in lieu", "merger", "stock split", "reverse stock split", "exchange ratio", "no fractional", "fractional shares will not", "converted into", "share issuance", "common stock"]):
            return Decision("false_positive", "high", "Fractional-share reference appears to be stock, merger, split, issuance, or cash-in-lieu mechanics.")
        if beneficiary and has_any(text, ["invest", "investing", "brokerage", "retail", "individual", "minimum", "access"]):
            return Decision("true_positive_access_expansion", "medium", "Fractional-share wording is tied to investor access or retail participation.")
        return Decision("operational_access_or_platform_language", "medium", "Fractional-share wording lacks clear external investor-access mechanism.")

    if phrase == "affordable housing" or "affordable housing" in phrase:
        if table_or_accounting_context(text) and not positive:
            return Decision("operational_access_or_platform_language", "high", "Affordable-housing reference appears in tax-credit, partnership, accounting, portfolio, or commitments context.")
        if beneficiary and mechanism and has_any(text, ["loan", "lending", "mortgage", "financing", "homeownership", "community", "low- and moderate-income", "lmi", "families"]):
            return Decision("true_positive_access_expansion", "medium", "Affordable-housing wording is tied to financing or housing access for external beneficiaries.")
        return Decision("ambiguous", "low", "Affordable-housing context lacks enough detail to distinguish access-oriented disclosure from investment/accounting exposure.")

    if phrase == "institutional quality":
        if has_any(text, ["property", "properties", "real estate", "office", "multifamily", "assets", "portfolio", "tenant", "leasing"]):
            return Decision("false_positive", "high", "Institutional-quality wording appears to describe property, real-estate, asset, or portfolio quality.")
        if beneficiary and mechanism and has_any(text, ["retail", "individual", "access", "available"]):
            return Decision("true_positive_access_expansion", "medium", "Institutional-quality wording is tied to access for external users.")
        return Decision("false_positive", "medium", "Institutional-quality wording does not identify expanded access for external financial users.")

    if phrase in {"institutional-grade", "institutional grade", "institutional caliber", "institutional-level", "institutional level"}:
        if beneficiary and mechanism and has_any(text, ["retail", "individual", "consumer", "small business", "access", "available", "democrat"]):
            return Decision("true_positive_access_expansion", "medium", "Institutional-grade capability is tied to access for retail, individual, consumer, or small-business users.")
        return Decision("operational_access_or_platform_language", "high", "Institutional-grade wording appears to describe platform, infrastructure, quality, or internal capability.")

    if phrase in {"market access", "access to markets", "capital markets access"}:
        if beneficiary and mechanism and has_any(text, ["customers", "clients", "borrowers", "investors", "smaller issuers", "communities", "small business", "access to capital markets for"]):
            return Decision("true_positive_access_expansion", "medium", "Market-access wording identifies external financial beneficiaries.")
        if risk:
            return Decision("risk_disclosure_only", "high", "Market-access wording appears in issuer financing, adverse-market, regulatory, or risk-disclosure context.")
        return Decision("operational_access_or_platform_language", "high", "Market-access wording appears to concern issuer, regulatory, competitive, distribution, or infrastructure access.")

    if phrase in {"access to credit", "credit access", "affordable credit", "access to affordable credit", "expand access to credit", "expanded access to credit", "expanding access to credit", "broaden access to credit", "broader access to credit"}:
        if risk and not beneficiary:
            return Decision("risk_disclosure_only", "high", "Credit-access wording concerns issuer liquidity, funding, or risk disclosure rather than external beneficiaries.")
        if beneficiary and mechanism:
            return Decision("true_positive_access_expansion", "high" if positive else "medium", "Credit-access wording identifies consumers, borrowers, underserved groups, customers, communities, or small businesses as beneficiaries.")
        if in_risk_section:
            return Decision("risk_disclosure_only", "medium", "Credit-access wording is in Item 1A without a clear external beneficiary.")
        return Decision("ambiguous", "low", "Credit-access wording lacks a clear external beneficiary.")

    if category == "homeownership access":
        if table_or_accounting_context(text) and not has_any(text, ["homeowner", "homebuyer", "borrower", "mortgage", "families"]):
            return Decision("operational_access_or_platform_language", "medium", "Housing wording appears in investment, accounting, tax-credit, or commitments context.")
        if beneficiary and mechanism and has_any(text, ["homeownership", "housing", "mortgage", "loan", "lending", "affordable"]):
            return Decision("true_positive_access_expansion", "medium", "Housing wording is tied to external access to housing, lending, or homeownership.")
        return Decision("ambiguous", "low", "Housing-access wording lacks enough beneficiary/mechanism detail.")

    if category == "underserved / underbanked / unbanked":
        if mechanism and has_any(text, ["financial", "bank", "banking", "credit", "loan", "payments", "insurance", "mortgage", "invest"]):
            return Decision("true_positive_access_expansion", "high", "Underserved, underbanked, or unbanked wording appears in financial-services context.")
        if has_any(text, ["healthcare", "education", "telecommunications", "broadband", "media", "entertainment"]):
            return Decision("customer_access_unrelated_to_finance", "high", "Underserved wording appears outside financial access.")
        return Decision("ambiguous", "medium", "Underserved wording lacks clear financial-access mechanism.")

    if category == "financial inclusion":
        if mechanism or positive:
            return Decision("true_positive_access_expansion", "medium", "Financial-inclusion wording is access-related in financial-services context.")
        return Decision("generic_marketing", "medium", "Financial-inclusion wording is broad and lacks specific mechanism.")

    if category == "democratized access":
        if beneficiary and mechanism:
            return Decision("true_positive_access_expansion", "high" if positive else "medium", "Democratized-access wording identifies external financial beneficiaries.")
        if mechanism:
            return Decision("generic_marketing", "medium", "Democratization wording is financial but lacks clear external beneficiary.")
        return Decision("generic_marketing", "medium", "Democratization wording is broad without clear financial-access mechanism.")

    if category == "retail access to investing":
        if phrase in {"retail investors", "individual investors"}:
            if has_any(text, ["available to", "access", "offering", "platform", "product", "minimum", "fractional", "democrat", "expand"]) and mechanism:
                return Decision("true_positive_access_expansion", "medium", "Retail/individual investor wording is tied to investment access or availability.")
            return Decision("false_positive", "medium", "Retail/individual investor wording appears as generic securities, investor-relations, or market-participant language.")
        if beneficiary and mechanism:
            return Decision("true_positive_access_expansion", "medium", "Investing-access wording identifies retail or individual investor beneficiaries.")
        return Decision("ambiguous", "low", "Investing-access wording lacks clear access-oriented disclosure context.")

    if category == "lower barriers / level playing field":
        if beneficiary and mechanism:
            return Decision("true_positive_access_expansion", "medium", "Barrier-reduction wording is tied to external financial beneficiaries.")
        if has_any(text, ["competition", "competitors", "regulatory", "operations", "technology", "platform"]):
            return Decision("operational_access_or_platform_language", "medium", "Barrier or level-playing-field wording appears operational, competitive, or regulatory.")
        return Decision("generic_marketing", "medium", "Barrier-reduction wording is broad without clear financial beneficiary.")

    if category == "affordable financial products":
        if beneficiary and mechanism:
            return Decision("true_positive_access_expansion", "medium", "Affordability wording is tied to external financial beneficiaries.")
        return Decision("generic_marketing", "medium", "Affordability wording lacks enough beneficiary detail.")

    if category == "broader market participation":
        if beneficiary and mechanism and positive:
            return Decision("true_positive_access_expansion", "medium", "Market-participation wording is tied to external financial beneficiaries.")
        if risk:
            return Decision("risk_disclosure_only", "medium", "Market-participation wording appears in risk or issuer-financing context.")
        return Decision("operational_access_or_platform_language", "medium", "Market-participation wording appears operational or generic without beneficiary.")

    if risk and not beneficiary:
        return Decision("risk_disclosure_only", "medium", "Risk or issuer-financing context without external beneficiary.")
    if beneficiary and mechanism and positive:
        return Decision("true_positive_access_expansion", "medium", "External beneficiary and financial-access mechanism are present.")
    if beneficiary and not mechanism:
        return Decision("customer_access_unrelated_to_finance", "medium", "External access context lacks financial-access mechanism.")
    return Decision("ambiguous", "low", "Insufficient context for a more specific label.")


def load_manual_labels(path: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    validate_fields(rows, MANUAL_FIELDS, "manual calibration labels")
    labels: dict[str, dict[str, str]] = {}
    for row in rows:
        hit_id = row.get("hit_id", "").strip()
        label = row.get("human_label", "").strip()
        confidence = row.get("confidence", "").strip()
        if not hit_id:
            raise ValueError("manual calibration row missing hit_id")
        validate_label(label, f"manual hit_id {hit_id}")
        if hit_id in labels:
            raise ValueError(f"duplicate manual calibration hit_id: {hit_id}")
        labels[hit_id] = {
            "human_label": label,
            "confidence": confidence,
            "reviewer_notes": row.get("reviewer_notes", ""),
            "reviewer_source": row.get("reviewer_source", ""),
            "review_date": row.get("review_date", ""),
        }
    return labels


def classify_rows(sample_rows: list[dict[str, str]], manual: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    validate_fields(sample_rows, REQUIRED_SAMPLE_FIELDS, "review sample")
    output: list[dict[str, str]] = []
    sample_hit_ids = {row["hit_id"] for row in sample_rows}
    missing_manual = sorted(set(manual) - sample_hit_ids, key=lambda value: int(value))
    if missing_manual:
        raise ValueError(f"manual calibration hit_ids not present in review sample: {missing_manual[:10]}")

    for row in sample_rows:
        item = dict(row)
        hit_id = item.get("hit_id", "")
        if hit_id in manual:
            manual_row = manual[hit_id]
            item["human_label"] = manual_row["human_label"]
            item["confidence"] = manual_row["confidence"]
            item["reviewer_notes"] = manual_row["reviewer_notes"]
            item["codex_assisted_label"] = ""
            item["codex_assisted_confidence"] = ""
            item["codex_assisted_notes"] = ""
            item["final_label"] = manual_row["human_label"]
            item["final_confidence"] = manual_row["confidence"]
            item["label_source"] = "manual_calibration"
        else:
            decision = classify_codex_assisted(item)
            validate_label(decision.label, f"codex-assisted hit_id {hit_id}")
            item["codex_assisted_label"] = decision.label
            item["codex_assisted_confidence"] = decision.confidence
            item["codex_assisted_notes"] = decision.notes
            item["final_label"] = decision.label
            item["final_confidence"] = decision.confidence
            item["label_source"] = "codex_assisted"
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


def label_counts_rows(counter: Counter[str]) -> list[list[str]]:
    return [[label, str(counter.get(label, 0))] for label in sorted(ALLOWED_LABELS)]


def true_positive_rate_rows(rows: list[dict[str, str]]) -> list[list[str]]:
    by_category: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        by_category[row.get("category", "")][row.get("final_label", "")] += 1
    table: list[list[str]] = []
    for category in sorted(by_category):
        total = sum(by_category[category].values())
        tp = by_category[category].get("true_positive_access_expansion", 0)
        rate = tp / total if total else 0
        table.append([category, str(total), str(tp), f"{rate:.1%}"])
    return table


def high_false_positive_phrase_rows(rows: list[dict[str, str]]) -> list[list[str]]:
    negative = {
        "false_positive",
        "risk_disclosure_only",
        "operational_access_or_platform_language",
        "customer_access_unrelated_to_finance",
    }
    by_phrase: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        by_phrase[row.get("phrase", "")][row.get("final_label", "")] += 1
    table: list[list[str]] = []
    for phrase, counts in by_phrase.items():
        total = sum(counts.values())
        neg = sum(counts.get(label, 0) for label in negative)
        if total >= 3 and (neg / total) >= 0.65:
            table.append(
                [
                    phrase,
                    str(total),
                    str(neg),
                    f"{(neg / total):.1%}",
                    str(counts.get("true_positive_access_expansion", 0)),
                ]
            )
    return sorted(table, key=lambda row: (-float(row[3].strip("%")), -int(row[1]), row[0]))[:30]


def ambiguous_examples(rows: list[dict[str, str]]) -> list[list[str]]:
    examples = [row for row in rows if row.get("final_label") == "ambiguous"]
    output: list[list[str]] = []
    for row in examples[:10]:
        excerpt = re.sub(r"\s+", " ", row.get("excerpt", "")).strip()
        if len(excerpt) > 260:
            excerpt = excerpt[:257].rstrip() + "..."
        output.append(
            [
                row.get("hit_id", ""),
                row.get("ticker", ""),
                row.get("filing_year", ""),
                row.get("phrase", ""),
                row.get("category", ""),
                excerpt,
            ]
        )
    return output


def recommended_exclusions(rows: list[dict[str, str]]) -> list[list[str]]:
    rows_by_phrase: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        rows_by_phrase[row.get("phrase", "")].append(row)
    recs: list[list[str]] = []
    for phrase, phrase_rows in rows_by_phrase.items():
        total = len(phrase_rows)
        label_counts = Counter(row.get("final_label", "") for row in phrase_rows)
        tp = label_counts.get("true_positive_access_expansion", 0)
        noisy = total - tp
        if total < 3:
            continue
        if tp == 0:
            rec = "exclude from primary classified-treatment construction; retain for sensitivity/audit"
        elif noisy / total >= 0.75:
            rec = "high-risk flag; require manual review before treatment use"
        else:
            continue
        recs.append([phrase, str(total), str(tp), str(noisy), rec])
    return sorted(recs, key=lambda row: (int(row[2]), -int(row[1]), row[0]))[:30]


def write_report(rows: list[dict[str, str]], manual_count: int, raw_hash_before: str, raw_hash_after: str) -> None:
    QUALITY_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    total = len(rows)
    codex_count = sum(1 for row in rows if row.get("label_source") == "codex_assisted")
    label_counts = Counter(row.get("final_label", "") for row in rows)
    source_counts = Counter(row.get("label_source", "") for row in rows)

    lines = [
        "# Review Sample Classification Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "- Text-signal validation for the 600-row review sample only.",
        "- Manual calibration labels are preserved separately from Codex-assisted labels.",
        "- Raw phrase hits remain separate from interpreted labels.",
        "- No prices, returns, outcomes, SEC requests, later news, litigation, bankruptcies, acquisitions, or external firm events were used.",
        f"- Script version: `{SCRIPT_VERSION}`.",
        "",
        "## Acceptance Counts",
        "",
        f"- Total rows classified: {total}",
        f"- Manual calibration row count: {manual_count}",
        f"- Codex-assisted row count: {codex_count}",
        f"- Label source counts: {dict(source_counts)}",
        f"- Raw `phrase_hits.csv` SHA256 before: `{raw_hash_before}`",
        f"- Raw `phrase_hits.csv` SHA256 after: `{raw_hash_after}`",
        f"- Raw file unchanged by this stage: {'yes' if raw_hash_before == raw_hash_after else 'no'}",
        "",
        "## Label Counts Overall",
        "",
    ]
    lines.extend(markdown_table(["Label", "Count"], label_counts_rows(label_counts)))

    lines.extend(["", "## Label Counts By Category", ""])
    category_label = counter_by(rows, "category", "final_label")
    category_rows = [[cat, label, str(count)] for (cat, label), count in sorted(category_label.items())]
    lines.extend(markdown_table(["Category", "Final label", "Count"], category_rows))

    lines.extend(["", "## Label Counts By Phrase", ""])
    phrase_label = counter_by(rows, "phrase", "final_label")
    phrase_rows = [[phrase, label, str(count)] for (phrase, label), count in sorted(phrase_label.items())]
    lines.extend(markdown_table(["Phrase", "Final label", "Count"], phrase_rows))

    lines.extend(["", "## True-Positive Rate By Category", ""])
    lines.extend(markdown_table(["Category", "Rows", "True positives", "Rate"], true_positive_rate_rows(rows)))

    lines.extend(["", "## High-False-Positive Phrases", ""])
    high_risk = high_false_positive_phrase_rows(rows)
    lines.extend(
        markdown_table(["Phrase", "Rows", "Negative/noise labels", "Noise rate", "True positives"], high_risk)
        if high_risk
        else ["- None met the high-risk threshold in this sample."]
    )

    lines.extend(["", "## Examples Of Ambiguous Cases", ""])
    ambiguous = ambiguous_examples(rows)
    lines.extend(
        markdown_table(["Hit ID", "Ticker", "Year", "Phrase", "Category", "Excerpt"], ambiguous)
        if ambiguous
        else ["- No ambiguous cases in classified sample."]
    )

    lines.extend(["", "## Recommended Phrase Exclusions Or High-Risk Flags", ""])
    recs = recommended_exclusions(rows)
    lines.extend(
        markdown_table(["Phrase", "Rows", "True positives", "Other labels", "Recommendation"], recs)
        if recs
        else ["- No exclusions recommended from this sample."]
    )

    lines.extend(
        [
            "",
            "## Recommended Treatment-Variable Construction For Future Analysis",
            "",
            "- Do not use raw phrase hits as treatment without validation.",
            "- Primary text-valid treatment should be `final_label == true_positive_access_expansion`, auditable by `hit_id`, accession number, section, phrase, excerpt, final label, confidence, and label source.",
            "- Preserve separate indicators for `label_source == manual_calibration` and `label_source == codex_assisted` in any downstream table.",
            "- Build filing-level treatment only after aggregating validated labels by accession number and documenting unresolved or ambiguous rows.",
            "- Exclude or separately flag high-risk phrases from primary treatment construction unless manually reviewed.",
            "- Keep `risk_disclosure_only`, `operational_access_or_platform_language`, `customer_access_unrelated_to_finance`, `generic_marketing`, `ambiguous`, and `false_positive` as non-treatment or sensitivity categories.",
            "",
            "## Explicit Warning",
            "",
            "No returns, prices, benchmarks, outcomes, SEC requests, later news, litigation, bankruptcies, acquisitions, or empirical performance information were used in this classification stage.",
        ]
    )
    QUALITY_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def validate_output(rows: list[dict[str, str]], manual: dict[str, dict[str, str]]) -> None:
    if len(rows) != 600:
        raise ValueError(f"expected 600 classified rows, found {len(rows)}")
    for row in rows:
        hit_id = row.get("hit_id", "")
        for field in ["final_label", "final_confidence", "label_source"]:
            if not row.get(field):
                raise ValueError(f"hit_id {hit_id} missing {field}")
        validate_label(row["final_label"], f"final hit_id {hit_id}")
        if hit_id in manual and row["final_label"] != manual[hit_id]["human_label"]:
            raise ValueError(f"manual label mismatch for hit_id {hit_id}")
        if hit_id in manual and row["final_confidence"] != manual[hit_id]["confidence"]:
            raise ValueError(f"manual confidence mismatch for hit_id {hit_id}")
    manual_rows = [row for row in rows if row.get("label_source") == "manual_calibration"]
    if len(manual_rows) != len(manual):
        raise ValueError(f"expected {len(manual)} manual rows, found {len(manual_rows)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify review sample using manual calibration plus Codex-assisted text rules.")
    parser.add_argument("--review-sample", default=str(REVIEW_SAMPLE_PATH))
    parser.add_argument("--manual-labels", default=str(MANUAL_LABELS_PATH))
    parser.add_argument("--output", default=str(CLASSIFIED_OUTPUT_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    field_size_limit()
    if not GUIDELINES_PATH.exists():
        raise FileNotFoundError(GUIDELINES_PATH)
    raw_hash_before = file_sha256(RAW_PHRASE_HITS_PATH)
    sample_rows = read_csv(Path(args.review_sample))
    manual = load_manual_labels(Path(args.manual_labels))
    classified = classify_rows(sample_rows, manual)
    validate_output(classified, manual)
    write_csv(Path(args.output), classified, REQUIRED_SAMPLE_FIELDS + ADDED_FIELDS)
    raw_hash_after = file_sha256(RAW_PHRASE_HITS_PATH)
    write_report(classified, len(manual), raw_hash_before, raw_hash_after)
    print(
        "Classified review sample: "
        f"rows={len(classified)}, manual={len(manual)}, "
        f"codex_assisted={sum(1 for row in classified if row.get('label_source') == 'codex_assisted')}"
    )
    print(f"Wrote {Path(args.output).resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {QUALITY_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
