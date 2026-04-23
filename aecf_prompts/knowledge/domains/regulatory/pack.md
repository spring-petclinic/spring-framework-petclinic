# Regulatory Compliance Domain Pack

## Cross-cutting Rules
- Treat regulatory compliance as a code-level verification concern: only audit what is observable in source code, configuration, and project artifacts.
- Never claim full regulatory compliance from code audit alone — organizational, procedural, and contractual obligations exist outside the codebase.
- Always emit an `ORGANIZATIONAL_WARNING` section listing compliance dimensions that cannot be verified from code (e.g., DPO appointment, data processing agreements, staff training).
- Map findings to specific regulation articles when possible (e.g., "GDPR Art. 32(1)(a)" not just "encryption missing").
- Use deterministic severity classification aligned with regulatory risk: CRITICAL for direct violations with enforcement risk, HIGH for significant gaps, MEDIUM for incomplete controls, LOW for best-practice deviations.

## Obsolescence Control
- Every regulatory semantic profile MUST declare `regulation_reference_date` (ISO 8601) and `max_staleness_months` (integer).
- At execution time, if `current_date - regulation_reference_date > max_staleness_months`, the skill MUST emit a `⚠️ REGULATORY PROFILE STALENESS WARNING` at the top of the report.
- The staleness warning MUST include: profile name, reference date, staleness threshold, and recommendation to update the profile.
- Staleness does NOT block execution — it produces a visible warning so the responsible person can update the regulatory reference.

## Required Review Angles (All Regulatory Skills)
- Personal data identification and classification (PII, sensitive, special categories).
- Consent and legal basis evidence in code flows.
- Data retention and deletion logic.
- Encryption at rest and in transit.
- Logging and audit trail adequacy (without logging personal data).
- Access control and authorization boundaries.
- Third-party data sharing and processor identification.
- Cross-border transfer indicators.

## Override Guidance
- Regulatory domain packs layer on top of the `security` domain — security checks still apply.
- If a project has a resolved `AECF_PROJECT_CONTEXT` with `compliance_requirements`, those MUST be cross-referenced.
