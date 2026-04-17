# AECF SCORING — APPLICABILITY RULES

LAST_REVIEW: 2026-02-24

## Purpose

This document defines when AECF Scoring applies and when alternative evaluation methods are used.

---

## RULE 1: AECF Scoring Applies to Code Production Phases

### ✅ Phases that MUST include AECF Scoring:

| Phase | Checklist | Scoring Type |
|-------|-----------|--------------|
| 00_PLAN | PLAN_CHECKLIST.md | Full AECF Scoring |
| 02_AUDIT_PLAN | AUDIT_PLAN_CHECKLIST.md | Full AECF Scoring |
| 04_IMPLEMENT | IMPLEMENT_CHECKLIST.md | Full AECF Scoring |
| 05_AUDIT_CODE | AUDIT_CODE_CHECKLIST.md | Full AECF Scoring |
| 08_TEST_STRATEGY | TEST_STRATEGY_CHECKLIST.md | Full AECF Scoring |
| 09_TEST_IMPLEMENTATION | TEST_IMPLEMENTATION_CHECKLIST.md | Full AECF Scoring |
| 10_AUDIT_TESTS | AUDIT_TESTS_CHECKLIST.md | Full AECF Scoring |
| 17_SECURITY_AUDIT | SECURITY_AUDIT_CHECKLIST.md | Full AECF Scoring |
| 00_HOTFIX | N/A (inline checklist) | **Simplified AECF Scoring** |

### Rationale:

These phases produce or evaluate code/tests for production. AECF Scoring quantifies production readiness and maturity level.

---

## RULE 2: Skills with Alternative Evaluation

### ❌ Skills that DO NOT use AECF Scoring:

#### 1. **skill_document_legacy** (Documentation Skill)

**Why**: Does not produce code; reverse-engineers existing functionality.

**Alternative Evaluation**: Documentation Completeness Score

```markdown
## DOCUMENTATION QUALITY ASSESSMENT

| Aspect | Status |
|--------|--------|
| Entry points identified | ✓/✗ |
| Flow diagrams generated | ✓/✗ |
| Dependencies mapped | ✓/✗ |
| Side effects documented | ✓/✗ |
| Unknowns explicit | ✓/✗ |

Completeness: X/5
```

---

#### 2. **skill_code_standards_audit** (Audit Skill)

**Why**: Already produces its own compliance scoring system.

**Output IS a Score**: Standards Compliance Report with severity-weighted violations.

```markdown
## STANDARDS COMPLIANCE REPORT

### Findings by Severity:
- CRITICAL: 12
- WARNING: 45
- INFO: 23

### Compliance Score:
- Total violations: 80
- Compliance rate: 45%
- Severity-weighted score: 32/100 → FAIL
```

**Rationale**: Applying AECF Scoring to an audit that produces scoring would be meta-circular and redundant.

---

#### 3. **00_DEBUG** (Diagnostic Skill)

**Why**: Investigative phase; produces RCA (Root Cause Analysis), not code.

**Alternative Evaluation**: RCA Completeness

```markdown
## RCA QUALITY ASSESSMENT

- [ ] Root cause identified
- [ ] Reproduction steps documented
- [ ] Related components traced
- [ ] Fix suggestions provided (if applicable)
```

---

#### 4. **00_DOCUMENT_EXISTING_FUNCTIONALITY** (Documentation Skill)

**Why**: Similar to `skill_document_legacy`; produces documentation, not code.

**Alternative Evaluation**: Documentation Completeness.

---

#### 5. **00_DISCOVERY_LEGACY** (Investigation Skill)

**Why**: Exploration phase; identifies what exists before any planning.

**Alternative Evaluation**: Discovery completeness (scope identified, unknowns documented).

---

#### 6. **00_EXPLAIN_BEHAVIOR** (Informational Skill)

**Why**: Purely informational; explains existing behavior without producing artifacts.

**Alternative Evaluation**: None required (informational only).

---

## RULE 3: Simplified Scoring for Emergency Flows

### Hotfix Scoring (00_HOTFIX)

**Purpose**: Emergency response requires speed but not full governance depth.

**Scoring Model**: Simplified AECF Scoring

