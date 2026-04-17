# Regulatory Compliance Domain

## What is this domain?

The **Regulatory** domain provides cross-cutting regulatory compliance knowledge for AECF security review skills. It supplies article-level checklists, severity mappings, and code-scoped audit criteria for EU/international data protection and digital resilience regulations.

## Capabilities

- **GDPR code audit guidance** — personal data handling, consent patterns, retention logic, encryption, logging constraints.
- **EU AI Act compliance** — risk classification, transparency obligations, human oversight, logging requirements for AI systems.
- **DORA digital resilience** — ICT risk management, incident reporting, third-party dependency resilience, testing obligations.
- **Code-scoped only** — regulatory skills audit what is observable in the codebase. Organizational/procedural compliance (DPO appointment, contracts, policies) is flagged as out-of-scope warnings.
- **Obsolescence-aware** — each semantic profile carries a `regulation_reference_date` and a `max_staleness_months` field. Skills emit a WARNING when the profile has not been reviewed within the staleness window.

### Semantic Profiles

| Profile | Regulation | Reference Date |
|---------|-----------|----------------|
| `gdpr.md` | EU General Data Protection Regulation (2016/679) | 2026-03-16 |
| `eu_ai_act.md` | EU Artificial Intelligence Act (2024/1689) | 2026-03-16 |
| `dora.md` | Digital Operational Resilience Act (2022/2554) | 2026-03-16 |

## Activation

Regulatory profiles are activated by invoking the corresponding `security_review_*` skill:

```
@aecf run skill=security_review_gdpr
@aecf run skill=security_review_eu_ai_act
@aecf run skill=security_review_dora
```

## Scope limitation

These skills audit CODE only. They cannot verify:
- Whether a Data Protection Officer has been appointed
- Whether Data Processing Agreements exist with third-party processors
- Whether a Record of Processing Activities has been filed
- Whether organizational privacy impact assessments have been conducted outside the codebase

Such gaps are surfaced as `ORGANIZATIONAL_WARNING` items in the report.
