#!/usr/bin/env python3
"""
Prepare a post-scale spot-check sample from full-corpus V2 classifications.

This script validates classification quality only. It does not fetch prices,
compute returns, make SEC requests, modify raw phrase hits, or modify the
classified full-corpus file.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import random
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLASSIFIED_PATH = PROJECT_ROOT / "data" / "classified" / "phrase_hits_classified_v2.csv"
RAW_PHRASE_HITS_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"
SAMPLE_PATH = PROJECT_ROOT / "data" / "review" / "full_corpus_v2_spotcheck_sample.csv"
PLAN_PATH = PROJECT_ROOT / "quality_reports" / "full_corpus_v2_spotcheck_plan.md"

SCRIPT_VERSION = "prepare_full_corpus_classification_spotcheck_v1"
DEFAULT_SEED = 20260629
POSITIVE_TARGET = 100
NON_POSITIVE_TARGET = 50

HIGH_RISK_PHRASES = {
    "affordable housing",
    "fractional share",
    "market access",
    "access to markets",
    "capital markets access",
    "institutional quality",
    "institutional-grade",
    "institutional caliber",
    "institutional level",
    "access to credit",
    "lower barriers",
    "reduce barriers",
    "reduced barriers",
    "removing barriers",
    "eliminate barriers",
}

SPOTCHECK_FIELDS = [
    "spotcheck_label",
    "spotcheck_confidence",
    "spotcheck_notes",
    "spotcheck_disagreement_flag",
]


def field_size_limit() -> None:
    csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        for index, row in enumerate(rows, start=1):
            row["_row_number"] = str(index)
        return rows, list(reader.fieldnames or [])


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


def stable_key(row: dict[str, str], seed: int, salt: str = "") -> str:
    raw = "|".join(
        [
            str(seed),
            salt,
            row.get("_row_number", ""),
            row.get("firm_id", ""),
            row.get("accession_number", ""),
            row.get("section_name", ""),
            row.get("filing_year", ""),
            row.get("phrase", ""),
            row.get("final_label_v2", ""),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def grouped(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        out[row.get(field, "")].append(row)
    return out


def true_positive_filing_count(rows: list[dict[str, str]]) -> int:
    return len(
        {
            (row.get("cik", ""), row.get("accession_number", ""))
            for row in rows
            if row.get("final_label_v2") == "true_positive_access_expansion"
        }
    )


def top_positive_firms(rows: list[dict[str, str]], limit: int = 20) -> set[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        if row.get("final_label_v2") == "true_positive_access_expansion":
            counts[row.get("firm_id", "")] += 1
    return {firm for firm, _ in counts.most_common(limit)}


def select_rows(
    rows: list[dict[str, str]],
    target: int,
    seed: int,
    high_tp_firms: set[str],
    positive_sample: bool,
) -> list[dict[str, str]]:
    rng = random.Random(seed + (1 if positive_sample else 2))
    selected: dict[str, dict[str, str]] = {}
    firm_counts: Counter[str] = Counter()
    max_per_firm = 10 if positive_sample else 5

    def can_add(row: dict[str, str]) -> bool:
        row_id = row["_row_number"]
        if row_id in selected:
            return False
        return firm_counts[row.get("firm_id", "")] < max_per_firm

    def add(row: dict[str, str]) -> bool:
        if len(selected) >= target or not can_add(row):
            return False
        selected[row["_row_number"]] = row
        firm_counts[row.get("firm_id", "")] += 1
        return True

    # Force coverage across sections and filing years where feasible.
    for field in ["section_name", "filing_year"]:
        groups = grouped(rows, field)
        keys = list(groups)
        rng.shuffle(keys)
        for key in keys:
            candidates = sorted(groups[key], key=lambda r: stable_key(r, seed, f"cover:{field}:{key}"))
            for row in candidates:
                if add(row):
                    break

    # Force high-risk phrase coverage, with positives emphasizing high-risk rows still labeled positive.
    high_risk_groups = grouped([row for row in rows if row.get("phrase", "").lower() in HIGH_RISK_PHRASES], "phrase")
    for phrase in sorted(high_risk_groups):
        quota = 4 if positive_sample else 3
        added = 0
        candidates = sorted(high_risk_groups[phrase], key=lambda r: stable_key(r, seed, f"risk:{phrase}"))
        for row in candidates:
            if add(row):
                added += 1
            if added >= quota:
                break

    # Oversample firms with the largest full-corpus true-positive counts.
    high_firm_rows = [row for row in rows if row.get("firm_id", "") in high_tp_firms]
    for row in sorted(high_firm_rows, key=lambda r: stable_key(r, seed, "high-tp-firms")):
        if len(selected) >= int(target * 0.65):
            break
        add(row)

    # Fill with high-risk rows first, then deterministic broad coverage.
    preferred = [row for row in rows if row.get("phrase", "").lower() in HIGH_RISK_PHRASES]
    for row in sorted(preferred, key=lambda r: stable_key(r, seed, "risk-fill")):
        if len(selected) >= int(target * 0.8):
            break
        add(row)
    for row in sorted(rows, key=lambda r: stable_key(r, seed, "final-fill")):
        if len(selected) >= target:
            break
        add(row)

    if len(selected) < target:
        for row in sorted(rows, key=lambda r: stable_key(r, seed, "uncapped-fill")):
            if row["_row_number"] not in selected:
                selected[row["_row_number"]] = row
            if len(selected) >= target:
                break

    return sorted(selected.values(), key=lambda row: int(row["_row_number"]))


def add_blank_spotcheck_fields(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        item = dict(row)
        for field in SPOTCHECK_FIELDS:
            item[field] = ""
        out.append(item)
    return out


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


def write_plan(
    all_rows: list[dict[str, str]],
    sample_rows: list[dict[str, str]],
    raw_before: str,
    raw_after: str,
    classified_before: str,
    classified_after: str,
    seed: int,
) -> None:
    positives = [row for row in sample_rows if row.get("final_label_v2") == "true_positive_access_expansion"]
    non_positives = [row for row in sample_rows if row.get("final_label_v2") != "true_positive_access_expansion"]
    high_risk = [row for row in sample_rows if row.get("phrase", "").lower() in HIGH_RISK_PHRASES]
    high_risk_positive = [
        row
        for row in sample_rows
        if row.get("phrase", "").lower() in HIGH_RISK_PHRASES
        and row.get("final_label_v2") == "true_positive_access_expansion"
    ]
    high_tp_firms = top_positive_firms(all_rows)
    high_tp_firm_sample = [row for row in sample_rows if row.get("firm_id", "") in high_tp_firms]

    lines = [
        "# Full Corpus V2 Spot-Check Sample Plan",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope And Guardrails",
        "",
        "- Prepared a 150-row post-scale spot-check sample from `data/classified/phrase_hits_classified_v2.csv`.",
        "- This stage validates full-corpus classification quality only.",
        "- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.",
        "- Raw `phrase_hits.csv` and classified `phrase_hits_classified_v2.csv` were not modified.",
        f"- Script version: `{SCRIPT_VERSION}`.",
        f"- Deterministic seed: `{seed}`.",
        "",
        "## Input Integrity",
        "",
        f"- Raw `phrase_hits.csv` SHA256 before: `{raw_before}`",
        f"- Raw `phrase_hits.csv` SHA256 after: `{raw_after}`",
        f"- Raw file unchanged: {'yes' if raw_before == raw_after else 'no'}",
        f"- Classified `phrase_hits_classified_v2.csv` SHA256 before: `{classified_before}`",
        f"- Classified `phrase_hits_classified_v2.csv` SHA256 after: `{classified_after}`",
        f"- Classified file unchanged: {'yes' if classified_before == classified_after else 'no'}",
        "",
        "## Full Corpus Counts",
        "",
        f"- Full classified rows: {len(all_rows)}",
        f"- Full-corpus true-positive rows: {sum(1 for row in all_rows if row.get('final_label_v2') == 'true_positive_access_expansion')}",
        f"- Full-corpus true-positive filings: {true_positive_filing_count(all_rows)}",
        "",
        "## Sample Counts",
        "",
        f"- Spot-check sample size: {len(sample_rows)}",
        f"- Sampled full-corpus positives: {len(positives)}",
        f"- Sampled full-corpus non-positives: {len(non_positives)}",
        f"- Sampled high-risk phrase rows: {len(high_risk)}",
        f"- Sampled high-risk phrase rows labeled true positive: {len(high_risk_positive)}",
        f"- Sampled rows from top true-positive firms: {len(high_tp_firm_sample)}",
        "",
        "## Sample Label Distribution Before Spot Check",
        "",
    ]
    lines.extend(markdown_table(["Final label V2", "Rows"], counter_rows(count(sample_rows, "final_label_v2"))))
    lines.extend(["", "## Sample Section Coverage", ""])
    lines.extend(markdown_table(["Section", "Rows"], counter_rows(count(sample_rows, "section_name"))))
    lines.extend(["", "## Sample Filing-Year Coverage", ""])
    lines.extend(markdown_table(["Filing year", "Rows"], counter_rows(count(sample_rows, "filing_year"))))
    lines.extend(["", "## Sample High-Risk Phrase Coverage", ""])
    lines.extend(markdown_table(["Phrase", "Rows"], counter_rows(count(high_risk, "phrase"))))
    lines.extend(["", "## Sample Category Coverage", ""])
    lines.extend(markdown_table(["Category", "Rows"], counter_rows(count(sample_rows, "category"))))
    lines.extend(["", "## Planned Audit Fields", ""])
    lines.extend(
        [
            "- `spotcheck_label`",
            "- `spotcheck_confidence`",
            "- `spotcheck_notes`",
            "- `spotcheck_disagreement_flag`",
            "",
            "## Audit Instructions",
            "",
            "- Use only the excerpt and `classification_guidelines_v3.md`.",
            "- Do not use returns, prices, later news, outside firm knowledge, or external events.",
            "- Set `spotcheck_disagreement_flag = yes` only when `spotcheck_label` differs from `final_label_v2`.",
            "- Keep notes concise and specific.",
        ]
    )
    PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLAN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def prepare_sample(rows: list[dict[str, str]], seed: int) -> list[dict[str, str]]:
    positives = [row for row in rows if row.get("final_label_v2") == "true_positive_access_expansion"]
    non_positives = [row for row in rows if row.get("final_label_v2") != "true_positive_access_expansion"]
    if len(positives) < POSITIVE_TARGET:
        raise ValueError(f"not enough positives for target: {len(positives)}")
    if len(non_positives) < NON_POSITIVE_TARGET:
        raise ValueError(f"not enough non-positives for target: {len(non_positives)}")
    high_tp_firms = top_positive_firms(rows)
    selected = select_rows(positives, POSITIVE_TARGET, seed, high_tp_firms, True)
    selected.extend(select_rows(non_positives, NON_POSITIVE_TARGET, seed, high_tp_firms, False))
    selected = sorted(selected, key=lambda row: int(row["_row_number"]))
    return add_blank_spotcheck_fields(selected)


def validate_sample(rows: list[dict[str, str]]) -> None:
    if len(rows) != POSITIVE_TARGET + NON_POSITIVE_TARGET:
        raise ValueError(f"expected 150 rows, found {len(rows)}")
    positives = sum(1 for row in rows if row.get("final_label_v2") == "true_positive_access_expansion")
    non_positives = len(rows) - positives
    if positives != POSITIVE_TARGET or non_positives != NON_POSITIVE_TARGET:
        raise ValueError(f"expected 100 positives and 50 non-positives, found {positives}/{non_positives}")
    for row in rows:
        for field in SPOTCHECK_FIELDS:
            if row.get(field, None) != "":
                raise ValueError(f"spot-check field should be blank before audit: {field}")
    sections = {row.get("section_name", "") for row in rows}
    years = {row.get("filing_year", "") for row in rows}
    if len(sections) < 3:
        raise ValueError("sample does not cover all three sections")
    if not set(str(year) for year in range(2015, 2026)).issubset(years):
        raise ValueError("sample does not cover all filing years 2015-2025")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare full-corpus V2 classification spot-check sample.")
    parser.add_argument("--input", default=str(CLASSIFIED_PATH))
    parser.add_argument("--output", default=str(SAMPLE_PATH))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    field_size_limit()
    raw_before = file_sha256(RAW_PHRASE_HITS_PATH)
    classified_before = file_sha256(Path(args.input))
    rows, fields = read_csv(Path(args.input))
    sample = prepare_sample(rows, args.seed)
    validate_sample(sample)
    output_fields = fields + SPOTCHECK_FIELDS
    write_csv(Path(args.output), sample, output_fields)
    raw_after = file_sha256(RAW_PHRASE_HITS_PATH)
    classified_after = file_sha256(Path(args.input))
    if raw_before != raw_after:
        raise ValueError("raw phrase_hits.csv hash changed")
    if classified_before != classified_after:
        raise ValueError("classified phrase_hits_classified_v2.csv hash changed")
    write_plan(rows, sample, raw_before, raw_after, classified_before, classified_after, args.seed)
    print(
        "Prepared full-corpus V2 spot-check sample: "
        f"rows={len(sample)}, positives={sum(1 for row in sample if row['final_label_v2'] == 'true_positive_access_expansion')}, "
        f"non_positives={sum(1 for row in sample if row['final_label_v2'] != 'true_positive_access_expansion')}"
    )
    print(f"Wrote {Path(args.output).resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {PLAN_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
