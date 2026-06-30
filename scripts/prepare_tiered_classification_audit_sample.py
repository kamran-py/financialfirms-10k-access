"""Prepare a post-tiered classification audit sample.

This script samples from the already-created tiered classification output only.
It does not modify raw phrase hits or the tiered classified file, and it does
not fetch prices, compute returns, or make SEC requests.
"""

from __future__ import annotations

import csv
import hashlib
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


INPUT_PATH = Path("data/classified/phrase_hits_tiered_v1.csv")
RAW_PATH = Path("data/extracted/phrase_hits.csv")
OUTPUT_PATH = Path("data/review/tiered_classification_audit_sample.csv")
PLAN_PATH = Path("quality_reports/tiered_classification_audit_plan.md")

RANDOM_SEED = 1601

TARGETS = {
    "tier_1_conservative": 75,
    "tier_2_broader_validated": 50,
    "excluded_non_treatment": 25,
}

AUDIT_FIELDS = [
    "audit_tiered_label",
    "audit_confidence",
    "audit_narrative_subcategory",
    "audit_notes",
    "audit_disagreement_flag",
]

TREATMENT_LABELS = {"tier_1_conservative", "tier_2_broader_validated"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError(f"No header found in {path}")
        return list(reader.fieldnames), rows


def normalize(value: str | None) -> str:
    return (value or "").strip()


def row_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        normalize(row.get("firm_id")),
        normalize(row.get("ticker")),
        normalize(row.get("cik")),
        normalize(row.get("accession_number")),
        normalize(row.get("filing_date")),
        normalize(row.get("section_name")),
        normalize(row.get("phrase")),
        normalize(row.get("match_start")),
        normalize(row.get("match_end")),
        normalize(row.get("source_file")),
    )


def firm_key(row: dict[str, str]) -> str:
    firm_id = normalize(row.get("firm_id"))
    if firm_id:
        return firm_id
    cik = normalize(row.get("cik"))
    return f"CIK{cik}" if cik else normalize(row.get("ticker"))


def table(counter: Counter[str], headers: tuple[str, str]) -> str:
    lines = [f"| {headers[0]} | {headers[1]} |", "| --- | ---: |"]
    for key, count in counter.most_common():
        lines.append(f"| {key or '(blank)'} | {count} |")
    return "\n".join(lines)


def label_counts_by(rows: list[dict[str, str]], column: str) -> dict[str, Counter[str]]:
    result: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        result[normalize(row.get(column))][normalize(row.get("tiered_label"))] += 1
    return result


def score_row(
    row: dict[str, str],
    high_count_firms: set[str],
    high_count_subcategories: set[str],
    rng: random.Random,
) -> tuple[float, str, str, str]:
    label = normalize(row.get("tiered_label"))
    family = normalize(row.get("high_risk_phrase_family"))
    score = 0.0

    if normalize(row.get("high_risk_phrase_flag")).lower() == "yes":
        score += 100
    if family and family != "none":
        score += 75
    if "risk-section access language" in family:
        score += 35
    if "CRA/regulatory language" in family:
        score += 30
    if firm_key(row) in high_count_firms:
        score += 25
    if normalize(row.get("narrative_subcategory")) in high_count_subcategories:
        score += 15
    if label in TREATMENT_LABELS and normalize(row.get("tiered_confidence")).lower() == "medium":
        score += 8
    if label == "excluded_non_treatment" and family != "none":
        score += 12
    score += rng.random()
    return (
        -score,
        normalize(row.get("filing_year")),
        normalize(row.get("firm_id")),
        normalize(row.get("accession_number")),
    )


def add_best_for_value(
    pool: list[dict[str, str]],
    selected: list[dict[str, str]],
    selected_keys: set[tuple[str, ...]],
    value_column: str,
    value: str,
    target: int,
    high_count_firms: set[str],
    high_count_subcategories: set[str],
    rng: random.Random,
) -> None:
    if len(selected) >= target:
        return
    candidates = [
        row
        for row in pool
        if row_key(row) not in selected_keys and normalize(row.get(value_column)) == value
    ]
    if not candidates:
        return
    candidates.sort(key=lambda row: score_row(row, high_count_firms, high_count_subcategories, rng))
    chosen = candidates[0]
    selected.append(chosen)
    selected_keys.add(row_key(chosen))


