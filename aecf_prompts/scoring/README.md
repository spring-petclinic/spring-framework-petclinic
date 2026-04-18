# AECF SCORING SYSTEM

## Overview

The AECF Scoring System provides quantifiable metrics for evaluating technical maturity and production readiness across all AECF phases.

---

## Contents

- **[AECF_SCORING_MODEL.md](AECF_SCORING_MODEL.md)**: Core scoring methodology, weights, and maturity levels
- **[SCORING_APPLICABILITY.md](SCORING_APPLICABILITY.md)**: Rules for when and how to apply scoring across phases and skills

---

## Quick Reference

### Scoring Scale (Per Item)

| Value | Meaning |
|-------|---------|
| 0 | Does NOT comply |
| 1 | Partially complies |
| 2 | Fully complies |

### Category Weights

| Category | Weight |
|----------|--------|
| Scope Validation | 2 |
| Security Controls | 3 |
| Resource Management | 2 |
| Logging & Observability | 2 |
| Compliance with Previous Phase | 3 |
| Production Readiness | 2 |
| Decision Integrity | 3 |
| Phase-specific sections | 2 |

### Maturity Levels

| Score | Level |
|-------|-------|
| 90-100 | ENTERPRISE READY |
| 75-89 | PRODUCTION READY |
| 60-74 | CONDITIONAL |
| 40-59 | HIGH RISK |
| 0-39 | FAIL |

### Verdict Rules

1. **Any CRITICAL finding** → Automatic NO-GO (Score = 0)
2. Score < 60 → NO-GO
3. Score 60-74 → GO CONDICIONAL
4. Score >= 75 → GO
5. Score >= 90 → GO ENTERPRISE

---

## Where Scoring Applies

### Full AECF Scoring

All main AECF phases that produce or evaluate code:
- 00_PLAN
- 02_AUDIT_PLAN
- 04_IMPLEMENT
- 05_AUDIT_CODE
- 08_TEST_STRATEGY
- 09_TEST_IMPLEMENTATION
- 10_AUDIT_TESTS
- 17_SECURITY_AUDIT

### Simplified Scoring

- **00_HOTFIX**: Emergency response with reduced scoring table (5 categories, threshold = 70)

### No AECF Scoring

Skills that use alternative evaluation:
- **skill_document_legacy**: Documentation completeness
- **skill_code_standards_audit**: Native compliance scoring
- **skill_maturity_assessment**: Assessment completeness (X/6) — meta-circular
- **skill_tech_debt_assessment**: Assessment completeness (X/6)
- **skill_release_readiness**: Release Readiness Score (native)
- **skill_dependency_audit**: Supply Chain Risk Score (native)
- **00_DEBUG**: RCA completeness
- **Informational phases**: No scoring

### Full AECF Scoring

Skills that produce code and use the standard AECF scoring model:
- **skill_refactor**: Full AECF scoring (produces refactored code)

See [SCORING_APPLICABILITY.md](SCORING_APPLICABILITY.md) for detailed rules.

---

## Implementation

### In Checklists

All phase checklists include:
```markdown
## SCORING TABLE

| Categoría | Peso | Items evaluados | Score |
|-----------|------|----------------|-------|
| ... | ... | ... |  |

## FINAL SCORE
- Score bruto:
- Score normalizado:
- Nivel de madurez:
- Veredicto automático:

**RULE**: If any CRITICAL finding exists → Score = 0 and automatic NO-GO
```

### In Prompts

All phase prompts include:
```markdown
────────────────────────
SCORING ENFORCEMENT (MANDATORY)
────────────────────────

You MUST:

1. Score each checklist item (0,1,2).
2. Apply category weights.
3. Compute normalized score.
4. Declare maturity level.
5. Apply automatic verdict rules.

If scoring is not included → Phase invalid.

Include in AECF_COMPLIANCE_REPORT:

## AECF_SCORE_REPORT

- Raw Score:
- Normalized Score:
- Maturity Level:
- Automatic Verdict:
- Critical Findings Present: YES / NO
```

---

## Usage

1. Agent executes phase (PLAN, IMPLEMENT, AUDIT, etc.)
2. Agent validates each checklist item → assigns score (0/1/2)
3. Agent fills SCORING TABLE with computed scores per category
4. Agent calculates:
   - Raw Score = Σ (item_score × category_weight)
   - Normalized Score = (Raw Score / Max Possible) × 100
5. Agent determines maturity level based on normalized score
6. Agent applies verdict rules (including CRITICAL override)
7. Agent includes AECF_SCORE_REPORT in compliance report

---

## Examples

### Example: AUDIT_CODE with Score 85

```markdown
## SCORING TABLE

| Categoría | Peso | Items evaluados | Score |
|-----------|------|----------------|-------|
| Scope Validation | 2 | 3 | 6 |
| Security Controls | 3 | 4 | 21 |
| Resource Management | 2 | 2 | 4 |
| Logging & Observability | 2 | 3 | 5 |
| Compliance with Previous Phase | 3 | 3 | 15 |
| Production Readiness | 2 | 4 | 14 |
| Decision Integrity | 3 | 2 | 12 |
| Code Audit Integrity | 2 | 3 | 6 |

## FINAL SCORE
- Score bruto: 83/96
- Score normalizado: 86.5
- Nivel de madurez: PRODUCTION READY
- Veredicto automático: GO

## AECF_SCORE_REPORT

- Raw Score: 83/96
- Normalized Score: 86.5/100
- Maturity Level: PRODUCTION READY
- Automatic Verdict: GO
- Critical Findings Present: NO
```

---

## Enforcement

- Phases without scoring are **INVALID**
- Incorrect scoring computation → **Phase must be repeated**
- Omitting AECF_SCORE_REPORT → **Non-compliant**

---

## Version

- **Implemented**: 2026-02-12
- **Status**: Active
- **Owner**: Enterprise Governance Architect
