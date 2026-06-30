#!/usr/bin/env python3
"""
Prepare an audit sample from Codex-assisted review-sample labels.

This script is validation-only. It does not fetch prices, run return analysis,
make SEC requests, modify raw phrase hits, or classify all raw hits.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import random
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLASSIFIED_SAMPLE_PATH = PROJECT_ROOT / "data" / "review" / "phrase_hit_review_sample_classified_v1.csv"
AUDIT_SAMPLE_PATH = PROJECT_ROOT / "data" / "review" / "codex_assisted_label_audit_sample.csv"
AUDIT_PLAN_PATH = PROJECT_ROOT / "quality_reports" / "codex_assisted_label_audit_plan.md"
RAW_PHRASE_HITS_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"

SCRIPT_VERSION = "prepare_label_audit_sample_v1"
DEFAULT_SEED = 20260629
POSITIVE_TARGET = 100
NON_POSITIVE_TARGET = 50

AUDIT_FIELDS = [
    "audit_label",
    "audit_confidence",
    "audit_notes",
    "audit_disagreement_flag",
]


@dataclass
class AuditResult:
    eligible_rows: list[dict[str, str]]
    positive_rows: list[dict[str, str]]
    non_positive_rows: list[dict[str, str]]
    selected_rows: list[dict[str, str]]
    raw_hash_before: str
    raw_hash_after: str


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


def stable_key(row: dict[str, str], seed: int, suffix: str = "") -> str:
    raw = "|".join(
        [
            str(seed),
            suffix,
            row.get("hit_id", ""),
            row.get("category", ""),
            row.get("phrase", ""),
            row.get("filing_year", ""),
            row.get("section_name", ""),
            row.get("firm_id", ""),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def grouped(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row.get(field, "")].append(row)
    return groups


def select_stratified(rows: list[dict[str, str]], target: int, seed: int, max_per_firm: int) -> list[dict[str, str]]:
    rng = random.Random(seed)
    ordered = sorted(rows, key=lambda row: stable_key(row, seed))
    selected: dict[str, dict[str, str]] = {}
    firm_counts: Counter[str] = Counter()

    def can_add(row: dict[str, str]) -> bool:
        if row["hit_id"] in selected:
            return False
        firm = row.get("firm_id") or row.get("cik") or row.get("ticker") or "(blank)"
        return firm_counts[firm] < max_per_firm

    def add(row: dict[str, str]) -> bool:
        if len(selected) >= target or not can_add(row):
            return False
        selected[row["hit_id"]] = row
        firm = row.get("firm_id") or row.get("cik") or row.get("ticker") or "(blank)"
        firm_counts[firm] += 1
        return True

    def coverage_pass(field: str, per_group: int) -> None:
        groups = grouped(ordered, field)
        keys = list(groups)
        rng.shuffle(keys)
        for key in keys:
            candidates = sorted(groups[key], key=lambda row: stable_key(row, seed, f"{field}:{key}"))
            added = 0
            for row in candidates:
                if add(row):
                    added += 1
                if added >= per_group or len(selected) >= target:
                    break
            if len(selected) >= target:
                return

    coverage_pass("phrase", 2)
    coverage_pass("category", 6)
    coverage_pass("filing_year", 5)
    coverage_pass("section_name", 8)
    coverage_pass("firm_id", 1)

    for row in ordered:
        if len(selected) >= target:
            break
        add(row)

    if len(selected) < target:
        for row in ordered:
            if row["hit_id"] not in selected:
                selected[row["hit_id"]] = row
            if len(selected) >= target:
                break

    return sorted(selected.values(), key=lambda row: int(row["hit_id"]))


def add_audit_fields(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in rows:
        item = dict(row)
        for field in AUDIT_FIELDS:
            item[field] = ""
        output.append(item)
    return output


def count(rows: list[dict[str, str]], field: str) -> Counter[str]:
    return Counter(row.get(field, "") for row in rows)


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


def write_report(result: AuditResult, seed: int) -> None:
    selected = result.selected_rows
    positives = [row for row in selected if row.get("final_label") == "true_positive_access_expansion"]
    non_positives = [row for row in selected if row.get("final_label") != "true_positive_access_expansion"]
    lines = [
        "# Codex-Assisted Label Audit Plan",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "- Prepared a manual audit sample from Codex-assisted review-sample labels only.",
        "- Excluded all manual calibration rows.",
        "- Did not fetch prices, run return analysis, make SEC requests, load outcome data, modify raw files, or scale classification to all 9,400 hits.",
        f"- Script version: `{SCRIPT_VERSION}`.",
        f"- Deterministic sample seed: {seed}",
        "",
        "## Guardrail Warning",
        "",
        "Treatment construction is not finalized yet. This audit sample is a pre-scaling validation step for the text-treatment variable only.",
        "",
        "## Eligible Rows And Sample Size",
        "",
        f"- Eligible Codex-assisted rows: {len(result.eligible_rows)}",
        f"- Eligible Codex-assisted true-positive rows: {len(result.positive_rows)}",
        f"- Eligible Codex-assisted non-true-positive rows: {len(result.non_positive_rows)}",
        f"- Audit sample size: {len(selected)}",
        f"- Audit true-positive target / actual: {POSITIVE_TARGET} / {len(positives)}",
        f"- Audit non-true-positive target / actual: {NON_POSITIVE_TARGET} / {len(non_positives)}",
        f"- Raw `phrase_hits.csv` SHA256 before: `{result.raw_hash_before}`",
        f"- Raw `phrase_hits.csv` SHA256 after: `{result.raw_hash_after}`",
        f"- Raw file unchanged by this stage: {'yes' if result.raw_hash_before == result.raw_hash_after else 'no'}",
        "",
        "## Counts By Final Label",
        "",
    ]
    lines.extend(markdown_table(["Final label", "Audit rows"], counter_rows(count(selected, "final_label"))))
    lines.extend(["", "## Counts By Category", ""])
    lines.extend(markdown_table(["Category", "Audit rows"], counter_rows(count(selected, "category"))))
    lines.extend(["", "## Counts By Phrase", ""])
    lines.extend(markdown_table(["Phrase", "Audit rows"], counter_rows(count(selected, "phrase"))))
    lines.extend(["", "## Counts By Section", ""])
    lines.extend(markdown_table(["Section", "Audit rows"], counter_rows(count(selected, "section_name"))))
    lines.extend(["", "## Counts By Filing Year", ""])
    year_rows = [[year, str(count(selected, "filing_year")[year])] for year in sorted(count(selected, "filing_year"))]
    lines.extend(markdown_table(["Filing year", "Audit rows"], year_rows))
    lines.extend(
        [
            "",
            "## Why This Audit Sample Is Sufficient Before Scaling",
            "",
            "- The sample audits 150 of 480 Codex-assisted rows, or 31.25% of the Codex-assisted review-sample labels.",
            "- It deliberately oversamples `true_positive_access_expansion` rows, where the main risk is over-calling positives that would later become treatment observations.",
            "- The 50 non-positive rows provide checks for false negatives, label-boundary errors, and confusion among risk, operational, marketing, ambiguous, and false-positive labels.",
            "- Stratification across category, phrase, filing year, section, and firm gives coverage of common wording families and known high-risk phrases before any full-corpus scaling.",
            "- This is sufficient as a pre-scaling validation gate, not as final evidence that the full 9,400-hit corpus is correctly classified.",
            "",
            "## Specific Risks To Check",
            "",
            "- Over-calling true positives where the excerpt lacks an external beneficiary.",
            "- Over-calling true positives where the excerpt lacks a financial-access mechanism.",
            "- `affordable housing` in tax-credit, partnership, accounting, portfolio, or commitments-table context.",
            "- `market access`, `access to markets`, and `capital markets access` in issuer financing, regulatory, competitive, risk, or operational contexts.",
            "- `fractional share` in stock split, merger, issuance, or cash-in-lieu mechanics.",
            "- `institutional quality`, `institutional-grade`, and related phrases in real-estate quality, platform, infrastructure, or internal capability contexts.",
            "- `access to credit` in Item 1A or liquidity-risk language about issuer funding rather than consumers, borrowers, customers, LMI communities, or underserved groups.",
            "- Regulatory or CRA language that lists compliance objectives without issuer action benefiting external financial users.",
            "- Codex-assisted confidence values that look too high for short, noisy, or ambiguous excerpts.",
            "",
            "## Audit Instructions",
            "",
            "- Fill `audit_label`, `audit_confidence`, `audit_notes`, and `audit_disagreement_flag` only after manual review.",
            "- Set `audit_disagreement_flag` to `yes` when audit label or confidence materially differs from the Codex-assisted/final label.",
            "- Do not use returns, prices, later news, litigation, bankruptcies, acquisitions, or external firm events during audit.",
            "- Do not construct treatment variables until audit results are reviewed.",
        ]
    )
    AUDIT_PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_PLAN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def prepare(args: argparse.Namespace) -> AuditResult:
    field_size_limit()
    raw_hash_before = file_sha256(RAW_PHRASE_HITS_PATH)
    rows, fields = read_csv(Path(args.input))
    if not rows:
        raise ValueError("classified sample is empty")
    eligible = [row for row in rows if row.get("label_source") == "codex_assisted"]
    positives = [row for row in eligible if row.get("final_label") == "true_positive_access_expansion"]
    non_positives = [row for row in eligible if row.get("final_label") != "true_positive_access_expansion"]
    if len(positives) < POSITIVE_TARGET:
        raise ValueError(f"not enough Codex-assisted true-positive rows: {len(positives)}")
    if len(non_positives) < NON_POSITIVE_TARGET:
        raise ValueError(f"not enough Codex-assisted non-positive rows: {len(non_positives)}")

    selected_positive = select_stratified(positives, POSITIVE_TARGET, args.seed, max_per_firm=8)
    selected_non_positive = select_stratified(non_positives, NON_POSITIVE_TARGET, args.seed + 17, max_per_firm=5)
    selected = sorted(selected_positive + selected_non_positive, key=lambda row: int(row["hit_id"]))
    selected_with_audit = add_audit_fields(selected)
    write_csv(Path(args.output), selected_with_audit, fields + AUDIT_FIELDS)
    raw_hash_after = file_sha256(RAW_PHRASE_HITS_PATH)
    result = AuditResult(
        eligible_rows=eligible,
        positive_rows=positives,
        non_positive_rows=non_positives,
        selected_rows=selected_with_audit,
        raw_hash_before=raw_hash_before,
        raw_hash_after=raw_hash_after,
    )
    write_report(result, args.seed)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a Codex-assisted label audit sample.")
    parser.add_argument("--input", default=str(CLASSIFIED_SAMPLE_PATH))
    parser.add_argument("--output", default=str(AUDIT_SAMPLE_PATH))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = prepare(args)
    selected = result.selected_rows
    positives = sum(1 for row in selected if row.get("final_label") == "true_positive_access_expansion")
    non_positives = len(selected) - positives
    print(
        "Prepared audit sample: "
        f"eligible={len(result.eligible_rows)}, sample={len(selected)}, "
        f"positive={positives}, non_positive={non_positives}"
    )
    print(f"Wrote {Path(args.output).resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {AUDIT_PLAN_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
