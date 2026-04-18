---
profile_id: gdpr
title: GDPR — EU General Data Protection Regulation (2016/679)
version: 1.0.0
status: active
owner: AECF
last_review: 2026-03-16
regulation_reference_date: 2026-03-16
max_staleness_months: 6
profile_type: regulatory
stack_nodes:
  - regulatory
requires: []
precedence: 100
fallback_mode: warn_continue
compatibility:
  - python
  - java
  - dotnet
  - node
  - go
  - rust
  - react
conflicts_with: []
activation_mode: skill_bound
evidence_hint:
  - skill=security_review_gdpr
max_lines_per_section: 8
tags:
  - gdpr
  - privacy
  - data-protection
  - regulatory
  - eu
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## REGULATION SCOPE

EU General Data Protection Regulation (Regulation 2016/679). Applies to any system that processes personal data of EU residents, regardless of where the system is hosted.

## CODE-LEVEL AUDIT CHECKLIST

### Art. 5 — Principles (lawfulness, fairness, transparency, purpose limitation, data minimization, accuracy, storage limitation, integrity and confidentiality, accountability)
- Verify that personal data fields are explicitly identified and classified (PII markers, data annotations, schema comments).
- Check that data collection points document or reference a legal basis (consent, contract, legitimate interest).
- Verify data minimization: no collection of fields beyond stated purpose.

### Art. 6 — Lawfulness of processing
- Look for consent acquisition flows (opt-in, not pre-checked).
- Verify consent is granular (separate purposes) and withdrawable.
- Check for evidence of legal basis documentation in code comments, config, or metadata.

### Art. 7 — Conditions for consent
- Consent must be freely given, specific, informed, and unambiguous.
- Look for consent toggles with default-off state.
- Check withdrawal mechanisms are as easy as giving consent.

### Art. 9 — Special categories of personal data
- Detect processing of health, biometric, genetic, racial/ethnic, political, religious, sexual orientation, or trade union data.
- These require explicit consent or specific legal basis — flag any processing without evidence.

### Art. 13/14 — Information to be provided
- Check for privacy notice content in user-facing flows.
- Verify data collection forms reference or link to privacy policy.

### Art. 15-22 — Data subject rights
- Right of access (Art. 15): look for data export/download endpoints.
- Right to rectification (Art. 16): look for user data edit capabilities.
- Right to erasure (Art. 17): look for account deletion / data purge logic.
- Right to data portability (Art. 20): look for structured data export (JSON, CSV).
- Right to object (Art. 21): look for opt-out mechanisms for profiling/marketing.
- Automated decision-making (Art. 22): flag any automated decisions with legal effects without human review.

### Art. 25 — Data protection by design and by default
- Privacy-by-default: check default settings minimize data exposure.
- Pseudonymization and anonymization logic where applicable.
- Check for data masking in non-production environments.

### Art. 30 — Records of processing activities
- Look for processing activity metadata in code (purpose, categories, recipients, retention periods).
- Flag absence of structured processing records as MEDIUM finding.

### Art. 32 — Security of processing
- Encryption at rest: database encryption, file encryption, encrypted config values.
- Encryption in transit: TLS/HTTPS enforcement, certificate validation.
- Pseudonymization capabilities.
- Access control: role-based, attribute-based, or policy-based controls on personal data.
- Logging: security events must be logged WITHOUT logging personal data content.

### Art. 33/34 — Breach notification
- Check for incident detection mechanisms (error monitoring, anomaly detection).
- Look for breach notification automation or hooks.
- Flag absence of breach response infrastructure as MEDIUM finding.

### Art. 35 — Data Protection Impact Assessment
- Look for DPIA references or templates in project documentation.
- Flag high-risk processing (profiling, large-scale special categories, systematic monitoring) without DPIA evidence.

### Art. 44-49 — International transfers
- Detect cross-border data flows (cloud regions, API endpoints in non-EU jurisdictions).
- Check for Standard Contractual Clauses references or adequacy decision documentation.
- Flag data flows to countries without adequacy decisions as HIGH finding.

## SEVERITY MAPPING

| GDPR Article | Violation Type | Default Severity | Rationale |
|-------------|----------------|-----------------|-----------|
| Art. 5(1)(f) | No encryption on personal data at rest | CRITICAL | Direct violation of integrity/confidentiality principle |
| Art. 6 | Processing without documented legal basis | HIGH | Lawfulness requirement |
| Art. 7 | Pre-checked consent boxes | HIGH | Invalid consent |
| Art. 9 | Special category data without explicit consent | CRITICAL | Enhanced protection requirement |
| Art. 17 | No erasure/deletion capability | HIGH | Data subject right violation |
| Art. 25 | Default settings maximize data collection | MEDIUM | Design principle violation |
| Art. 32 | No TLS/HTTPS enforcement | CRITICAL | Security of processing |
| Art. 32 | Personal data in logs | HIGH | Security of processing |
| Art. 33 | No breach detection mechanism | MEDIUM | Breach notification readiness |
| Art. 44 | Data transfer to non-adequate country without SCCs | HIGH | Transfer safeguards |

## ORGANIZATIONAL WARNINGS (OUT OF SCOPE)

The following GDPR requirements CANNOT be verified from code alone and MUST be listed as `ORGANIZATIONAL_WARNING` items:

- Art. 37-39: Data Protection Officer appointment and role.
- Art. 28: Data Processing Agreements with third-party processors.
- Art. 30: Complete Record of Processing Activities (organizational document).
- Art. 35: Full Data Protection Impact Assessment (organizational process).
- Art. 12: Transparency of privacy notices (content review, not just existence).
- Staff training and awareness programs.
- Physical security measures.
- Data subject request handling procedures (SLA, process documentation).
