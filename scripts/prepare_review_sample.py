#!/usr/bin/env python3
"""
Prepare a manual review sample for raw access-phrase hits.

This script does not classify hits, fetch prices, make SEC requests, run return
analysis, or modify the raw phrase-hit table.
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
PHRASE_HITS_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"
TAXONOMY_PATH = PROJECT_ROOT / "config" / "access_phrases.csv"
FIRM_UNIVERSE_PATH = PROJECT_ROOT / "config" / "firm_universe.csv"
REVIEW_DIR = PROJECT_ROOT / "data" / "review"
REVIEW_SAMPLE_PATH = REVIEW_DIR / "phrase_hit_review_sample.csv"
REVIEW_TEMPLATE_PATH = REVIEW_DIR / "phrase_hit_review_template.csv"
QUALITY_REPORT_DIR = PROJECT_ROOT / "quality_reports"
CLASSIFICATION_PREP_REPORT_PATH = QUALITY_REPORT_DIR / "classification_prep_report.md"

SCRIPT_VERSION = "prepare_review_sample_v1"
DEFAULT_SAMPLE_SIZE = 600
DEFAULT_SEED = 20260629

INPUT_HIT_FIELDS = [
    "firm_id",
    "ticker",
    "cik",
    "accession_number",
    "filing_date",
    "filing_year",
    "section_name",
    "phrase",
    "category",
    "matched_text",
    "excerpt",
    "match_start",
    "match_end",
    "source_file",
]

REVIEW_FIELDS = [
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


@dataclass
class SampleResult:
    total_hits: int
    sample_rows: list[dict[str, str]]
    taxonomy_rows: list[dict[str, str]]
    category_counts: Counter[str]
    year_counts: Counter[str]
    section_counts: Counter[str]
    phrase_counts: Counter[str]
    firm_counts: Counter[str]
    sample_category_counts: Counter[str]
    sample_year_counts: Counter[str]
    sample_section_counts: Counter[str]
    sample_phrase_counts: Counter[str]
    sample_firm_counts: Counter[str]
    company_name_source: str


def field_size_limit() -> None:
    csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def stable_key(row: dict[str, str], seed: int) -> str:
    raw = "|".join(
        [
            str(seed),
            row.get("hit_id", ""),
            row.get("accession_number", ""),
            row.get("section_name", ""),
            row.get("phrase", ""),
            row.get("match_start", ""),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_company_names(path: Path) -> tuple[dict[str, str], str]:
    if not path.exists():
        return {}, "not available"
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields = set(reader.fieldnames or [])
        name_field = "company_name" if "company_name" in fields else "entity_name" if "entity_name" in fields else ""
        if not name_field:
            return {}, "not available"
        mapping: dict[str, str] = {}
        for row in reader:
            name = (row.get(name_field) or "").strip()
            if not name:
                continue
            for key_field in ["firm_id", "cik", "ticker"]:
                key = (row.get(key_field) or "").strip()
                if key and key not in mapping:
                    mapping[key] = name
        return mapping, str(path.relative_to(PROJECT_ROOT))


def add_hit_ids(rows: list[dict[str, str]], company_names: dict[str, str]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for idx, row in enumerate(rows, start=1):
        item = dict(row)
        item["hit_id"] = str(idx)
        item["company_name"] = (
            company_names.get(item.get("firm_id", ""))
            or company_names.get(item.get("cik", ""))
            or company_names.get(item.get("ticker", ""))
            or ""
        )
        item["human_label"] = ""
        item["reviewer_notes"] = ""
        item["confidence"] = ""
        output.append(item)
    return output


def validate_hits(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("phrase hit table is empty")
    missing = [field for field in INPUT_HIT_FIELDS if field not in rows[0]]
    if missing:
        raise ValueError(f"phrase hit table missing required fields: {', '.join(missing)}")


def grouped(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row.get(field, "")].append(row)
    return groups


def select_sample(rows: list[dict[str, str]], sample_size: int, seed: int, max_per_firm: int) -> list[dict[str, str]]:
    rng = random.Random(seed)
    selected: dict[str, dict[str, str]] = {}
    selected_firms: Counter[str] = Counter()

    shuffled = sorted(rows, key=lambda row: stable_key(row, seed))

    def can_add(row: dict[str, str]) -> bool:
        if row["hit_id"] in selected:
            return False
        firm_key = row.get("firm_id") or row.get("cik") or row.get("ticker") or "(blank)"
        return selected_firms[firm_key] < max_per_firm

    def add(row: dict[str, str]) -> bool:
        if len(selected) >= sample_size or not can_add(row):
            return False
        firm_key = row.get("firm_id") or row.get("cik") or row.get("ticker") or "(blank)"
        selected[row["hit_id"]] = row
        selected_firms[firm_key] += 1
        return True

    def pass_by_stratum(field: str, per_group: int) -> None:
        groups = grouped(shuffled, field)
        group_keys = list(groups)
        rng.shuffle(group_keys)
        for key in group_keys:
            choices = sorted(groups[key], key=lambda row: stable_key(row, seed + len(key)))
            added = 0
            for row in choices:
                if add(row):
                    added += 1
                if added >= per_group or len(selected) >= sample_size:
                    break
            if len(selected) >= sample_size:
                return

    pass_by_stratum("phrase", 3)
    pass_by_stratum("category", 25)
    pass_by_stratum("filing_year", 20)
    pass_by_stratum("section_name", 45)
    pass_by_stratum("firm_id", 1)

    for row in shuffled:
        if len(selected) >= sample_size:
            break
        add(row)

    if len(selected) < sample_size:
        for row in shuffled:
            if row["hit_id"] not in selected:
                selected[row["hit_id"]] = row
            if len(selected) >= sample_size:
                break

    return sorted(selected.values(), key=lambda row: int(row["hit_id"]))


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


def high_risk_category_rows(taxonomy_rows: list[dict[str, str]], hit_category_counts: Counter[str]) -> list[list[str]]:
    category_risk: dict[str, Counter[str]] = defaultdict(Counter)
    for row in taxonomy_rows:
        category_risk[row.get("category", "")][row.get("false_positive_risk", "").lower()] += 1
    rows: list[list[str]] = []
    for category, risks in sorted(category_risk.items(), key=lambda item: (-item[1].get("high", 0), item[0])):
        if risks.get("high", 0):
            rows.append(
                [
                    category,
                    str(hit_category_counts.get(category, 0)),
                    str(risks.get("high", 0)),
                    str(risks.get("medium", 0)),
                    str(risks.get("low", 0)),
                ]
            )
    return rows


def write_report(result: SampleResult, sample_size: int, seed: int, max_per_firm: int) -> None:
    QUALITY_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Classification Preparation Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "- Prepared a manual review sample from raw phrase hits.",
        "- Did not classify hits, fetch prices, make SEC requests, run return analysis, or make empirical claims.",
        "- Raw phrase hits remain unchanged in `data/extracted/phrase_hits.csv`.",
        f"- Script version: `{SCRIPT_VERSION}`.",
        "",
        "## Warning",
        "",
        "No return outcomes have been loaded yet. Raw phrase hits and review samples are text-validation artifacts only.",
        "",
        "## Raw Hits Available For Review",
        "",
        f"- Raw phrase hits available: {result.total_hits}",
        f"- Proposed initial review sample size: {len(result.sample_rows)}",
        f"- Requested sample size parameter: {sample_size}",
        f"- Deterministic sample seed: {seed}",
        f"- Firm-level soft cap before fallback fill: {max_per_firm}",
        f"- Company-name source: {result.company_name_source}",
        "",
        "## Recommended Initial Sample Size And Tradeoffs",
        "",
        "The recommended initial sample is 600 raw hits. This is large enough to cover all phrase categories, common phrases, years, sections, and a broad firm set, while remaining practical for manual review. A smaller sample near 300 would be faster but would provide weak coverage of rare phrases and section/year combinations. A larger sample near 1,000 would improve phrase-level precision but should usually wait until reviewers calibrate on the first batch.",
        "",
        "## Stratification Method",
        "",
        "- Assigned stable `hit_id` values from raw phrase-hit row order without modifying the raw file.",
        "- Selected deterministic coverage passes by phrase, category, filing year, section, and firm.",
        "- Applied a firm-level cap during the main selection passes to reduce concentration in frequent issuers.",
        "- Filled remaining slots deterministically from the remaining raw hits.",
        "",
        "## Proposed Review Sample Counts By Category",
        "",
    ]
    lines.extend(markdown_table(["Category", "Sample count"], counter_rows(result.sample_category_counts)))
    lines.extend(["", "## Proposed Review Sample Counts By Year", ""])
    lines.extend(markdown_table(["Filing year", "Sample count"], [[year, str(result.sample_year_counts[year])] for year in sorted(result.sample_year_counts)]))
    lines.extend(["", "## Proposed Review Sample Counts By Section", ""])
    lines.extend(markdown_table(["Section", "Sample count"], counter_rows(result.sample_section_counts)))
    lines.extend(["", "## Likely High-False-Positive Categories", ""])
    risk_rows = high_risk_category_rows(result.taxonomy_rows, result.category_counts)
    lines.extend(
        markdown_table(["Category", "Raw hits", "High-risk phrases", "Medium-risk phrases", "Low-risk phrases"], risk_rows)
        if risk_rows
        else ["- None identified from taxonomy."]
    )
    lines.extend(["", "## Top Sampled Phrases", ""])
    lines.extend(markdown_table(["Phrase", "Sample count"], counter_rows(result.sample_phrase_counts)[:25]))
    lines.extend(["", "## Top Sampled Firms", ""])
    lines.extend(markdown_table(["Firm ID", "Sample count"], counter_rows(result.sample_firm_counts)[:25]))
    lines.extend(
        [
            "",
            "## Recommended Next Stage",
            "",
            "Review `data/review/phrase_hit_review_sample.csv` under `config/classification_guidelines.md`. After reviewer calibration, create a locked classified-hit table that preserves raw hit IDs, human labels, confidence, reviewer metadata, and audit notes. Only after that should return data be loaded and merged under the pre-analysis plan.",
            "",
            "## Output Files",
            "",
            f"- `{REVIEW_SAMPLE_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{REVIEW_TEMPLATE_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{CLASSIFICATION_PREP_REPORT_PATH.relative_to(PROJECT_ROOT)}`",
        ]
    )
    CLASSIFICATION_PREP_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def prepare(args: argparse.Namespace) -> SampleResult:
    field_size_limit()
    hits = read_csv(Path(args.phrase_hits))
    validate_hits(hits)
    taxonomy_rows = read_csv(Path(args.taxonomy))
    company_names, company_name_source = load_company_names(FIRM_UNIVERSE_PATH)
    hits_with_ids = add_hit_ids(hits, company_names)
    sample_rows = select_sample(hits_with_ids, args.sample_size, args.seed, args.max_per_firm)
    result = SampleResult(
        total_hits=len(hits_with_ids),
        sample_rows=sample_rows,
        taxonomy_rows=taxonomy_rows,
        category_counts=count(hits_with_ids, "category"),
        year_counts=count(hits_with_ids, "filing_year"),
        section_counts=count(hits_with_ids, "section_name"),
        phrase_counts=count(hits_with_ids, "phrase"),
        firm_counts=count(hits_with_ids, "firm_id"),
        sample_category_counts=count(sample_rows, "category"),
        sample_year_counts=count(sample_rows, "filing_year"),
        sample_section_counts=count(sample_rows, "section_name"),
        sample_phrase_counts=count(sample_rows, "phrase"),
        sample_firm_counts=count(sample_rows, "firm_id"),
        company_name_source=company_name_source,
    )
    write_csv(Path(args.sample_output), sample_rows, REVIEW_FIELDS)
    write_csv(Path(args.template_output), [], REVIEW_FIELDS)
    write_report(result, args.sample_size, args.seed, args.max_per_firm)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a stratified manual review sample from raw phrase hits.")
    parser.add_argument("--phrase-hits", default=str(PHRASE_HITS_PATH))
    parser.add_argument("--taxonomy", default=str(TAXONOMY_PATH))
    parser.add_argument("--sample-output", default=str(REVIEW_SAMPLE_PATH))
    parser.add_argument("--template-output", default=str(REVIEW_TEMPLATE_PATH))
    parser.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE_SIZE)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--max-per-firm", type=int, default=12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = prepare(args)
    print(
        "Prepared review sample: "
        f"raw_hits={result.total_hits}, sample_rows={len(result.sample_rows)}, "
        f"categories={len(result.sample_category_counts)}"
    )
    print(f"Wrote {Path(args.sample_output).resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {Path(args.template_output).resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CLASSIFICATION_PREP_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
