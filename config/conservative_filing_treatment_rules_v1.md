# Conservative Filing-Level Treatment Rules V1

Date: 2026-06-29

## Purpose

These rules reset treatment construction from failed hit-level V2/tiered classification to conservative filing-level treatment candidate construction. They define high-evidence text patterns that can mark an issuer filing as a candidate for later manual validation.

These rules do not create final treatment variables, do not approve return analysis, do not fetch prices, do not make SEC requests, and do not make empirical performance claims.

## Unit Of Construction

The construction unit is the filing/accession number. A filing-level conservative candidate can be positive only when at least one raw phrase-hit excerpt in that filing satisfies a high-evidence positive rule below.

Candidate evidence must preserve:

- `firm_id`
- `ticker`
- `cik`
- `accession_number`
- `filing_date`
- `filing_year`
- `section_name`
- `phrase`
- `category`
- `excerpt`
- assigned `narrative_subcategory`
- evidence rule and confidence

The candidate flag is not a final treatment variable. It is a filing-level candidate for manual audit.

## Universal Positive Requirements

Every evidence excerpt used for a conservative candidate must show:

- An external beneficiary such as consumers, customers, members, borrowers, homeowners, residents, retail or individual investors, small businesses, merchants, smaller issuers, low- and moderate-income communities, underserved communities, unbanked or underbanked consumers, or similar external users.
- A financial-access mechanism such as credit, banking, payments, money movement, investing, brokerage, alternative investments, financial markets, insurance, mortgage access, homeownership access, affordable financial services, low-cost financial services, or affordable loans.

When either element is absent, the excerpt is excluded.

## High-Evidence Positive Patterns

A filing-level conservative candidate can be positive only if at least one excerpt in the filing contains one of these patterns.

### Democratized Financial Access

Positive only when the excerpt explicitly democratizes or democratized access to finance, financial services, financial markets, investing, alternative investments, or money movement for external users.

Required context:

- Democratization wording such as `democratize`, `democratizing`, `democratized access`, or close equivalent.
- A financial mechanism: finance, financial services, financial markets, investing, investment products, alternative investments, brokerage, payments, money movement, or similar.
- An external user group such as customers, consumers, people, retail investors, individual investors, users, members, merchants, or clients.

Narrative subcategory:

- `retail investing / brokerage democratization`
- `private-market or alternative-investment access`
- `payments / money movement / SMB commerce access`
- `generic/other access-oriented disclosure` only if the mechanism is financial but does not fit the prior groups.

### Financial Inclusion With Mechanism

Positive only when the excerpt explicitly discusses financial inclusion with an external beneficiary or direct financial-access mechanism.

Required context:

- `financial inclusion`, `promote financial inclusion`, `inclusive financial system`, or close equivalent.
- A beneficiary or access mechanism tied to financial services, banking, credit, payments, insurance, savings, investing, or similar.

Narrative subcategory:

- `financial inclusion / underbanked / underserved`

### Unbanked / Underbanked / Underserved With Financial Mechanism

Positive only when `unbanked`, `underbanked`, `underserved`, low- and moderate-income, minority, or community-beneficiary language is tied to a direct financial product or service mechanism.

Required context:

- Beneficiary language: unbanked, underbanked, underserved consumers, underserved borrowers, underserved communities, low- and moderate-income, LMI, minority borrowers, small businesses, or similar.
- Mechanism language: banking, bank account, deposit, credit, loan, lending, mortgage, payment, money movement, investing, brokerage, insurance, financial services, savings, or similar.

Narrative subcategory:

- `financial inclusion / underbanked / underserved`
- `consumer credit access`
- `payments / money movement / SMB commerce access`
- `insurance / benefits access`

### Expanded Access To Credit

Positive only when the excerpt says the issuer or financial system expands, expanded, or is expanding access to credit and identifies an external beneficiary.

Required context:

- `expand access to credit`, `expanded access to credit`, `expanding access to credit`, or close equivalent.
- Beneficiary language: consumer, borrower, member, customer, small business, LMI, minority, underserved, community, household, homeowner, or similar.

Narrative subcategory:

- `consumer credit access`

### Affordable Financial Products

Positive only when affordable credit, affordable financial services, low-cost financial services, or affordable loans are tied to external beneficiaries.