| Category | Weight | Items |
|----------|--------|-------|
| Root Cause Validated | 3 | 2 |
| Fix is Minimal | 2 | 1 |
| Security Controls | 3 | 3 |
| Rollback Plan Exists | 3 | 2 |
| Production Readiness | 2 | 3 |

**Thresholds**:
- Score >= 70 → GO
- Score < 70 → NO-GO
- Any CRITICAL → Automatic NO-GO

**Rationale**: Full AECF Scoring would slow emergency response. Simplified model focuses on critical aspects: root cause, security, and rollback safety.

---

## RULE 4: General Applicability Logic

### When to Apply AECF Scoring:

```
IF phase_produces_code OR phase_evaluates_code_for_production THEN
    Apply AECF Scoring
ELSE IF phase_is_hotfix THEN
    Apply Simplified AECF Scoring
ELSE IF phase_produces_own_scoring THEN
    Use native scoring (no AECF Scoring)
ELSE IF phase_is_informational OR phase_is_investigative THEN
    No scoring required OR domain-specific completeness check
END
```

---

## RULE 5: Mandatory Dependency Outage Resilience Evaluation

Cuando una fase **consume o depende** de BBDD, red, Redis/cache, colas o APIs externas, la evaluación debe incluir explícitamente la categoría **Dependency Outage Resilience**.

### Mandatory controls to score

- Timeouts explícitos en llamadas externas
- Retries acotados con backoff + jitter (o no-retry justificado)
- Circuit breaker/fail-fast o equivalente
- Error de usuario/sistema alineado con causa transitoria de dependencia
- Protección anti retry-storm (límite de concurrencia/rate limiting/backpressure)

### Enforcement

- Si la fase aplica AECF Scoring y no puntúa esta categoría cuando hay dependencias externas → salida **INVÁLIDA**.
- Si se detecta retry no acotado o ausencia total de timeout en ruta crítica → **CRITICAL**.

---

## Summary Table

| Phase/Skill | AECF Scoring | Alternative | Rationale |
|-------------|--------------|-------------|-----------|
| 00_PLAN | ✅ Full | - | Produces plan for code |
| 00_DEBUG | ❌ | RCA completeness | Investigative, not code |
| 00_DISCOVERY_LEGACY | ❌ | Discovery completeness | Exploration phase |
| 00_DOCUMENT_EXISTING_FUNCTIONALITY | ❌ | Doc completeness | Documentary only |
| 00_EXPLAIN_BEHAVIOR | ❌ | None | Informational only |
| 02_AUDIT_PLAN | ✅ Full | - | Evaluates plan quality |
| 04_IMPLEMENT | ✅ Full | - | Produces code |
| 05_AUDIT_CODE | ✅ Full | - | Evaluates code quality |
| 08_TEST_STRATEGY | ✅ Full | - | Plans tests |
| 09_TEST_IMPLEMENTATION | ✅ Full | - | Produces test code |
| 10_AUDIT_TESTS | ✅ Full | - | Evaluates test quality |
| 17_SECURITY_AUDIT | ✅ Full | - | Security evaluation |
| 00_HOTFIX | ✅ Simplified | - | Emergency code fix |
| skill_document_legacy | ❌ | Doc completeness | Documentary only |
| skill_code_standards_audit | ❌ | Native scoring | Already produces score |
| skill_maturity_assessment | ❌ | Assessment completeness (X/6) | Produces maturity score itself — meta-circular |
| skill_refactor | ✅ Full | - | Produces refactored code (uses IMPLEMENT + AUDIT_CODE phases) |
| skill_tech_debt_assessment | ❌ | Assessment completeness (X/6) | Evaluative, does not produce code |
| skill_release_readiness | ❌ | Release Readiness Score (native) | Produces its own cross-phase scoring |
| skill_dependency_audit | ❌ | Supply Chain Risk Score (native) | Produces its own risk scoring |

---

## Enforcement

- Phases marked with **✅ Full** MUST include complete AECF_SCORE_REPORT.
- Phases marked with **✅ Simplified** MUST include simplified HOTFIX score.
- Phases marked with **❌** MUST NOT attempt AECF Scoring; use specified alternative.

Failure to comply invalidates the phase output.
