# Methodology Notes

## Interpretive Boundaries

This project measures associations between filing language and later stock returns. It does not establish that access-related language caused later performance unless a separate causal research design is specified and justified.

The project also does not infer management intent. Statements should be limited to what the filing text says. For example, "the filing states that the company seeks to broaden access to credit" is acceptable when supported by text. "Management intended to democratize finance" is not acceptable unless the filing itself says that.

## Claims We Are Not Allowed To Make

- No causal claims about filing language and subsequent stock performance without a separate identification strategy.
- No claims about management intent, sincerity, strategic priority, or actual access expansion unless the filing text directly supports the statement.
- No claims about 1-, 3-, or 5-year returns when the corresponding window is not observable as of 2026-06-27.
- No claims that right-censored windows are equivalent to zero returns, ordinary missingness, or complete observations.
- No claims that a current index, current exchange, or current ticker universe represents the historical US-listed financial and fintech universe.
- No claims that adjusted price data are reliable until corporate actions, stale prices, missing observations, and extreme returns have been checked.
- No claims that raw phrase hits are substantively about access expansion without classification or manual audit evidence.
- No claims based on selected favorable phrases, sections, horizons, benchmarks, or subgroups unless the selection was pre-specified or labeled exploratory.

## Minimum Evidence Required Before Interpretation

Interpretive writeups require the following minimum evidence:

- A point-in-time firm universe with inclusion and exclusion reason-code counts.
- Historical identifiers covering ticker changes, name changes, exchange changes, delistings, mergers, bankruptcies, and unresolved mappings.
- Filing-level metadata including CIK, accession number, EDGAR filing date, acceptance datetime where available, fiscal year end or report period, filing URL, and document URL.
- Extraction status and section-parsing status for every filing, including failures and low-confidence sections.
- Raw phrase hits linked to exact phrase, excerpt, section, taxonomy version, matcher version, filing URL, and accession number.
- A validated classification layer that distinguishes substantive access-expansion use from false positives, generic language, negative context, and ambiguous cases.
- Return-window status for every filing-window pair, including complete, right-censored, delisted, merged, bankrupt, unresolved security link, missing start price, and missing end price.
- Price-source provenance and adjusted-price quality checks.
- Pre-specified market and financial-sector benchmarks with dated source metadata.
- A multiple-testing inventory that records all planned and exploratory tests.

## Sample Period And Observability

The filing sample covers filing years 2015-2025. The project as-of date is 2026-06-27.

Return-window observability:

- 1-year windows are observable only for filings whose target 1-year end date is on or before 2026-06-27.
- 3-year windows are observable only for filings whose target 3-year end date is on or before 2026-06-27.
- 5-year windows are observable only for filings whose target 5-year end date is on or before 2026-06-27.

Windows that are not mature by 2026-06-27 must remain in the dataset with a reason code. They must not be filtered out silently.

Right-censoring is a design feature, not a data-cleaning nuisance. For example, most 2024 and 2025 filings cannot have 3- or 5-year returns by 2026-06-27. These windows should be counted and reported as right-censored. They should not be imputed, backfilled, annualized from shorter windows, or excluded from denominators without disclosure.

## Filing Year Definition

The proposed default is to define filing year by SEC filing date, not fiscal year end. This avoids look-ahead ambiguity and aligns the language date with the return-measurement anchor. This should be confirmed before implementation.

Fiscal year end and report period must still be stored. EDGAR filing date and fiscal year end answer different questions: filing date is the market-information release date for return windows, while fiscal year end is an accounting-period descriptor. Tables and figures must label which date convention they use.

## Point-In-Time Universe And Index Membership

The issuer universe must be built from point-in-time listing and filing eligibility, not from firms active in 2026. A firm remains in scope if it was US-listed during a relevant filing year and filed a 10-K, even if it later delisted, merged, went bankrupt, changed name, or changed ticker.

If index membership is used for either universe construction or benchmarking, membership dates must be stored. Current constituents must not be projected backward. Index inclusion after the filing date cannot be used to classify a filing-date observation.

Industry classification should also be dated where possible. If only current industry data are available, the resulting sample should be labeled as potentially look-ahead biased and used only as a sensitivity analysis.

## Raw Phrase Hits

Raw phrase hits are exact, deterministic matches against a versioned phrase taxonomy. They are not interpreted as claims about intent or true business practice.

Required raw-hit fields include:

- CIK
- accession number
- filing URL
- filing date
- section label or section parse status
- exact matched phrase
- phrase family
- excerpt
- offsets where available
- taxonomy version
- matching-run version

Zero-hit filings should be represented explicitly in a filing-level summary table.

Known false-positive risks include generic "market access", technology access, customer-service language, risk-factor hypotheticals, boilerplate, negative statements, litigation language, quotations, historical descriptions, and references to access restrictions rather than expansion. The raw-hit table should preserve these cases; the classification layer should identify them.

## Interpreted Or Classified Hits

Interpreted hits are a second layer built from raw hits. They may label whether a raw phrase actually refers to expanding access, democratization, barrier reduction, affordability, product availability, market access, or other dimensions.

Interpreted labels should never overwrite raw matches. Multiple classification runs can coexist. Each run needs:

- method type
- version
- codebook or prompt location if applicable
- model or reviewer metadata if applicable
- confidence score or equivalent uncertainty field
- classification status and reason code

The codebook must include at least one negative or non-substantive label and at least one ambiguous label. A phrase should not be coded as access expansion merely because it contains a dictionary phrase.

