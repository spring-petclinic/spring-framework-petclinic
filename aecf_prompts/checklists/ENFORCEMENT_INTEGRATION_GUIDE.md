# AECF CHECKLIST ENFORCEMENT — INTEGRATION GUIDE

## OVERVIEW
This guide shows how to integrate mandatory checklist enforcement into existing AECF phase prompts.

## ENFORCEMENT BLOCK TEMPLATE

Add this block to each phase prompt **BEFORE** the verdict/output section:

```markdown
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/<PHASE>_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

## PHASE-SPECIFIC INTEGRATIONS

### 1. PLAN PHASE
**Checklist:** `./aecf/checklists/PLAN_CHECKLIST.md`

Add before "OUTPUT FORMAT" section:

```
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/PLAN_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

---

### 2. AUDIT_PLAN PHASE
**Checklist:** `./aecf/checklists/AUDIT_PLAN_CHECKLIST.md`

Add before "VERDICT LOGIC" section:

```
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/AUDIT_PLAN_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

---

### 3. IMPLEMENT PHASE
**Checklist:** `./aecf/checklists/IMPLEMENT_CHECKLIST.md`

Add before "CONSTRAINTS" section:

```
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/IMPLEMENT_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

**Example Integration in IMPLEMENT Prompt:**

```markdown
## YOUR ROLE
You are IMPLEMENT. You convert approved PLAN into production code.

[... existing content ...]

────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/IMPLEMENT_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.

## CONSTRAINTS
- No print() — use logging
- No direct commits
[... rest of constraints ...]
```

---

### 4. AUDIT_CODE PHASE
**Checklist:** `./aecf/checklists/AUDIT_CODE_CHECKLIST.md`

Add before "BUG CLASSIFICATION" section:

```
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/AUDIT_CODE_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

**Example Integration in AUDIT_CODE Prompt:**

```markdown
## YOUR ROLE
You are AUDIT_CODE. You validate implementation against PLAN.

[... existing content ...]

────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/AUDIT_CODE_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.

## BUG CLASSIFICATION
### CRITICAL
- Security vulnerabilities
[... rest of classification ...]
```

---

### 5. SECURITY_AUDIT PHASE
**Checklist:** `./aecf/checklists/SECURITY_AUDIT_CHECKLIST.md`

Add before "SECURITY VALIDATION" section:

```
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/SECURITY_AUDIT_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

---

### 6. TEST_STRATEGY PHASE
**Checklist:** `./aecf/checklists/TEST_STRATEGY_CHECKLIST.md`

Add before "OUTPUT FORMAT" section:

```
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/TEST_STRATEGY_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

---

### 7. TEST_IMPLEMENTATION PHASE
**Checklist:** `./aecf/checklists/TEST_IMPLEMENTATION_CHECKLIST.md`

Add before "CONSTRAINTS" section:

```
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/TEST_IMPLEMENTATION_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

---

### 8. AUDIT_TESTS PHASE
**Checklist:** `./aecf/checklists/AUDIT_TESTS_CHECKLIST.md`

Add before "VERDICT LOGIC" section:

```
────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/AUDIT_TESTS_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.
```

---

## COMPLIANCE REPORT FORMAT

At the end of each phase output, agents must include:

```markdown
## AECF_COMPLIANCE_REPORT

### Checklist: <PHASE>_CHECKLIST.md

#### Scope Validation
- [x] Scope matches PLAN
- [x] No scope expansion
- [x] No implicit redesign

#### Security Controls
- [x] No sensitive data exposure
- [x] Access control validated
- [x] Enumeration mitigated
- [x] Logging covers security events

[... all sections ...]

### VERDICT
All checklist items: PASS
Phase result: GO / NO-GO
```

---

## INTEGRATION RULES

1. **DO NOT** remove existing prompt logic
2. **DO NOT** modify verdict classification rules
3. **ONLY** add the enforcement block
4. Enforcement block position: **before** verdict/output sections
5. Checklist validation is **mandatory** — cannot be skipped
6. If any checklist item fails → immediate NO-GO
7. All checklist items must be tracked in AECF_COMPLIANCE_REPORT

---

## VALIDATION

After integration, verify:

- [ ] Enforcement block added to all 8 phase prompts
- [ ] Correct checklist file referenced per phase
- [ ] Enforcement block positioned correctly
- [ ] Existing logic preserved
- [ ] AECF_COMPLIANCE_REPORT template included

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
