# Proposed Directory Structure

The structure below is proposed only. It should be created after design approval.

```text
financialfirms_10K_access/
  README.md
  research_plan.md
  project_tasks.md
  schema.sql
  methodology_notes.md
  data_provenance.md
  proposed_directory_structure.md
  unresolved_design_questions.md

  config/
    project.yml
    sample_period.yml
    source_systems.yml
    reason_codes.yml
    phrase_taxonomy.yml
    classification_codebook.yml

  data/
    raw/
      sec/
        submissions/
        filings/
      prices/
      reference/
    interim/
      extracted_text/
      section_text/
      matched_phrases/
      security_links/
    processed/
      database/
      analysis_inputs/
    manifests/
      source_manifests/
      checksums/
      retrieval_logs/

  docs/
    data_dictionary.md
    reason_codes.md
    phrase_taxonomy.md
    classification_codebook.md
    qa_protocol.md
    limitations.md

  sql/
    schema.sql
    seed_reason_codes.sql
    validation_queries.sql

  src/
    universe/
    sec_filings/
    text_extraction/
    phrase_matching/
    classification/
    prices/
    returns/
    qa/

  tests/
    fixtures/
    unit/
    integration/

  notebooks/
    exploratory/
    descriptive_analysis/

  outputs/
    qa_reports/
    tables/
    figures/
    logs/
```

## Directory Roles

`config/` stores versioned project settings and taxonomies.

`data/raw/` stores immutable source downloads. Raw files should never be overwritten after retrieval.

`data/interim/` stores reproducible intermediate artifacts such as extracted text and matched phrases.

`data/processed/` stores analysis-ready datasets after all reason codes and audit fields are attached.

`data/manifests/` stores provenance metadata, checksums, and retrieval logs.

`docs/` stores human-readable codebooks, QA procedures, and limitations.

`sql/` stores database schema, seed tables, and validation queries. A copy of the root `schema.sql` can be moved here after project setup if preferred.

`src/` stores implementation modules after design approval.

`tests/` stores synthetic and small public fixtures. Tests should not rely on large live downloads.

`outputs/` stores generated reports, figures, and logs. Analysis outputs should not be created until after data construction begins.

