#!/usr/bin/env python3
"""
Prepare a targeted validation sample from V2 Codex-assisted labels.

This script does not fetch prices, run return analysis, make SEC requests,
scale classification to all raw hits, or modify data/extracted/phrase_hits.csv.
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
CLASSIFIED_V2_PATH = PROJECT_ROOT / "data" / "review" / "phrase_hit_review_sample_classified_v2.csv"
MANUAL_CALIBRATION_PATH = PROJECT_ROOT / "data" / "review" / "manual_calibration_labels_20260629.csv"
MANUAL_AUDIT_PATH = PROJECT_ROOT / "data" / "review" / "codex_assisted_label_audit_sample_audited_20260629.csv"
VALIDATION_SAMPLE_PATH = PROJECT_ROOT / "data" / "review" / "v2_codex_assisted_validation_sample.csv"
VALIDATION_PLAN_PATH = PROJECT_ROOT / "quality_reports" / "v2_validation_sample_plan.md"
RAW_PHRASE_HITS_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"

SCRIPT_VERSION = "prepare_v2_validation_sample_v1"
DEFAULT_SEED = 20260629
POSITIVE_TARGET = 75
NON_POSITIVE_TARGET = 25

HIGH_RISK_PHRASES = {
    "institutional quality",
    "institutional-grade",
    "institutional caliber",
    "institutional level",
    "market access",
    "access to markets",
    "capital markets access",
    "affordable housing",
    "access to credit",
    "fractional share",
    "lower barriers",
    "reduce barriers",
    "reduced barriers",
    "removing barriers",
    "eliminate barriers",
}

VALIDATION_FIELDS = [
    "validation_label",
    "validation_confidence",
    "validation_notes",
    "validation_disagreement_flag",
]


@dataclass
class SampleResult:
    eligible_rows: list[dict[str, str]]
    positive_rows: list[dict[str, str]]
    non_positive_rows: list[dict[str, str]]
    selected_rows: list[dict[str, str]]
    raw_hash_before: str
    raw_hash_after: str
    manual_ids: set[str]


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


def stable_key(row: dict[str, str], seed: int, salt: str = "") -> str:
    raw = "|".join(
        [
            str(seed),
            salt,
            row.get("hit_id", ""),
            row.get("phrase", ""),
            row.get("category", ""),
            row.get("filing_year", ""),
            row.get("section_name", ""),
            row.get("firm_id", ""),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_ids(path: Path, field: str = "hit_id") -> set[str]:
    rows, _ = read_csv(path)
    return {row.get(field, "") for row in rows if row.get(field, "")}


def grouped(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row.get(field, "")].append(row)
    return groups


def select_targeted(rows: list[dict[str, str]], target: int, seed: int, max_per_firm: int) -> list[dict[str, str]]:
    rng = random.Random(seed)
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

    high_risk = [row for row in rows if row.get("phrase", "") in HIGH_RISK_PHRASES]
    for row in sorted(high_risk, key=lambda r: stable_key(r, seed, "high-risk")):
        if len(selected) >= max(1, target // 2):
            break
        add(row)

    for field, per_group in [("phrase", 2), ("category", 5), ("section_name", 6), ("filing_year", 4), ("firm_id", 1)]:
        groups = grouped(rows, field)
        keys = list(groups)
        rng.shuffle(keys)
        for key in keys:
            added = 0
            candidates = sorted(groups[key], key=lambda r: stable_key(r, seed, f"{field}:{key}"))
            for row in candidates:
                if add(row):
                    added += 1
                if added >= per_group or len(selected) >= target:
                    break
            if len(selected) >= target:
                break

    ordered = sorted(rows, key=lambda r: stable_key(r, seed, "fill"))
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

    return sorted(selected.values(), key=lambda r: int(r["hit_id"]))


def add_blank_validation(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        item = dict(row)
        for field in VALIDATION_FIELDS:
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


def write_plan(result: SampleResult, seed: int) -> None:
    selected = result.selected_rows
    positives = [r for r in selected if r.get("final_label_v2") == "true_positive_access_expansion"]
    non_positives = [r for r in selected if r.get("final_label_v2") != "true_positive_access_expansion"]
    high_risk_selected = [r for r in selected if r.get("phrase", "") in HIGH_RISK_PHRASES]
    lines = [
        "# V2 Codex-Assisted Validation Sample Plan",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "- Prepared a targeted validation sample from V2 Codex-assisted labels only.",
        "- Excluded manual calibration and prior manual audit rows.",
        "- Did not fetch prices, compute returns, make SEC requests, make empirical claims, scale classification to all 9,400 raw hits, or modify raw files.",
        f"- Script version: `{SCRIPT_VERSION}`.",
        f"- Deterministic seed: {seed}",
        "",
        "## Guardrail Warning",
        "",
        "Treatment construction is not finalized. This sample validates the text-treatment classifier only.",
        "",
        "## Eligibility And Sample Size",
        "",
        f"- Eligible V2 Codex-assisted rows: {len(result.eligible_rows)}",
        f"- Eligible V2 true-positive rows: {len(result.positive_rows)}",
        f"- Eligible V2 non-positive rows: {len(result.non_positive_rows)}",
        f"- Validation sample rows: {len(selected)}",
        f"- Target / actual V2 positives: {POSITIVE_TARGET} / {len(positives)}",
        f"- Target / actual V2 non-positives: {NON_POSITIVE_TARGET} / {len(non_positives)}",
        f"- High-risk phrase rows selected: {len(high_risk_selected)}",
        f"- Raw `phrase_hits.csv` SHA256 before: `{result.raw_hash_before}`",
        f"- Raw `phrase_hits.csv` SHA256 after: `{result.raw_hash_after}`",
        f"- Raw file unchanged by this stage: {'yes' if result.raw_hash_before == result.raw_hash_after else 'no'}",
        "",
        "## Counts By V2 Final Label",
        "",
    ]
    lines.extend(markdown_table(["V2 final label", "Rows"], counter_rows(count(selected, "final_label_v2"))))
    lines.extend(["", "## Counts By Category", ""])
    lines.extend(markdown_table(["Category", "Rows"], counter_rows(count(selected, "category"))))
    lines.extend(["", "## Counts By Phrase", ""])
    lines.extend(markdown_table(["Phrase", "Rows"], counter_rows(count(selected, "phrase"))))
    lines.extend(["", "## Counts By Section", ""])
    lines.extend(markdown_table(["Section", "Rows"], counter_rows(count(selected, "section_name"))))
    lines.extend(["", "## Counts By Filing Year", ""])
    year_counts = count(selected, "filing_year")
    lines.extend(markdown_table(["Filing year", "Rows"], [[year, str(year_counts[year])] for year in sorted(year_counts)]))
    lines.extend(["", "## Counts By High-Risk Phrase", ""])
    hr_counts = count(high_risk_selected, "phrase")
    lines.extend(markdown_table(["High-risk phrase", "Rows"], counter_rows(hr_counts)) if hr_counts else ["- None"])
    lines.extend(
        [
            "",
            "## Validation Instructions",
            "",
            "- Fill `validation_label`, `validation_confidence`, `validation_notes`, and `validation_disagreement_flag` using only the excerpt and `config/classification_guidelines_v3.md`.",
            "- Set `validation_disagreement_flag` to `yes` when `validation_label` differs from `final_label_v2`; otherwise set it to `no`.",
            "- Do not use returns, prices, later news, outside firm knowledge, litigation, bankruptcies, acquisitions, or external events.",
            "- Keep notes concise but specific.",
        ]
    )
    VALIDATION_PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PLAN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def prepare(args: argparse.Namespace) -> SampleResult:
    field_size_limit()
    raw_before = file_sha256(RAW_PHRASE_HITS_PATH)
    rows, fields = read_csv(Path(args.input))
    manual_ids = load_ids(MANUAL_CALIBRATION_PATH) | load_ids(MANUAL_AUDIT_PATH)
    eligible = [
        row for row in rows
        if row.get("label_source_v2") == "codex_assisted_v2" and row.get("hit_id", "") not in manual_ids
    ]
    positives = [row for row in eligible if row.get("final_label_v2") == "true_positive_access_expansion"]
    non_positives = [row for row in eligible if row.get("final_label_v2") != "true_positive_access_expansion"]
    if len(positives) < POSITIVE_TARGET:
        raise ValueError(f"not enough eligible positives: {len(positives)}")
    if len(non_positives) < NON_POSITIVE_TARGET:
        raise ValueError(f"not enough eligible non-positives: {len(non_positives)}")

    selected_pos = select_targeted(positives, POSITIVE_TARGET, args.seed, max_per_firm=8)
    selected_non = select_targeted(non_positives, NON_POSITIVE_TARGET, args.seed + 23, max_per_firm=5)
    selected = sorted(selected_pos + selected_non, key=lambda r: int(r["hit_id"]))
    selected_blank = add_blank_validation(selected)
    write_csv(Path(args.output), selected_blank, fields + VALIDATION_FIELDS)
    raw_after = file_sha256(RAW_PHRASE_HITS_PATH)
    result = SampleResult(
        eligible_rows=eligible,
        positive_rows=positives,
        non_positive_rows=non_positives,
        selected_rows=selected_blank,
        raw_hash_before=raw_before,
        raw_hash_after=raw_after,
        manual_ids=manual_ids,
    )
    write_plan(result, args.seed)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare targeted V2 Codex-assisted validation sample.")
    parser.add_argument("--input", default=str(CLASSIFIED_V2_PATH))
    parser.add_argument("--output", default=str(VALIDATION_SAMPLE_PATH))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = prepare(args)
    selected = result.selected_rows
    pos = sum(1 for r in selected if r.get("final_label_v2") == "true_positive_access_expansion")
    non = len(selected) - pos
    print(
        "Prepared V2 validation sample: "
        f"eligible={len(result.eligible_rows)}, sample={len(selected)}, "
        f"positive={pos}, non_positive={non}"
    )
    print(f"Wrote {Path(args.output).resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {VALIDATION_PLAN_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
