# CHECKPOINT 32: Power And Inference Diagnostics

## Status

Completed baseline power, MDE, interval, cluster-count, and table-footnote diagnostics.

## Created

- `scripts/build_inference_diagnostics_v1.py`
- `data/analysis/baseline_inference_diagnostics_v1.csv`
- `data/analysis/baseline_table_footnotes_v1.csv`
- `quality_reports/baseline_inference_diagnostics_v1_report.md`
- `CHECKPOINT_32_POWER_AND_INFERENCE_DIAGNOSTICS.md`

## Validation

- Treatment estimate rows processed: 3
- Table footnote rows written: 12
- Upstream estimate, diagnostic, modeling, return-panel, and winsor-threshold files unchanged.

## Guardrails

- No new regression specification estimated.
- No causal claims made.
- Non-significance not interpreted as proof of no association.
- Long-horizon estimates explicitly marked as lower-information because of wide intervals and larger MDEs.
