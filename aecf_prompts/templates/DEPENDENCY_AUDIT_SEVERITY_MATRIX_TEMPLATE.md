# AECF — DEPENDENCY AUDIT SEVERITY MATRIX

## Metadata

| Field | Value |
|---|---|
| Document Type | DEPENDENCY_AUDIT_SEVERITY_MATRIX |
| Phase | TEMPLATE |
| Version | v1 |
| Status | baseline |
| Scope | project-local |
| Owner | project team |
| Created | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |

---

## Purpose

Provide a **project-specific severity calibration** for `aecf_dependency_audit` so repeated dependency audits on the same repository produce consistent classification of vulnerability risk, license compliance, maintenance health, and supply chain exposure.

This matrix is local to the project and must live at the root of documentation:

`documentation/AECF_DEPENDENCY_AUDIT_SEVERITY_MATRIX.md`

---

## Canonical Rules — Vulnerability (CVE)

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| DEP-CVE-01 | Vulnerability | Direct dependency with CVSS ≥ 9.0, exploit available | CRITICAL |
| DEP-CVE-02 | Vulnerability | Direct dependency with CVSS 7.0–8.9 | HIGH |
| DEP-CVE-03 | Vulnerability | Direct dependency with CVSS 4.0–6.9 | MEDIUM |
| DEP-CVE-04 | Vulnerability | Direct dependency with CVSS 0.1–3.9 | LOW |
| DEP-CVE-05 | Vulnerability | Transitive dependency with CVSS ≥ 9.0 | HIGH |
| DEP-CVE-06 | Vulnerability | Transitive dependency with CVSS 7.0–8.9 | MEDIUM |
| DEP-CVE-07 | Vulnerability | Multiple CVEs in single dependency (any CVSS) | Escalate one level |

## Canonical Rules — License Compliance

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| DEP-LIC-01 | License | No license declared | CRITICAL |
| DEP-LIC-02 | License | AGPL license in SaaS/network-exposed project | CRITICAL |
| DEP-LIC-03 | License | GPL v2/v3 in proprietary/commercial project | HIGH |
| DEP-LIC-04 | License | LGPL in statically linked context | HIGH |
| DEP-LIC-05 | License | LGPL in dynamically linked context | MEDIUM |
| DEP-LIC-06 | License | Unknown or custom license requiring legal review | HIGH |
| DEP-LIC-07 | License | Permissive license (MIT, BSD, Apache 2.0) | PASS |

## Canonical Rules — Maintenance Health

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| DEP-HEALTH-01 | Maintenance | Dependency officially deprecated or end-of-life | CRITICAL |
| DEP-HEALTH-02 | Maintenance | Last release > 18 months, 1 maintainer (bus factor) | HIGH |
| DEP-HEALTH-03 | Maintenance | Last release > 18 months, active community | MEDIUM |
| DEP-HEALTH-04 | Maintenance | Last release 6–18 months | LOW |
| DEP-HEALTH-05 | Maintenance | Last release < 6 months, multiple maintainers | PASS |

## Canonical Rules — Version Freshness

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| DEP-FRESH-01 | Freshness | 1+ major version behind with breaking security changes | HIGH |
| DEP-FRESH-02 | Freshness | 1+ major version behind, no security implications | MEDIUM |
| DEP-FRESH-03 | Freshness | 1–2 minor versions behind | LOW |
| DEP-FRESH-04 | Freshness | On latest version | PASS |

## Canonical Rules — Supply Chain

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| DEP-CHAIN-01 | Supply Chain | Known supply chain attack on dependency | CRITICAL |
| DEP-CHAIN-02 | Supply Chain | Typosquatting risk (similar name to popular package) | HIGH |
| DEP-CHAIN-03 | Supply Chain | Dependency tree depth > 10 levels | MEDIUM |
| DEP-CHAIN-04 | Supply Chain | Over-dependency (trivial functionality imported) | LOW |

---

## Tie-breaker Rules

If severity is ambiguous, apply in this order:

1. Actively exploited CVE in the wild? → CRITICAL
2. Breaks legal/license compliance for project distribution model? → CRITICAL
3. Dependency is end-of-life with no migration path? → HIGH
4. Risk is theoretical with no known exploit or compliance issue? → MEDIUM
5. Otherwise → LOW

---

## Counting Rules

1. CRITICAL counted per unique dependency + unique issue combination.
2. If one dependency has multiple issues, count each separately but flag as compound risk.
3. Transitive dependencies: count only if no parent upgrade resolves the issue.
4. Always include totals: direct vs transitive, per severity, per category.

---

## MATRIX-PENDING Workflow

When a finding does not match existing rules:

1. Classify as `MATRIX-PENDING`.
2. Use provisional severity based on tie-breaker rules.
3. Propose a new rule ID in the audit report.
4. After approval, add the new rule to this matrix and increment version (`v1.1`, `v1.2`, ...).

---

## Auto-Apply Protocol

This matrix supports **automatic rule insertion** by the `aecf_dependency_audit` skill:

- When the Classification Decision Protocol produces `ADD_RULE` decisions, new rules are inserted automatically into the Canonical Rules table above.
- The skill bumps the version (e.g., `v1` → `v1.1`), updates `Last Updated`, and appends a changelog entry.
- No manual intervention is required — the `ADD_RULE` decision is the confirmation.
- `NO_ADD_RULE` findings are documented in the audit report only and do not modify this file.
- Every auto-applied rule is traceable to a specific dependency audit report via the Change Log.

---

## Change Log

- v1: Initial project baseline from template.
