# CHECKPOINT 05: Phrase Matching

Generated at: 2026-06-29T04:50:28.200906+00:00

## Completed

- Built initial phrase taxonomy for access-related raw phrase matching.
- Implemented local-only raw exact-match hit detector.
- Ran a small sample dry-run before full-corpus matching.
- Wrote raw phrase hits separately from any later classification layer.
- Wrote phrase-hit quality report with aggregate counts and representative excerpts.

## Explicit Non-Actions

- No true-positive classification.
- No price fetching.
- No SEC requests.
- No research claims.
- No return analysis.

## Inputs

- Phrase taxonomy rows: 88
- Section rows scanned: 17862
- Sample dry-run rows scanned first: 250

## Outputs

- `config\access_phrases.csv`
- `scripts\match_phrases.py`
- `data\extracted\phrase_hits.csv`
- `quality_reports\phrase_hit_report.md`
- `CHECKPOINT_05_PHRASE_MATCHING.md`

## Raw Hit Counts

- Total phrase hits: 9400
- Unique filings with at least one hit: 3042
- Candidate matches before overlap suppression: 10130
- Overlapping duplicate candidates suppressed: 730

## Warning

Raw phrase hits are not interpreted evidence. Later classification or manual audit is required before treating any hit as substantively about access-oriented disclosure.

## Next Recommended Prompt

Audit `quality_reports/phrase_hit_report.md` and review representative raw excerpts and high false-positive-risk phrases before building a classification layer.
