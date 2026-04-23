---
profile_id: dora
title: DORA — Digital Operational Resilience Act (Regulation (EU) 2022/2554)
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
  - skill=security_review_dora
max_lines_per_section: 8
tags:
  - dora
  - financial-services
  - ict-resilience
  - regulatory
  - eu
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## REGULATION SCOPE

Digital Operational Resilience Act (Regulation (EU) 2022/2554). Applies to financial entities (banks, insurance, investment firms, payment institutions, crypto-asset service providers) and their critical ICT third-party service providers. In force since 17 January 2025.

## CODE-LEVEL AUDIT CHECKLIST

### Art. 5-6 — ICT Risk Management Framework (Governance)
- Verify existence of ICT risk management configuration or policy references in code/documentation.
- Check for risk tolerance thresholds configured in monitoring systems.
- Look for documented ICT asset inventory or references to one.
- Flag financial-sector applications without ICT risk management evidence.

### Art. 7 — ICT Systems, Protocols and Tools
- Verify ICT infrastructure security configurations (firewall rules, network segmentation references).
- Check for system hardening evidence (secure defaults, disabled unnecessary services).
- Look for capacity planning configurations (auto-scaling, resource limits).
- Verify segregation of development, testing, and production environments.

### Art. 8 — Identification of ICT Risks
- Check for asset classification in code/config (critical vs. non-critical systems).
- Verify dependency mapping of ICT components (service mesh configs, API gateway routes).
- Look for documented single points of failure analysis.
- Flag critical services without redundancy configuration.

### Art. 9 — Protection and Prevention
- Verify encryption at rest and in transit (TLS enforcement, database encryption, key management).
- Check access control mechanisms (RBAC, ABAC, MFA enforcement).
- Look for patch management automation or dependency update mechanisms.
- Verify secure configuration baselines (hardened container images, security headers).
- Check for data loss prevention controls.

### Art. 10 — Detection
- Verify anomaly detection mechanisms (log analysis, SIEM integration, alerting rules).
- Check for intrusion detection/prevention system configurations.
- Look for real-time monitoring dashboards and alert thresholds.
- Verify security event correlation rules.
- Flag critical systems without monitoring integration.

### Art. 11 — Response and Recovery
- Check for incident response automation (runbooks, auto-remediation scripts).
- Verify backup configuration (frequency, retention, encryption, off-site storage).
- Look for disaster recovery procedures referenced in code/config.
- Check for RTO/RPO definitions tied to system configurations.
- Verify failover mechanisms (active-passive, active-active configurations).

### Art. 12 — Backup Policies and Recovery Methods
- Verify automated backup schedules and retention policies.
- Check backup encryption and access controls.
- Look for backup integrity verification (checksums, test restores).
- Verify backup scope covers critical data and system state.
- Check for geographically separated backup storage.

### Art. 13 — Learning and Evolving
- Check for post-incident review processes triggered by monitoring.
- Look for security telemetry feeding back into detection rules.
- Verify vulnerability management integration (scan → track → remediate cycle).

### Art. 14 — Communication
- Check for incident notification mechanisms (webhooks, API integrations for reporting).
- Look for status page or incident communication infrastructure.
- Verify logging of communication events during incidents.

### Art. 15-16 — ICT-Related Incident Management
- Verify incident classification logic (severity levels, escalation rules).
- Check for incident lifecycle tracking (detection → triage → containment → recovery → post-mortem).
- Look for automated incident ticket creation from monitoring alerts.
- Verify incident response SLA configurations.
- Flag critical systems without incident management integration.

### Art. 17 — ICT-Related Incident Classification and Reporting
- Check for incident severity classification criteria in configuration.
- Verify major incident reporting hooks (to competent authorities).
- Look for incident data retention policies (5 years per DORA).
- Check for structured incident report generation capabilities.

### Art. 23-24 — Digital Operational Resilience Testing
- Verify existence of integration/load/stress test configurations.
- Check for chaos engineering or fault injection test setups.
- Look for penetration testing references or TLPT (Threat-Led Penetration Testing) evidence.
- Verify scenario-based testing for critical business processes.
- Check for test result documentation and remediation tracking.

### Art. 25-27 — Threat-Led Penetration Testing (TLPT)
- Look for TLPT scope definitions referencing critical functions.
- Check for red team exercise configurations or references.
- Verify TLPT covers live production systems (as required by DORA).
- Flag critical financial systems without TLPT evidence.

### Art. 28-30 — ICT Third-Party Risk Management
- Identify third-party ICT service dependencies (cloud providers, SaaS, APIs).
- Check for vendor risk assessment references in configuration.
- Look for concentration risk analysis (multiple critical services from same provider).
- Verify exit strategy provisions (data portability, alternative provider configs).
- Check for sub-outsourcing controls (chain dependency tracking).

### Art. 31-44 — Critical Third-Party Providers Oversight
- Verify monitoring of critical third-party service health (health checks, SLA monitoring).
- Check for contractual SLA enforcement in monitoring configurations.
- Look for third-party audit log ingestion.
- Flag critical business functions running on single third-party provider without fallback.

## SEVERITY MAPPING

| DORA Article | Violation Type | Default Severity | Rationale |
|-------------|----------------|-----------------|-----------|
| Art. 9 | No encryption at rest on financial data | CRITICAL | Protection and prevention — direct security violation |
| Art. 9 | No TLS/HTTPS enforcement | CRITICAL | Encryption in transit mandate |
| Art. 9 | No access control (RBAC/ABAC) on financial data | CRITICAL | Protection mandate |
| Art. 10 | No monitoring or anomaly detection on critical systems | HIGH | Detection mandate |
| Art. 11 | No backup or disaster recovery configuration | CRITICAL | Recovery mandate |
| Art. 11 | No documented RTO/RPO for critical systems | HIGH | Business continuity |
| Art. 12 | Backups without encryption or integrity verification | HIGH | Backup security mandate |
| Art. 15 | No incident management integration | HIGH | Incident management mandate |
| Art. 17 | No major incident reporting mechanism | MEDIUM | Reporting obligation |
| Art. 23 | No resilience testing (load/stress/integration) | MEDIUM | Testing mandate |
| Art. 25 | No TLPT evidence for critical functions | HIGH | Penetration testing mandate |
| Art. 28 | Third-party dependencies without risk assessment | HIGH | Third-party risk mandate |
| Art. 28 | Critical dependency on single provider without exit strategy | MEDIUM | Concentration risk |
| Art. 7 | No environment segregation (dev/test/prod) | MEDIUM | ICT system security |
| Art. 8 | Critical systems without redundancy | HIGH | Availability requirement |

## ORGANIZATIONAL WARNINGS (OUT OF SCOPE)

The following DORA requirements CANNOT be verified from code alone and MUST be listed as `ORGANIZATIONAL_WARNING` items:

- Art. 5: ICT risk management framework governance (board-level responsibility).
- Art. 6: ICT risk management function appointment and organizational reporting line.
- Art. 13: Lessons learned and training programs from past ICT incidents.
- Art. 14: Crisis communication plans with competent authorities and clients.
- Art. 17: Major ICT incident reporting to competent national authorities (EBA/EIOPA/ESMA).
- Art. 19: Centralized ICT incident reporting hub coordination.
- Art. 28: Full ICT third-party risk management policy (contractual elements, not just config).
- Art. 30: Contractual arrangements with ICT third-party providers (key contractual provisions).
- Art. 31-44: Oversight framework for critical third-party providers (regulatory interaction).
- Staff ICT security training and awareness programs.
- Business Impact Analysis (organizational process beyond RTO/RPO in config).
- ICT asset register (comprehensive organizational document).
