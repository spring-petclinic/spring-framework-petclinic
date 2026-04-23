# AECF — PLAN: {{TOPIC}}

## METADATA

| Field | Value |
| --- | --- |
| Skill | {{skill}} |
| Phase | PLAN |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |
| Refinement Iteration | {{N or omit if first delivery approved}} |
| Selected Option | {{chosen option or N/A if only one}} |

## 1. Scope

### In Scope

-

### Out of Scope

-

## 1B. Design Options

<!-- MANDATORY when >= 2 viable approaches exist. If only one, justify briefly. -->
<!-- Mark the recommended option with [RECOMMENDED]. -->

### Option A: {{name}}
- **Approach:**
- **Pros:**
- **Cons:**

### Option B: {{name}}
- **Approach:**
- **Pros:**
- **Cons:**

**Recommendation:** Option {{X}} — <!-- brief justification -->

## 2. Functional Requirements

1.
2.
3.

## 3. Non-Functional Requirements

| Category | Requirement |
| --- | --- |
| Performance | |
| Security | |
| Maintainability | |
| Scalability | |

## 4. Assumptions

1.
2.

## 5. Impact on Existing Architecture

| Component | Change | Risk |
| --- | --- | --- |
| | | |

## 6. Risks

| ID | Type | Description | Mitigation | Probability | Impact |
| --- | --- | --- | --- | --- | --- |
| R1 | Technical | | | | |
| R2 | Security | | | | |
| R3 | Functional | | | | |

## 7. Design Decisions

| Decision | Justification | Rejected Alternatives |
| --- | --- | --- |
| | | |

## 8. Acceptance Criteria

- [ ]
- [ ]
- [ ]

## 9. Output Budget Assessment

| Aspect | Value |
| --- | --- |
| Estimated lines | |
| Fits in one response? | Yes / No |
| If not, what is deferred | |

## 9A. User Validation Checkpoint

<!-- MANDATORY STOP POINT. User must choose an action before proceeding. -->

**Recommended option:** {{X}} — {{option name}}

| Action | Instruction |
| --- | --- |
| **APPROVE** | Plan is ready → proceeds to AUDIT_PLAN |
| **SELECT OPTION `<N>`** | Choose another option from section 1B → plan is regenerated |
| **REFINE PROMPT** | Provide feedback or improved prompt → plan is regenerated |
| **BLOCK** | State reason → plan closes with NO-GO |

> **Respond with the desired action.** If you choose REFINE PROMPT, include your feedback below.

## 10. Gate Condition

**Verdict**: GO / NO-GO

**Justification**:

## AECF_COMPLIANCE_REPORT

- [ ] No code generated
- [ ] Scope defined
- [ ] Risks identified
- [ ] Decisions justified