Required context:

- Product language: affordable credit, affordable financial services, low-cost financial services, affordable loans, access to affordable credit, or close equivalent.
- Beneficiary language: consumer, customer, member, borrower, small business, underserved, underbanked, unbanked, LMI, community, or similar.

Narrative subcategory:

- `consumer credit access`
- `financial inclusion / underbanked / underserved`

### Homeownership / Housing Access

Positive only when homeownership or housing access is tied to a mortgage, borrower, homeowner, resident, LMI/community housing access, affordable homeownership, or a direct housing-finance mechanism.

Required context:

- Homeownership or housing-access language.
- One of: mortgage, mortgage credit, borrower, homeowner, resident, renter, low- and moderate-income, LMI, community housing access, affordable homeownership, construction financing, preservation financing, or expanded availability for external beneficiaries.

Narrative subcategory:

- `affordable housing / homeownership access`

## Default Exclusions

The following contexts are excluded unless the excerpt independently satisfies a high-evidence positive rule with explicit beneficiary and financial mechanism:

- Fractional-share stock mechanics: stock splits, reverse splits, merger exchange ratios, cash-in-lieu, conversion mechanics, issuance mechanics, dividend mechanics, or other share-count/accounting mechanics.
- Institutional quality, institutional caliber, institutional grade, or institutional level unless explicitly tied to retail or individual investor access.
- Generic market access, access to markets, or capital markets access unless smaller issuers, municipalities, borrowers, customers, or external clients are the beneficiaries.
- Issuer liquidity, issuer funding, issuer access to credit, issuer access to credit facilities, FHLB advances, issuer credit ratings, issuer debt-market access, or issuer capital resources.
- Risk-only access language, including competitor actions, adverse-risk disclosure, market-entry risk, or statements about what competitors may do.
- Affordable-housing accounting, tax-credit, partnership, portfolio, investment-income, sale, impairment, commitment-table, or LIHTC context without direct external housing-access mechanism.
- Generic barriers language in AI, HR, healthcare, sports, regulation, competition, product listing, legislation, or internal operations.
- Generic ESG, community, philanthropy, or mission language without both a beneficiary and a financial mechanism.
- Platform, API, custody, analytics, infrastructure, data, connectivity, security, operational-quality, or internal technology language unless end-user financial access is explicit.

## High-Risk Evidence Flag

Candidate evidence receives `high_risk_phrase_flag = yes` when the positive evidence comes from one of these phrase families or contexts:

- affordable housing or homeownership access
- fractional share or retail-investor mechanics
- institutional quality / institutional grade / institutional caliber / institutional level
- market access / access to markets / capital markets access
- access to credit
- lower barriers / reduce barriers / removing barriers / eliminate barriers
- risk-section language
- CRA/regulatory language

High-risk evidence can still enter the candidate file only when the excerpt satisfies the high-evidence positive rules above.

## Filing-Level Aggregation

For each filing:

- `conservative_candidate_flag = yes` if one or more evidence excerpts satisfy these rules.
- `conservative_candidate_flag = no` otherwise.
- `candidate_confidence` is `high` when evidence is direct and not high-risk, and `medium_high` when evidence is high-risk but still passes a conservative positive rule.
- `narrative_subcategories_present` lists distinct positive subcategories in that filing.
- `evidence_hit_count` counts positive evidence excerpts.
- `evidence_section_count` counts distinct sections containing positive evidence.
- `strongest_evidence_phrase` is the phrase from the highest-ranked evidence excerpt.
- `high_risk_evidence_flag` is `yes` if any positive evidence excerpt is high-risk.

## Manual Audit Requirement

These candidate flags are not final treatment variables. They must pass a filing-level manual audit before any return-window construction, benchmark loading, or return analysis.

The audit should evaluate whether the filing-level evidence supports a conservative access-oriented disclosure treatment candidate under these rules, not whether later returns were favorable.

## Prohibited Use

- Do not use V2 full-corpus labels as treatment variables.
- Do not use tiered V1 hit-level labels as treatment variables.
- Do not use these filing-level candidates in return analysis until manual audit validates them.
- Do not fetch prices, load benchmarks, compute returns, or make empirical performance claims at this stage.
