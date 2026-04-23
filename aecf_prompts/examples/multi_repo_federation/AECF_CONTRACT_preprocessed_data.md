# AECF_CONTRACT_preprocessed_data

## METADATA

| Field | Value |
| --- | --- |
| LAST_REVIEW | 2026-04-17 |
| Owner | SEACHAD — parser team |
| Contract ID | preprocessed_data |
| Contract Type | data_pipeline |
| Status | active |
| Change Policy | versioned_schema |

## 1. Summary

The `parser` repository preprocesses raw data fetched via API_ROBOT into normalized datasets. These datasets are consumed by Flask_Dashboards (for real-time dashboards) and PowerBI (for analytical reports). This contract defines the file format, schema versioning, column naming, and delivery conventions.

## 2. Participants

| Repo (logical ID) | Role | Surface (if known) | Notes |
| --- | --- | --- | --- |
| parser | provider | data_preprocessing | Produces normalized output files |
| flask_dashboards | consumer | dashboard_rendering | Reads preprocessed files for dashboard data |
| powerbi | consumer | analytics_reporting | Imports preprocessed files for BI reports |

## 3. Contract Specification

### 3.1 Protocol / Mechanism

- **Type**: File-based data pipeline
- **Formats**: CSV (primary), Parquet (optional for PowerBI)
- **Delivery**: Shared network path or object storage, configured per environment
- **Cadence**: Batch runs on schedule (configurable) + on-demand trigger

### 3.2 Exposed Interface

**Output directory structure**:

```
output/
  {dataset_name}/
    {dataset_name}_{YYYYMMDD}_{run_id}.csv
    {dataset_name}_{YYYYMMDD}_{run_id}.parquet   # optional
    _schema.json                                   # schema definition
    _latest.txt                                    # pointer to latest file
```

**CSV format**:

- First row: `# schema_version={version}`  (metadata comment)
- Second row: column headers
- Subsequent rows: data
- Encoding: UTF-8
- Delimiter: `,` (comma)
- Quoting: RFC 4180

**Schema definition** (`_schema.json`):

```json
{
  "dataset": "customers",
  "schema_version": "2.1",
  "columns": [
    {"name": "id", "type": "string", "nullable": false},
    {"name": "name", "type": "string", "nullable": false},
    {"name": "status", "type": "enum", "values": ["active", "inactive", "suspended"]},
    {"name": "created_at", "type": "datetime", "format": "ISO8601"},
    {"name": "revenue_ytd", "type": "decimal", "precision": 2}
  ],
  "deprecated_columns": [
    {"name": "old_status_code", "deprecated_in": "2.0", "removed_in": "2.2"}
  ]
}
```

### 3.3 Consumer Expectations

**Flask_Dashboards** depends on:

1. CSV files with `schema_version` header comment.
2. Column names as defined in `_schema.json`.
3. `_latest.txt` pointing to the most recent file.
4. UTF-8 encoding, comma-delimited.

**PowerBI** depends on:

1. Parquet files when available (falls back to CSV).
2. Column types matching `_schema.json`.
3. Stable column names across runs for the same schema version.

## 4. Invariants

1. Every output file MUST include `# schema_version={version}` as the first line.
2. Column names MUST NOT change within the same major schema version.
3. New columns MAY be added in minor versions; consumers must ignore unknown columns.
4. Deprecated columns MUST be kept for at least 2 schema versions before removal.
5. `_schema.json` MUST be updated before any column change is deployed.
6. `_latest.txt` MUST always point to a valid, complete file.

## 5. Change Rules

### 5.1 Allowed Without Coordination

- Adding new columns (minor version bump: `2.1` → `2.2`).
- Adding new datasets (new `{dataset_name}` folder).
- Changing internal processing logic without affecting output format.

### 5.2 Requires Notification

- Deprecating a column (mark in `deprecated_columns`, bump minor version).
- Changing output cadence or schedule.
- Adding Parquet output for a dataset that previously only had CSV.

### 5.3 Requires Coordinated Change

- Removing a column (only after 2-version deprecation window).
- Renaming a column (major version bump: `2.x` → `3.0`).
- Changing CSV delimiter, encoding, or quoting rules.
- Changing the output directory structure.

## 6. Versioning

| Field | Value |
| --- | --- |
| Current Version | 2.1 |
| Versioning Strategy | semver (major.minor) |
| Backward Compatibility Window | 2 minor versions for deprecated columns |

## 7. Observability

- **Monitoring**: Parser logs output file size, row count, and schema version per run.
- **Alerting**: Alert if output file has 0 rows or is significantly smaller than historical average.
- **Health checks**: Consumers check `_latest.txt` freshness (timestamp within expected cadence).

## 8. Testing

### 8.1 Provider-Side Tests (parser)

1. Schema validation: output files match `_schema.json`.
2. Regression test: compare output row counts and column set against known baselines.
3. Encoding test: verify UTF-8 output with special characters.

### 8.2 Consumer-Side Tests (Flask_Dashboards, PowerBI)

1. Parse test: verify consumer can parse the latest schema version correctly.
2. Unknown-column test: verify consumer ignores extra columns.
3. Freshness test: verify `_latest.txt` resolution works.

### 8.3 Contract Tests

1. Shared `_schema.json` validated in parser CI and consumed in Flask_Dashboards CI as a fixture.

## 9. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Schema drift without version bump | Consumer parsing errors | CI-enforced schema validation on every parser build |
| Output file missing or empty | Dashboard shows stale data, PowerBI import fails | Alerting on file size; consumers show "data unavailable" |
| Column removed too early | Consumer breaks on missing column | 2-version deprecation window enforced in `_schema.json` |
| Large file sizes | Slow dashboard loading | Parquet format for PowerBI; pagination for Flask |

## 10. History

| Date | Change | Actor |
| --- | --- | --- |
| 2026-04-17 | Contract boundary created as AECF example | SEACHAD |
