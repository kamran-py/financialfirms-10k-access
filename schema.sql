-- Proposed PostgreSQL schema for the 10-K access-language research dataset.
-- This file defines structure only. It should not be used to load data until
-- the research design is approved.

CREATE SCHEMA IF NOT EXISTS research;

CREATE TABLE research.reason_codes (
    reason_code TEXT PRIMARY KEY,
    reason_group TEXT NOT NULL,
    description TEXT NOT NULL,
    applies_to TEXT NOT NULL,
    is_terminal BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE research.source_systems (
    source_id BIGSERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_url TEXT,
    provider_version TEXT,
    retrieval_date DATE,
    license_notes TEXT,
    UNIQUE (source_name, source_type, provider_version, retrieval_date)
);

CREATE TABLE research.issuer_candidates (
    issuer_candidate_id BIGSERIAL PRIMARY KEY,
    cik TEXT,
    entity_name TEXT NOT NULL,
    ticker TEXT,
    exchange TEXT,
    sic TEXT,
    naics TEXT,
    country_incorporation TEXT,
    country_listing TEXT,
    candidate_source_id BIGINT REFERENCES research.source_systems(source_id),
    candidate_as_of_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cik, ticker, exchange, candidate_as_of_date)
);

CREATE TABLE research.universe_decisions (
    universe_decision_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT NOT NULL REFERENCES research.issuer_candidates(issuer_candidate_id),
    universe_version TEXT NOT NULL,
    is_included BOOLEAN NOT NULL,
    decision_reason_code TEXT NOT NULL REFERENCES research.reason_codes(reason_code),
    decision_notes TEXT,
    decided_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (issuer_candidate_id, universe_version)
);

CREATE TABLE research.issuer_identifiers (
    issuer_identifier_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT NOT NULL REFERENCES research.issuer_candidates(issuer_candidate_id),
    identifier_type TEXT NOT NULL,
    identifier_value TEXT NOT NULL,
    valid_from DATE,
    valid_to DATE,
    source_id BIGINT REFERENCES research.source_systems(source_id),
    UNIQUE (issuer_candidate_id, identifier_type, identifier_value, valid_from)
);

CREATE TABLE research.issuer_name_history (
    issuer_name_history_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT NOT NULL REFERENCES research.issuer_candidates(issuer_candidate_id),
    issuer_name TEXT NOT NULL,
    name_type TEXT NOT NULL,
    valid_from DATE,
    valid_to DATE,
    source_id BIGINT REFERENCES research.source_systems(source_id),
    UNIQUE (issuer_candidate_id, issuer_name, name_type, valid_from)
);

CREATE TABLE research.industry_classification_history (
    industry_classification_history_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT NOT NULL REFERENCES research.issuer_candidates(issuer_candidate_id),
    classification_system TEXT NOT NULL,
    classification_code TEXT NOT NULL,
    classification_label TEXT,
    valid_from DATE,
    valid_to DATE,
    is_point_in_time BOOLEAN NOT NULL DEFAULT TRUE,
    source_id BIGINT REFERENCES research.source_systems(source_id),
    UNIQUE (issuer_candidate_id, classification_system, classification_code, valid_from)
);

CREATE TABLE research.index_membership_history (
    index_membership_history_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT NOT NULL REFERENCES research.issuer_candidates(issuer_candidate_id),
    index_name TEXT NOT NULL,
    index_identifier TEXT,
    membership_start_date DATE,
    membership_end_date DATE,
    membership_status TEXT NOT NULL,
    is_point_in_time BOOLEAN NOT NULL DEFAULT TRUE,
    source_id BIGINT REFERENCES research.source_systems(source_id),
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    UNIQUE (issuer_candidate_id, index_name, membership_start_date, source_id)
);

CREATE TABLE research.expected_issuer_years (
    expected_issuer_year_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT NOT NULL REFERENCES research.issuer_candidates(issuer_candidate_id),
    filing_year INTEGER NOT NULL CHECK (filing_year BETWEEN 2015 AND 2025),
    expected_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    UNIQUE (issuer_candidate_id, filing_year)
);