## Proposed Phrase Families

Initial phrase families for design discussion:

- democratization: "democratize", "democratizing", "democratized"
- broadening access: "broaden access", "broader access", "expand access", "expanded access", "expanding access"
- barrier reduction: "lower barriers", "lowering barriers", "reduce barriers", "reducing barriers", "remove barriers"
- financial inclusion: "financial inclusion", "inclusive finance", "underserved", "underbanked", "unbanked"
- credit access: "access to credit", "credit access", "affordable credit"
- banking access: "access to banking", "banking access", "digital banking access"
- investing access: "access to investing", "retail investors", "fractional shares"
- market access: "market access", "access to markets", "capital markets access"
- institutional-grade access: "institutional-grade", "institutional quality", "previously available only to institutions"
- housing access: "access to housing", "homeownership access", "affordable housing"

The final taxonomy should be reviewed for false positives, overly broad terms, and sector-specific usage.

Before using interpreted labels in return comparisons, the project should complete a validation sample that estimates false-positive and ambiguous-use rates by phrase family and section. The validation sample should include both hits and non-hits if the analysis makes statements about absence of access language.

## Section Treatment

Section labels are useful for auditability and interpretation but may be noisy in SEC filings. The pipeline should record section-parser confidence and reason codes.

Potential section buckets:

- Business
- Risk Factors
- Management's Discussion and Analysis
- Properties
- Legal Proceedings
- Market for Registrant's Common Equity
- Other or unknown

The analysis should be able to include all sections or restrict to selected sections as a robustness check.

Section extraction failures must be represented explicitly. A failed or low-confidence section parse means "section unknown" or "section unreliable"; it does not mean the phrase was absent from that section. Section-restricted analyses must report how many filings and hits were excluded or moved to unknown-section buckets.

## Stock Return Measurement

The return convention must be selected before implementation.

Recommended default for discussion:

- Anchor at the first tradable close after the filing becomes public.
- If SEC acceptance datetime is after market close, use the next trading day as the start price date.
- Use adjusted close or total return series, depending on source availability.
- Include delisting returns where the provider supports them.
- Track ticker changes, name changes, exchange changes, mergers, bankruptcies, and delistings as dated events, not as free-text exceptions.
- Compute raw returns and pre-specified benchmark-adjusted returns separately.

Return observations must include:

- filing ID
- security ID
- anchor date
- target end date
- realized start price date
- realized end price date
- start price
- end price
- return value
- source
- status
- reason code

Adjusted price data require validation before interpretation. Minimum checks include split adjustment continuity, dividend or total-return treatment, missing start and end prices, stale prices, currency consistency, duplicate prices, extreme one-day returns, delisting returns, and provider revision or vintage notes.

## Benchmark Selection

Benchmark choice must be pre-specified. A broad US equity benchmark and a financial-sector benchmark should be considered separately because financial and fintech firms can have sector-specific risk exposures.

Candidate benchmark decisions:

- Broad market benchmark, such as a total-market or S&P 500 return series.
- Financial-sector benchmark, such as a financial-sector index or ETF return series.
- Fintech-specific benchmark only if point-in-time constituents and investable return history are available.
- Equal-weighted versus value-weighted benchmark treatment.

Benchmark-adjusted returns should not replace raw returns. Both should be retained, and benchmark source, date, construction, and limitations should be documented.

## Missingness And Reason Codes

No observation should disappear without explanation. Missingness should be explicit for:

- no expected filing
- filing metadata unavailable
- filing document unavailable
- text extraction failed
- section parsing failed
- no raw phrase hit
- security mapping failed
- price missing at start
- price missing at end
- security delisted
- ticker changed
- company name changed
- merger or acquisition
- bankruptcy or liquidation
- index membership unavailable
- benchmark price missing
- return window not mature by 2026-06-27
- provider unavailable or license restriction

Reason-code summaries should be part of quality assurance.

## Bias Controls

Survivorship bias:

- Do not restrict to firms still listed in 2026.
- Preserve delisted, merged, bankrupt, renamed, and ticker-changed firms where source data allows.
- Do not use current index constituents as the historical universe.

Selection bias:

- Store the candidate issuer universe before final inclusion rules.
- Record inclusion and exclusion reason codes.
- Store point-in-time index membership and industry classification when used.

Look-ahead bias:

- Do not use post-filing information to define filing-time firm attributes unless explicitly flagged as retrospective.
- Do not classify a return window as available unless mature as of 2026-06-27.
- Keep current identifiers separate from historical identifiers.
- Do not revise phrase taxonomy or primary classification rules after inspecting return results unless the revision is labeled exploratory and versioned separately.

Text measurement bias:

- Separate raw phrase hits from interpreted labels.
- Version dictionaries, parsers, and classifiers.
- Audit excerpts manually for a sample of hits and non-hits.

Semantic overreach:

- Do not translate disclosure wording into claims about real-world access expansion without external evidence.
- Do not infer managerial intent from access-related wording.
- Use "raw access-related phrase hit" for dictionary matches and reserve stronger labels for validated interpreted classifications.

Multiple testing and narrative cherry-picking:

- Pre-register or freeze the primary phrase families, classification labels, return horizons, benchmarks, and subgroup cuts before analysis.
- Maintain a test inventory that includes null, mixed, and unfavorable results.
- Apply multiple-testing corrections or false-discovery procedures for families of related tests.
- Clearly separate confirmatory tests from exploratory searches.
