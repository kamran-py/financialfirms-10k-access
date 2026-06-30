# CHECKPOINT 23: Validated Conservative Filing Treatments

Generated at: 2026-06-29

## Completed

- Converted V3 candidate layer into a validated conservative filing-level treatment dataset.
- Preserved validation metadata from CHECKPOINT_22.
- Added event dates based on 10-K filing dates.
- Added calendar-only 1-year, 3-year, and 5-year window maturity flags.
- Retained evidence excerpts for treated filings.
- Did not fetch prices, compute returns, load benchmarks, make SEC requests, or make empirical claims.

## Files Created

- `scripts/build_validated_conservative_treatments_v1.py`
- `data/treatments/validated_conservative_filing_treatments_v1.csv`
- `data/treatments/validated_conservative_filing_treatment_evidence_v1.csv`
- `quality_reports/validated_conservative_filing_treatments_v1_report.md`
- `CHECKPOINT_23_VALIDATED_CONSERVATIVE_TREATMENTS.md`

## Counts

- Treatment panel filings: 5,954
- Validated conservative treated filings: 182
- Untreated/control filings: 5,772
- Treated evidence rows: 330

## Validation Metadata

- Candidate-positive precision estimate: 92.0%.
- Candidate-negative false-negative estimate: 0.0%.
- Validation source: `CHECKPOINT_22_CONSERVATIVE_FILING_TREATMENT_V3_AUDIT.md`.

## Guardrails

- No prices fetched.
- No returns computed.
- No benchmarks loaded.
- No SEC requests made.
- No empirical performance claims made.

## Next

Proceed to security-linking and return-data preparation only after reviewing the validated treatment output. Ask for the SEC user-agent before any future SEC request stage.
