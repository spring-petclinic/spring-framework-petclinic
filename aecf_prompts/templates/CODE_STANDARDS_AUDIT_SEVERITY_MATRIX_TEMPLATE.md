# AECF — CODE STANDARDS AUDIT SEVERITY MATRIX

## Metadata

| Field | Value |
|---|---|
| Document Type | CODE_STANDARDS_AUDIT_SEVERITY_MATRIX |
| Phase | TEMPLATE |
| Version | v1 |
| Status | baseline |
| Scope | project-local |
| Owner | project team |
| Created | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |

---

## Purpose

Provide a **project-specific severity calibration** for `aecf_code_standards_audit` so repeated audits on the same repository produce consistent `CRITICAL/WARNING/PASS` classification.

This matrix is local to the project and must live at the root of documentation:

`documentation/AECF_CODE_STANDARDS_AUDIT_SEVERITY_MATRIX.md`

---

## Canonical Rules

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| MATRIX-RUN-01 | Runtime/Execution | Import/module/dependency broken and blocks execution | CRITICAL |
| MATRIX-SEC-01 | Security SQL | Dynamic SQL with interpolated identifiers without whitelist/sanitization | CRITICAL |
| MATRIX-SEC-02 | Secrets | Hardcoded password/token/private key | CRITICAL |
| MATRIX-SEC-03 | Infra Exposure | Hardcoded host/IP/port without secret | WARNING |
| MATRIX-LOG-01 | Logging | `print()` in production code | WARNING |
| MATRIX-LOG-02 | Error Handling | Generic catch with lost traceback/context | WARNING |
| MATRIX-TST-01 | Testing | No automated tests in critical business flow | CRITICAL |
| MATRIX-TST-02 | Testing | Partial coverage missing edge/error cases | WARNING |
| MATRIX-CFG-01 | Config | Hardcoded runtime paths | WARNING |
| MATRIX-CFG-02 | Config | Runtime settings not externalized to `CM_*` | WARNING |
| MATRIX-CON-01 | Concurrency | Missing lock with race/overwrite risk in shared resource | CRITICAL |
| MATRIX-CON-02 | Concurrency | Missing `CM_*` thread/queue toggle when pattern applies | WARNING |
| MATRIX-RES-01 | Resources | Resource lifecycle not explicit (`dispose`/close/context manager missing) | WARNING |
| MATRIX-NAM-01 | Naming Runtime | File/module naming breaks import/runtime | CRITICAL |
| MATRIX-NAM-02 | Naming Style | Naming/style convention violations not breaking runtime | WARNING |
| MATRIX-DOC-01 | Documentation | Missing docstrings/type hints in public APIs | WARNING |
| MATRIX-IMP-01 | Import Hygiene | Unused imports or unnecessary function-local imports | WARNING |

---

## Tie-breaker Rules

If severity is ambiguous, apply in this order:

1. Breaks end-to-end execution? → CRITICAL
2. Can cause data loss/corruption? → CRITICAL
3. Creates exploitable security surface? → CRITICAL
4. Otherwise → WARNING

---

## Counting Rules

1. CRITICAL counted per root cause.
2. WARNING can be grouped per repeated pattern per file.
3. PASS only when a control is explicitly verified.
4. Always include totals: unique findings, unique critical, unique warning, verified pass.

---

## MATRIX-PENDING Workflow

When a finding does not match existing rules:

1. Classify as `MATRIX-PENDING`.
2. Use provisional severity `WARNING` by default.
3. Escalate to provisional `CRITICAL` only if tie-breaker rules 1-3 apply.
4. Propose a new rule ID in the audit report.
5. After approval, add the new rule to this matrix and increment version (`v1.1`, `v1.2`, ...).

---

## Auto-Apply Protocol

This matrix supports **automatic rule insertion** by the `aecf_code_standards_audit` skill:

- When the Classification Decision Protocol produces `ADD_RULE` decisions, new rules are inserted automatically into the Canonical Rules table above.
- The skill bumps the version (e.g., `v1` → `v1.1`), updates `Last Updated`, and appends a changelog entry.
- No manual intervention is required — the `ADD_RULE` decision is the confirmation.
- `NO_ADD_RULE` findings are documented in the audit report only and do not modify this file.
- Every auto-applied rule is traceable to a specific audit report via the Change Log.

---

## Change Log

- v1: Initial project baseline template.