def add_best_matching(
    pool: list[dict[str, str]],
    selected: list[dict[str, str]],
    selected_keys: set[tuple[str, ...]],
    target: int,
    high_count_firms: set[str],
    high_count_subcategories: set[str],
    rng: random.Random,
    predicate,
) -> None:
    if len(selected) >= target:
        return
    candidates = [row for row in pool if row_key(row) not in selected_keys and predicate(row)]
    if not candidates:
        return
    candidates.sort(key=lambda row: score_row(row, high_count_firms, high_count_subcategories, rng))
    chosen = candidates[0]
    selected.append(chosen)
    selected_keys.add(row_key(chosen))


def sample_label(
    rows: list[dict[str, str]],
    label: str,
    target: int,
    high_count_firms: set[str],
    high_count_subcategories: set[str],
    rng: random.Random,
) -> list[dict[str, str]]:
    pool = [row for row in rows if normalize(row.get("tiered_label")) == label]
    if len(pool) < target:
        raise ValueError(f"Cannot sample {target} rows for {label}; only {len(pool)} available")

    selected: list[dict[str, str]] = []
    selected_keys: set[tuple[str, ...]] = set()

    # Cover high-risk families first, especially where the classifier admitted
    # high-risk language into Tier 1 or Tier 2.
    families = Counter(normalize(row.get("high_risk_phrase_family")) for row in pool)
    for family, _ in families.most_common():
        if family and family != "none":
            add_best_for_value(
                pool,
                selected,
                selected_keys,
                "high_risk_phrase_family",
                family,
                target,
                high_count_firms,
                high_count_subcategories,
                rng,
            )

    # Ensure all available sections and years are represented when feasible.
    for section, _ in Counter(normalize(row.get("section_name")) for row in pool).most_common():
        add_best_for_value(
            pool,
            selected,
            selected_keys,
            "section_name",
            section,
            target,
            high_count_firms,
            high_count_subcategories,
            rng,
        )
    for year in sorted({normalize(row.get("filing_year")) for row in pool}):
        add_best_for_value(
            pool,
            selected,
            selected_keys,
            "filing_year",
            year,
            target,
            high_count_firms,
            high_count_subcategories,
            rng,
        )

    # Include major positive subcategories and high-count firms.
    for subcat, _ in Counter(normalize(row.get("narrative_subcategory")) for row in pool).most_common():
        add_best_for_value(
            pool,
            selected,
            selected_keys,
            "narrative_subcategory",
            subcat,
            target,
            high_count_firms,
            high_count_subcategories,
            rng,
        )
    for firm in sorted(high_count_firms):
        add_best_matching(
            pool,
            selected,
            selected_keys,
            target,
            high_count_firms,
            high_count_subcategories,
            rng,
            lambda row, firm=firm: firm_key(row) == firm,
        )

    # Fill the remainder with a score that favors high-risk rows, high-count
    # firms, and high-count positive subcategories.
    remaining = [row for row in pool if row_key(row) not in selected_keys]
    remaining.sort(key=lambda row: score_row(row, high_count_firms, high_count_subcategories, rng))
    for row in remaining:
        if len(selected) >= target:
            break
        selected.append(row)
        selected_keys.add(row_key(row))

    return selected


