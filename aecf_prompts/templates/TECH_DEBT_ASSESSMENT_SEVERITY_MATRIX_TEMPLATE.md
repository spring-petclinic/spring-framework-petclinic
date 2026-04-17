# AECF — TECH DEBT ASSESSMENT SEVERITY MATRIX

## Metadata

| Field | Value |
|---|---|
| Document Type | TECH_DEBT_ASSESSMENT_SEVERITY_MATRIX |
| Phase | TEMPLATE |
| Version | v1 |
| Status | baseline |
| Scope | project-local |
| Owner | project team |
| Created | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |

---

## Purpose

Provide a **project-specific severity calibration** for `aecf_tech_debt_assessment` so repeated tech debt assessments on the same repository produce consistent classification of debt severity and remediation effort.

This matrix is local to the project and must live at the root of documentation:

`documentation/AECF_TECH_DEBT_ASSESSMENT_SEVERITY_MATRIX.md`

---

## Canonical Rules — Design Debt

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| TD-DESIGN-01 | Design | God class/module (> 500 LOC, > 10 responsibilities) | CRITICAL |
| TD-DESIGN-02 | Design | Tight coupling between unrelated modules (circular deps) | HIGH |
| TD-DESIGN-03 | Design | Missing abstraction causing code duplication across modules | HIGH |
| TD-DESIGN-04 | Design | SOLID principle violation with measurable maintenance impact | MEDIUM |
| TD-DESIGN-05 | Design | Minor design pattern misapplication, no operational impact | LOW |

## Canonical Rules — Code Debt

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| TD-CODE-01 | Code | Duplicated logic blocks (> 20 LOC identical in ≥ 2 places) | HIGH |
| TD-CODE-02 | Code | Cyclomatic complexity > 20 per function | HIGH |
| TD-CODE-03 | Code | Function > 100 LOC | MEDIUM |
| TD-CODE-04 | Code | Nesting depth > 4 levels | MEDIUM |
| TD-CODE-05 | Code | Magic numbers/strings without named constants | MEDIUM |
| TD-CODE-06 | Code | Dead code / unreachable code blocks | LOW |
| TD-CODE-07 | Code | Global state without documented justification | HIGH |
| TD-CODE-08 | Code | Variable naming ambiguous or single-letter (outside loops) | LOW |

## Canonical Rules — Testing Debt

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| TD-TEST-01 | Testing | No automated tests for business-critical flow | CRITICAL |
| TD-TEST-02 | Testing | Test coverage < 40% on critical module | HIGH |
| TD-TEST-03 | Testing | Test coverage 40–80% (below target) | MEDIUM |
| TD-TEST-04 | Testing | Tests missing edge cases / error paths | MEDIUM |
| TD-TEST-05 | Testing | Fragile tests dependent on external state or ordering | HIGH |
| TD-TEST-06 | Testing | Excessive mocking hiding integration issues | MEDIUM |

## Canonical Rules — Documentation Debt

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| TD-DOC-01 | Documentation | No README or project onboarding documentation | HIGH |
| TD-DOC-02 | Documentation | Public API functions without docstrings | MEDIUM |
| TD-DOC-03 | Documentation | Missing type hints on public functions | MEDIUM |
| TD-DOC-04 | Documentation | Outdated/misleading comments or docs | MEDIUM |
| TD-DOC-05 | Documentation | Missing architecture decision records for key decisions | LOW |

## Canonical Rules — Dependency Debt

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| TD-DEP-01 | Dependencies | Dependency with known critical CVE | CRITICAL |
| TD-DEP-02 | Dependencies | Dependency abandoned (> 24 months, no maintainer) | HIGH |
| TD-DEP-03 | Dependencies | Over-dependency (trivial utility imported as full package) | MEDIUM |
| TD-DEP-04 | Dependencies | Dependencies not version-pinned | MEDIUM |
| TD-DEP-05 | Dependencies | Dependency 1+ major version behind | LOW |

## Canonical Rules — Infrastructure Debt

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| TD-INFRA-01 | Infrastructure | No CI/CD pipeline | HIGH |
| TD-INFRA-02 | Infrastructure | No automated linting or formatting | MEDIUM |
| TD-INFRA-03 | Infrastructure | Logging inconsistent or insufficient for production debugging | HIGH |
| TD-INFRA-04 | Infrastructure | Configuration hardcoded (no externalization) | MEDIUM |
| TD-INFRA-05 | Infrastructure | No health checks or monitoring hooks | MEDIUM |
| TD-INFRA-06 | Infrastructure | Missing containerization or reproducible environment setup | LOW |

---

## Effort Calibration

| Effort | Description | Typical Time |
|--------|-------------|-------------|
| **XS** | Trivial fix (rename, remove dead code, add constant) | < 30 min |
| **S** | Simple fix (add docstring, fix magic number, pin version) | 30 min – 2h |
| **M** | Moderate (extract function, add tests, externalize config) | 2h – 1 day |
| **L** | Significant (restructure module, add test suite, add CI/CD) | 1 – 3 days |
| **XL** | Major (architecture change, rewrite module, migrate dependency) | 3 – 10 days |

---

## Tie-breaker Rules

If severity is ambiguous, apply in this order:

1. Blocks ability to add features or fix bugs safely? → CRITICAL
2. Causes recurring production incidents? → CRITICAL
3. Significantly slows development velocity on business-critical path? → HIGH
4. Increases risk but workaround exists? → MEDIUM
5. Cosmetic or minor improvement? → LOW

---

## Counting Rules

1. CRITICAL counted per unique root cause (not per symptom).
2. HIGH/MEDIUM grouped per category per module when same pattern repeats.
3. LOW/INFO can be aggregated at project level.
4. Always include totals per category and per severity.
5. Effort estimates are per-item, with aggregated total for the full backlog.

---

## MATRIX-PENDING Workflow

When a finding does not match existing rules:

1. Classify as `MATRIX-PENDING`.
2. Use provisional severity based on tie-breaker rules.
3. Propose a new rule ID in the audit report.
4. After approval, add the new rule to this matrix and increment version (`v1.1`, `v1.2`, ...).

---

## Auto-Apply Protocol

This matrix supports **automatic rule insertion** by the `aecf_tech_debt_assessment` skill:

- When the Classification Decision Protocol produces `ADD_RULE` decisions, new rules are inserted automatically into the Canonical Rules table above.
- The skill bumps the version (e.g., `v1` → `v1.1`), updates `Last Updated`, and appends a changelog entry.
- No manual intervention is required — the `ADD_RULE` decision is the confirmation.
- `NO_ADD_RULE` findings are documented in the audit report only and do not modify this file.
- Every auto-applied rule is traceable to a specific tech debt assessment report via the Change Log.

---

## Change Log

- v1: Initial project baseline from template.
