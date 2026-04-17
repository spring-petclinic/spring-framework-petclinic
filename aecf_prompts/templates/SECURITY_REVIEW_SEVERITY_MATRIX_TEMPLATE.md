# AECF — SECURITY REVIEW SEVERITY MATRIX

## Metadata

| Field | Value |
|---|---|
| Document Type | SECURITY_REVIEW_SEVERITY_MATRIX |
| Phase | TEMPLATE |
| Version | v1 |
| Status | baseline |
| Scope | project-local |
| Owner | project team |
| Created | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |

---

## Purpose

Provide a **project-specific severity calibration** for `aecf_security_review` so repeated security audits on the same repository produce consistent classification of vulnerabilities and operational risk.

This matrix is local to the project and must live at the root of documentation:

`documentation/AECF_SECURITY_REVIEW_SEVERITY_MATRIX.md`

---

## Canonical Rules

| Rule ID | Category | Condition | Severity |
|---|---|---|---|
| SEC-INJ-01 | Injection | SQL/NoSQL/Command injection via unsanitized user input | CRITICAL |
| SEC-INJ-02 | Injection | Template injection (SSTI) | CRITICAL |
| SEC-AUTH-01 | Authentication | Missing authentication on sensitive endpoint | CRITICAL |
| SEC-AUTH-02 | Authentication | Weak password policy or plaintext password storage | CRITICAL |
| SEC-AUTH-03 | Authentication | Session token with insufficient entropy or no expiration | HIGH |
| SEC-AUTHZ-01 | Authorization | Missing authorization check (IDOR, privilege escalation) | CRITICAL |
| SEC-AUTHZ-02 | Authorization | Role-based access control inconsistency | HIGH |
| SEC-CRYPT-01 | Cryptography | Use of broken/weak algorithm (MD5, SHA1 for security, DES) | CRITICAL |
| SEC-CRYPT-02 | Cryptography | Missing encryption for sensitive data at rest | HIGH |
| SEC-CRYPT-03 | Cryptography | Missing TLS/encryption for data in transit | HIGH |
| SEC-SECRET-01 | Secrets | Hardcoded password, API key, token, or private key in source | CRITICAL |
| SEC-SECRET-02 | Secrets | Secrets in logs, error messages, or stack traces | HIGH |
| SEC-CONF-01 | Configuration | Debug mode enabled in production config | HIGH |
| SEC-CONF-02 | Configuration | Security headers missing (CSP, X-Frame-Options, etc.) | MEDIUM |
| SEC-CONF-03 | Configuration | CORS misconfiguration (wildcard or overly permissive) | HIGH |
| SEC-INPUT-01 | Input Validation | Missing server-side input validation on business-critical field | HIGH |
| SEC-INPUT-02 | Input Validation | Missing server-side input validation on non-critical field | MEDIUM |
| SEC-XSS-01 | XSS | Reflected or Stored XSS via unescaped output | HIGH |
| SEC-XSS-02 | XSS | DOM-based XSS | MEDIUM |
| SEC-SSRF-01 | SSRF | Server-side request forgery via user-controlled URL | CRITICAL |
| SEC-DEP-01 | Dependencies | Dependency with known CRITICAL CVE (CVSS ≥ 9.0) | CRITICAL |
| SEC-DEP-02 | Dependencies | Dependency with known HIGH CVE (CVSS 7.0–8.9) | HIGH |
| SEC-DEP-03 | Dependencies | Dependency with known MEDIUM CVE (CVSS 4.0–6.9) | MEDIUM |
| SEC-LOG-01 | Logging | Security events not logged (auth failures, access denied) | MEDIUM |
| SEC-LOG-02 | Logging | Sensitive data logged (passwords, tokens, PII) | HIGH |
| SEC-RATE-01 | Rate Limiting | No rate limiting on authentication/sensitive endpoints | MEDIUM |
| SEC-FILE-01 | File Handling | Unrestricted file upload without validation | HIGH |
| SEC-DESER-01 | Deserialization | Insecure deserialization of untrusted data | CRITICAL |

---

## Tie-breaker Rules

If severity is ambiguous, apply in this order:

1. Remotely exploitable without authentication? → CRITICAL
2. Leads to data exfiltration or unauthorized access? → CRITICAL
3. Requires authentication but escalates privileges? → HIGH
4. Information disclosure only, no direct exploitation? → MEDIUM
5. Theoretical risk, no practical exploit path in context? → LOW

---

## Counting Rules

1. CRITICAL counted per unique vulnerability instance (unique location + unique type).
2. HIGH grouped per vulnerability type per module if same root cause.
3. MEDIUM/LOW can be grouped per repeated pattern.
4. Always include totals: unique findings per severity, CVSS range.
5. Each finding must reference OWASP Top 10 category where applicable.

---

## MATRIX-PENDING Workflow

When a finding does not match existing rules:

1. Classify as `MATRIX-PENDING`.
2. Use provisional severity based on CVSS score (if available) or tie-breaker rules.
3. Propose a new rule ID in the audit report.
4. After approval, add the new rule to this matrix and increment version (`v1.1`, `v1.2`, ...).

---

## Auto-Apply Protocol

This matrix supports **automatic rule insertion** by the `aecf_security_review` skill:

- When the Classification Decision Protocol produces `ADD_RULE` decisions, new rules are inserted automatically into the Canonical Rules table above.
- The skill bumps the version (e.g., `v1` → `v1.1`), updates `Last Updated`, and appends a changelog entry.
- No manual intervention is required — the `ADD_RULE` decision is the confirmation.
- `NO_ADD_RULE` findings are documented in the audit report only and do not modify this file.
- Every auto-applied rule is traceable to a specific security review report via the Change Log.

---

## Change Log

- v1: Initial project baseline from template.
