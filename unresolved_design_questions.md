# Unresolved Design Questions

## Firm Universe

1. Should "financial and fintech-related" be defined primarily by SIC, NAICS, GICS, exchange-listed industry classifications, keyword/company descriptions, or a curated firm list?
2. Should non-bank fintech firms outside financial SIC ranges be included through a separate taxonomy?
3. Should insurers, REITs, asset managers, exchanges, payment processors, mortgage firms, crypto-related firms, and data/analytics vendors all be included?
4. Should SPACs, blank-check companies, ETFs, closed-end funds, BDCs, and trusts be excluded by default?
5. How should duplicate share classes be handled?
6. Should delisted, acquired, bankrupt, or renamed firms be included if they were US-listed during the sample period?

## Filing Scope

1. Does "filing years 2015-2025" mean SEC filing-date year or fiscal year-end year?
2. Should 10-K/A amendments be excluded, included separately, or allowed to replace original 10-K filings?
3. How should firms with multiple 10-K filings in a calendar year be handled?
4. Should transition reports or 20-F/40-F foreign issuer reports be excluded?
5. Should inline XBRL exhibits or only the primary HTML/text document be used for text extraction?

## Text Extraction And Sections

1. Which parser should be used for SEC HTML, legacy text filings, and inline XBRL filings?
2. What section taxonomy is required for auditability?
3. Should phrase matching search the whole filing or only selected sections?
4. How should tables, exhibits, signatures, and repeated navigation text be handled?
5. What excerpt length is sufficient for audit while avoiding excessive storage?

## Phrase Taxonomy

1. Which exact phrases should be included in the first taxonomy version?
2. Should matching use exact phrase boundaries, stemming, lemmatization, or regex variants?
3. How should broad terms such as "access", "underserved", or "market access" be constrained to reduce false positives?
4. Should negative contexts, boilerplate, risk-factor hypotheticals, and customer quotes be classified separately?
5. Should phrase families distinguish consumer access, business access, institutional access, housing access, credit access, investing access, and banking access?

## Classification

1. Should interpreted hit classification be manual, rule-based, model-assisted, or hybrid?
2. What labels should be used for interpreted access-language categories?
3. Should the project classify filing-level presence, phrase-level context, or both?
4. What confidence thresholds or adjudication rules should apply?
5. How should inter-rater reliability or model validation be documented?

## Market Data And Returns

1. Which price source should be used: CRSP, Compustat, Bloomberg, FactSet, Polygon, Yahoo Finance, Nasdaq Data Link, or another provider?
2. Should returns be total returns including dividends, split-adjusted price returns, or both?
3. How should delisting returns be incorporated?
4. Should the start price be filing-date close, next trading-day close, or based on SEC acceptance time?
5. If a target anniversary date is not a trading day, should the next trading day, prior trading day, or nearest trading day be used?
6. How should mergers, acquisitions, ticker changes, and security identifier changes be handled?
7. Should returns be raw returns, market-adjusted returns, industry-adjusted returns, or all of these?

## Missingness And Reason Codes

1. What is the final reason-code taxonomy?
2. Which reason codes are terminal exclusions and which are recoverable processing states?
3. Should no-hit filings receive a reason code or a separate explicit zero-hit status?
4. Should missing prices due to delisting be distinguished from provider gaps?
5. How should license-restricted data be represented in public replication artifacts?

## Bias And Inference

1. What universe definition best minimizes survivorship bias?
2. How will selection bias from fintech universe construction be assessed?
3. What fields might introduce look-ahead bias if sourced retrospectively?
4. Should the primary analysis be filing-level, firm-year-level, or firm-level?
5. What robustness checks are required before describing return differences?
6. Is any causal research design intended, or is the project strictly descriptive?