CREATE TABLE research.filings (
    filing_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT NOT NULL REFERENCES research.issuer_candidates(issuer_candidate_id),
    cik TEXT NOT NULL,
    accession_number TEXT NOT NULL,
    form_type TEXT NOT NULL,
    filing_date DATE NOT NULL,
    filing_year INTEGER NOT NULL CHECK (filing_year BETWEEN 2015 AND 2025),
    report_period DATE,
    fiscal_year INTEGER,
    fiscal_year_end_date DATE,
    filing_year_basis TEXT NOT NULL DEFAULT 'SEC_FILING_DATE',
    acceptance_datetime TIMESTAMPTZ,
    filing_url TEXT NOT NULL,
    primary_document_url TEXT,
    sec_source_id BIGINT REFERENCES research.source_systems(source_id),
    is_amendment BOOLEAN NOT NULL DEFAULT FALSE,
    filing_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (cik, accession_number)
);

CREATE TABLE research.filing_documents (
    filing_document_id BIGSERIAL PRIMARY KEY,
    filing_id BIGINT NOT NULL REFERENCES research.filings(filing_id),
    document_sequence TEXT,
    document_type TEXT,
    document_description TEXT,
    document_url TEXT NOT NULL,
    local_raw_path TEXT,
    sha256 TEXT,
    content_type TEXT,
    byte_size BIGINT,
    source_id BIGINT REFERENCES research.source_systems(source_id),
    UNIQUE (filing_id, document_url)
);

CREATE TABLE research.extraction_runs (
    extraction_run_id BIGSERIAL PRIMARY KEY,
    extractor_name TEXT NOT NULL,
    extractor_version TEXT NOT NULL,
    run_started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    run_finished_at TIMESTAMPTZ,
    parameters_json JSONB,
    notes TEXT,
    UNIQUE (extractor_name, extractor_version, run_started_at)
);

CREATE TABLE research.extracted_filings (
    extracted_filing_id BIGSERIAL PRIMARY KEY,
    filing_id BIGINT NOT NULL REFERENCES research.filings(filing_id),
    filing_document_id BIGINT REFERENCES research.filing_documents(filing_document_id),
    extraction_run_id BIGINT NOT NULL REFERENCES research.extraction_runs(extraction_run_id),
    extraction_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    extracted_text_path TEXT,
    extracted_text_sha256 TEXT,
    extracted_char_count BIGINT,
    parser_warnings TEXT,
    UNIQUE (filing_id, extraction_run_id)
);

CREATE TABLE research.filing_sections (
    filing_section_id BIGSERIAL PRIMARY KEY,
    extracted_filing_id BIGINT NOT NULL REFERENCES research.extracted_filings(extracted_filing_id),
    section_label TEXT NOT NULL,
    section_title TEXT,
    section_start_char BIGINT,
    section_end_char BIGINT,
    section_text_path TEXT,
    section_text_sha256 TEXT,
    section_confidence NUMERIC(6,5),
    section_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code)
);

CREATE TABLE research.phrase_taxonomy_versions (
    phrase_taxonomy_version_id BIGSERIAL PRIMARY KEY,
    taxonomy_name TEXT NOT NULL,
    taxonomy_version TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    UNIQUE (taxonomy_name, taxonomy_version)
);

CREATE TABLE research.phrase_taxonomy_terms (
    phrase_term_id BIGSERIAL PRIMARY KEY,
    phrase_taxonomy_version_id BIGINT NOT NULL REFERENCES research.phrase_taxonomy_versions(phrase_taxonomy_version_id),
    phrase_family TEXT NOT NULL,
    exact_phrase TEXT NOT NULL,
    normalized_phrase TEXT NOT NULL,
    concept_hint TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (phrase_taxonomy_version_id, normalized_phrase)
);

CREATE TABLE research.phrase_match_runs (
    phrase_match_run_id BIGSERIAL PRIMARY KEY,
    phrase_taxonomy_version_id BIGINT NOT NULL REFERENCES research.phrase_taxonomy_versions(phrase_taxonomy_version_id),
    matcher_name TEXT NOT NULL,
    matcher_version TEXT NOT NULL,
    run_started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    run_finished_at TIMESTAMPTZ,
    parameters_json JSONB,
    UNIQUE (phrase_taxonomy_version_id, matcher_name, matcher_version, run_started_at)
);

