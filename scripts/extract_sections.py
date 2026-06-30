#!/usr/bin/env python3
"""
Extract Item 1, Item 1A, and Item 7 sections from cached 10-K filings only.

This script does not make SEC requests, does not match phrases, does not classify
text, and does not fetch prices. It reads local raw filing documents referenced
by data/metadata/download_attempts.csv and writes structured section output plus
quality reports.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILING_INDEX_PATH = PROJECT_ROOT / "data" / "metadata" / "filing_index.csv"
DOWNLOAD_ATTEMPTS_PATH = PROJECT_ROOT / "data" / "metadata" / "download_attempts.csv"
EXTRACTED_DIR = PROJECT_ROOT / "data" / "extracted"
SECTION_OUTPUT_PATH = EXTRACTED_DIR / "filing_sections.csv"
QUALITY_REPORT_DIR = PROJECT_ROOT / "quality_reports"
SECTION_REPORT_PATH = QUALITY_REPORT_DIR / "section_extraction_report.md"
CHECKPOINT_PATH = PROJECT_ROOT / "CHECKPOINT_04_EXTRACTION.md"

EXTRACTION_METHOD = "htmlparser_regex_item_boundaries_v1"

SECTION_FIELDS = [
    "firm_id",
    "ticker",
    "cik",
    "accession_number",
    "filing_date",
    "filing_year",
    "section_name",
    "section_text",
    "char_count",
    "word_count",
    "extraction_status",
    "extraction_method",
    "source_file",
]

SECTIONS = {
    "Item 1 Business": {
        "start": ["ITEM_1"],
        "end": ["ITEM_1A", "ITEM_1B", "ITEM_2"],
        "min_chars": 1000,
        "max_chars": 900000,
    },
    "Item 1A Risk Factors": {
        "start": ["ITEM_1A"],
        "end": ["ITEM_1B", "ITEM_2"],
        "min_chars": 1000,
        "max_chars": 1000000,
    },
    "Item 7 MD&A": {
        "start": ["ITEM_7"],
        "end": ["ITEM_7A", "ITEM_8"],
        "min_chars": 1000,
        "max_chars": 1200000,
    },
}

BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "caption",
    "center",
    "dd",
    "div",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "hr",
    "li",
    "main",
    "nav",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "tbody",
    "td",
    "tfoot",
    "th",
    "thead",
    "tr",
    "ul",
}


class FilingTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style"}:
            self.skip_depth += 1
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and data:
            self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


@dataclass
class Candidate:
    label: str
    start: int
    end: int
    line: str


@dataclass
class ExtractedSection:
    text: str
    status: str
    start: int | None
    end: int | None


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


def decode_file(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ["utf-8", "latin-1"]:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="ignore")


def html_to_text(markup: str) -> str:
    match = re.search(r"<TEXT[^>]*>(.*)</TEXT>", markup, flags=re.I | re.S)
    if match:
        markup = match.group(1)
    parser = FilingTextParser()
    try:
        parser.feed(markup)
        parser.close()
        text = parser.text()
    except Exception:
        text = re.sub(r"<[^>]+>", " ", markup)
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def canonical_line(line: str) -> str:
    value = html.unescape(line).replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value).strip().lower()
    value = value.replace("’", "'")
    return value


def is_toc_like(line: str) -> bool:
    value = canonical_line(line)
    if re.search(r"\.{3,}", value):
        return True
    if re.search(r"\s+\d{1,4}$", value) and len(value) > 14:
        return True
    if len(value) > 160:
        return True
    return False


def classify_heading(line: str) -> str | None:
    value = canonical_line(line)
    if not value or is_toc_like(value):
        return None
    value = re.sub(r"^[^a-z0-9]*(part\s+i[^a-z0-9]+)?", "", value)
    value = re.sub(r"[^a-z0-9&']+", " ", value).strip()

    if re.match(r"^item 1a( |$)", value):
        if value in {"item 1a"} or "risk factor" in value:
            return "ITEM_1A"
    if re.match(r"^item 1b( |$)", value):
        return "ITEM_1B"
    if re.match(r"^item 1( |$)", value) and not re.match(r"^item 1[0-9ab]( |$)", value):
        if value in {"item 1"} or "business" in value:
            return "ITEM_1"
    if re.match(r"^item 2( |$)", value):
        return "ITEM_2"
    if re.match(r"^item 7a( |$)", value):
        return "ITEM_7A"
    if re.match(r"^item 7( |$)", value) and not re.match(r"^item 7a( |$)", value):
        if value in {"item 7"} or "management" in value or "md&a" in value or "discussion" in value:
            return "ITEM_7"
    if re.match(r"^item 8( |$)", value):
        return "ITEM_8"
    return None


def find_candidates(text: str) -> list[Candidate]:
    candidates: list[Candidate] = []
    position = 0
    for raw_line in text.splitlines(keepends=True):
        clean = raw_line.strip()
        label = classify_heading(clean)
        if label:
            candidates.append(Candidate(label=label, start=position, end=position + len(raw_line), line=clean))
        position += len(raw_line)
    return candidates


def nearest_end(start: Candidate, labels: list[str], candidates: list[Candidate], text_len: int) -> int:
    endings = [c.start for c in candidates if c.label in labels and c.start > start.end + 20]
    return min(endings) if endings else text_len


def toc_only(section_text: str) -> bool:
    sample = "\n".join(section_text.splitlines()[:25])
    item_heading_count = len(re.findall(r"(?im)^\s*item\s+\d+[a-z]?\b", sample))
    dot_leaders = len(re.findall(r"\.{3,}", sample))
    return len(section_text) < 1500 and (item_heading_count >= 2 or dot_leaders >= 1)


def choose_section(text: str, candidates: list[Candidate], section_name: str) -> ExtractedSection:
    spec = SECTIONS[section_name]
    starts = [c for c in candidates if c.label in spec["start"]]
    if not starts:
        return ExtractedSection("", "SECTION_NOT_FOUND", None, None)

    attempts: list[tuple[int, int, Candidate, str]] = []
    for start in starts:
        end = nearest_end(start, spec["end"], candidates, len(text))
        body = text[start.start:end].strip()
        status = "OK"
        if toc_only(body):
            status = "LIKELY_TOC_ONLY"
        elif len(body) < int(spec["min_chars"]):
            status = "SUSPICIOUSLY_SHORT"
        elif len(body) > int(spec["max_chars"]):
            status = "SUSPICIOUSLY_LONG"
        attempts.append((len(body), end, start, status))

    clean = [a for a in attempts if a[3] == "OK"]
    if clean:
        length, end, start, status = max(clean, key=lambda a: a[0])
    else:
        non_toc = [a for a in attempts if a[3] != "LIKELY_TOC_ONLY"]
        length, end, start, status = max(non_toc or attempts, key=lambda a: a[0])

    body = text[start.start:end].strip()
    flags = [status]
    if status == "OK":
        if len(body) < int(spec["min_chars"]):
            flags.append("SUSPICIOUSLY_SHORT")
        if len(body) > int(spec["max_chars"]):
            flags.append("SUSPICIOUSLY_LONG")
        if toc_only(body):
            flags.append("LIKELY_TOC_ONLY")
    return ExtractedSection(body, "|".join(dict.fromkeys(flags)), start.start, end)


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def latest_downloads_by_accession(attempts: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    latest: dict[str, dict[str, str]] = {}
    for row in attempts:
        accession = row.get("accession_number", "")
        if not accession:
            continue
        current = latest.get(accession)
        if current is None or int(row.get("attempt_id") or 0) >= int(current.get("attempt_id") or 0):
            latest[accession] = row
    return latest


def section_row(base: dict[str, str], section_name: str, section: ExtractedSection, source_file: str) -> dict[str, str]:
    return {
        "firm_id": base.get("firm_id", ""),
        "ticker": base.get("ticker", ""),
        "cik": base.get("cik", ""),
        "accession_number": base.get("accession_number", ""),
        "filing_date": base.get("filing_date", ""),
        "filing_year": base.get("filing_year", ""),
        "section_name": section_name,
        "section_text": section.text,
        "char_count": str(len(section.text)),
        "word_count": str(word_count(section.text)),
        "extraction_status": section.status,
        "extraction_method": EXTRACTION_METHOD,
        "source_file": source_file,
    }


def extract_all(index_rows: list[dict[str, str]], attempts: list[dict[str, str]]) -> list[dict[str, str]]:
    latest_attempts = latest_downloads_by_accession(attempts)
    output: list[dict[str, str]] = []
    found_rows = [r for r in index_rows if r.get("expected_status") == "FOUND"]
    for idx, filing in enumerate(found_rows, start=1):
        accession = filing.get("accession_number", "")
        attempt = latest_attempts.get(accession)
        source_file = attempt.get("local_path", "") if attempt else ""
        if not attempt or attempt.get("status") != "DOWNLOADED":
            for section_name in SECTIONS:
                output.append(
                    section_row(
                        filing,
                        section_name,
                        ExtractedSection("", "SOURCE_FILE_UNAVAILABLE", None, None),
                        source_file,
                    )
                )
            continue

        path = PROJECT_ROOT / source_file
        if not path.exists():
            for section_name in SECTIONS:
                output.append(
                    section_row(
                        filing,
                        section_name,
                        ExtractedSection("", "SOURCE_FILE_MISSING", None, None),
                        source_file,
                    )
                )
            continue

        try:
            text = html_to_text(decode_file(path))
            candidates = find_candidates(text)
            if not text:
                raise ValueError("empty parsed text")
            for section_name in SECTIONS:
                output.append(section_row(filing, section_name, choose_section(text, candidates, section_name), source_file))
        except Exception as exc:  # noqa: BLE001 - persisted for audit
            for section_name in SECTIONS:
                output.append(
                    section_row(
                        filing,
                        section_name,
                        ExtractedSection("", f"EXTRACTION_ERROR: {type(exc).__name__}: {exc}", None, None),
                        source_file,
                    )
                )

        if idx % 250 == 0 or idx == len(found_rows):
            print(f"Extracted sections for {idx}/{len(found_rows)} filings")
    return output


def success(status: str) -> bool:
    return status == "OK"


def write_report(section_rows: list[dict[str, str]], index_rows: list[dict[str, str]]) -> None:
    QUALITY_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    by_section_status: dict[str, Counter[str]] = defaultdict(Counter)
    by_year_status: dict[str, Counter[str]] = defaultdict(Counter)
    by_section_year_ok: dict[str, Counter[str]] = defaultdict(Counter)
    for row in section_rows:
        section = row["section_name"]
        status = row["extraction_status"]
        year = row["filing_year"]
        by_section_status[section][status] += 1
        by_year_status[year][status] += 1
        if success(status):
            by_section_year_ok[section][year] += 1

    lines = [
        "# Section Extraction Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope",
        "",
        "- Source: existing cached raw 10-K filings only.",
        "- Sections extracted: Item 1 Business, Item 1A Risk Factors, Item 7 MD&A.",
        "- No phrase matching, classification, price fetching, research interpretation, or SEC requests were performed.",
        f"- Extraction method: `{EXTRACTION_METHOD}`.",
        "",
        "## Input Counts",
        "",
        f"- Filing index rows: {len(index_rows)}",
        f"- Found 10-K filing rows: {sum(1 for r in index_rows if r.get('expected_status') == 'FOUND')}",
        f"- Section output rows: {len(section_rows)}",
        "",
        "## Extraction Success By Section",
        "",
    ]
    for section in SECTIONS:
        total = sum(by_section_status[section].values())
        ok = by_section_status[section].get("OK", 0)
        lines.append(f"- {section}: {ok}/{total} OK")
        for status, count in sorted(by_section_status[section].items()):
            lines.append(f"  - {status}: {count}")

    lines.extend(["", "## Extraction Success By Filing Year", ""])
    years = sorted({row["filing_year"] for row in section_rows})
    for year in years:
        total = sum(by_year_status[year].values())
        ok = by_year_status[year].get("OK", 0)
        lines.append(f"- {year}: {ok}/{total} section rows OK")
        section_bits = [f"{section}={by_section_year_ok[section].get(year, 0)}" for section in SECTIONS]
        lines.append(f"  - OK by section: {', '.join(section_bits)}")

    for section in SECTIONS:
        extracted = [r for r in section_rows if r["section_name"] == section and int(r["char_count"] or 0) > 0]
        extracted.sort(key=lambda r: int(r["char_count"] or 0))
        lines.extend(["", f"## 25 Shortest Extracted Sections: {section}", ""])
        if not extracted:
            lines.append("- None")
        else:
            lines.append("| Rank | Ticker | Filing Year | Accession | Chars | Words | Status | Source File |")
            lines.append("|---:|---|---:|---|---:|---:|---|---|")
            for rank, row in enumerate(extracted[:25], start=1):
                lines.append(
                    f"| {rank} | {row['ticker']} | {row['filing_year']} | {row['accession_number']} | "
                    f"{row['char_count']} | {row['word_count']} | {row['extraction_status']} | `{row['source_file']}` |"
                )

    for section in SECTIONS:
        missing = [
            r
            for r in section_rows
            if r["section_name"] == section
            and (
                r["extraction_status"].startswith("SECTION_NOT_FOUND")
                or r["extraction_status"].startswith("SOURCE_FILE")
                or r["extraction_status"].startswith("EXTRACTION_ERROR")
            )
        ]
        lines.extend(["", f"## Filings Missing {section}", ""])
        lines.append(f"Count: {len(missing)}")
        if missing:
            lines.append("")
            lines.append("| Ticker | Filing Year | Accession | Filing Date | Status | Source File |")
            lines.append("|---|---:|---|---|---|---|")
            for row in missing:
                lines.append(
                    f"| {row['ticker']} | {row['filing_year']} | {row['accession_number']} | "
                    f"{row['filing_date']} | {row['extraction_status']} | `{row['source_file']}` |"
                )

    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- `{SECTION_OUTPUT_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{SECTION_REPORT_PATH.relative_to(PROJECT_ROOT)}`",
            "",
            "## Next Recommended Prompt",
            "",
            "Review `quality_reports/section_extraction_report.md` and audit the shortest and missing sections. "
            "Then improve section-boundary rules or approve moving to raw phrase matching against `data/extracted/filing_sections.csv`.",
        ]
    )
    SECTION_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_checkpoint(section_rows: list[dict[str, str]], index_rows: list[dict[str, str]]) -> None:
    status_counts = Counter(row["extraction_status"] for row in section_rows)
    section_ok = {
        section: sum(1 for row in section_rows if row["section_name"] == section and row["extraction_status"] == "OK")
        for section in SECTIONS
    }
    total_by_section = {
        section: sum(1 for row in section_rows if row["section_name"] == section)
        for section in SECTIONS
    }
    lines = [
        "# CHECKPOINT 04: Section Extraction",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Completed",
        "",
        "- Implemented local-only section extraction for downloaded 10-K filings.",
        "- Extracted sections: Item 1 Business, Item 1A Risk Factors, Item 7 MD&A.",
        "- Wrote structured section rows with required metadata and full section text.",
        "- Wrote quality report with success by section/year, shortest sections, and missing section lists.",
        "",
        "## Explicit Non-Actions",
        "",
        "- No phrase matching.",
        "- No classification.",
        "- No price fetching.",
        "- No research claims.",
        "- No SEC requests.",
        "- No raw filing overwrites.",
        "",
        "## Inputs",
        "",
        f"- Filing index rows: {len(index_rows)}",
        f"- Found 10-K filing rows: {sum(1 for r in index_rows if r.get('expected_status') == 'FOUND')}",
        "",
        "## Outputs",
        "",
        f"- `{SECTION_OUTPUT_PATH.relative_to(PROJECT_ROOT)}`",
        f"- `{SECTION_REPORT_PATH.relative_to(PROJECT_ROOT)}`",
        f"- `{CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}`",
        "",
        "## OK Counts By Section",
        "",
    ]
    for section in SECTIONS:
        lines.append(f"- {section}: {section_ok[section]}/{total_by_section[section]}")
    lines.extend(["", "## Status Counts", ""])
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(
        [
            "",
            "## Known Limitation",
            "",
            "The extractor uses standard-library HTML parsing and regex item boundaries. "
            "Shortest, missing, suspiciously short, suspiciously long, and table-of-contents-only cases require audit before phrase matching.",
            "",
            "## Next Recommended Prompt",
            "",
            "Audit `quality_reports/section_extraction_report.md`, especially missing sections and the 25 shortest sections for each type. "
            "If acceptable, proceed to implement raw phrase matching on `data/extracted/filing_sections.csv`; otherwise refine extraction rules first.",
        ]
    )
    CHECKPOINT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Item 1, Item 1A, and Item 7 from cached raw 10-K filings.")
    parser.add_argument("--filing-index", default=str(FILING_INDEX_PATH))
    parser.add_argument("--download-attempts", default=str(DOWNLOAD_ATTEMPTS_PATH))
    parser.add_argument("--output", default=str(SECTION_OUTPUT_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    index_rows = read_csv(Path(args.filing_index))
    attempts = read_csv(Path(args.download_attempts))
    section_rows = extract_all(index_rows, attempts)
    write_csv(Path(args.output), section_rows, SECTION_FIELDS)
    write_report(section_rows, index_rows)
    write_checkpoint(section_rows, index_rows)
    print(f"Wrote {Path(args.output).relative_to(PROJECT_ROOT)} with {len(section_rows)} rows")
    print(f"Wrote {SECTION_REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {CHECKPOINT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
