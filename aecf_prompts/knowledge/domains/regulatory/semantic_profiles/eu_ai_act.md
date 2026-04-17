---
profile_id: eu_ai_act
title: EU AI Act — Regulation (EU) 2024/1689
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
  - skill=security_review_eu_ai_act
max_lines_per_section: 8
tags:
  - eu-ai-act
  - ai-regulation
  - high-risk-ai
  - regulatory
  - eu
---

LAST_REVIEW: 2026-03-16
OWNER SEACHAD

## REGULATION SCOPE

EU Artificial Intelligence Act (Regulation (EU) 2024/1689). Applies to providers and deployers of AI systems placed on the EU market or whose output is used in the EU. Entered into force 1 August 2024; high-risk AI obligations apply from 2 August 2026.

## CODE-LEVEL AUDIT CHECKLIST

### Art. 6 — Risk Classification (High-Risk AI)
- Identify whether the system falls under Annex III high-risk categories (biometrics, critical infrastructure, education, employment, essential services, law enforcement, migration, justice).
- Check for explicit risk classification in project documentation or configuration.
- Flag systems that process biometric data, make employment decisions, or score creditworthiness without risk classification evidence.

### Art. 9 — Risk Management System
- Verify existence of risk management artifacts (risk register, mitigation plans) referenced in code or documentation.
- Check for residual risk documentation or comments in critical decision paths.
- Flag high-risk paths without documented risk mitigation evidence.

### Art. 10 — Data and Data Governance
- Check training data pipelines for bias detection mechanisms.
- Verify data quality validation steps (schema validation, completeness checks, statistical tests).
- Look for data versioning and lineage tracking.
- Check for ground truth validation and annotation quality controls.
- Flag training pipelines without documented data governance.

### Art. 11 — Technical Documentation
- Verify existence of model cards, datasheets, or equivalent technical documentation referenced in code.
- Check for architecture documentation (model topology, hyperparameters, training procedure).
- Look for documented intended use and foreseeable misuse scenarios.

### Art. 12 — Record-Keeping (Logging)
- Verify automatic logging of AI system events (predictions, decisions, confidence scores).
- Check log retention configuration and adequacy for traceability.
- Verify logs capture: input data reference, output, timestamp, model version, user/operator ID.
- Flag decision-making endpoints without audit logging.

### Art. 13 — Transparency
- Check for user-facing disclosure that they are interacting with an AI system.
- Verify explainability mechanisms (feature importance, decision rationale, confidence scores).
- Look for content labelling on AI-generated outputs (synthetic media, generated text).
- Flag AI interaction points without transparency disclosure.

### Art. 14 — Human Oversight
- Verify human-in-the-loop mechanisms for high-stakes decisions.
- Check for override/intervention capabilities in automated decision flows.
- Look for escalation paths when AI confidence is below threshold.
- Flag fully automated critical decisions without human review capability.

### Art. 15 — Accuracy, Robustness and Cybersecurity
- Check for model performance monitoring (accuracy metrics, drift detection).
- Verify adversarial robustness testing or input validation against adversarial inputs.
- Check for model integrity verification (hash validation, signing).
- Look for fallback mechanisms when model performance degrades.
- Verify cybersecurity measures on model serving endpoints (authentication, rate limiting, input validation).

### Art. 16-22 — Provider Obligations
- Check for quality management system artifacts referenced in code.
- Verify CE marking or conformity assessment documentation references.
- Look for post-market monitoring integration (telemetry, feedback loops).
- Check for serious incident reporting mechanisms or hooks.

### Art. 26 — Deployer Obligations
- Verify input data relevance validation before feeding to the AI system.
- Check that deployers log usage as required by Art. 12.
- Look for DPIA or fundamental rights impact assessment references.

### Art. 50 — Transparency Obligations for Certain AI Systems
- Check for deep fake / synthetic content labelling.
- Verify chatbot disclosure ("You are interacting with an AI system").
- Look for emotion recognition or biometric categorization disclosures.
- Flag generative AI outputs without provenance metadata.

### Art. 52 — General-Purpose AI Models (GPAI)
- Check for technical documentation of GPAI capabilities and limitations.
- Verify copyright compliance in training data (opt-out mechanisms, licensing records).
- Look for systemic risk assessment if model exceeds 10^25 FLOP training threshold.
- Check for model evaluation results documentation.

## SEVERITY MAPPING

| EU AI Act Article | Violation Type | Default Severity | Rationale |
|-------------------|----------------|-----------------|-----------|
| Art. 5 | Prohibited AI practice in code (social scoring, real-time biometric for law enforcement) | CRITICAL | Prohibited practice — fines up to €35M or 7% turnover |
| Art. 6/Annex III | High-risk system without risk classification | HIGH | Compliance prerequisite |
| Art. 10 | Training pipeline without bias detection or data quality validation | HIGH | Data governance mandate |
| Art. 12 | AI decisions without audit logging | HIGH | Record-keeping mandate |
| Art. 13 | No AI interaction disclosure to users | HIGH | Transparency mandate |
| Art. 14 | Automated critical decisions without human override | CRITICAL | Human oversight mandate |
| Art. 15 | No model drift detection or performance monitoring | MEDIUM | Robustness requirement |
| Art. 15 | No adversarial input validation on model endpoints | HIGH | Cybersecurity of AI |
| Art. 50 | Generative output without provenance labelling | MEDIUM | Transparency for GPAI |
| Art. 52 | GPAI without technical documentation | MEDIUM | GPAI provider obligation |
| Art. 9 | High-risk AI without documented risk management | HIGH | Risk management system |
| Art. 11 | No model card or technical documentation | MEDIUM | Documentation requirement |

## ORGANIZATIONAL WARNINGS (OUT OF SCOPE)

The following EU AI Act requirements CANNOT be verified from code alone and MUST be listed as `ORGANIZATIONAL_WARNING` items:

- Art. 9: Complete risk management system (organizational process, not just code artifacts).
- Art. 16: Quality management system certification and CE marking process.
- Art. 17: Quality management system documentation (organizational).
- Art. 22: Serious incident reporting to national authorities (process, not code).
- Art. 26: Deployer's fundamental rights impact assessment (organizational process).
- Art. 27: Registration in EU AI database (administrative).
- Staff AI literacy training (Art. 4).
- Authorized representative appointment for non-EU providers.
- Conformity assessment procedures with notified bodies.
- Post-market monitoring plan (organizational, beyond telemetry hooks).
