# Data Availability

This repository does not publish raw SEC filing downloads, WRDS/CRSP files, or row-level security-return panels.

The project uses:

- Public SEC EDGAR 10-K filings.
- WRDS/CRSP security links and daily returns, subject to WRDS licensing.
- Project-generated text classifications and return-window outputs.

Only aggregate, publication-safe analysis tables are tracked in Git:

- baseline coefficient tables,
- inference diagnostics,
- bootstrap diagnostics,
- equivalence diagnostics,
- sample-support summaries,
- winsorization thresholds.

Row-level datasets can be regenerated from the scripts if the user has the required SEC and WRDS/CRSP access.