CREATE TABLE research.raw_phrase_hits (
    raw_phrase_hit_id BIGSERIAL PRIMARY KEY,
    filing_id BIGINT NOT NULL REFERENCES research.filings(filing_id),
    extracted_filing_id BIGINT NOT NULL REFERENCES research.extracted_filings(extracted_filing_id),
    filing_section_id BIGINT REFERENCES research.filing_sections(filing_section_id),
    phrase_match_run_id BIGINT NOT NULL REFERENCES research.phrase_match_runs(phrase_match_run_id),
    phrase_term_id BIGINT NOT NULL REFERENCES research.phrase_taxonomy_terms(phrase_term_id),
    matched_text TEXT NOT NULL,
    excerpt TEXT NOT NULL,
    excerpt_start_char BIGINT,
    excerpt_end_char BIGINT,
    match_start_char BIGINT,
    match_end_char BIGINT,
    context_risk_flags JSONB,
    false_positive_review_status TEXT,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    filing_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research.filing_phrase_summary (
    filing_phrase_summary_id BIGSERIAL PRIMARY KEY,
    filing_id BIGINT NOT NULL REFERENCES research.filings(filing_id),
    phrase_match_run_id BIGINT NOT NULL REFERENCES research.phrase_match_runs(phrase_match_run_id),
    raw_hit_count INTEGER NOT NULL DEFAULT 0,
    has_raw_hit BOOLEAN NOT NULL,
    summary_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    UNIQUE (filing_id, phrase_match_run_id)
);

CREATE TABLE research.classification_runs (
    classification_run_id BIGSERIAL PRIMARY KEY,
    classification_name TEXT NOT NULL,
    classification_version TEXT NOT NULL,
    method_type TEXT NOT NULL,
    codebook_path TEXT,
    model_name TEXT,
    model_version TEXT,
    run_started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    run_finished_at TIMESTAMPTZ,
    parameters_json JSONB,
    notes TEXT,
    UNIQUE (classification_name, classification_version, run_started_at)
);

CREATE TABLE research.interpreted_phrase_hits (
    interpreted_phrase_hit_id BIGSERIAL PRIMARY KEY,
    raw_phrase_hit_id BIGINT NOT NULL REFERENCES research.raw_phrase_hits(raw_phrase_hit_id),
    classification_run_id BIGINT NOT NULL REFERENCES research.classification_runs(classification_run_id),
    interpreted_label TEXT NOT NULL,
    interpreted_dimension TEXT,
    semantic_scope_label TEXT,
    evidence_level TEXT,
    confidence_score NUMERIC(8,6),
    rationale_short TEXT,
    reviewer_id TEXT,
    classification_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (raw_phrase_hit_id, classification_run_id)
);

CREATE TABLE research.securities (
    security_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT NOT NULL REFERENCES research.issuer_candidates(issuer_candidate_id),
    ticker TEXT NOT NULL,
    exchange TEXT,
    security_name TEXT,
    security_type TEXT,
    primary_security_flag BOOLEAN,
    valid_from DATE,
    valid_to DATE,
    source_id BIGINT REFERENCES research.source_systems(source_id)
);

CREATE TABLE research.security_identifier_history (
    security_identifier_history_id BIGSERIAL PRIMARY KEY,
    security_id BIGINT NOT NULL REFERENCES research.securities(security_id),
    identifier_type TEXT NOT NULL,
    identifier_value TEXT NOT NULL,
    valid_from DATE,
    valid_to DATE,
    source_id BIGINT REFERENCES research.source_systems(source_id),
    UNIQUE (security_id, identifier_type, identifier_value, valid_from)
);

CREATE TABLE research.security_events (
    security_event_id BIGSERIAL PRIMARY KEY,
    issuer_candidate_id BIGINT REFERENCES research.issuer_candidates(issuer_candidate_id),
    security_id BIGINT REFERENCES research.securities(security_id),
    event_type TEXT NOT NULL,
    event_date DATE,
    effective_date DATE,
    event_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    successor_issuer_candidate_id BIGINT REFERENCES research.issuer_candidates(issuer_candidate_id),
    successor_security_id BIGINT REFERENCES research.securities(security_id),
    source_id BIGINT REFERENCES research.source_systems(source_id),
    notes TEXT
);

CREATE TABLE research.filing_security_links (
    filing_security_link_id BIGSERIAL PRIMARY KEY,
    filing_id BIGINT NOT NULL REFERENCES research.filings(filing_id),
    security_id BIGINT REFERENCES research.securities(security_id),
    link_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    link_method TEXT NOT NULL,
    link_confidence NUMERIC(6,5),
    source_id BIGINT REFERENCES research.source_systems(source_id),
    UNIQUE (filing_id, security_id, link_method)
);

CREATE TABLE research.security_prices (
    security_price_id BIGSERIAL PRIMARY KEY,
    security_id BIGINT NOT NULL REFERENCES research.securities(security_id),
    price_date DATE NOT NULL,
    open_price NUMERIC(20,8),
    close_price NUMERIC(20,8),
    adjusted_close_price NUMERIC(20,8),
    total_return_index NUMERIC(20,8),
    volume NUMERIC(24,4),
    currency TEXT,
    adjustment_policy TEXT,
    adjustment_status TEXT,
    quality_flags JSONB,
    price_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    source_id BIGINT NOT NULL REFERENCES research.source_systems(source_id),
    UNIQUE (security_id, price_date, source_id)
);

CREATE TABLE research.price_quality_checks (
    price_quality_check_id BIGSERIAL PRIMARY KEY,
    security_id BIGINT REFERENCES research.securities(security_id),
    security_price_id BIGINT REFERENCES research.security_prices(security_price_id),
    check_name TEXT NOT NULL,
    check_version TEXT NOT NULL,
    check_status TEXT NOT NULL,
    severity TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    observed_value NUMERIC(24,10),
    threshold_value NUMERIC(24,10),
    details_json JSONB,
    checked_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE research.benchmarks (
    benchmark_id BIGSERIAL PRIMARY KEY,
    benchmark_name TEXT NOT NULL,
    benchmark_type TEXT NOT NULL,
    benchmark_identifier TEXT,
    weighting_method TEXT,
    sector_scope TEXT,
    is_point_in_time BOOLEAN NOT NULL DEFAULT TRUE,
    source_id BIGINT REFERENCES research.source_systems(source_id),
    notes TEXT,
    UNIQUE (benchmark_name, benchmark_type, benchmark_identifier, source_id)
);

CREATE TABLE research.benchmark_prices (
    benchmark_price_id BIGSERIAL PRIMARY KEY,
    benchmark_id BIGINT NOT NULL REFERENCES research.benchmarks(benchmark_id),
    price_date DATE NOT NULL,
    close_value NUMERIC(24,10),
    adjusted_close_value NUMERIC(24,10),
    total_return_index NUMERIC(24,10),
    benchmark_price_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    source_id BIGINT NOT NULL REFERENCES research.source_systems(source_id),
    UNIQUE (benchmark_id, price_date, source_id)
);

CREATE TABLE research.return_window_definitions (
    return_window_definition_id BIGSERIAL PRIMARY KEY,
    window_label TEXT NOT NULL UNIQUE,
    window_years INTEGER NOT NULL CHECK (window_years IN (1, 3, 5)),
    as_of_date DATE NOT NULL DEFAULT DATE '2026-06-27',
    anchor_policy TEXT NOT NULL,
    end_date_policy TEXT NOT NULL,
    price_adjustment_policy TEXT NOT NULL,
    benchmark_policy TEXT
);

CREATE TABLE research.filing_return_windows (
    filing_return_window_id BIGSERIAL PRIMARY KEY,
    filing_id BIGINT NOT NULL REFERENCES research.filings(filing_id),
    security_id BIGINT REFERENCES research.securities(security_id),
    return_window_definition_id BIGINT NOT NULL REFERENCES research.return_window_definitions(return_window_definition_id),
    anchor_date DATE NOT NULL,
    target_end_date DATE NOT NULL,
    realized_start_price_date DATE,
    realized_end_price_date DATE,
    start_price NUMERIC(20,8),
    end_price NUMERIC(20,8),
    return_value NUMERIC(20,10),
    censoring_status TEXT NOT NULL DEFAULT 'NOT_CENSORED',
    terminal_security_event_id BIGINT REFERENCES research.security_events(security_event_id),
    return_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    price_source_id BIGINT REFERENCES research.source_systems(source_id),
    computed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (filing_id, return_window_definition_id, price_source_id)
);

CREATE TABLE research.filing_benchmark_returns (
    filing_benchmark_return_id BIGSERIAL PRIMARY KEY,
    filing_return_window_id BIGINT NOT NULL REFERENCES research.filing_return_windows(filing_return_window_id),
    benchmark_id BIGINT NOT NULL REFERENCES research.benchmarks(benchmark_id),
    benchmark_start_date DATE,
    benchmark_end_date DATE,
    benchmark_start_value NUMERIC(24,10),
    benchmark_end_value NUMERIC(24,10),
    benchmark_return_value NUMERIC(20,10),
    excess_return_value NUMERIC(20,10),
    benchmark_return_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    source_id BIGINT REFERENCES research.source_systems(source_id),
    computed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (filing_return_window_id, benchmark_id, source_id)
);

CREATE TABLE research.analysis_test_registry (
    analysis_test_registry_id BIGSERIAL PRIMARY KEY,
    test_family TEXT NOT NULL,
    test_name TEXT NOT NULL,
    test_type TEXT NOT NULL,
    preregistered_flag BOOLEAN NOT NULL DEFAULT FALSE,
    exploratory_flag BOOLEAN NOT NULL DEFAULT TRUE,
    phrase_taxonomy_version_id BIGINT REFERENCES research.phrase_taxonomy_versions(phrase_taxonomy_version_id),
    classification_run_id BIGINT REFERENCES research.classification_runs(classification_run_id),
    return_window_definition_id BIGINT REFERENCES research.return_window_definitions(return_window_definition_id),
    benchmark_id BIGINT REFERENCES research.benchmarks(benchmark_id),
    subgroup_definition TEXT,
    multiple_testing_family TEXT,
    adjustment_method TEXT,
    registered_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    UNIQUE (test_family, test_name)
);

CREATE TABLE research.interpretation_evidence_checks (
    interpretation_evidence_check_id BIGSERIAL PRIMARY KEY,
    evidence_item TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    status_reason_code TEXT REFERENCES research.reason_codes(reason_code),
    checked_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    checked_by TEXT,
    notes TEXT,
    UNIQUE (evidence_item)
);

CREATE TABLE research.pipeline_events (
    pipeline_event_id BIGSERIAL PRIMARY KEY,
    event_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    stage_name TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    event_status TEXT NOT NULL,
    reason_code TEXT REFERENCES research.reason_codes(reason_code),
    message TEXT,
    metadata_json JSONB
);

CREATE INDEX idx_filings_filing_date ON research.filings (filing_date);
CREATE INDEX idx_filings_cik_year ON research.filings (cik, filing_year);
CREATE INDEX idx_index_membership_dates ON research.index_membership_history (index_name, membership_start_date, membership_end_date);
CREATE INDEX idx_raw_phrase_hits_filing ON research.raw_phrase_hits (filing_id);
CREATE INDEX idx_raw_phrase_hits_phrase ON research.raw_phrase_hits (phrase_term_id);
CREATE INDEX idx_interpreted_hits_raw ON research.interpreted_phrase_hits (raw_phrase_hit_id);
CREATE INDEX idx_security_events_security_date ON research.security_events (security_id, event_date, event_type);
CREATE INDEX idx_prices_security_date ON research.security_prices (security_id, price_date);
CREATE INDEX idx_benchmark_prices_date ON research.benchmark_prices (benchmark_id, price_date);
CREATE INDEX idx_return_windows_status ON research.filing_return_windows (return_status, status_reason_code);
