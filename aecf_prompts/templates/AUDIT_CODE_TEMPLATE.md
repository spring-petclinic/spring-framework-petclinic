# AECF — AUDIT_CODE: {{TOPIC}}

LAST_REVIEW: 2026-04-17

## METADATA

| Field | Value |
| --- | --- |
| Skill | {{skill}} |
| Phase | AUDIT_CODE |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |
| Code audited | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_05_IMPLEMENT.md |

## 1. Scope Compliance

| Aspect | Result |
| --- | --- |
| Does code match the PLAN? | ✅ / ❌ |
| Scope expansion? | ✅ / ❌ |
| Unplanned features? | ✅ / ❌ |

## 2. Security Audit

| Control | Status | Observation |
| --- | --- | --- |
| Input validation | ✅ / ❌ | |
| Access control | ✅ / ❌ | |
| Data exposure | ✅ / ❌ | |
| Enumeration mitigation | ✅ / ❌ | |
| Security logging | ✅ / ❌ | |

## 3. Resource Management

| Aspect | Status |
| --- | --- |
| Resources closed correctly | ✅ / ❌ |
| Context managers used | ✅ / ❌ |
| Timeouts on external calls | ✅ / ❌ |

## 4. Code Quality

| Aspect | Status | Observation |
| --- | --- | --- |
| Error handling | ✅ / ❌ | |
| Logging (no print()) | ✅ / ❌ | |
| Edge cases | ✅ / ❌ | |
| Side effects | ✅ / ❌ | |

## 5. Testing Evidence

| Aspect | Status |
| --- | --- |
| Evidence source (`## 6. Tests Executed`) | ✅ / ❌ |
| Tests executed | ✅ / ❌ |
| Evidence (output) | ✅ / ❌ |
| Tests passing | ✅ / ❌ |
| Coverage measured | ✅ / ❌ / Blocker: ___ |

## 6. Findings

| ID | Severity | Category | Description | Recommendation |
| --- | --- | --- | --- | --- |
| F1 | CRITICAL / WARNING / INFO | | | |

## AECF_SCORE_REPORT

| Category | Weight | Raw Score | Max Raw | Weighted | Max Weighted |
| --- | --- | --- | --- | --- | --- |
| Scope Validation | 2 | __ | 6 | __ | 12 |
| Security Controls | 3 | __ | 8 | __ | 24 |
| Resource Management | 2 | __ | 4 | __ | 8 |
| Dep. Outage Resilience | 3 | __ / N/A | 10 | __ / N/A | 30 / N/A |
| Logging & Observability | 2 | __ | 6 | __ | 12 |
| Compliance with Previous Phase | 3 | __ | 6 | __ | 18 |
| Production Readiness | 2 | __ | 8 | __ | 16 |
| Decision Integrity | 3 | __ | 4 | __ | 12 |
| Code Audit Integrity | 2 | __ | 6 | __ | 12 |
| Testing Evidence | 3 | __ | 6 | __ | 18 |
| Anti-patterns | 3 | __ | 26 | __ | 78 |
| **TOTAL** | | **__** | **__** | **__** | **__** |

**Raw Score**: __ / __ | **Normalized Score**: ___% | **Level**: ___ | **Verdict**: GO / NO-GO

## AECF_COMPLIANCE_REPORT

- [ ] Checklist `checklists/AUDIT_CODE_CHECKLIST.md` applied
- [ ] Scoring calculated according to `scoring/SCORING_MODEL.md`
- [ ] Findings classified by severity
- [ ] Testing evidence verified
- [ ] Verdict justified with evidence
- [ ] Missing testing evidence -> automatic NO-GO applied

