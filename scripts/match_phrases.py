#!/usr/bin/env python3
"""
Match raw access-related phrases against locally extracted 10-K sections.

This script only reads local extracted section text. It does not classify raw
hits, fetch prices, make SEC requests, run return analysis, or make research
claims.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = PROJECT_ROOT / "config" / "access_phrases.csv"
SECTION_INPUT_PATH = PROJECT_ROOT / "data" / "extracted" / "filing_sections.csv"
PHRASE_HIT_OUTPUT_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"
QUALITY_REPORT_DIR = PROJECT_ROOT / "quality_reports"
PHRASE_HIT_REPORT_PATH = QUALITY_REPORT_DIR / "phrase_hit_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_05_PHRASE_MATCHING.md"

MATCHER_NAME = "local_exact_phrase_matcher"
MATCHER_VERSION = "access_phrase_matcher_v1"
EXCERPT_RADIUS = 180

TAXONOMY_FIELDS = [
    "phrase",
    "category",
    "match_type",
    "include_plural",
    "false_positive_risk",
    "notes",
]

HIT_FIELDS = [
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


@dataclass(frozen=True)
class PhraseTerm:
    phrase: str
    category: str
    match_type: str
    include_plural: bool
    false_positive_risk: str
    notes: str
    variants: tuple[str, ...]


@dataclass(frozen=True)
class HitCandidate:
    start: int
    end: int
    phrase: str
    category: str
    matched_text: str


@dataclass
class MatchSummary:
    source_rows: int = 0
    rows_with_text: int = 0
    total_candidates: int = 0
    total_hits: int = 0
    overlaps_suppressed: int = 0
    unique_filings: set[str] | None = None
    phrase_counts: Counter[str] | None = None
    category_counts: Counter[str] | None = None
    year_counts: Counter[str] | None = None
    section_counts: Counter[str] | None = None
    firm_counts: Counter[tuple[str, str]] | None = None
    reps_by_category: dict[str, list[dict[str, str]]] | None = None

    def __post_init__(self) -> None:
        self.unique_filings = set()
        self.phrase_counts = Counter()
        self.category_counts = Counter()
        self.year_counts = Counter()
        self.section_counts = Counter()
        self.firm_counts = Counter()
        self.reps_by_category = defaultdict(list)


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


def bool_value(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def normalize_for_match(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower()).strip()


def phrase_variants(phrase: str, include_plural: bool) -> tuple[str, ...]:
    parts = phrase.strip().split()
    if not parts:
        raise ValueError("empty phrase")

    variants = [normalize_for_match(phrase)]
    if include_plural:
        last = parts[-1]
        if re.search(r"[A-Za-z]$", last) and not last.lower().endswith("s"):
            plural_parts = [*parts[:-1], f"{last}s"]
            variants.append(normalize_for_match(" ".join(plural_parts)))
    return tuple(dict.fromkeys(variants))


def normalized_text_with_offsets(text: str) -> tuple[str, list[int]]:
    chars: list[str] = []
    offsets: list[int] = []
    last_was_space = True
    for idx, char in enumerate(text):
        if char.isspace():
            if not last_was_space:
                chars.append(" ")
                offsets.append(idx)
                last_was_space = True
            continue
        chars.append(char.lower())
        offsets.append(idx)
        last_was_space = False
    if chars and chars[-1] == " ":
        chars.pop()
        offsets.pop()
    return "".join(chars), offsets


def word_boundary_ok(value: str, start: int, end: int) -> bool:
    before = value[start - 1] if start > 0 else ""
    after = value[end] if end < len(value) else ""
    return (not before or not before.isalnum()) and (not after or not after.isalnum())


def read_taxonomy(path: Path) -> list[PhraseTerm]:
    rows = read_csv(path)
    if not rows:
        raise ValueError(f"taxonomy is empty: {path}")
    missing = [field for field in TAXONOMY_FIELDS if field not in rows[0]]
    if missing:
        raise ValueError(f"taxonomy missing required fields: {', '.join(missing)}")

    terms: list[PhraseTerm] = []
    seen: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        phrase = (row.get("phrase") or "").strip()
        category = (row.get("category") or "").strip()
        match_type = (row.get("match_type") or "").strip()
        include_plural = bool_value(row.get("include_plural") or "")
        risk = (row.get("false_positive_risk") or "").strip()
        notes = (row.get("notes") or "").strip()
        if not phrase or not category or not match_type:
            raise ValueError(f"taxonomy row {row_number} has blank phrase, category, or match_type")
        if match_type != "word_phrase":
            raise ValueError(f"taxonomy row {row_number} uses unsupported match_type: {match_type}")
        key = phrase.casefold()
        if key in seen:
            raise ValueError(f"duplicate taxonomy phrase: {phrase}")
        seen.add(key)
        terms.append(
            PhraseTerm(
                phrase=phrase,
                category=category,
                match_type=match_type,
                include_plural=include_plural,
                false_positive_risk=risk,
                notes=notes,
                variants=phrase_variants(phrase, include_plural),
            )
        )
    return terms


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def excerpt(text: str, start: int, end: int) -> str:
    excerpt_start = max(0, start - EXCERPT_RADIUS)
    excerpt_end = min(len(text), end + EXCERPT_RADIUS)
    return clean_text(text[excerpt_start:excerpt_end])


def find_candidates(text: str, terms: list[PhraseTerm]) -> list[HitCandidate]:
    candidates: list[HitCandidate] = []
    normalized, offsets = normalized_text_with_offsets(text)
    if not normalized:
        return candidates
    for term in terms:
        for variant in term.variants:
            search_start = 0
            while True:
                start = normalized.find(variant, search_start)
                if start == -1:
                    break
                end = start + len(variant)
                search_start = start + 1
                if not word_boundary_ok(normalized, start, end):
                    continue
                original_start = offsets[start]
                original_end = offsets[end - 1] + 1
                matched_text = text[original_start:original_end]
                if not clean_text(matched_text):
                    continue
                candidates.append(
                    HitCandidate(
                        start=original_start,
                        end=original_end,
                        phrase=term.phrase,
                        category=term.category,
                        matched_text=matched_text,
                    )
                )
    return candidates


def overlaps(left: HitCandidate, right: HitCandidate) -> bool:
    return left.start < right.end and right.start < left.end


def select_non_overlapping(candidates: list[HitCandidate]) -> list[HitCandidate]:
    selected: list[HitCandidate] = []
    for candidate in sorted(
        candidates,
        key=lambda hit: (-(hit.end - hit.start), -len(hit.phrase), hit.start, hit.phrase.casefold()),
    ):
        if any(overlaps(candidate, existing) for existing in selected):
            continue
        selected.append(candidate)
    return sorted(selected, key=lambda hit: (hit.start, hit.end, hit.phrase.casefold()))


def hit_row(section_row: dict[str, str], hit: HitCandidate) -> dict[str, str]:
    text = section_row.get("section_text", "")
    return {
        "firm_id": section_row.get("firm_id", ""),
        "ticker": section_row.get("ticker", ""),
        "cik": section_row.get("cik", ""),
        "accession_number": section_row.get("accession_number", ""),
        "filing_date": section_row.get("filing_date", ""),
        "filing_year": section_row.get("filing_year", ""),
        "section_name": section_row.get("section_name", ""),
        "phrase": hit.phrase,
        "category": hit.category,
        "matched_text": clean_text(hit.matched_text),
        "excerpt": excerpt(text, hit.start, hit.end),
        "match_start": str(hit.start),
        "match_end": str(hit.end),
        "source_file": section_row.get("source_file", ""),
    }


def update_summary(summary: MatchSummary, row: dict[str, str], hits: list[HitCandidate], candidates_count: int) -> None:
    summary.total_candidates += candidates_count
    summary.total_hits += len(hits)
    summary.overlaps_suppressed += max(0, candidates_count - len(hits))
    accession = row.get("accession_number", "")
    ticker = row.get("ticker", "")
    firm_id = row.get("firm_id", "")
    if hits and accession:
        summary.unique_filings.add(accession)
    for hit in hits:
        summary.phrase_counts[hit.phrase] += 1
        summary.category_counts[hit.category] += 1
        summary.year_counts[row.get("filing_year", "")] += 1
        summary.section_counts[row.get("section_name", "")] += 1
        summary.firm_counts[(ticker, firm_id)] += 1
        reps = summary.reps_by_category[hit.category]
        if len(reps) < 10:
            reps.append(hit_row(row, hit))


def process_sections(
    input_path: Path,
    terms: list[PhraseTerm],
    output_path: Path | None = None,
    sample_size: int | None = None,
) -> MatchSummary:
    summary = MatchSummary()
    output_file = None
    writer = None
    try:
        if output_path is not None:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_file = output_path.open("w", encoding="utf-8", newline="")
            writer = csv.DictWriter(output_file, fieldnames=HIT_FIELDS, extrasaction="ignore", lineterminator="\n")
            writer.writeheader()

        with input_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            required = {"section_text", "accession_number", "section_name"}
            missing = sorted(required - set(reader.fieldnames or []))
            if missing:
                raise ValueError(f"section input missing required fields: {', '.join(missing)}")
            for row in reader:
                summary.source_rows += 1
                text = row.get("section_text", "")
                if text:
                    summary.rows_with_text += 1
                candidates = find_candidates(text, terms) if text else []
                hits = select_non_overlapping(candidates)
                update_summary(summary, row, hits, len(candidates))
                if writer is not None:
                    for hit in hits:
                        writer.writerow(hit_row(row, hit))
                if sample_size is not None and summary.source_rows >= sample_size:
                    break
    finally:
        if output_file is not None:
            output_file.close()
    return summary


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe = [str(value).replace("|", "\\|") for value in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def counter_rows(counter: Counter[str]) -> list[list[str]]:
    return [[key or "(blank)", str(count)] for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))]


def high_risk_terms(terms: list[PhraseTerm]) -> list[PhraseTerm]:
    return [term for term in terms if term.false_positive_risk.strip().lower() == "high"]


def write_report(full: MatchSummary, sample: MatchSummary, terms: list[PhraseTerm]) -> None:
    QUALITY_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phrase Hit Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "- Source: local `data/extracted/filing_sections.csv` section text only.",
        "- Matching layer: raw exact phrase hits only.",
        "- No true-positive classification, price fetching, SEC requests, return analysis, or research claims were performed.",
        f"- Matcher: `{MATCHER_NAME}` `{MATCHER_VERSION}`.",
        "- Match rule: case-insensitive `word_phrase` matching with word boundaries and flexible whitespace between phrase tokens.",
        "- Overlap rule: when candidate matches overlap within a section row, keep the longest span; ties use longer phrase text, then earliest offset.",
        "",
        "## Warning",
        "",
        "Raw phrase hits are not interpreted evidence. They are deterministic text matches that require later classification or manual audit before substantive interpretation.",
        "",
        "## Input Counts",
        "",
        f"- Phrase taxonomy rows: {len(terms)}",
        f"- Section rows scanned: {full.source_rows}",
        f"- Section rows with non-empty text: {full.rows_with_text}",
        "",
        "## Dry-Run/Sample Validation Notes",
        "",
        f"- Sample section rows scanned before full matching: {sample.source_rows}",
        f"- Sample rows with non-empty text: {sample.rows_with_text}",
        f"- Sample raw candidate matches before overlap suppression: {sample.total_candidates}",
        f"- Sample retained hits after overlap suppression: {sample.total_hits}",
        f"- Sample overlapping duplicate candidates suppressed: {sample.overlaps_suppressed}",
        "- Sample run used the same taxonomy, regex construction, excerpt builder, and overlap-suppression logic as the full run.",
        "",
        "## Aggregate Hit Counts",
        "",
        f"- Total phrase hits: {full.total_hits}",
        f"- Candidate matches before overlap suppression: {full.total_candidates}",
        f"- Overlapping duplicate candidates suppressed: {full.overlaps_suppressed}",
        f"- Unique filings with at least one hit: {len(full.unique_filings)}",
        "",
        "## Hit Counts By Phrase",
        "",
    ]
    phrase_rows = counter_rows(full.phrase_counts)
    lines.extend(markdown_table(["Phrase", "Raw hit count"], phrase_rows) if phrase_rows else ["- None"])

    lines.extend(["", "## Hit Counts By Category", ""])
    category_rows = counter_rows(full.category_counts)
    lines.extend(markdown_table(["Category", "Raw hit count"], category_rows) if category_rows else ["- None"])

    lines.extend(["", "## Hit Counts By Year", ""])
    year_rows = [[year or "(blank)", str(full.year_counts[year])] for year in sorted(full.year_counts)]
    lines.extend(markdown_table(["Filing year", "Raw hit count"], year_rows) if year_rows else ["- None"])

    lines.extend(["", "## Hit Counts By Section", ""])
    section_rows = counter_rows(full.section_counts)
    lines.extend(markdown_table(["Section", "Raw hit count"], section_rows) if section_rows else ["- None"])

    lines.extend(["", "## Top 25 Firms By Raw Hit Count", ""])
    firm_rows = [
        [ticker or "(blank)", firm_id or "(blank)", str(count)]
        for (ticker, firm_id), count in full.firm_counts.most_common(25)
    ]
    lines.extend(markdown_table(["Ticker", "Firm ID", "Raw hit count"], firm_rows) if firm_rows else ["- None"])

    lines.extend(["", "## Representative Excerpts By Category", ""])
    for category in sorted({term.category for term in terms}):
        lines.extend(["", f"### {category}", ""])
        reps = full.reps_by_category.get(category, [])
        if not reps:
            lines.append("- No raw hits.")
            continue
        excerpt_rows = [
            [
                row["ticker"] or "(blank)",
                row["filing_year"] or "(blank)",
                row["section_name"] or "(blank)",
                row["phrase"],
                row["excerpt"],
            ]
            for row in reps[:10]
        ]
        lines.extend(markdown_table(["Ticker", "Year", "Section", "Phrase", "Excerpt"], excerpt_rows))

    lines.extend(["", "## Phrases With Likely High False-Positive Risk", ""])
    risk_rows = [[term.phrase, term.category, term.notes] for term in high_risk_terms(terms)]
    lines.extend(markdown_table(["Phrase", "Category", "Notes"], risk_rows) if risk_rows else ["- None"])

    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- `{PHRASE_HIT_OUTPUT_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{PHRASE_HIT_REPORT_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}`",
        ]
    )
    PHRASE_HIT_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_checkpoint(full: MatchSummary, sample: MatchSummary, terms: list[PhraseTerm]) -> None:
    lines = [
        "# CHECKPOINT 05: Phrase Matching",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Completed",
        "",
        "- Built initial phrase taxonomy for access-related raw phrase matching.",
        "- Implemented local-only raw exact-match hit detector.",
        "- Ran a small sample dry-run before full-corpus matching.",
        "- Wrote raw phrase hits separately from any later classification layer.",
        "- Wrote phrase-hit quality report with aggregate counts and representative excerpts.",
        "",
        "## Explicit Non-Actions",
        "",
        "- No true-positive classification.",
        "- No price fetching.",
        "- No SEC requests.",
        "- No research claims.",
        "- No return analysis.",
        "",
        "## Inputs",
        "",
        f"- Phrase taxonomy rows: {len(terms)}",
        f"- Section rows scanned: {full.source_rows}",
        f"- Sample dry-run rows scanned first: {sample.source_rows}",
        "",
        "## Outputs",
        "",
        f"- `{TAXONOMY_PATH.relative_to(PROJECT_ROOT)}`",
        f"- `{Path(__file__).resolve().relative_to(PROJECT_ROOT)}`",
        f"- `{PHRASE_HIT_OUTPUT_PATH.relative_to(PROJECT_ROOT)}`",
        f"- `{PHRASE_HIT_REPORT_PATH.relative_to(PROJECT_ROOT)}`",
        f"- `{CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}`",
        "",
        "## Raw Hit Counts",
        "",
        f"- Total phrase hits: {full.total_hits}",
        f"- Unique filings with at least one hit: {len(full.unique_filings)}",
        f"- Candidate matches before overlap suppression: {full.total_candidates}",
        f"- Overlapping duplicate candidates suppressed: {full.overlaps_suppressed}",
        "",
        "## Warning",
        "",
        "Raw phrase hits are not interpreted evidence. Later classification or manual audit is required before treating any hit as substantively about access expansion.",
        "",
        "## Next Recommended Prompt",
        "",
        "Audit `quality_reports/phrase_hit_report.md` and review representative raw excerpts and high false-positive-risk phrases before building a classification layer.",
    ]
    CHECKPOINT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Match raw access phrases against local extracted 10-K sections.")
    parser.add_argument("--taxonomy", default=str(TAXONOMY_PATH))
    parser.add_argument("--input", default=str(SECTION_INPUT_PATH))
    parser.add_argument("--output", default=str(PHRASE_HIT_OUTPUT_PATH))
    parser.add_argument("--sample-size", type=int, default=250)
    parser.add_argument("--dry-run", action="store_true", help="Run sample matching only and do not write outputs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    field_size_limit()
    terms = read_taxonomy(Path(args.taxonomy))
    sample_size = max(1, args.sample_size)
    sample = process_sections(Path(args.input), terms, output_path=None, sample_size=sample_size)
    print(
        "Sample dry-run: "
        f"rows={sample.source_rows}, hits={sample.total_hits}, suppressed_overlaps={sample.overlaps_suppressed}"
    )
    if args.dry_run:
        return 0

    full = process_sections(Path(args.input), terms, output_path=Path(args.output), sample_size=None)
    write_report(full, sample, terms)
    write_checkpoint(full, sample, terms)
    print(
        "Full phrase matching: "
        f"rows={full.source_rows}, hits={full.total_hits}, unique_filings={len(full.unique_filings)}"
    )
    print(f"Wrote {Path(args.output).relative_to(PROJECT_ROOT)}")
    print(f"Wrote {PHRASE_HIT_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
