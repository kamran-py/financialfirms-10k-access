#!/usr/bin/env python3
"""
Classify the full raw phrase-hit corpus using the validated V2 framework.

This script is treatment-candidate construction only. It does not fetch
prices, compute returns, make SEC requests, or modify
data/extracted/phrase_hits.csv.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from classify_review_sample_v2 import ALLOWED_LABELS, Decision, classify, validate_label


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PHRASE_HITS_PATH = PROJECT_ROOT / "data" / "extracted" / "phrase_hits.csv"
REVIEW_CLASSIFIED_V2_PATH = PROJECT_ROOT / "data" / "review" / "phrase_hit_review_sample_classified_v2.csv"
VALIDATION_AUDITED_PATH = PROJECT_ROOT / "data" / "review" / "v2_codex_assisted_validation_sample_audited.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "classified" / "phrase_hits_classified_v2.csv"
REPORT_PATH = PROJECT_ROOT / "quality_reports" / "full_corpus_classification_v2_report.md"
GUIDELINES_V3_PATH = PROJECT_ROOT / "config" / "classification_guidelines_v3.md"

CLASSIFIER_VERSION = "classification_guidelines_v3"
SCRIPT_VERSION = "classify_all_phrase_hits_v2"

OUTPUT_FIELDS = [
    "final_label_v2",
    "final_confidence_v2",
    "label_source_v2",
    "classifier_version",
    "high_risk_phrase_flag",
    "classification_notes_v2",
]

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


@dataclass(frozen=True)
class ClassificationArtifact:
    label: str
    confidence: str
    source: str
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


def high_risk_flag(phrase: str) -> str:
    return "yes" if phrase.strip().lower() in HIGH_RISK_PHRASES else "no"


def load_review_artifacts(path: Path) -> dict[int, ClassificationArtifact]:
    rows, _ = read_csv(path)
    artifacts: dict[int, ClassificationArtifact] = {}
    for row in rows:
        hit_id = int(row["hit_id"])
        label = row.get("final_label_v2", "").strip()
        confidence = row.get("final_confidence_v2", "").strip()
        source = row.get("label_source_v2", "").strip()
        validate_label(label, f"review artifact hit_id {hit_id}")
        if not confidence or not source:
            raise ValueError(f"review artifact hit_id {hit_id} missing confidence/source")
        notes = (
            row.get("reviewer_notes", "").strip()
            or row.get("codex_assisted_notes_v2", "").strip()
            or "Locked V2 review-sample label."
        )
        artifacts[hit_id] = ClassificationArtifact(label, confidence, source, notes)
    return artifacts


def load_validation_artifacts(path: Path) -> dict[int, ClassificationArtifact]:
    rows, _ = read_csv(path)
    artifacts: dict[int, ClassificationArtifact] = {}
    for row in rows:
        hit_id = int(row["hit_id"])
        label = row.get("validation_label", "").strip()
        confidence = row.get("validation_confidence", "").strip()
        notes = row.get("validation_notes", "").strip() or "Locked V2 validation-audit label."
        validate_label(label, f"validation artifact hit_id {hit_id}")
        if not confidence:
            raise ValueError(f"validation artifact hit_id {hit_id} missing confidence")
        artifacts[hit_id] = ClassificationArtifact(label, confidence, "v2_validation_audit", notes)
    return artifacts


def classify_all(
    raw_rows: list[dict[str, str]],
    review_artifacts: dict[int, ClassificationArtifact],
    validation_artifacts: dict[int, ClassificationArtifact],
) -> list[dict[str, str]]:
    classified: list[dict[str, str]] = []
    for index, row in enumerate(raw_rows, start=1):
        item = dict(row)
        artifact = validation_artifacts.get(index) or review_artifacts.get(index)
        if artifact:
            label = artifact.label
            confidence = artifact.confidence
            source = artifact.source
            notes = f"Derived hit_id={index}; {artifact.notes}"
        else:
            decision: Decision = classify(item)
            validate_label(decision.label, f"full corpus hit_id {index}")
            label = decision.label
            confidence = decision.confidence
            source = "codex_assisted_full_corpus_v2"
            notes = f"Derived hit_id={index}; {decision.notes}"

        item["final_label_v2"] = label
        item["final_confidence_v2"] = confidence
        item["label_source_v2"] = source
        item["classifier_version"] = CLASSIFIER_VERSION
        item["high_risk_phrase_flag"] = high_risk_flag(item.get("phrase", ""))
        item["classification_notes_v2"] = notes
        classified.append(item)
    return classified


def counter_by(rows: list[dict[str, str]], field: str) -> Counter[str]:
    return Counter(row.get(field, "") for row in rows)


def nested_label_counts(rows: list[dict[str, str]], field: str) -> dict[str, Counter[str]]:
    out: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        out[row.get(field, "")][row.get("final_label_v2", "")] += 1
    return out


def markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return lines


def label_distribution_rows(counter: Counter[str]) -> list[list[str]]:
    return [[label, str(counter.get(label, 0))] for label in sorted(ALLOWED_LABELS)]


def label_distribution_by_field(rows: list[dict[str, str]], field: str) -> list[list[str]]:
    grouped = nested_label_counts(rows, field)
    out: list[list[str]] = []
    for value in sorted(grouped):
        counts = grouped[value]
        total = sum(counts.values())
        tp = counts["true_positive_access_expansion"]
        distribution = "; ".join(f"{label}: {counts[label]}" for label in sorted(ALLOWED_LABELS) if counts[label])
        out.append([value or "(blank)", str(total), str(tp), f"{tp / total:.1%}" if total else "0.0%", distribution])
    return out


def high_risk_rows(rows: list[dict[str, str]]) -> list[list[str]]:
    grouped = nested_label_counts([row for row in rows if row.get("high_risk_phrase_flag") == "yes"], "phrase")
    out: list[list[str]] = []
    for phrase in sorted(grouped):
        counts = grouped[phrase]
        total = sum(counts.values())
        tp = counts["true_positive_access_expansion"]
        distribution = "; ".join(f"{label}: {counts[label]}" for label in sorted(ALLOWED_LABELS) if counts[label])
        out.append([phrase, str(total), str(tp), f"{tp / total:.1%}" if total else "0.0%", distribution])
    return out


def top_true_positive_firms(rows: list[dict[str, str]], limit: int = 25) -> list[list[str]]:
    counts: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        if row.get("final_label_v2") == "true_positive_access_expansion":
            counts[(row.get("firm_id", ""), row.get("ticker", ""), row.get("cik", ""))] += 1
    return [[firm, ticker, cik, str(count)] for (firm, ticker, cik), count in counts.most_common(limit)]


def top_true_positive_phrases(rows: list[dict[str, str]], limit: int = 25) -> list[list[str]]:
    counts: Counter[str] = Counter()
    for row in rows:
        if row.get("final_label_v2") == "true_positive_access_expansion":
            counts[row.get("phrase", "")] += 1
    return [[phrase or "(blank)", str(count)] for phrase, count in counts.most_common(limit)]


def filing_key(row: dict[str, str]) -> tuple[str, str]:
    return (row.get("cik", ""), row.get("accession_number", ""))


def write_report(
    rows: list[dict[str, str]],
    raw_before: str,
    raw_after: str,
    review_artifacts: dict[int, ClassificationArtifact],
    validation_artifacts: dict[int, ClassificationArtifact],
) -> None:
    label_counts = counter_by(rows, "final_label_v2")
    source_counts = counter_by(rows, "label_source_v2")
    confidence_counts = counter_by(rows, "final_confidence_v2")
    true_positive_rows = [row for row in rows if row.get("final_label_v2") == "true_positive_access_expansion"]
    true_positive_filings = {filing_key(row) for row in true_positive_rows}
    high_risk = [row for row in rows if row.get("high_risk_phrase_flag") == "yes"]
    high_risk_tp = sum(1 for row in high_risk if row.get("final_label_v2") == "true_positive_access_expansion")
    low_confidence_positive_count = sum(
        1
        for row in rows
        if row.get("final_label_v2") == "true_positive_access_expansion" and row.get("final_confidence_v2") == "low"
    )
    output_hash = file_sha256(OUTPUT_PATH) if OUTPUT_PATH.exists() else ""

    lines = [
        "# Full Corpus Classification V2 Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope And Guardrails",
        "",
        "- Classified all rows in `data/extracted/phrase_hits.csv` under `classification_guidelines_v3.md`.",
        "- Preserved all raw phrase-hit fields in the classified output.",
        "- Preserved manual calibration, manual audit, and V2 validation-audit labels as label-source artifacts where their derived row-number `hit_id` matched the full corpus.",
        "- Classification outputs are treatment-candidate construction only, not final empirical results.",
        "- No prices, return outcomes, benchmarks, or empirical performance outcomes were loaded.",
        "- No return analysis was run and no SEC requests were made.",
        f"- Script version: `{SCRIPT_VERSION}`.",
        f"- Classifier version: `{CLASSIFIER_VERSION}`.",
        "",
        "## File Integrity",
        "",
        f"- Raw `phrase_hits.csv` SHA256 before: `{raw_before}`",
        f"- Raw `phrase_hits.csv` SHA256 after: `{raw_after}`",
        f"- Raw file unchanged: {'yes' if raw_before == raw_after else 'no'}",
        f"- Classified output SHA256: `{output_hash}`",
        "",
        "## Row Counts",
        "",
        f"- Total classified rows: {len(rows)}",
        f"- Expected raw-hit count from checkpoint: 9,400",
        f"- Raw-hit count matches expected: {'yes' if len(rows) == 9400 else 'no'}",
        f"- True-positive count: {len(true_positive_rows)}",
        f"- True-positive filings count: {len(true_positive_filings)}",
        f"- High-risk phrase rows: {len(high_risk)}",
        f"- High-risk true-positive rows: {high_risk_tp}",
        f"- High-risk positive rate: {high_risk_tp / len(high_risk):.1%}" if high_risk else "- High-risk positive rate: 0.0%",
        f"- Low-confidence true positives: {low_confidence_positive_count}",
        f"- Review-sample artifact labels applied: {len(set(review_artifacts) - set(validation_artifacts))}",
        f"- V2 validation-audit labels applied: {len(validation_artifacts)}",
        "",
        "## Label Distribution",
        "",
    ]
    lines.extend(markdown_table(["Final label V2", "Rows"], label_distribution_rows(label_counts)))
    lines.extend(["", "## Confidence Distribution", ""])
    lines.extend(markdown_table(["Final confidence V2", "Rows"], [[k or "(blank)", str(v)] for k, v in sorted(confidence_counts.items())]))
    lines.extend(["", "## Label Source Distribution", ""])
    lines.extend(markdown_table(["Label source V2", "Rows"], [[k or "(blank)", str(v)] for k, v in sorted(source_counts.items())]))
    lines.extend(["", "## Label Distribution By Category", ""])
    lines.extend(markdown_table(["Category", "Rows", "True positives", "TP rate", "Label distribution"], label_distribution_by_field(rows, "category")))
    lines.extend(["", "## Label Distribution By Phrase", ""])
    lines.extend(markdown_table(["Phrase", "Rows", "True positives", "TP rate", "Label distribution"], label_distribution_by_field(rows, "phrase")))
    lines.extend(["", "## Label Distribution By Section", ""])
    lines.extend(markdown_table(["Section", "Rows", "True positives", "TP rate", "Label distribution"], label_distribution_by_field(rows, "section_name")))
    lines.extend(["", "## Label Distribution By Filing Year", ""])
    lines.extend(markdown_table(["Filing year", "Rows", "True positives", "TP rate", "Label distribution"], label_distribution_by_field(rows, "filing_year")))
    lines.extend(["", "## High-Risk Phrase Counts And Positive Rates", ""])
    lines.extend(markdown_table(["Phrase", "Rows", "True positives", "TP rate", "Label distribution"], high_risk_rows(rows)))
    lines.extend(["", "## Top Firms By Classified True-Positive Count", ""])
    lines.extend(markdown_table(["Firm ID", "Ticker", "CIK", "True-positive rows"], top_true_positive_firms(rows)))
    lines.extend(["", "## Top Phrases Driving True Positives", ""])
    lines.extend(markdown_table(["Phrase", "True-positive rows"], top_true_positive_phrases(rows)))
    lines.extend(
        [
            "",
            "## Recommended Post-Scale Spot Checks",
            "",
            "- Audit high-risk phrase positives, especially `affordable housing`, market-access phrases, `access to credit`, institutional-quality phrases, `fractional share`, and barrier-reduction phrases.",
            "- Audit low-confidence true positives and a small sample of medium-confidence positives from each category.",
            "- Review firms with the largest true-positive counts for repeated boilerplate or section-extraction artifacts.",
            "- Review phrases with unusually high true-positive concentration before constructing filing-level treatment variables.",
            "- Confirm that validation-source rows remain locked before any downstream treatment-variable build.",
            "",
            "## Guardrail Warning",
            "",
            "No return outcomes, prices, benchmark returns, or empirical performance data have been loaded. This report makes no empirical performance claims and should not be used as a return-analysis result.",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def validate_output(rows: list[dict[str, str]], raw_fields: list[str], raw_before: str, raw_after: str) -> None:
    if len(rows) != 9400:
        raise ValueError(f"expected 9,400 classified rows, found {len(rows)}")
    if raw_before != raw_after:
        raise ValueError("raw phrase_hits.csv hash changed during classification")
    for index, row in enumerate(rows, start=1):
        for field in OUTPUT_FIELDS:
            if not row.get(field):
                raise ValueError(f"row {index} missing required output field {field}")
        validate_label(row["final_label_v2"], f"final output hit_id {index}")
        if row["classifier_version"] != CLASSIFIER_VERSION:
            raise ValueError(f"row {index} has unexpected classifier_version")
        if row["high_risk_phrase_flag"] not in {"yes", "no"}:
            raise ValueError(f"row {index} has invalid high_risk_phrase_flag")
    for field in raw_fields:
        if field not in rows[0]:
            raise ValueError(f"raw field missing from output: {field}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify all raw phrase hits using V2 classification framework.")
    parser.add_argument("--input", default=str(RAW_PHRASE_HITS_PATH))
    parser.add_argument("--review-artifacts", default=str(REVIEW_CLASSIFIED_V2_PATH))
    parser.add_argument("--validation-artifacts", default=str(VALIDATION_AUDITED_PATH))
    parser.add_argument("--output", default=str(OUTPUT_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    field_size_limit()
    if not GUIDELINES_V3_PATH.exists():
        raise FileNotFoundError(GUIDELINES_V3_PATH)

    raw_path = Path(args.input)
    output_path = Path(args.output)
    raw_before = file_sha256(raw_path)
    raw_rows, raw_fields = read_csv(raw_path)
    review_artifacts = load_review_artifacts(Path(args.review_artifacts))
    validation_artifacts = load_validation_artifacts(Path(args.validation_artifacts))
    overlap = set(review_artifacts) & set(validation_artifacts)
    for hit_id in overlap:
        review = review_artifacts[hit_id]
        validation = validation_artifacts[hit_id]
        if review.label != validation.label:
            raise ValueError(f"validation disagreement with review artifact at hit_id {hit_id}")

    classified = classify_all(raw_rows, review_artifacts, validation_artifacts)
    output_fields = raw_fields + OUTPUT_FIELDS
    write_csv(output_path, classified, output_fields)
    raw_after = file_sha256(raw_path)
    validate_output(classified, raw_fields, raw_before, raw_after)
    write_report(classified, raw_before, raw_after, review_artifacts, validation_artifacts)

    print(
        "Classified full phrase-hit corpus v2: "
        f"rows={len(classified)}, true_positives={sum(1 for row in classified if row['final_label_v2'] == 'true_positive_access_expansion')}, "
        f"raw_hash_unchanged={'yes' if raw_before == raw_after else 'no'}"
    )
    print(f"Wrote {output_path.resolve().relative_to(PROJECT_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
