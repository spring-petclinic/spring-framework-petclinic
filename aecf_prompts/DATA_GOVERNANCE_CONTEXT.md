# DATA_GOVERNANCE_CONTEXT

## Purpose
Define rules and lifecycle of data inside this project.

## Data Classification
- Public
- Internal
- Confidential
- Sensitive (PII)

Example:
User table:
- email → Sensitive (PII)
- login_timestamp → Internal

## Data Lineage
For every feature:
- Source
- Transformation
- Storage
- Exposure

Example:
Azure cost ingestion:
- Source: Azure API
- Transform: normalize schema
- Store: PostgreSQL (tenant schema)
- Expose: Dashboard API

## Data Retention Policy
Define retention per category.

Example:
- Audit logs → 2 years
- Temporary exports → 7 days

## Data Quality Rules
- Required fields
- Validation checks
- Duplication policy

## VALIDATION CHECKLIST
- [ ] Data category assigned for each dataset/field
- [ ] PII fields identified and documented
- [ ] End-to-end lineage recorded (Source → Transformation → Storage → Exposure)
- [ ] Retention period defined per data category
- [ ] Data quality validations documented and implemented
- [ ] Duplication handling policy defined
- [ ] Data exposure endpoints reviewed for least privilege
- [ ] Governance owner and review date assigned
