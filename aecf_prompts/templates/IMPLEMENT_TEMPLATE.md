# AECF — IMPLEMENT: {{TOPIC}}

## METADATA

| Field | Value |
| --- | --- |
| Skill | {{skill}} |
| Phase | IMPLEMENT |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |
| Plan source | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_01_PLAN.md |
| Test strategy | <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_04_TEST_STRATEGY.md |
| Refinement Iteration | {{N or omit if first delivery approved}} |
| Selected Option | {{chosen option or N/A if only one}} |

## 1. Implementation Summary

<!-- Brief summary of what was implemented -->

## 1A. Implementation Options

<!-- MANDATORY when the PLAN allows >= 2 concrete implementation strategies. -->
<!-- If the PLAN fixes a single strategy, justify briefly and omit options. -->
<!-- Mark the recommended option with [RECOMMENDED]. -->

### Option A: {{name}}
- **Strategy:**
- **Pros:**
- **Cons:**

### Option B: {{name}}
- **Strategy:**
- **Pros:**
- **Cons:**

**Recommendation:** Option {{X}} — <!-- brief justification -->

## 2. Files Changed

| File | Action | Description |
| --- | --- | --- |
| | Created / Modified / Deleted | |

## 3. Implementation Steps

### Step 1: {{description}}

```text
<!-- Implemented code -->
```

### Step 2: {{description}}

```text
<!-- Implemented code -->
```

## 4. Security Controls Applied

| Control | Implementation |
| --- | --- |
| Input validation | |
| Access control | |
| Data protection | |
| Logging | |

## 4A. User Validation Checkpoint

<!-- STOP POINT if options were presented in 1A. If no options, state "Single implementation — no selection required". -->

**Applied option:** {{X}} — {{option name or "single"}}

| Action | Instruction |
| --- | --- |
| **APPROVE** | Implementation is ready → proceeds to AUDIT_CODE |
| **SELECT OPTION `<N>`** | Choose another option from section 1A → implementation is regenerated |
| **REFINE APPROACH** | Provide feedback → implementation is regenerated within approved PLAN |
| **BLOCK** | State reason → implementation closes with NO-GO |

> **Respond with the desired action.** If you choose REFINE APPROACH, include your feedback below.

## 5. Tests Implemented

| Test ID | Description | Type | Status |
| --- | --- | --- | --- |
| T01 | | Unit | ✅ Pass / ❌ Fail |

## 6. Test Execution Evidence

```text
<!-- Paste test runner output here -->
```

## 7. Deviation Log

| # | Deviation from PLAN | Justification |
| --- | --- | --- |
| | None / Describe | |

## AECF_COMPLIANCE_REPORT

- [ ] Code produces functional output
- [ ] All PLAN steps implemented
- [ ] Tests implemented and executed
- [ ] No unplanned features
- [ ] No unauthorized decisions

