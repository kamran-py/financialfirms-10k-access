"""Build conservative filing-level access-expansion treatment candidates.

This script uses only local extracted text artifacts:
- data/extracted/phrase_hits.csv
- data/extracted/filing_sections.csv

It does not use V2 or tiered labels for treatment construction.
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHRASE_HITS = ROOT / "data" / "extracted" / "phrase_hits.csv"
FILING_SECTIONS = ROOT / "data" / "extracted" / "filing_sections.csv"
V2_CLASSIFIED = ROOT / "data" / "classified" / "phrase_hits_classified_v2.csv"
TIERED_CLASSIFIED = ROOT / "data" / "classified" / "phrase_hits_tiered_v1.csv"

TREATMENT_DIR = ROOT / "data" / "treatments"
REVIEW_DIR = ROOT / "data" / "review"
REPORT_DIR = ROOT / "quality_reports"

CANDIDATE_OUT = TREATMENT_DIR / "conservative_filing_treatment_candidates_v1.csv"
EVIDENCE_OUT = TREATMENT_DIR / "conservative_filing_treatment_evidence_v1.csv"
REPORT_OUT = REPORT_DIR / "conservative_filing_treatment_candidates_v1_report.md"
AUDIT_SAMPLE_OUT = REVIEW_DIR / "conservative_filing_treatment_audit_sample.csv"
AUDIT_PLAN_OUT = REPORT_DIR / "conservative_filing_treatment_audit_plan.md"
CHECKPOINT_OUT = ROOT / "CHECKPOINT_17_CONSERVATIVE_FILING_TREATMENT_CANDIDATES.md"

FILING_KEY = ("firm_id", "ticker", "cik", "accession_number", "filing_date", "filing_year")
csv.field_size_limit(sys.maxsize)


def rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


BENEFICIARY_RX = rx(
    r"\b(consumers?|customers?|members?|borrowers?|homeowners?|residents?|renters?|"
    r"retail investors?|individual investors?|individuals?|people|users?|clients?|"
    r"small businesses?|merchants?|smaller issuers?|municipalities|communities|"
    r"households?|low[- ]and[- ]moderate[- ]income|LMI|minority|underserved|"
    r"underbanked|unbanked)\b"
)
FINANCIAL_MECHANISM_RX = rx(
    r"\b(financial services?|finance|banking|bank accounts?|deposits?|credit|loans?|"
    r"lending|mortgages?|homeownership|housing|payments?|money movement|remittances?|"
    r"investing|investments?|brokerage|trading|financial markets?|capital markets?|"
    r"insurance|savings|wealth management|retirement|financial products?)\b"
)
DEMOCRATIZE_RX = rx(r"\b(democratiz(?:e|es|ed|ing)|democratized access|democratizing access)\b")
DEMO_MECHANISM_RX = rx(
    r"\b(finance|financial services?|financial markets?|investing|investment products?|"
    r"alternative investments?|private markets?|brokerage|payments?|money movement)\b"
)
FINANCIAL_INCLUSION_RX = rx(r"\b(financial inclusion|promote financial inclusion|inclusive financial system)\b")
UNBANKED_RX = rx(
    r"\b(unbanked|underbanked|underserved(?: consumers?| borrowers?| communities?| populations?| customers?)?|"
    r"low[- ]and[- ]moderate[- ]income|LMI|minority borrowers?|community(?: lending| banking| development)?)\b"
)
CREDIT_EXPANSION_RX = rx(r"\b(expand(?:ed|ing)? access to (?:affordable )?credit|access to affordable credit)\b")
CREDIT_BENEFICIARY_RX = rx(
    r"\b(consumers?|borrowers?|members?|customers?|small businesses?|LMI|minority|"
    r"underserved|communities|households?|homeowners?)\b"
)
AFFORDABLE_PRODUCT_RX = rx(
    r"\b(affordable credit|affordable financial services?|low-cost financial services?|"
    r"affordable loans?|access to affordable credit)\b"
)
HOMEOWNERSHIP_RX = rx(
    r"\b(homeownership|home ownership|housing access|access to housing|access to homeownership|"
    r"affordable homeownership|affordable housing)\b"
)
HOUSING_MECHANISM_RX = rx(
    r"\b(mortgages?|mortgage credit|borrowers?|homeowners?|residents?|renters?|"
    r"low[- ]and[- ]moderate[- ]income|LMI|community housing|affordable homeownership|"
    r"construction financing|preservation financing|housing finance|financing affordable housing)\b"
)
HOUSING_DIRECT_ACCESS_RX = rx(
    r"\b(loans?|lending|financ(?:e|es|ed|ing)|investments?)\b.{0,80}"
    r"\b(create|preserve|construct|develop|provide|support|expand|increase)\b.{0,80}"
    r"\b(affordable housing|affordable homeownership|housing options|housing availability)\b|"
    r"\b(affordable housing|affordable homeownership|housing options|housing availability)\b.{0,80}"
    r"\b(loans?|lending|financ(?:e|es|ed|ing)|investments?)\b"
)
INSTITUTIONAL_ACCESS_RX = rx(
    r"\b(retail|individual|non-institutional|customers?|users?)\b.{0,80}"
    r"\b(institutional[- ](?:quality|grade|caliber|level)|institutional quality|institutional grade)\b|"
    r"\b(institutional[- ](?:quality|grade|caliber|level)|institutional quality|institutional grade)\b"
    r".{0,80}\b(retail|individual|non-institutional|customers?|users?)\b"
)
MARKET_ACCESS_EXTERNAL_RX = rx(
    r"\b(smaller issuers?|municipalities|clients?|customers?|borrowers?|small businesses?|companies|issuers)\b"
    r".{0,120}\b(access to (?:capital )?markets|capital markets access|market access|bond market|financing)\b|"
    r"\b(access to (?:capital )?markets|capital markets access|market access|bond market|financing)\b"
    r".{0,120}\b(smaller issuers?|municipalities|clients?|customers?|borrowers?|small businesses?|companies|issuers)\b"
)

FRACTIONAL_MECHANICS_RX = rx(
    r"\b(stock split|reverse split|merger|exchange ratio|cash in lieu|cash-in-lieu|"
    r"conversion|convertible|share issuance|issued shares?|dividend|common stock|preferred stock|"
    r"fractional shares? of (?:common|preferred) stock|rounding)\b"
)
ISSUER_OWN_FUNDING_RX = rx(
    r"\b(our|we|company|issuer|registrant)\b.{0,70}\b(access to credit|credit facilit(?:y|ies)|"
    r"liquidity|capital resources|funding|borrowings?|debt markets?|FHLB advances?|credit ratings?)\b|"
    r"\b(access to credit|credit facilit(?:y|ies)|liquidity|capital resources|funding|borrowings?|"
    r"debt markets?|FHLB advances?|credit ratings?)\b.{0,70}\b(our|we|company|issuer|registrant)\b"
)
AFFORDABLE_HOUSING_ACCOUNTING_RX = rx(
    r"\b(tax[- ]credit|tax advantaged|tax-advantaged|LIHTC|partnership investments?|"
    r"investment income|portfolio|sale of|sold|impairment|commitments? table|unfunded commitments?|"
    r"designed to generate a return|federal tax|consolidated balance sheets?|in millions|"
    r"assets:|bonds available for sale|other bond securities|tax benefits?|"
    r"proportional amortization|qualified affordable housing projects?|account for the investments?|"
    r"affordable housing partnerships?|construction guarantees?|letters of credit|"
    r"other commercial commitments?|investments by our|life insurance companies)\b"
)
AFFORDABLE_HOUSING_GENERIC_RX = rx(
    r"\b(charitable|charity|philanthrop(?:y|ic)|donat(?:e|ed|ion|ions)|grants?|foundation|"
    r"arts and culture|child care|food security|workforce preparedness|financial literacy|"
    r"mental and physical health|transportation and more|community leaders|affordable housing developers)\b"
)
GENERIC_BARRIERS_RX = rx(
    r"\b(AI|artificial intelligence|human resources|HR|healthcare|sports|competition|competitors?|"
    r"product listing|listing standards?|regulatory barriers?|legislation|internal operations?|"
    r"affiliation among banks|Gramm-Leach-Bliley)\b"
)
PLATFORM_ONLY_RX = rx(
    r"\b(platform|API|infrastructure|custody|analytics|data|connectivity|security|technology|"
    r"operational|institutional[- ]quality|institutional[- ]grade)\b"
)
RISK_ONLY_RX = rx(
    r"\b(risk|risks|adverse|could|may|might|competition|competitors?|compete|loss of|"
    r"depend(?:s|ent)|uncertain|subject to)\b"
)
REGULATORY_RX = rx(r"\b(CRA|Community Reinvestment Act|regulat(?:ion|ory)|rulemaking|legislation|agency|Treasury|RFI)\b")
ISSUER_ACTION_RX = rx(
    r"\b(we|our|us|company|corporation|issuer|registrant|the bank|our bank|platform|products?|services?)\b"
    r".{0,120}\b(provid(?:e|es|ed|ing)|offer(?:s|ed|ing)?|launch(?:ed|es|ing)?|"
    r"enable(?:s|d|ing)?|serve(?:s|d|ing)?|support(?:s|ed|ing)?|make available|"
    r"expand(?:s|ed|ing)?|increase(?:s|d|ing)?|help(?:s|ed|ing)?|facilitat(?:e|es|ed|ing)|"
    r"develop(?:s|ed|ing)?|creat(?:e|es|ed|ing)|originat(?:e|es|ed|ing)|fund(?:s|ed|ing)|"
    r"financ(?:e|es|ed|ing))\b|"
    r"\b(provid(?:e|es|ed|ing)|offer(?:s|ed|ing)?|launch(?:ed|es|ing)?|"
    r"enable(?:s|d|ing)?|serve(?:s|d|ing)?|support(?:s|ed|ing)?|make available|"
    r"expand(?:s|ed|ing)?|increase(?:s|d|ing)?|help(?:s|ed|ing)?|facilitat(?:e|es|ed|ing)|"
    r"develop(?:s|ed|ing)?|creat(?:e|es|ed|ing)|originat(?:e|es|ed|ing)|fund(?:s|ed|ing)|"
    r"financ(?:e|es|ed|ing))\b.{0,120}"
    r"\b(we|our|us|company|corporation|issuer|registrant|the bank|our bank|platform|products?|services?)\b"
)
REGULATORY_ISSUER_ACTION_RX = rx(
    r"\b(we|our|us|company|corporation|issuer|registrant|the bank|our bank)\b"
    r".{0,120}\b(provid(?:e|es|ed|ing)|offer(?:s|ed|ing)?|launch(?:ed|es|ing)?|"
    r"enable(?:s|d|ing)?|serve(?:s|d|ing)?|support(?:s|ed|ing)?|make available|"
    r"expand(?:s|ed|ing)?|increase(?:s|d|ing)?|help(?:s|ed|ing)?|facilitat(?:e|es|ed|ing)|"
    r"develop(?:s|ed|ing)?|creat(?:e|es|ed|ing)|originat(?:e|es|ed|ing)|fund(?:s|ed|ing)|"
    r"financ(?:e|es|ed|ing))\b|"
    r"\b(provid(?:e|es|ed|ing)|offer(?:s|ed|ing)?|launch(?:ed|es|ing)?|"
    r"enable(?:s|d|ing)?|serve(?:s|d|ing)?|support(?:s|ed|ing)?|make available|"
    r"expand(?:s|ed|ing)?|increase(?:s|d|ing)?|help(?:s|ed|ing)?|facilitat(?:e|es|ed|ing)|"
    r"develop(?:s|ed|ing)?|creat(?:e|es|ed|ing)|originat(?:e|es|ed|ing)|fund(?:s|ed|ing)|"
    r"financ(?:e|es|ed|ing))\b.{0,120}"
    r"\b(we|our|us|company|corporation|issuer|registrant|the bank|our bank)\b"
)
FHLB_ISSUER_LIQUIDITY_RX = rx(
    r"\b(FHLB|Federal Home Loan Bank|advances?)\b.{0,120}\b(liquidity|annuity operations|"
    r"outstanding advances|included in)\b|"
    r"\b(liquidity|annuity operations|outstanding advances|included in)\b.{0,120}"
    r"\b(FHLB|Federal Home Loan Bank|advances?)\b"
)
NON_FINANCIAL_CONTEXT_RX = rx(
    r"\b(health equity|health care|healthcare|care delivery|doctors?|patients?|medical|"
    r"ACO REACH|education|school|career readiness|workforce|sports|food security|"
    r"arts and culture|child care|transportation)\b"
)
STRONG_FINANCIAL_ACCESS_RX = rx(
    r"\b(financial services?|banking|bank accounts?|deposits?|credit|loans?|lending|"
    r"mortgages?|payments? (?:services?|network|platform|processing)|money movement|"
    r"remittances?|investing|investments?|brokerage|trading|insurance|savings|"
    r"wealth management|retirement|financial products?)\b"
)


NARRATIVE_PRIORITY = {
    "financial inclusion / underbanked / underserved": 1,
    "consumer credit access": 2,
    "affordable housing / homeownership access": 3,
    "retail investing / brokerage democratization": 4,
    "private-market or alternative-investment access": 5,
    "payments / money movement / SMB commerce access": 6,
    "insurance / benefits access": 7,
    "smaller-issuer capital-market access": 8,
    "fee / cost / minimum-reduction framing": 9,
    "generic/other access-expansion": 10,
}


def normalize(value: str | None) -> str:
    return " ".join((value or "").replace("\u2014", " ").replace("\u2013", " ").split())


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def filing_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row.get(field, "") for field in FILING_KEY)


def is_high_risk(row: dict[str, str]) -> tuple[bool, list[str]]:
    phrase = normalize(row.get("phrase")).lower()
    category = normalize(row.get("category")).lower()
    section = normalize(row.get("section_name")).lower()
    text = f"{phrase} {category}"
    risks: list[str] = []
    if "affordable housing" in text or "homeownership" in text or "housing access" in text:
        risks.append("affordable housing / homeownership access")
    if "fractional share" in text:
        risks.append("fractional share")
    if "institutional" in text:
        risks.append("institutional quality / institutional grade")
    if "market access" in text or "access to markets" in text or "capital markets access" in text:
        risks.append("market access / access to markets / capital markets access")
    if "access to credit" in text or "credit access" in text:
        risks.append("access to credit")
    if (
        "barrier" in text
        or "level playing field" in text
        or "removing barriers" in text
        or "reduce barriers" in text
    ):
        risks.append("lower/reduce/remove/eliminate barriers")
    if "risk factors" in section:
        risks.append("risk-section access language")
    if REGULATORY_RX.search(normalize(row.get("excerpt"))):
        risks.append("CRA/regulatory language")
    return bool(risks), sorted(set(risks))


def exclusion_reasons(row: dict[str, str]) -> list[str]:
    phrase = normalize(row.get("phrase")).lower()
    text = normalize(row.get("excerpt"))
    reasons: list[str] = []
    if "fractional share" in phrase and FRACTIONAL_MECHANICS_RX.search(text):
        reasons.append("fractional-share stock mechanics")
    if ISSUER_OWN_FUNDING_RX.search(text):
        reasons.append("issuer liquidity/funding/access-to-credit context")
    if FHLB_ISSUER_LIQUIDITY_RX.search(text):
        reasons.append("FHLB/issuer-liquidity context")
    if "affordable housing" in phrase and AFFORDABLE_HOUSING_ACCOUNTING_RX.search(text):
        reasons.append("affordable-housing accounting/tax-credit/portfolio context")
    if "affordable housing" in phrase and AFFORDABLE_HOUSING_GENERIC_RX.search(text):
        reasons.append("generic affordable-housing philanthropy/community context")
    if ("barrier" in phrase or "level playing field" in phrase) and GENERIC_BARRIERS_RX.search(text):
        reasons.append("generic non-end-user barriers context")
    if ("institutional" in phrase or "institutional" in text.lower()) and not INSTITUTIONAL_ACCESS_RX.search(text):
        reasons.append("institutional-quality/platform context without retail access")
    if ("market access" in phrase or "access to markets" in phrase or "capital markets access" in phrase) and not MARKET_ACCESS_EXTERNAL_RX.search(text):
        reasons.append("generic or issuer market-access context")
    if PLATFORM_ONLY_RX.search(text) and not (BENEFICIARY_RX.search(text) and FINANCIAL_MECHANISM_RX.search(text)):
        reasons.append("platform/API/infrastructure without explicit end-user financial access")
    if RISK_ONLY_RX.search(text) and not (BENEFICIARY_RX.search(text) and FINANCIAL_MECHANISM_RX.search(text)):
        reasons.append("risk-only or competitor access language")
    if NON_FINANCIAL_CONTEXT_RX.search(text) and not STRONG_FINANCIAL_ACCESS_RX.search(text):
        reasons.append("non-financial underserved/access context")
    if REGULATORY_RX.search(text) and not REGULATORY_ISSUER_ACTION_RX.search(text):
        reasons.append("generic regulatory/agency context without issuer action")
    return sorted(set(reasons))


def infer_democratization_subcategory(text: str) -> str:
    lower = text.lower()
    if any(term in lower for term in ["alternative", "private market", "private equity", "private credit"]):
        return "private-market or alternative-investment access"
    if any(term in lower for term in ["payment", "money movement", "merchant", "remittance"]):
        return "payments / money movement / SMB commerce access"
    if any(term in lower for term in ["invest", "brokerage", "trading", "financial market"]):
        return "retail investing / brokerage democratization"
    return "generic/other access-expansion"


def infer_unbanked_subcategory(text: str) -> str:
    lower = text.lower()
    if any(term in lower for term in ["credit", "loan", "lending", "mortgage", "borrower"]):
        return "consumer credit access"
    if any(term in lower for term in ["payment", "money movement", "merchant", "remittance"]):
        return "payments / money movement / SMB commerce access"
    if "insurance" in lower:
        return "insurance / benefits access"
    return "financial inclusion / underbanked / underserved"


def positive_rule(row: dict[str, str]) -> tuple[bool, str, str, str]:
    """Return positive flag, rule name, subcategory, notes."""
    text = normalize(row.get("excerpt"))
    phrase = normalize(row.get("phrase")).lower()
    reasons = exclusion_reasons(row)
    housing_phrase = any(term in phrase for term in ["affordable housing", "homeownership", "access to housing"])

    if "fractional share" in phrase and FRACTIONAL_MECHANICS_RX.search(text):
        return False, "", "", "; ".join(reasons)
    if ISSUER_OWN_FUNDING_RX.search(text):
        return False, "", "", "; ".join(reasons)
    if FHLB_ISSUER_LIQUIDITY_RX.search(text):
        return False, "", "", "; ".join(reasons)
    if "affordable housing" in phrase and AFFORDABLE_HOUSING_ACCOUNTING_RX.search(text):
        return False, "", "", "; ".join(reasons)
    if "affordable housing" in phrase and AFFORDABLE_HOUSING_GENERIC_RX.search(text) and not HOUSING_DIRECT_ACCESS_RX.search(text):
        return False, "", "", "; ".join(reasons)
    if ("barrier" in phrase or "level playing field" in phrase) and GENERIC_BARRIERS_RX.search(text):
        return False, "", "", "; ".join(reasons)
    if NON_FINANCIAL_CONTEXT_RX.search(text) and not STRONG_FINANCIAL_ACCESS_RX.search(text):
        return False, "", "", "; ".join(reasons)
    if REGULATORY_RX.search(text) and not REGULATORY_ISSUER_ACTION_RX.search(text):
        return False, "", "", "; ".join(reasons)

    has_beneficiary = bool(BENEFICIARY_RX.search(text))
    has_mechanism = bool(FINANCIAL_MECHANISM_RX.search(text))

    if DEMOCRATIZE_RX.search(text) and DEMO_MECHANISM_RX.search(text) and has_beneficiary:
        return True, "explicit democratized financial access", infer_democratization_subcategory(text), (
            "Democratization wording plus external users and financial mechanism."
        )

    if FINANCIAL_INCLUSION_RX.search(text) and (has_beneficiary or has_mechanism):
        return True, "explicit financial inclusion with beneficiary or mechanism", (
            "financial inclusion / underbanked / underserved"
        ), "Financial-inclusion wording with beneficiary or direct financial mechanism."

    if not housing_phrase and UNBANKED_RX.search(text) and has_mechanism:
        return True, "unbanked/underbanked/underserved with financial mechanism", infer_unbanked_subcategory(text), (
            "Excluded-group language tied to direct financial service mechanism."
        )

    if CREDIT_EXPANSION_RX.search(text) and CREDIT_BENEFICIARY_RX.search(text):
        return True, "expanded access to credit with external beneficiary", "consumer credit access", (
            "Access-to-credit expansion wording plus borrower/customer/community beneficiary."
        )

    if AFFORDABLE_PRODUCT_RX.search(text) and CREDIT_BENEFICIARY_RX.search(text):
        return True, "affordable financial product with beneficiary", "consumer credit access", (
            "Affordable credit/financial-services product tied to external beneficiary."
        )

    if HOMEOWNERSHIP_RX.search(text) and (HOUSING_MECHANISM_RX.search(text) or HOUSING_DIRECT_ACCESS_RX.search(text)):
        return True, "homeownership/housing access with direct housing mechanism", (
            "affordable housing / homeownership access"
        ), "Homeownership or housing-access wording tied to mortgage/borrower/resident/community mechanism."

    if ("institutional" in phrase or "institutional" in text.lower()) and INSTITUTIONAL_ACCESS_RX.search(text):
        return True, "institutional capability explicitly tied to retail/individual access", (
            "private-market or alternative-investment access"
        ), "Institutional capability is explicitly framed as accessible to retail or individual users."

    if (
        ("market access" in phrase or "access to markets" in phrase or "capital markets access" in phrase)
        and MARKET_ACCESS_EXTERNAL_RX.search(text)
        and has_beneficiary
    ):
        return True, "external beneficiary capital-market access", "smaller-issuer capital-market access", (
            "Market-access language identifies external clients/issuers/borrowers as beneficiaries."
        )

    return False, "", "", "; ".join(reasons) if reasons else "No conservative positive rule satisfied."


def evidence_rank(row: dict[str, str]) -> tuple[int, int, str, str]:
    confidence = row.get("evidence_confidence", "")
    high_risk = row.get("high_risk_phrase_flag", "")
    subcat = row.get("narrative_subcategory", "")
    return (
        0 if confidence == "high" else 1,
        1 if high_risk == "yes" else 0,
        f"{NARRATIVE_PRIORITY.get(subcat, 99):02d}",
        row.get("phrase", ""),
    )


def compact(text: str, limit: int = 360) -> str:
    value = normalize(text)
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def round_robin_select(rows: list[dict[str, str]], target: int, bucket_fields: list[str]) -> list[dict[str, str]]:
    buckets: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = "|".join(row.get(field, "") for field in bucket_fields)
        buckets[key].append(row)
    for bucket_rows in buckets.values():
        bucket_rows.sort(key=lambda r: r.get("_sample_sort", ""))

    selected: list[dict[str, str]] = []
    bucket_keys = sorted(buckets)
    while len(selected) < target and bucket_keys:
        next_keys: list[str] = []
        for key in bucket_keys:
            if len(selected) >= target:
                break
            if buckets[key]:
                selected.append(buckets[key].pop(0))
            if buckets[key]:
                next_keys.append(key)
        bucket_keys = next_keys
    return selected


def make_representative_excerpt(
    key: tuple[str, ...],
    evidence_by_filing: dict[tuple[str, ...], list[dict[str, str]]],
    hits_by_filing: dict[tuple[str, ...], list[dict[str, str]]],
) -> str:
    if evidence_by_filing.get(key):
        parts = []
        for ev in sorted(evidence_by_filing[key], key=evidence_rank)[:3]:
            parts.append(
                f"[{ev['section_name']} | {ev['phrase']} | {ev['evidence_rule']}] "
                f"{compact(ev['excerpt'], 260)}"
            )
        return " || ".join(parts)
    if hits_by_filing.get(key):
        parts = []
        for hit in hits_by_filing[key][:3]:
            parts.append(
                f"[NO CANDIDATE: {hit.get('section_name', '')} | {hit.get('phrase', '')}] "
                f"{compact(hit.get('excerpt', ''), 260)}"
            )
        return " || ".join(parts)
    return "No raw phrase hits in extracted filing sections."


def markdown_table(headers: list[str], rows: list[list[str | int]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def main() -> None:
    TREATMENT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    input_hashes_before = {
        "phrase_hits": file_sha256(PHRASE_HITS),
        "classified_v2": file_sha256(V2_CLASSIFIED),
        "tiered_v1": file_sha256(TIERED_CLASSIFIED),
    }

    section_rows = read_csv(FILING_SECTIONS)
    hit_rows = read_csv(PHRASE_HITS)

    filings: dict[tuple[str, ...], dict[str, str]] = {}
    for row in section_rows:
        key = filing_key(row)
        if key not in filings:
            filings[key] = {
                "firm_id": row.get("firm_id", ""),
                "ticker": row.get("ticker", ""),
                "company_name": row.get("company_name", ""),
                "cik": row.get("cik", ""),
                "accession_number": row.get("accession_number", ""),
                "filing_date": row.get("filing_date", ""),
                "filing_year": row.get("filing_year", ""),
            }

    hits_by_filing: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    evidence_by_filing: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    excluded_reasons_by_filing: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    excluded_family_counts: Counter[str] = Counter()

    evidence_rows: list[dict[str, str]] = []
    for hit in hit_rows:
        key = filing_key(hit)
        hits_by_filing[key].append(hit)
        positive, rule, subcategory, notes = positive_rule(hit)
        high_risk, risk_families = is_high_risk(hit)
        if positive:
            confidence = "medium_high" if high_risk else "high"
            ev = {
                "firm_id": hit.get("firm_id", ""),
                "ticker": hit.get("ticker", ""),
                "company_name": hit.get("company_name", ""),
                "cik": hit.get("cik", ""),
                "accession_number": hit.get("accession_number", ""),
                "filing_date": hit.get("filing_date", ""),
                "filing_year": hit.get("filing_year", ""),
                "section_name": hit.get("section_name", ""),
                "phrase": hit.get("phrase", ""),
                "category": hit.get("category", ""),
                "narrative_subcategory": subcategory,
                "excerpt": hit.get("excerpt", ""),
                "evidence_rule": rule,
                "evidence_confidence": confidence,
                "high_risk_phrase_flag": "yes" if high_risk else "no",
                "evidence_notes": notes + (
                    f" High-risk families: {'; '.join(risk_families)}." if risk_families else ""
                ),
            }
            evidence_rows.append(ev)
            evidence_by_filing[key].append(ev)
        else:
            reasons = exclusion_reasons(hit)
            if not reasons and risk_families:
                reasons = [f"high-risk raw phrase did not pass conservative positive rule: {risk_families[0]}"]
            if not reasons:
                reasons = ["raw hit did not satisfy conservative positive rule"]
            for reason in reasons:
                excluded_reasons_by_filing[key][reason] += 1
            for family in risk_families:
                excluded_family_counts[family] += 1

    candidate_rows: list[dict[str, str]] = []
    for key, filing in sorted(filings.items(), key=lambda item: item[0]):
        evidence = sorted(evidence_by_filing.get(key, []), key=evidence_rank)
        positive = bool(evidence)
        subcategories = sorted(
            {row["narrative_subcategory"] for row in evidence},
            key=lambda name: NARRATIVE_PRIORITY.get(name, 99),
        )
        sections = sorted({row["section_name"] for row in evidence})
        high_risk = any(row["high_risk_phrase_flag"] == "yes" for row in evidence)
        if positive:
            strongest_phrase = evidence[0]["phrase"]
            confidence = "medium_high" if high_risk else "high"
            reason = "candidate_only_pending_manual_audit"
        elif not hits_by_filing.get(key):
            strongest_phrase = ""
            confidence = "not_applicable"
            reason = "no_raw_phrase_hits_in_extracted_sections"
        else:
            strongest_phrase = ""
            confidence = "not_applicable"
            reason_counter = excluded_reasons_by_filing.get(key, Counter())
            reason = reason_counter.most_common(1)[0][0] if reason_counter else "no_conservative_evidence"

        candidate_rows.append(
            {
                **filing,
                "conservative_candidate_flag": "yes" if positive else "no",
                "candidate_confidence": confidence,
                "narrative_subcategories_present": "; ".join(subcategories),
                "evidence_hit_count": str(len(evidence)),
                "evidence_section_count": str(len(sections)),
                "strongest_evidence_phrase": strongest_phrase,
                "high_risk_evidence_flag": "yes" if high_risk else "no",
                "exclusion_or_no_candidate_reason": reason,
            }
        )

    candidate_fields = [
        "firm_id",
        "ticker",
        "company_name",
        "cik",
        "accession_number",
        "filing_date",
        "filing_year",
        "conservative_candidate_flag",
        "candidate_confidence",
        "narrative_subcategories_present",
        "evidence_hit_count",
        "evidence_section_count",
        "strongest_evidence_phrase",
        "high_risk_evidence_flag",
        "exclusion_or_no_candidate_reason",
    ]
    evidence_fields = [
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

    write_csv(CANDIDATE_OUT, candidate_fields, candidate_rows)
    write_csv(EVIDENCE_OUT, evidence_fields, evidence_rows)

    yes_rows = [row for row in candidate_rows if row["conservative_candidate_flag"] == "yes"]
    no_rows = [row for row in candidate_rows if row["conservative_candidate_flag"] == "no"]

    for row in yes_rows:
        key = tuple(row[field] for field in FILING_KEY)
        first_evidence = sorted(evidence_by_filing.get(key, []), key=evidence_rank)[0]
        row["_primary_section"] = first_evidence.get("section_name", "")
        row["_primary_subcategory"] = first_evidence.get("narrative_subcategory", "")
        row["_sample_sort"] = (
            ("0" if row["high_risk_evidence_flag"] == "yes" else "1")
            + "|"
            + f"{int(row['evidence_hit_count']):04d}"
            + "|"
            + row["ticker"]
            + "|"
            + row["accession_number"]
        )
    for row in no_rows:
        reason = row["exclusion_or_no_candidate_reason"]
        row["_primary_section"] = ""
        row["_primary_subcategory"] = reason
        row["_sample_sort"] = (
            ("0" if reason != "no_raw_phrase_hits_in_extracted_sections" else "1")
            + "|"
            + row["filing_year"]
            + "|"
            + row["ticker"]
            + "|"
            + row["accession_number"]
        )

    sample_yes = round_robin_select(
        yes_rows,
        100,
        ["filing_year", "_primary_subcategory", "_primary_section"],
    )
    sample_no = round_robin_select(no_rows, 50, ["filing_year", "_primary_subcategory"])
    audit_rows: list[dict[str, str]] = []
    for row in sample_yes + sample_no:
        key = tuple(row[field] for field in FILING_KEY)
        audit_row = {field: row.get(field, "") for field in candidate_fields}
        audit_row["representative_evidence_excerpts"] = make_representative_excerpt(
            key, evidence_by_filing, hits_by_filing
        )
        audit_row["audit_candidate_flag"] = ""
        audit_row["audit_confidence"] = ""
        audit_row["audit_subcategory"] = ""
        audit_row["audit_notes"] = ""
        audit_row["audit_disagreement_flag"] = ""
        audit_rows.append(audit_row)

    audit_fields = candidate_fields + [
        "representative_evidence_excerpts",
        "audit_candidate_flag",
        "audit_confidence",
        "audit_subcategory",
        "audit_notes",
        "audit_disagreement_flag",
    ]
    write_csv(AUDIT_SAMPLE_OUT, audit_fields, audit_rows)

    report_text = build_report(
        candidate_rows,
        evidence_rows,
        excluded_family_counts,
        evidence_by_filing,
        hits_by_filing,
        input_hashes_before,
    )
    REPORT_OUT.write_text(report_text, encoding="utf-8")

    audit_plan_text = build_audit_plan(audit_rows, candidate_rows)
    AUDIT_PLAN_OUT.write_text(audit_plan_text, encoding="utf-8")

    input_hashes_after = {
        "phrase_hits": file_sha256(PHRASE_HITS),
        "classified_v2": file_sha256(V2_CLASSIFIED),
        "tiered_v1": file_sha256(TIERED_CLASSIFIED),
    }
    checkpoint_text = build_checkpoint(
        candidate_rows,
        evidence_rows,
        audit_rows,
        excluded_family_counts,
        input_hashes_before,
        input_hashes_after,
    )
    CHECKPOINT_OUT.write_text(checkpoint_text, encoding="utf-8")

    print(f"Wrote {CANDIDATE_OUT.relative_to(ROOT)} ({len(candidate_rows)} filings)")
    print(f"Wrote {EVIDENCE_OUT.relative_to(ROOT)} ({len(evidence_rows)} evidence rows)")
    print(f"Wrote {AUDIT_SAMPLE_OUT.relative_to(ROOT)} ({len(audit_rows)} audit rows)")
    print(f"Wrote {REPORT_OUT.relative_to(ROOT)}")
    print(f"Wrote {CHECKPOINT_OUT.relative_to(ROOT)}")


def build_report(
    candidate_rows: list[dict[str, str]],
    evidence_rows: list[dict[str, str]],
    excluded_family_counts: Counter[str],
    evidence_by_filing: dict[tuple[str, ...], list[dict[str, str]]],
    hits_by_filing: dict[tuple[str, ...], list[dict[str, str]]],
    input_hashes: dict[str, str],
) -> str:
    yes_count = sum(1 for row in candidate_rows if row["conservative_candidate_flag"] == "yes")
    no_count = len(candidate_rows) - yes_count
    year_counts = Counter(row["filing_year"] for row in candidate_rows if row["conservative_candidate_flag"] == "yes")
    subcat_counts: Counter[str] = Counter()
    for ev in evidence_rows:
        subcat_counts[ev["narrative_subcategory"]] += 1
    section_counts = Counter(ev["section_name"] for ev in evidence_rows)
    phrase_counts = Counter(ev["phrase"] for ev in evidence_rows)
    firm_counts = Counter(
        f"{row['ticker']} ({row['firm_id']})"
        for row in candidate_rows
        if row["conservative_candidate_flag"] == "yes"
    )

    evidence_examples = sorted(evidence_rows, key=evidence_rank)[:25]
    no_examples = []
    for row in candidate_rows:
        if row["conservative_candidate_flag"] != "no":
            continue
        key = tuple(row[field] for field in FILING_KEY)
        no_examples.append(
            [
                row["ticker"],
                row["filing_year"],
                row["exclusion_or_no_candidate_reason"],
                compact(make_representative_excerpt(key, evidence_by_filing, hits_by_filing), 220),
            ]
        )
        if len(no_examples) >= 25:
            break

    lines = [
        "# Conservative Filing Treatment Candidates V1 Report",
        "",
        "Generated by `scripts/build_conservative_filing_treatments_v1.py`.",
        "",
        "## Guardrails",
        "",
        "- These are conservative filing-level candidates only, not final treatment variables.",
        "- V2 full-corpus labels and tiered V1 labels were not used for treatment construction.",
        "- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.",
        "- Raw `data/extracted/phrase_hits.csv` was not modified.",
        "",
        "## Input Integrity",
        "",
        f"- Raw phrase hits SHA256 before build: `{input_hashes['phrase_hits']}`",
        f"- V2 classified SHA256 before build: `{input_hashes['classified_v2']}`",
        f"- Tiered V1 classified SHA256 before build: `{input_hashes['tiered_v1']}`",
        "",
        "## Summary Counts",
        "",
        f"- Total filings considered: {len(candidate_rows):,}",
        f"- Candidate-positive filings: {yes_count:,}",
        f"- Candidate-negative filings: {no_count:,}",
        f"- Candidate evidence rows: {len(evidence_rows):,}",
        "",
        "## Candidate Count By Filing Year",
        "",
        markdown_table(["Filing year", "Candidate filings"], [[k, v] for k, v in sorted(year_counts.items())]),
        "",
        "## Candidate Count By Narrative Subcategory",
        "",
        markdown_table(["Narrative subcategory", "Evidence rows"], subcat_counts.most_common()),
        "",
        "## Candidate Count By Section",
        "",
        markdown_table(["Section", "Evidence rows"], section_counts.most_common()),
        "",
        "## Top Evidence Phrases",
        "",
        markdown_table(["Phrase", "Evidence rows"], phrase_counts.most_common(25)),
        "",
        "## Top Firms By Candidate Filings",
        "",
        markdown_table(["Firm", "Candidate filings"], firm_counts.most_common(25)),
        "",
        "## Excluded High-Risk Phrase Families",
        "",
        markdown_table(["High-risk phrase family", "Excluded raw-hit rows"], excluded_family_counts.most_common()),
        "",
        "## Candidate Evidence Examples",
        "",
        markdown_table(
            ["Ticker", "Year", "Section", "Phrase", "Rule", "Subcategory", "Excerpt"],
            [
                [
                    ev["ticker"],
                    ev["filing_year"],
                    ev["section_name"],
                    ev["phrase"],
                    ev["evidence_rule"],
                    ev["narrative_subcategory"],
                    compact(ev["excerpt"], 180),
                ]
                for ev in evidence_examples
            ],
        ),
        "",
        "## Excluded / No-Candidate Examples",
        "",
        markdown_table(["Ticker", "Year", "Reason", "Representative excerpt"], no_examples),
        "",
        "## Warning",
        "",
        "These filing-level candidates require manual audit before they can be considered final treatment variables. Returns, prices, benchmarks, and empirical performance analysis remain off-limits until the filing-level treatment candidates pass the next validation gate.",
        "",
    ]
    return "\n".join(lines)


def build_audit_plan(audit_rows: list[dict[str, str]], candidate_rows: list[dict[str, str]]) -> str:
    sample_counts = Counter(row["conservative_candidate_flag"] for row in audit_rows)
    year_counts = Counter(row["filing_year"] for row in audit_rows)
    subcat_counts: Counter[str] = Counter()
    for row in audit_rows:
        value = row["narrative_subcategories_present"] or row["exclusion_or_no_candidate_reason"]
        subcat_counts[value] += 1

    lines = [
        "# Conservative Filing Treatment Audit Plan",
        "",
        "## Purpose",
        "",
        "This plan defines the manual audit for conservative filing-level treatment candidates. The audit validates whether filing-level evidence supports candidate access-expansion treatment status under `config/conservative_filing_treatment_rules_v1.md`.",
        "",
        "## Guardrails",
        "",
        "- Audit only the filing-level candidate evidence and representative raw-hit excerpts.",
        "- Do not inspect prices, returns, benchmarks, or future outcomes.",
        "- Do not make SEC requests.",
        "- Do not treat candidate flags as final treatment variables before audit.",
        "",
        "## Sample Design",
        "",
        f"- Total sampled filings: {len(audit_rows):,}",
        f"- Candidate-positive sampled filings: {sample_counts.get('yes', 0):,}",
        f"- Candidate-negative sampled filings: {sample_counts.get('no', 0):,}",
        "- The sample is deterministic and oversamples high-risk evidence, borderline single-evidence filings, and negative filings with raw high-risk phrase hits.",
        "- The sample is round-robin stratified across filing years, narrative subcategories or no-candidate reasons, sections where available, and firms through deterministic accession ordering.",
        "",
        "## Audit Fields",
        "",
        "- `audit_candidate_flag`: yes/no.",
        "- `audit_confidence`: high/medium/low.",
        "- `audit_subcategory`: primary validated subcategory or excluded/non-treatment.",
        "- `audit_notes`: concise rationale based only on filing text excerpts.",
        "- `audit_disagreement_flag`: yes/no compared with constructed candidate flag.",
        "",
        "## Sample Count By Candidate Flag",
        "",
        markdown_table(["Candidate flag", "Sampled filings"], sample_counts.most_common()),
        "",
        "## Sample Count By Filing Year",
        "",
        markdown_table(["Filing year", "Sampled filings"], [[k, v] for k, v in sorted(year_counts.items())]),
        "",
        "## Sample Count By Subcategory Or Reason",
        "",
        markdown_table(["Subcategory or reason", "Sampled filings"], subcat_counts.most_common(30)),
        "",
        "## Validation Gate",
        "",
        "The candidate layer should not be used for return analysis unless the manual audit demonstrates acceptable precision under the conservative treatment definition and documents false negatives among sampled candidate-negative filings.",
        "",
        f"Full candidate universe size: {len(candidate_rows):,} filings.",
        "",
    ]
    return "\n".join(lines)


def build_checkpoint(
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
    year_counts = Counter(row["filing_year"] for row in candidate_rows if row["conservative_candidate_flag"] == "yes")
    subcat_counts = Counter(ev["narrative_subcategory"] for ev in evidence_rows)

    lines = [
        "# CHECKPOINT 17: Conservative Filing Treatment Candidates",
        "",
        "Generated at: 2026-06-29",
        "",
        "## Completed",
        "",
        "- Created conservative filing-level treatment rules.",
        "- Built filing-level candidate flags from raw extracted phrase hits and extracted filing sections.",
        "- Built candidate evidence table preserving hit-level excerpts.",
        "- Wrote candidate construction report.",
        "- Prepared filing-level audit sample and audit plan for the next validation gate.",
        "- Did not fetch prices, compute returns, make SEC requests, modify raw phrase hits, or make empirical performance claims.",
        "- Did not use V2 full-corpus labels or tiered V1 hit-level labels as treatment variables.",
        "",
        "## Files Created",
        "",
        "- `config/conservative_filing_treatment_rules_v1.md`",
        "- `scripts/build_conservative_filing_treatments_v1.py`",
        "- `data/treatments/conservative_filing_treatment_candidates_v1.csv`",
        "- `data/treatments/conservative_filing_treatment_evidence_v1.csv`",
        "- `quality_reports/conservative_filing_treatment_candidates_v1_report.md`",
        "- `data/review/conservative_filing_treatment_audit_sample.csv`",
        "- `quality_reports/conservative_filing_treatment_audit_plan.md`",
        "- `CHECKPOINT_17_CONSERVATIVE_FILING_TREATMENT_CANDIDATES.md`",
        "",
        "## Source File Integrity",
        "",
        f"- Raw `data/extracted/phrase_hits.csv` SHA256 before: `{hashes_before['phrase_hits']}`",
        f"- Raw `data/extracted/phrase_hits.csv` SHA256 after: `{hashes_after['phrase_hits']}`",
        f"- Raw file unchanged: {'yes' if hashes_before['phrase_hits'] == hashes_after['phrase_hits'] else 'no'}",
        f"- V2 classified SHA256 before: `{hashes_before['classified_v2']}`",
        f"- V2 classified SHA256 after: `{hashes_after['classified_v2']}`",
        f"- V2 classified file unchanged: {'yes' if hashes_before['classified_v2'] == hashes_after['classified_v2'] else 'no'}",
        f"- Tiered V1 SHA256 before: `{hashes_before['tiered_v1']}`",
        f"- Tiered V1 SHA256 after: `{hashes_after['tiered_v1']}`",
        f"- Tiered V1 file unchanged: {'yes' if hashes_before['tiered_v1'] == hashes_after['tiered_v1'] else 'no'}",
        "",
        "## Candidate Filing Counts",
        "",
        f"- Total filings considered: {len(candidate_rows):,}",
        f"- Conservative candidate-positive filings: {yes_count:,}",
        f"- Candidate-negative filings: {no_count:,}",
        "",
        "## Evidence Counts",
        "",
        f"- Candidate evidence rows: {len(evidence_rows):,}",
        "",
        "Candidate positives by filing year:",
        "",
        markdown_table(["Filing year", "Candidate filings"], [[k, v] for k, v in sorted(year_counts.items())]),
        "",
        "Candidate evidence by narrative subcategory:",
        "",
        markdown_table(["Narrative subcategory", "Evidence rows"], subcat_counts.most_common()),
        "",
        "## Audit Sample Counts",
        "",
        f"- Total audit sample filings: {len(audit_rows):,}",
        f"- Candidate-positive audit rows: {audit_counts.get('yes', 0):,}",
        f"- Candidate-negative audit rows: {audit_counts.get('no', 0):,}",
        "",
        "## Main Exclusion Rules",
        "",
        "- Exclude fractional-share stock mechanics.",
        "- Exclude institutional-quality/platform language unless explicitly tied to retail or individual investor access.",
        "- Exclude generic market access unless smaller issuers or external clients are beneficiaries.",
        "- Exclude issuer liquidity, issuer funding, issuer access to credit, FHLB advances, and issuer credit-rating contexts.",
        "- Exclude affordable-housing accounting, tax-credit, partnership, portfolio, investment-income, sale, and commitments-table context.",
        "- Exclude generic barriers language in AI, HR, healthcare, sports, regulation, competition, and internal operations.",
        "- Exclude generic ESG, mission, platform, API, infrastructure, or operational language without explicit end-user financial access.",
        "",
        "Excluded high-risk phrase families from raw hits:",
        "",
        markdown_table(["High-risk phrase family", "Excluded raw-hit rows"], excluded_family_counts.most_common()),
        "",
        "## Remaining Construct-Validity Risks",
        "",
        "- Conservative filing-level candidates may still include regulatory or risk-section text that names a beneficiary and mechanism but is not issuer-specific action.",
        "- Affordable-housing language remains difficult where community, development, program-definition, financing, and tax-credit language are adjacent.",
        "- Retail-investor and fractional-investing language can still mix product access with stock mechanics or risk disclosure.",
        "- Filing-level aggregation means one qualifying excerpt marks the filing as a candidate; manual audit must verify whether the evidence is strong enough for treatment construction.",
        "- Company names are blank because the requested construction inputs do not include `company_name`; identifiers are preserved through firm_id, ticker, CIK, accession, and filing date.",
        "",
        "## Guardrail Reminder",
        "",
        "Returns, prices, benchmark outcomes, SEC requests, and empirical performance analysis remain off-limits until filing-level treatment candidates pass audit. These outputs are candidate construction artifacts only and are not final treatment variables.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