def md_escape(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def write_plan(
    rows: list[dict[str, str]],
    sample: list[dict[str, str]],
    raw_hash_before: str,
    raw_hash_after: str,
    input_hash_before: str,
    input_hash_after: str,
) -> None:
    PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    full_counts = Counter(normalize(row.get("tiered_label")) for row in rows)
    sample_counts = Counter(normalize(row.get("tiered_label")) for row in sample)
    sample_hr = Counter(normalize(row.get("high_risk_phrase_flag")) for row in sample)
    sample_family = Counter(normalize(row.get("high_risk_phrase_family")) for row in sample)
    sample_section = Counter(normalize(row.get("section_name")) for row in sample)
    sample_year = Counter(normalize(row.get("filing_year")) for row in sample)
    sample_subcat = Counter(normalize(row.get("narrative_subcategory")) for row in sample)
    sample_phrase = Counter(normalize(row.get("phrase")) for row in sample)

    by_label_family = label_counts_by(sample, "high_risk_phrase_family")
    by_label_section = label_counts_by(sample, "section_name")
    by_label_year = label_counts_by(sample, "filing_year")

    lines = [
        "# Tiered Classification Audit Plan",
        "",
        f"Generated at: {now}",
        "",
        "## Scope And Guardrails",
        "",
        "- Prepared a post-tiered classification audit sample from `data/classified/phrase_hits_tiered_v1.csv`.",
        "- Did not modify `data/extracted/phrase_hits.csv`.",
        "- Did not modify `data/classified/phrase_hits_tiered_v1.csv`.",
        "- No prices were fetched, no returns were computed, no SEC requests were made, and no empirical performance claims were made.",
        "- This sample validates text-treatment candidates only.",
        "",
        "## File Integrity",
        "",
        f"- Raw `phrase_hits.csv` SHA256 before: `{raw_hash_before}`",
        f"- Raw `phrase_hits.csv` SHA256 after: `{raw_hash_after}`",
        f"- Raw file unchanged: {'yes' if raw_hash_before == raw_hash_after else 'no'}",
        f"- Tiered classified SHA256 before: `{input_hash_before}`",
        f"- Tiered classified SHA256 after: `{input_hash_after}`",
        f"- Tiered classified file unchanged: {'yes' if input_hash_before == input_hash_after else 'no'}",
        "",
        "## Full-Corpus Counts",
        "",
        f"- Total tiered classified rows: {len(rows)}",
        table(full_counts, ("Tiered label", "Rows")),
        "",
        "## Audit Sample Design",
        "",
        "- Total target sample size: 150 rows.",
        "- Target label split: 75 Tier 1, 50 Tier 2, 25 excluded.",
        "- Deterministic sampling seed: 1601.",
        "- Oversampling priorities: high-risk phrase flags and families, high-count firms, all sections where feasible, filing years 2015-2025, and high-count narrative subcategories.",
        "- Tier 3 rows are not sampled directly in this audit because the requested validation design focuses on Tier 1, Tier 2, and excluded false negatives.",
        "",
        "## Sample Counts",
        "",
        f"- Audit sample rows: {len(sample)}",
        table(sample_counts, ("Tiered label", "Sample rows")),
        "",
        "## High-Risk Coverage",
        "",
        table(sample_hr, ("High-risk flag", "Sample rows")),
        "",
        table(sample_family, ("High-risk phrase family", "Sample rows")),
        "",
        "## Coverage By Section",
        "",
        table(sample_section, ("Section", "Sample rows")),
        "",
        "## Coverage By Filing Year",
        "",
        table(sample_year, ("Filing year", "Sample rows")),
        "",
        "## Coverage By Narrative Subcategory",
        "",
        table(sample_subcat, ("Narrative subcategory", "Sample rows")),
        "",
        "## Top Sample Phrases",
        "",
        table(Counter(dict(sample_phrase.most_common(25))), ("Phrase", "Sample rows")),
        "",
        "## Label Coverage Diagnostics",
        "",
        "### High-Risk Family By Label",
        "",
    ]

    for family, counts in sorted(by_label_family.items()):
        lines.append(f"- {md_escape(family or '(blank)')}: " + ", ".join(f"{k}={v}" for k, v in counts.items()))

    lines.extend(["", "### Section By Label", ""])
    for section, counts in sorted(by_label_section.items()):
        lines.append(f"- {md_escape(section or '(blank)')}: " + ", ".join(f"{k}={v}" for k, v in counts.items()))

    lines.extend(["", "### Filing Year By Label", ""])
    for year, counts in sorted(by_label_year.items()):
        lines.append(f"- {md_escape(year or '(blank)')}: " + ", ".join(f"{k}={v}" for k, v in counts.items()))

    lines.extend(
        [
            "",
            "## Manual Audit Instructions",
            "",
            "Fill `audit_tiered_label`, `audit_confidence`, `audit_narrative_subcategory`, `audit_notes`, and `audit_disagreement_flag` using only the excerpt and tiered classification guidelines.",
            "",
            "Allowed `audit_tiered_label` values:",
            "",
            "- `tier_1_conservative`",
            "- `tier_2_broader_validated`",
            "- `tier_3_exploratory`",
            "- `excluded_non_treatment`",
            "",
            "`audit_disagreement_flag` must be `yes` when the audit label differs from the original `tiered_label`, otherwise `no`.",
            "",
            "## Decision Rules For Results Report",
            "",
            "- Tier 1 may proceed to main treatment-candidate construction only if sampled Tier 1 precision is at least 90%.",
            "- Tier 2 may proceed to broader/sensitivity treatment-candidate construction only if sampled Tier 2 precision is at least 80%.",
            "- If excluded false-negative rate exceeds 20%, revise the classifier before treatment construction.",
            "- If Tier 1 precision is below 90%, revise the classifier before treatment construction.",
        ]
    )

    PLAN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    raw_hash_before = sha256(RAW_PATH)
    input_hash_before = sha256(INPUT_PATH)

    fieldnames, rows = read_rows(INPUT_PATH)
    rng = random.Random(RANDOM_SEED)

    label_counts = Counter(normalize(row.get("tiered_label")) for row in rows)
    missing = [
        row
        for row in rows
        if not normalize(row.get("tiered_label"))
        or not normalize(row.get("tiered_confidence"))
        or not normalize(row.get("narrative_subcategory"))
        or not normalize(row.get("classifier_version"))
        or not normalize(row.get("high_risk_phrase_flag"))
    ]
    if missing:
        raise ValueError(f"Tiered classified file has {len(missing)} rows with required blank fields")

    treatment_rows = [row for row in rows if normalize(row.get("tiered_label")) in TREATMENT_LABELS]
    firm_counts = Counter(firm_key(row) for row in treatment_rows if firm_key(row))
    high_count_firms = {firm for firm, _ in firm_counts.most_common(30)}

    subcat_counts = Counter(
        normalize(row.get("narrative_subcategory"))
        for row in treatment_rows
        if normalize(row.get("narrative_subcategory")) != "excluded / non-treatment"
    )
    high_count_subcategories = {subcat for subcat, _ in subcat_counts.most_common(7)}

    sample: list[dict[str, str]] = []
    for label, target in TARGETS.items():
        if label_counts[label] < target:
            raise ValueError(
                f"Requested {target} rows for {label}, but only {label_counts[label]} rows are available"
            )
        sample.extend(sample_label(rows, label, target, high_count_firms, high_count_subcategories, rng))

    if len(sample) != sum(TARGETS.values()):
        raise ValueError(f"Expected {sum(TARGETS.values())} sampled rows, got {len(sample)}")
    if len({row_key(row) for row in sample}) != len(sample):
        raise ValueError("Duplicate sampled rows detected")

    sample_counts = Counter(normalize(row.get("tiered_label")) for row in sample)
    for label, target in TARGETS.items():
        if sample_counts[label] != target:
            raise ValueError(f"Expected {target} sampled {label} rows, got {sample_counts[label]}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    output_fields = list(fieldnames) + AUDIT_FIELDS
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=output_fields, lineterminator="\n")
        writer.writeheader()
        for row in sample:
            out = dict(row)
            for field in AUDIT_FIELDS:
                out[field] = ""
            writer.writerow(out)

    raw_hash_after = sha256(RAW_PATH)
    input_hash_after = sha256(INPUT_PATH)

    write_plan(rows, sample, raw_hash_before, raw_hash_after, input_hash_before, input_hash_after)

    print(f"rows_in={len(rows)}")
    print(f"sample_rows={len(sample)}")
    print("sample_counts=" + ", ".join(f"{label}:{sample_counts[label]}" for label in TARGETS))
    print(f"raw_unchanged={'yes' if raw_hash_before == raw_hash_after else 'no'}")
    print(f"tiered_unchanged={'yes' if input_hash_before == input_hash_after else 'no'}")
    print(f"sample_path={OUTPUT_PATH}")
    print(f"plan_path={PLAN_PATH}")


if __name__ == "__main__":
    main()
