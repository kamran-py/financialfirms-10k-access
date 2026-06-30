#!/usr/bin/env python3
"""
Classify raw phrase hits into stricter tiered treatment-candidate labels.

This stage is classification-only. It does not fetch prices, compute returns,
make SEC requests, modify raw phrase hits, or use full-corpus V2 as a
treatment variable.
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
RAW_PHRASE_HITS_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"
V2_CLASSIFIED_PATH = PROJECT_ROOT / "data" / "classified" / "phrase_hits_classified_v2.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "classified" / "phrase_hits_tiered_v1.csv"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "tiered_classification_v1_report.md"
GUIDELINES_PATH = PROJECT_ROOT / "config" / "tiered_treatment_classification_guidelines_v1.md"

CLASSIFIER_VERSION = "tiered_treatment_classification_guidelines_v1"
SCRIPT_VERSION = "classify_phrase_hits_tiered_v1"

TIER_1 = "tier_1_conservative"
TIER_2 = "tier_2_broader_validated"
TIER_3 = "tier_3_exploratory"
EXCLUDED = "excluded_non_treatment"

OUTPUT_FIELDS = [
    "tiered_label",
    "tier_1_treatment_candidate",
    "tier_2_treatment_candidate",
    "tier_3_exploratory_signal",
    "narrative_subcategory",
    "tiered_confidence",
    "high_risk_phrase_flag",
    "high_risk_phrase_family",
    "exclusion_reason",
    "classification_notes",
    "classifier_version",
]

SUB_EXCLUDED = "excluded / non-treatment"
SUB_FIN_INCL = "financial inclusion / underbanked / underserved"
SUB_CREDIT = "consumer credit access"
SUB_HOUSING = "affordable housing / homeownership access"
SUB_RETAIL = "retail investing / brokerage democratization"
SUB_PRIVATE = "private-market or alternative-investment access"
SUB_PAYMENTS = "payments / money movement / SMB commerce access"
SUB_INSURANCE = "insurance / benefits access"
SUB_SMALL_ISSUER = "smaller-issuer capital-market access"
SUB_FEE = "fee / cost / minimum-reduction framing"
SUB_OTHER = "generic/other access-oriented disclosure"

VALID_LABELS = {TIER_1, TIER_2, TIER_3, EXCLUDED}
VALID_CONFIDENCE = {"high", "medium", "low"}

HIGH_RISK_MAP = {
    "affordable housing": "affordable housing",
    "fractional share": "fractional share",
    "market access": "market access / access to markets / capital markets access",
    "access to markets": "market access / access to markets / capital markets access",
    "capital markets access": "market access / access to markets / capital markets access",
    "institutional quality": "institutional quality / institutional-grade / institutional caliber / institutional level",
    "institutional-grade": "institutional quality / institutional-grade / institutional caliber / institutional level",
    "institutional caliber": "institutional quality / institutional-grade / institutional caliber / institutional level",
    "institutional level": "institutional quality / institutional-grade / institutional caliber / institutional level",
    "access to credit": "access to credit",
    "lower barriers": "lower/reduce/remove/eliminate barriers",
    "reduce barriers": "lower/reduce/remove/eliminate barriers",
    "reduced barriers": "lower/reduce/remove/eliminate barriers",
    "removing barriers": "lower/reduce/remove/eliminate barriers",
    "eliminate barriers": "lower/reduce/remove/eliminate barriers",
}


@dataclass(frozen=True)
class Decision:
    tiered_label: str
    confidence: str
    subcategory: str
    exclusion_reason: str
    notes: str


def field_size_limit() -> None:
    csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
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


def clean_text(*values: str) -> str:
    return re.sub(r"\s+", " ", " ".join(values).lower()).strip()


def row_text(row: dict[str, str]) -> str:
    return clean_text(
        row.get("phrase", ""),
        row.get("section_name", ""),
        row.get("matched_text", ""),
        row.get("excerpt", ""),
    )


def has_any(text: str, terms: list[str] | tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def phrase_of(row: dict[str, str]) -> str:
    return row.get("phrase", "").strip().lower()


def category_of(row: dict[str, str]) -> str:
    return row.get("category", "").strip().lower()


def section_of(row: dict[str, str]) -> str:
    return row.get("section_name", "").strip().lower()


def high_risk_family(phrase: str, text: str, section: str) -> str:
    family = HIGH_RISK_MAP.get(phrase, "none")
    if family == "none" and has_any(text, ["community reinvestment act", " cra ", "cra rule", "regulatory"]):
        family = "CRA/regulatory language"
    if "risk" in section and has_any(text, ["access", "credit", "market", "funding", "liquidity"]):
        if family == "none":
            family = "risk-section access language"
        else:
            family = family + "; risk-section access language"
    return family


def is_high_risk(phrase: str, text: str, section: str) -> bool:
    return high_risk_family(phrase, text, section) != "none"


BENEFICIARY_TERMS = [
    "consumer", "consumers", "customer", "customers", "member", "members",
    "borrower", "borrowers", "investor", "investors", "retail", "individual",
    "individuals", "underserved", "underbanked", "unbanked", "low- and moderate-income",
    "low and moderate income", "low-to-moderate-income", "low income", "low-income",
    "lmi", "community", "communities", "small business", "small businesses",
    "smb", "smbs", "merchant", "merchants", "homeowner", "homeowners",
    "homebuyer", "homebuyers", "renter", "renters", "resident", "residents",
    "families", "households", "clients", "users", "smaller issuers",
    "issuers", "municipal", "municipalities", "emerging companies",
    "micro, small and medium", "msme",
]

MECHANISM_TERMS = [
    "credit", "loan", "loans", "lending", "underwriting", "mortgage", "mortgages",
    "banking", "bank", "financial services", "financial products", "payments",
    "payment", "money movement", "remittance", "commerce", "merchant",
    "investment", "investing", "brokerage", "trading", "capital markets",
    "markets", "market access", "homeownership", "housing", "insurance",
    "benefits", "savings", "wealth", "affordable", "low-cost", "low cost",
    "finance", "financing", "securities", "bonds", "bond", "retirement",
]

EXPANSION_TERMS = [
    "expand access", "expanded access", "expanding access", "broaden access",
    "broader access", "democratize", "democratizing", "democratized",
    "lower barriers", "lowering barriers", "reduce barriers", "reduced barriers",
    "remove barriers", "removing barriers", "financial inclusion", "inclusive finance",
    "provide access", "provides access", "providing access", "make available",
    "made available", "available to", "access to affordable", "affordable access",
    "low-cost", "low cost", "as little as", "minimum", "availability of financial",
    "promote the availability", "serve underserved", "serving underserved",
    "accessibility and affordability", "equal access",
]

ISSUER_OWN_CONTEXT = [
    "our access to credit", "company's access to credit", "corporation's access to credit",
    "access to credit facilities", "our access to credit facilities", "access to funding",
    "our access to funding", "access to liquidity", "our liquidity", "our funding",
    "our credit ratings", "credit ratings", "our cost of capital", "cost of capital",
    "our access to capital", "access to debt markets", "our ability to access",
    "access to financing", "fhlb advances", "fhlb borrowing", "fhlb of",
    "parent company relies upon capital markets access", "our capital markets access",
    "leverage our scale and capital markets access", "credit facility", "credit facilities",
]

ACCOUNTING_CONTEXT = [
    "tax credit", "tax credits", "low income housing tax credit", "lihtc",
    "partnership investment", "partnership investments", "affordable housing partnerships",
    "equity method", "investment income", "net investment income", "portfolio",
    "returns", "return primarily", "fair value", "carrying value", "gain on the closing",
    "gain from the sale", "sale of the affordable housing", "sold affordable housing",
    "commitments", "unfunded", "effective tax rate", "income tax", "tax benefits",
    "impairment", "expense", "net loss from affordable housing", "table",
]

STOCK_MECHANICS = [
    "reverse stock split", "stock split", "fractional shares rounded", "cash in lieu",
    "cash-in-lieu", "exchange ratio", "conversion", "converted into", "dividend reinvestment",
    "whole shares", "fractional share of the fixed", "mining pool", "share issuance",
]

OPERATIONAL_CONTEXT = [
    "platform", "infrastructure", "custody", "custodian", "api", "analytics",
    "advisor", "analyst", "process", "security", "technology", "internal",
    "data access", "exchange connectivity", "market data", "fees for market access",
    "regulatory permissions", "distribution", "branch access to markets",
    "prime brokers", "direct market access to markets", "property quality",
    "real estate", "institutional investors", "hedge funds", "high net worth",
    "hNW".lower(), "sponsors", "assets and sponsors",
]

NON_FINANCIAL_CONTEXT = [
    "healthcare", "health care", "patient", "patients", "sports", "stadium",
    "education", "students", "career readiness", "hr", "human resources",
    "employee inclusion", "employees", "ai innovation", "artificial intelligence",
    "internal inclusion", "website access", "data access", "culinary training",
    "health and wellness", "medical research",
]

RISK_TERMS = [
    "could adversely", "would adversely", "may adversely", "adverse effect",
    "material adverse", "risk", "risks", "inability", "unable to access",
    "loss of access", "reduced access", "deterioration", "volatility",
    "liquidity", "funding", "capital resources", "economic conditions",
    "competition", "competitors", "competitive pressure", "downward pricing pressure",
]


def has_beneficiary(text: str) -> bool:
    return has_any(text, BENEFICIARY_TERMS)


def has_mechanism(text: str) -> bool:
    return has_any(text, MECHANISM_TERMS)


def has_expansion(text: str) -> bool:
    return has_any(text, EXPANSION_TERMS)


def issuer_own(text: str) -> bool:
    return has_any(text, ISSUER_OWN_CONTEXT)


def accounting_artifact(text: str) -> bool:
    return has_any(text, ACCOUNTING_CONTEXT)


def stock_mechanics(text: str) -> bool:
    return has_any(text, STOCK_MECHANICS)


def non_financial(text: str) -> bool:
    return has_any(text, NON_FINANCIAL_CONTEXT) and not has_any(
        text,
        ["financial services", "credit", "loan", "banking", "payments", "investing", "insurance", "mortgage"],
    )


def risk_context(text: str, section: str) -> bool:
    return "risk" in section or has_any(text, RISK_TERMS)


def regulatory_context(text: str) -> bool:
    return has_any(
        text,
        [
            "community reinvestment act", "cra rule", "cra proposal", "cra regulations",
            "regulatory agencies", "bank regulatory agencies", "federal banking agencies",
            "fdic", "occ", "federal reserve", "cfpb", "agency", "agencies",
            "fio", "rule requires", "final rule", "regulatory relief act",
        ],
    )


def issuer_action_context(text: str) -> bool:
    return has_any(
        text,
        [
            "we offer", "we provide", "we continue to offer", "we invest in",
            "we finance", "we originate", "we make loans", "we serve",
            "our customers", "our products", "our services", "our platform",
            "the bank maintains", "the bank provides", "the bank offers",
            "merchants bank has acquired", "we have established",
        ],
    )


def direct_access_phrase(text: str) -> bool:
    return has_expansion(text) or has_any(
        text,
        [
            "access to credit", "access to affordable credit", "access to investing",
            "access to investment", "access to markets", "market access",
            "fractional shares", "retail access", "financial inclusion",
            "unbanked", "underbanked", "underserved", "homeownership access",
        ],
    )


def subcategory_for(row: dict[str, str], text: str) -> str:
    phrase = phrase_of(row)
    category = category_of(row)
    if has_any(text, ["payment", "payments", "money movement", "merchant", "commerce", "msme", "small and medium enterprises"]):
        return SUB_PAYMENTS
    if has_any(text, ["underbanked", "unbanked", "underserved", "financial inclusion", "lmi", "low- and moderate-income", "low income", "low-income"]):
        if has_any(text, ["credit", "loan", "lending", "mortgage"]) and "financial inclusion" not in phrase:
            return SUB_CREDIT
        return SUB_FIN_INCL
    if has_any(text, ["credit", "loan", "loans", "lending", "borrower", "borrowers", "underwriting"]):
        if has_any(text, ["housing", "mortgage", "homeownership", "homeowners", "home loans"]):
            return SUB_HOUSING
        return SUB_CREDIT
    if has_any(text, ["affordable housing", "housing", "homeownership", "mortgage", "home loans", "renters", "residents", "affordable units"]):
        return SUB_HOUSING
    if has_any(text, ["private market", "private markets", "alternative assets", "alternatives", "secondary liquidity", "institutional-grade", "institutional quality", "institutional caliber"]):
        if has_any(text, ["retail", "individual", "consumer", "non-institutional"]):
            return SUB_PRIVATE
    if has_any(text, ["retail investor", "retail investors", "individual investors", "brokerage", "trading", "fractional", "direct indexing", "investing"]):
        return SUB_RETAIL
    if has_any(text, ["insurance", "benefits", "retirement"]):
        return SUB_INSURANCE
    if has_any(text, ["smaller issuers", "issuers", "municipal", "capital markets", "bond", "bonds"]):
        return SUB_SMALL_ISSUER
    if has_any(text, ["low-cost", "low cost", "fees", "minimum", "as little as", "lower barriers", "reduced barriers"]):
        return SUB_FEE
    if category:
        if "retail access" in category:
            return SUB_RETAIL
        if "homeownership" in category:
            return SUB_HOUSING
        if "credit" in category:
            return SUB_CREDIT
        if "financial inclusion" in category or "underserved" in category:
            return SUB_FIN_INCL
    return SUB_OTHER


def positive_decision(tier: str, confidence: str, subcategory: str, notes: str) -> Decision:
    return Decision(tier, confidence, subcategory, "", notes)


def exclude(confidence: str, reason: str, notes: str) -> Decision:
    return Decision(EXCLUDED, confidence, SUB_EXCLUDED, reason, notes)


def exploratory(confidence: str, subcategory: str, reason: str, notes: str) -> Decision:
    return Decision(TIER_3, confidence, subcategory, reason, notes)


def classify_affordable_housing(row: dict[str, str], text: str) -> Decision:
    access_terms = [
        "housing loans", "mortgage", "homeownership", "homeowners", "homebuyer",
        "renters", "residents", "affordable units", "low-to-moderate-income families",
        "low- and moderate-income housing", "low income individuals", "low-income individuals",
        "construction and permanent financing", "preservation and construction",
        "financing for the preservation", "affordable housing programs for",
        "provide funding for affordable housing programs", "funding for affordable housing",
        "community housing access",
    ]
    strong_access = has_any(text, access_terms)
    if accounting_artifact(text) and not strong_access:
        return exclude("high", "accounting_tax_credit_or_portfolio_context", "Affordable-housing wording appears in tax-credit, portfolio, investment-income, commitment, sale, or accounting context.")
    if strong_access and has_any(text, ["low-to-moderate-income", "low- and moderate-income", "low income", "low-income", "families", "individuals", "renters", "residents", "homeowners", "borrowers", "affordable units"]):
        return positive_decision(TIER_1, "high", SUB_HOUSING, "Affordable-housing access names external beneficiaries and a direct housing finance/access mechanism.")
    if strong_access:
        return positive_decision(TIER_2, "medium", SUB_HOUSING, "Affordable-housing context is access-related but relies on regulatory/program context or partial beneficiary detail.")
    if has_any(text, ["community development and affordable housing", "affordable housing and homeownership"]):
        return exploratory("low", SUB_HOUSING, "generic_or_philanthropic_housing_signal", "Affordable-housing wording is access-adjacent but lacks a concrete financial-access mechanism.")
    return exclude("high", "affordable_housing_without_access_mechanism", "Affordable-housing phrase lacks explicit external housing-access or financing mechanism.")


def classify_fractional_share(row: dict[str, str], text: str) -> Decision:
    if stock_mechanics(text):
        return exclude("high", "stock_or_crypto_mechanics", "Fractional-share wording is stock split, share mechanics, cash-in-lieu, or mining-pool allocation context.")
    if has_any(text, ["buy fractional shares", "fractional shares of a stock", "fractional investing", "as little as $", "as little as $1"]) and has_any(text, ["customers", "retail", "individual", "consumer"]):
        return positive_decision(TIER_1, "high", SUB_RETAIL, "Fractional investing access is explicitly available to external customers or retail investors.")
    if has_any(text, ["fractional shares", "fractional investing"]) and has_beneficiary(text):
        return positive_decision(TIER_2, "medium", SUB_RETAIL, "Fractional-share wording appears tied to external investing access.")
    return exclude("high", "fractional_share_not_investing_access", "Fractional-share wording does not describe end-user fractional investing access.")


def classify_market_access(row: dict[str, str], text: str, section: str) -> Decision:
    external_capital = has_any(
        text,
        [
            "smaller issuers", "less well-known issuers", "municipal", "issuers to gain",
            "provide issuers", "issuers with capital markets advice", "customers obtain",
            "customers to search", "customers receive", "all market participants",
            "retail investors", "individual investors", "direct market access at a low cost",
        ],
    )
    if issuer_own(text) or has_any(text, ["our access to markets", "our access to capital markets", "we rely upon capital markets access"]):
        return exclude("high", "issuer_market_access_or_funding", "Market-access wording concerns issuer funding, liquidity, or own market access.")
    if risk_context(text, section) and not external_capital:
        return exclude("high", "risk_or_competitor_market_access", "Market-access wording appears in risk, competitor, macro, or liquidity context without external access-oriented activity.")
    if has_any(text, ["prime brokers", "market data", "fees for market access", "exchange fees", "regulatory", "permission", "connectivity", "branch access to markets"]) and not external_capital:
        return exclude("high", "operational_or_regulatory_market_access", "Market-access wording is operational, exchange-connectivity, regulatory, or distribution language.")
    if external_capital and has_any(text, ["smaller issuers", "less well-known issuers", "all market participants", "direct market access at a low cost", "customers obtain"]):
        return positive_decision(TIER_1, "high", SUB_SMALL_ISSUER, "Market-access wording identifies external beneficiaries and a direct financial-market access mechanism.")
    if external_capital:
        return positive_decision(TIER_2, "medium", SUB_SMALL_ISSUER, "Market-access wording is externally directed but context is less direct or partially advisory.")
    return exploratory("low", SUB_SMALL_ISSUER, "broad_market_access_signal", "Market-access phrase is broad and not validated as treatment.")


def classify_institutional(row: dict[str, str], text: str) -> Decision:
    non_inst_user = has_any(text, ["retail", "individual", "consumer", "small business", "underserved", "non-institutional", "customers"])
    access_bridge = has_any(text, ["available to", "access", "provides", "offering", "expand", "consumer solutions", "retail investors"])
    if has_any(text, ["commercial real estate", "real estate", "property", "assets and sponsors", "custodian", "custody", "api", "platform", "analyst", "advisor analytics", "hedge funds", "institutional investors", "high net worth", "hNW".lower(), "process quality"]):
        if not (non_inst_user and access_bridge and has_any(text, ["retail investors", "consumer solutions", "available to retail"])):
            return exclude("high", "institutional_quality_operational_or_property_context", "Institutional-quality wording describes property, custody, platform, analyst process, or institutional/HNW services.")
    if non_inst_user and access_bridge and has_any(text, ["institutional-grade", "institutional quality", "institutional caliber"]):
        return positive_decision(TIER_2, "medium", subcategory_for(row, text), "Institutional-quality capability appears linked to non-institutional external users.")
    return exclude("high", "institutional_quality_without_end_user_access", "Institutional-quality wording lacks explicit non-institutional end-user financial access.")


def classify_access_to_credit(row: dict[str, str], text: str, section: str) -> Decision:
    external_credit_terms = [
        "consumer access to credit", "small businesses", "borrowers", "customers access to credit",
        "customers access", "members", "low-to-moderate-income", "low- and moderate-income",
        "underserved", "lmi", "access to mortgage credit", "student borrowers",
        "veterans, consumers, and homeowners", "offer access to credit products",
        "lack of access to credit from traditional lenders", "equal access to credit",
        "expand access to credit", "expanded access to credit", "expanding access to credit",
    ]
    if issuer_own(text) or (risk_context(text, section) and not has_any(text, external_credit_terms)):
        return exclude("high", "issuer_credit_or_risk_context", "Credit-access wording concerns issuer funding, credit ratings, credit facilities, liquidity, or risk context.")
    if regulatory_context(text) and not issuer_action_context(text) and has_any(text, external_credit_terms):
        return positive_decision(TIER_2, "medium", SUB_CREDIT, "Regulatory or CRA credit-access language names external beneficiaries and mechanism but lacks issuer-specific action.")
    if has_any(text, external_credit_terms) and has_any(text, ["customers access to credit", "offer access to credit products", "expand access to credit", "consumer access to credit", "equal access to credit"]):
        return positive_decision(TIER_1, "high", SUB_CREDIT, "Credit-access wording explicitly identifies external beneficiaries and credit mechanism.")
    if has_any(text, external_credit_terms):
        return positive_decision(TIER_2, "medium", SUB_CREDIT, "Credit-access wording identifies external beneficiaries but relies on regulatory or contextual access language.")
    if has_any(text, ["credit", "access"]) and has_beneficiary(text):
        return exploratory("low", SUB_CREDIT, "credit_access_signal_needs_review", "Credit-access wording is access-adjacent but not validated under strict rule.")
    return exclude("high", "credit_access_without_external_beneficiary", "Credit-access wording lacks external borrower/customer beneficiary.")


def classify_barriers(row: dict[str, str], text: str, section: str) -> Decision:
    if has_any(text, ["barriers to affiliation", "barriers to entry", "product listing", "listing standards", "innovation act", "ai may lower barriers", "competitors"]) and not has_any(text, ["borrowers", "home loans", "market access", "customers", "investors"]):
        return exclude("high", "non_end_user_barrier_context", "Barrier language concerns affiliation, listing, competitor entry, technology, or legislation rather than end-user financial access.")
    if has_any(text, ["borrowers who are seeking access to home loans", "barriers to mortgage loans", "barriers to mortgage refinancing"]):
        return positive_decision(TIER_2, "medium", SUB_HOUSING, "Barrier reduction is tied to mortgage or home-loan access for borrowers.")
    if has_beneficiary(text) and has_mechanism(text) and has_expansion(text):
        return positive_decision(TIER_2, "medium", subcategory_for(row, text), "Barrier-reduction wording identifies beneficiary and financial mechanism.")
    if has_expansion(text):
        return exploratory("low", subcategory_for(row, text), "broad_barrier_reduction_signal", "Barrier-reduction wording is broad but lacks strict beneficiary/mechanism support.")
    return exclude("medium", "barrier_language_without_financial_access", "Barrier phrase lacks explicit financial-access activity.")


def classify_financial_inclusion(row: dict[str, str], text: str, section: str) -> Decision:
    if non_financial(text):
        return exclude("high", "non_financial_access_context", "Underserved or inclusion wording is non-financial.")
    if regulatory_context(text) and not issuer_action_context(text) and has_beneficiary(text) and has_mechanism(text):
        return positive_decision(TIER_2, "medium", subcategory_for(row, text), "Regulatory inclusion/access language identifies beneficiary and financial mechanism but lacks issuer-specific action.")
    if has_any(text, ["unbanked", "underbanked"]) and has_any(text, ["payments", "electronic transactions", "financial services", "banking", "credit", "loan", "customers", "consumers"]):
        return positive_decision(TIER_1, "high", SUB_FIN_INCL, "Unbanked/underbanked external users are tied to financial services or transactions.")
    if has_any(text, ["underserved consumers", "underserved borrowers", "underserved communities", "underserved markets"]) and has_mechanism(text):
        return positive_decision(TIER_1, "high", subcategory_for(row, text), "Underserved external beneficiaries are tied to a financial-access mechanism.")
    if has_any(text, ["financial inclusion"]) and has_mechanism(text) and has_beneficiary(text):
        return positive_decision(TIER_2, "medium", SUB_FIN_INCL, "Financial-inclusion language names beneficiary and financial mechanism.")
    if has_any(text, ["financial inclusion"]) and has_mechanism(text):
        return positive_decision(TIER_2, "medium", SUB_FIN_INCL, "Financial-inclusion wording is tied to a financial-access mechanism.")
    if has_any(text, ["underserved", "underbanked", "unbanked"]):
        return exploratory("low", SUB_FIN_INCL, "inclusion_signal_without_clear_mechanism", "Inclusion wording lacks a direct financial-access mechanism.")
    return exclude("medium", "no_financial_inclusion_mechanism", "Inclusion phrase lacks financial-access support.")


def classify_retail_investing(row: dict[str, str], text: str, section: str) -> Decision:
    if stock_mechanics(text):
        return exclude("high", "stock_mechanics", "Investing phrase appears in stock or share mechanics.")
    if risk_context(text, section) and has_any(text, ["halted", "restricted trading", "short positions", "adverse", "risk"]) and not has_any(text, ["products specifically designed", "services to individual retail investors"]):
        return exclude("medium", "retail_investor_risk_context", "Retail-investor wording appears in risk or market-structure context rather than access-oriented disclosure.")
    if has_any(text, ["products specifically designed for direct investment", "services to individual retail investors", "designed for individual investors", "brokerage services", "direct indexing for schwab's retail investors", "retail investors who primarily access our products"]):
        return positive_decision(TIER_1, "high", SUB_RETAIL, "Retail or individual investors are directly offered investing, brokerage, or investment products.")
    if has_any(text, ["retail investors", "individual investors"]) and has_any(text, ["available", "access", "products", "services", "distributed", "brokerage", "investing"]):
        return positive_decision(TIER_2, "medium", SUB_RETAIL, "Retail/individual investor language is tied to financial products or services.")
    if has_any(text, ["retail investors", "individual investors"]):
        return exploratory("low", SUB_RETAIL, "retail_investor_signal_without_access_mechanism", "Retail/individual investor wording lacks explicit access-oriented disclosure mechanism.")
    return exclude("medium", "retail_phrase_without_investing_access", "Retail investing phrase lacks treatment support.")


def classify_general(row: dict[str, str], text: str, section: str) -> Decision:
    category = category_of(row)
    phrase = phrase_of(row)
    if non_financial(text):
        return exclude("high", "non_financial_access_context", "Access wording concerns non-financial education, healthcare, HR, AI, sports, website, data, or philanthropy context.")
    if issuer_own(text):
        return exclude("high", "issuer_funding_liquidity_or_market_access", "Access wording concerns issuer funding, liquidity, credit, or own market access.")
    if accounting_artifact(text) or stock_mechanics(text):
        return exclude("high", "accounting_table_or_stock_mechanics", "Phrase appears in accounting, table, portfolio, tax-credit, investment-income, or stock-mechanics context.")
    if "risk" in section and not (has_beneficiary(text) and has_mechanism(text) and direct_access_phrase(text)):
        return exclude("medium", "risk_disclosure_only", "Risk-section language lacks clear external financial-access activity.")
    if "underserved" in category or "financial inclusion" in category:
        return classify_financial_inclusion(row, text, section)
    if "retail access" in category:
        return classify_retail_investing(row, text, section)
    if "credit" in category:
        return classify_access_to_credit(row, text, section)
    if "homeownership" in category:
        return classify_affordable_housing(row, text) if "affordable housing" in phrase else (
            positive_decision(TIER_1, "high", SUB_HOUSING, "Housing/homeownership wording clearly identifies external access.") if has_beneficiary(text) and has_mechanism(text) and direct_access_phrase(text)
            else exploratory("low", SUB_HOUSING, "housing_signal_needs_review", "Housing phrase is access-adjacent but lacks strict support.")
        )
    if has_beneficiary(text) and has_mechanism(text) and has_expansion(text):
        if has_any(text, ["customers", "consumers", "borrowers", "small businesses", "underserved", "underbanked", "unbanked", "retail investors"]):
            return positive_decision(TIER_1, "high", subcategory_for(row, text), "External beneficiary, direct financial mechanism, and access-oriented disclosure wording are explicit.")
        return positive_decision(TIER_2, "medium", subcategory_for(row, text), "External beneficiary and financial mechanism are present but context is less direct.")
    if has_beneficiary(text) and has_mechanism(text):
        return positive_decision(TIER_2, "medium", subcategory_for(row, text), "External beneficiary and financial mechanism are present, but expansion language is not explicit enough for Tier 1.")
    if has_mechanism(text) or direct_access_phrase(text):
        return exploratory("low", subcategory_for(row, text), "raw_access_signal_not_validated", "Raw phrase is access-related but lacks strict beneficiary/mechanism support.")
    return exclude("medium", "no_external_financial_access_mechanism", "No clear external beneficiary and direct financial-access mechanism.")


def classify(row: dict[str, str]) -> Decision:
    text = row_text(row)
    phrase = phrase_of(row)
    section = section_of(row)
    if phrase == "affordable housing":
        return classify_affordable_housing(row, text)
    if phrase == "fractional share":
        return classify_fractional_share(row, text)
    if phrase in {"market access", "access to markets", "capital markets access"}:
        return classify_market_access(row, text, section)
    if phrase in {"institutional quality", "institutional-grade", "institutional caliber", "institutional level", "institutional grade"}:
        return classify_institutional(row, text)
    if phrase == "access to credit":
        return classify_access_to_credit(row, text, section)
    if phrase in {"lower barriers", "reduce barriers", "reduced barriers", "removing barriers", "eliminate barriers", "remove barriers", "reducing barriers", "eliminating barriers"}:
        return classify_barriers(row, text, section)
    return classify_general(row, text, section)


def apply_decision(row: dict[str, str], decision: Decision) -> dict[str, str]:
    item = dict(row)
    phrase = phrase_of(row)
    text = row_text(row)
    section = section_of(row)
    family = high_risk_family(phrase, text, section)
    item["tiered_label"] = decision.tiered_label
    item["tier_1_treatment_candidate"] = "yes" if decision.tiered_label == TIER_1 else "no"
    item["tier_2_treatment_candidate"] = "yes" if decision.tiered_label in {TIER_1, TIER_2} else "no"
    item["tier_3_exploratory_signal"] = "yes" if decision.tiered_label in {TIER_1, TIER_2, TIER_3} else "no"
    item["narrative_subcategory"] = decision.subcategory
    item["tiered_confidence"] = decision.confidence
    item["high_risk_phrase_flag"] = "yes" if family != "none" else "no"
    item["high_risk_phrase_family"] = family
    item["exclusion_reason"] = decision.exclusion_reason if decision.tiered_label == EXCLUDED else ""
    item["classification_notes"] = decision.notes
    item["classifier_version"] = CLASSIFIER_VERSION
    return item


def validate_rows(rows: list[dict[str, str]], raw_fields: list[str], raw_hash_before: str, raw_hash_after: str, v2_hash_before: str, v2_hash_after: str) -> None:
    if len(rows) != 9400:
        raise ValueError(f"expected 9,400 classified rows, found {len(rows)}")
    if raw_hash_before != raw_hash_after:
        raise ValueError("raw phrase_hits.csv hash changed")
    if v2_hash_before != v2_hash_after:
        raise ValueError("V2 classified file hash changed")
    for index, row in enumerate(rows, start=1):
        for field in OUTPUT_FIELDS:
            if field in {"exclusion_reason"}:
                continue
            if not row.get(field):
                raise ValueError(f"row {index} missing {field}")
        if row["tiered_label"] not in VALID_LABELS:
            raise ValueError(f"row {index} invalid tiered_label {row['tiered_label']}")
        if row["tiered_confidence"] not in VALID_CONFIDENCE:
            raise ValueError(f"row {index} invalid tiered_confidence {row['tiered_confidence']}")
        if row["classifier_version"] != CLASSIFIER_VERSION:
            raise ValueError(f"row {index} invalid classifier_version")
        if row["high_risk_phrase_flag"] not in {"yes", "no"}:
            raise ValueError(f"row {index} invalid high_risk_phrase_flag")
        if row["high_risk_phrase_family"] == "":
            raise ValueError(f"row {index} missing high_risk_phrase_family")
        if row["tiered_label"] == EXCLUDED and not row.get("exclusion_reason"):
            raise ValueError(f"row {index} excluded row missing exclusion_reason")
    for field in raw_fields:
        if field not in rows[0]:
            raise ValueError(f"raw field missing from output: {field}")


def counter_by(rows: list[dict[str, str]], field: str) -> Counter[str]:
    return Counter(row.get(field, "") for row in rows)


def filing_count(rows: list[dict[str, str]], label: str) -> int:
    return len({(row.get("cik", ""), row.get("accession_number", "")) for row in rows if row.get("tiered_label") == label})


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return lines


def counter_rows(counter: Counter[str]) -> list[list[str]]:
    return [[key or "(blank)", str(value)] for key, value in sorted(counter.items(), key=lambda item: (-item[1], item[0]))]


def tier_rate_rows(rows: list[dict[str, str]], field: str) -> list[list[str]]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        grouped[row.get(field, "")][row.get("tiered_label", "")] += 1
    out: list[list[str]] = []
    for key in sorted(grouped):
        counts = grouped[key]
        total = sum(counts.values())
        tier1 = counts[TIER_1]
        tier2 = counts[TIER_2]
        tier3 = counts[TIER_3]
        excluded = counts[EXCLUDED]
        out.append([
            key or "(blank)",
            str(total),
            str(tier1),
            str(tier2),
            str(tier3),
            str(excluded),
            f"{tier1 / total:.1%}" if total else "0.0%",
            f"{(tier1 + tier2) / total:.1%}" if total else "0.0%",
        ])
    return out


def high_risk_rate_rows(rows: list[dict[str, str]]) -> list[list[str]]:
    high = [row for row in rows if row.get("high_risk_phrase_flag") == "yes"]
    return tier_rate_rows(high, "high_risk_phrase_family")


def top_firms(rows: list[dict[str, str]], label: str, limit: int = 20) -> list[list[str]]:
    counts: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        if row.get("tiered_label") == label:
            counts[(row.get("firm_id", ""), row.get("ticker", ""), row.get("cik", ""))] += 1
    return [[firm, ticker, cik, str(count)] for (firm, ticker, cik), count in counts.most_common(limit)]


def examples(rows: list[dict[str, str]], predicate, limit: int = 20) -> list[list[str]]:
    out: list[list[str]] = []
    for row in rows:
        if predicate(row):
            excerpt = re.sub(r"\s+", " ", row.get("excerpt", "")).strip()[:220]
            out.append([
                row.get("ticker", ""),
                row.get("filing_year", ""),
                row.get("section_name", ""),
                row.get("phrase", ""),
                row.get("tiered_label", ""),
                row.get("narrative_subcategory", ""),
                row.get("classification_notes", ""),
                excerpt,
            ])
            if len(out) >= limit:
                break
    return out


def write_report(rows: list[dict[str, str]], raw_before: str, raw_after: str, v2_before: str, v2_after: str) -> None:
    counts = counter_by(rows, "tiered_label")
    tier1_rows = [row for row in rows if row.get("tiered_label") == TIER_1]
    tier2_rows = [row for row in rows if row.get("tiered_label") == TIER_2]
    tier3_rows = [row for row in rows if row.get("tiered_label") == TIER_3]
    excluded_rows = [row for row in rows if row.get("tiered_label") == EXCLUDED]
    output_hash = file_sha256(OUTPUT_PATH) if OUTPUT_PATH.exists() else ""
    lines = [
        "# Tiered Classification V1 Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope And Guardrails",
        "",
        "- Classified the full raw phrase-hit corpus under `tiered_treatment_classification_guidelines_v1`.",
        "- Used `data/extracted/phrase_hits.csv` as the classification input.",
        "- Did not use full-corpus V2 as a treatment variable.",
        "- Outputs are treatment candidates only until validated by a post-classification audit.",
        "- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.",
        f"- Script version: `{SCRIPT_VERSION}`.",
        f"- Classifier version: `{CLASSIFIER_VERSION}`.",
        "",
        "## File Integrity",
        "",
        f"- Raw `phrase_hits.csv` SHA256 before: `{raw_before}`",
        f"- Raw `phrase_hits.csv` SHA256 after: `{raw_after}`",
        f"- Raw file unchanged: {'yes' if raw_before == raw_after else 'no'}",
        f"- V2 classified file SHA256 before: `{v2_before}`",
        f"- V2 classified file SHA256 after: `{v2_after}`",
        f"- V2 classified file unchanged: {'yes' if v2_before == v2_after else 'no'}",
        f"- Tiered output SHA256: `{output_hash}`",
        "",
        "## Row Counts",
        "",
        f"- Total rows classified: {len(rows)}",
        f"- Tier 1 row count: {len(tier1_rows)}",
        f"- Tier 1 unique filing count: {filing_count(rows, TIER_1)}",
        f"- Tier 2 row count: {len(tier2_rows)}",
        f"- Tier 2 unique filing count: {filing_count(rows, TIER_2)}",
        f"- Tier 3 row count: {len(tier3_rows)}",
        f"- Excluded row count: {len(excluded_rows)}",
        "",
        "## Counts By Tiered Label",
        "",
    ]
    lines.extend(markdown_table(["Tiered label", "Rows"], counter_rows(counts)))
    lines.extend(["", "## Counts By Narrative Subcategory", ""])
    lines.extend(markdown_table(["Narrative subcategory", "Rows"], counter_rows(counter_by(rows, "narrative_subcategory"))))
    lines.extend(["", "## Counts By Phrase", ""])
    lines.extend(markdown_table(["Phrase", "Total rows", "Tier 1", "Tier 2", "Tier 3", "Excluded", "Tier 1 rate", "Tier 1+2 rate"], tier_rate_rows(rows, "phrase")))
    lines.extend(["", "## Counts By Phrase Family", ""])
    lines.extend(markdown_table(["Phrase family", "Total rows", "Tier 1", "Tier 2", "Tier 3", "Excluded", "Tier 1 rate", "Tier 1+2 rate"], tier_rate_rows(rows, "category")))
    lines.extend(["", "## Counts By Section", ""])
    lines.extend(markdown_table(["Section", "Total rows", "Tier 1", "Tier 2", "Tier 3", "Excluded", "Tier 1 rate", "Tier 1+2 rate"], tier_rate_rows(rows, "section_name")))
    lines.extend(["", "## Counts By Filing Year", ""])
    lines.extend(markdown_table(["Filing year", "Total rows", "Tier 1", "Tier 2", "Tier 3", "Excluded", "Tier 1 rate", "Tier 1+2 rate"], tier_rate_rows(rows, "filing_year")))
    lines.extend(["", "## High-Risk Phrase Positive Rates By Tier", ""])
    lines.extend(markdown_table(["High-risk family", "Total rows", "Tier 1", "Tier 2", "Tier 3", "Excluded", "Tier 1 rate", "Tier 1+2 rate"], high_risk_rate_rows(rows)))
    lines.extend(["", "## Top Firms By Tier 1 Count", ""])
    lines.extend(markdown_table(["Firm ID", "Ticker", "CIK", "Tier 1 rows"], top_firms(rows, TIER_1)) if tier1_rows else ["- No Tier 1 rows."])
    lines.extend(["", "## Top Firms By Tier 2 Count", ""])
    lines.extend(markdown_table(["Firm ID", "Ticker", "CIK", "Tier 2 rows"], top_firms(rows, TIER_2)) if tier2_rows else ["- No Tier 2 rows."])
    lines.extend(["", "## Examples Of Tier 1 Rows", ""])
    lines.extend(markdown_table(["Ticker", "Year", "Section", "Phrase", "Tier", "Subcategory", "Notes", "Excerpt start"], examples(rows, lambda r: r.get("tiered_label") == TIER_1, 20)) if tier1_rows else ["- No Tier 1 rows."])
    lines.extend(["", "## Examples Of Excluded High-Risk Rows", ""])
    lines.extend(markdown_table(["Ticker", "Year", "Section", "Phrase", "Tier", "Subcategory", "Notes", "Excerpt start"], examples(rows, lambda r: r.get("tiered_label") == EXCLUDED and r.get("high_risk_phrase_flag") == "yes", 20)))
    lines.extend(
        [
            "",
            "## Remaining Construct-Validity Risks",
            "",
            "- Tier 1 and Tier 2 are treatment candidates only and require a post-tiered audit before use.",
            "- High-risk phrase families may still contain false positives despite stricter defaults.",
            "- Conservative Tier 1 rules prioritize precision over recall and may understate access-oriented disclosure language.",
            "- Narrative subcategories should be reviewed for support before any filing-level treatment aggregation.",
            "- V2 failed validation and was not used as the treatment variable in this classifier.",
            "- Returns remain off-limits until Tier 1 and Tier 2 classification is validated.",
            "",
            "## Warning",
            "",
            "These counts are classification diagnostics and treatment-candidate counts, not empirical findings. No return outcomes, prices, benchmarks, or performance data were loaded.",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify raw phrase hits into tiered treatment candidates.")
    parser.add_argument("--input", default=str(RAW_PHRASE_HITS_PATH))
    parser.add_argument("--output", default=str(OUTPUT_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    field_size_limit()
    if not GUIDELINES_PATH.exists():
        raise FileNotFoundError(GUIDELINES_PATH)
    raw_path = Path(args.input)
    output_path = Path(args.output)
    raw_before = file_sha256(raw_path)
    v2_before = file_sha256(V2_CLASSIFIED_PATH)
    raw_rows, raw_fields = read_csv(raw_path)
    classified = [apply_decision(row, classify(row)) for row in raw_rows]
    write_csv(output_path, classified, raw_fields + OUTPUT_FIELDS)
    raw_after = file_sha256(raw_path)
    v2_after = file_sha256(V2_CLASSIFIED_PATH)
    validate_rows(classified, raw_fields, raw_before, raw_after, v2_before, v2_after)
    write_report(classified, raw_before, raw_after, v2_before, v2_after)
    counts = Counter(row["tiered_label"] for row in classified)
    print(
        "Tiered classification complete: "
        f"rows={len(classified)}, tier1={counts[TIER_1]}, tier2={counts[TIER_2]}, "
        f"tier3={counts[TIER_3]}, excluded={counts[EXCLUDED]}"
    )
    print(f"Wrote {output_path.resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
