# AECF - TEST EXECUTION REPORT

> **@METADATA** - Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 11_TEST_EXECUTION_REPORT |

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This prompt operates under the following mandatory contexts:

- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- <workspace_root>/AECF_PROJECT_CONTEXT.md (if present anywhere in the active workspace)

Governance:
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

HARD PRECONDITION: Load and enforce context with hierarchy:
1. SYSTEM_CONTEXT: aecf_prompts/AECF_SYSTEM_CONTEXT.md
2. PROJECT_CONTEXT (workspace): <workspace_root>/AECF_PROJECT_CONTEXT.md (if exists, overrides defaults)

TOPIC: Maintain {{TOPIC}} from previous phase. All outputs in: documentation/{{TOPIC}}/

------------------------
TEMPLATE ENFORCEMENT (MANDATORY)
------------------------

You MUST load and strictly follow:

./aecf/templates/TEST_EXECUTION_REPORT_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure of TEST_EXECUTION_REPORT_TEMPLATE.md.
- Only execute approved tests.
- Record the exact commands used.
- Coverage, duration, failures, skips, and blockers must be explicitly documented.
- Missing sections invalidate TEST_EXECUTION_REPORT.

------------------------
CHECKLIST ENFORCEMENT (MANDATORY)
------------------------

You MUST load:

./aecf/checklists/TEST_EXECUTION_REPORT_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any critical execution evidence is missing -> automatic NO-GO.

Failure to enforce checklist invalidates the phase.

------------------------
SCORING ENFORCEMENT (MANDATORY)
------------------------

You MUST:

1. Score each checklist item (0,1,2).
2. Apply category weights.
3. Compute normalized score.
4. Declare maturity level.
5. Apply automatic verdict rules.

If scoring is not included -> Phase invalid.

Include in AECF_COMPLIANCE_REPORT:

## AECF_SCORE_REPORT

- Raw Score:
- Normalized Score:
- Maturity Level:
- Automatic Verdict:
- Critical Findings Present: YES / NO

---

## OBJECTIVE

Execute the approved tests and generate an extensive, traceable, and actionable report with evidence of coverage, failures, residual gaps, and category-level test results.

---

## STRICT RULES

- DO NOT modify production code during this phase.
- DO NOT modify tests during this phase.
- DO NOT hide failures: every error, skip, or blocker must be documented.
- If test execution is not possible, document the blocker with concrete evidence.
- If a command fails because of environment, dependency, or configuration, stop and reflect the real state.

---

## MINIMUM REQUIRED EVIDENCE

1. Commands executed
2. Working directory and environment assumptions
3. Passed / Failed / Skipped / Errors summary
4. Duration and coverage if available
5. Evidence by category:
   - happy path
   - edge cases
   - error forcing
   - security / permissions
   - SQL injection or input injection
   - performance / timeout / pagination when applicable
   - logging / observability
   - resource handling
6. Findings and next actions

---

## VERDICT LOGIC

### GO
- Commands executed successfully
- No failing tests in approved scope
- Coverage or equivalent evidence documented
- No critical blockers

### CONDITIONAL GO
- Some warnings or skips exist
- Partial evidence available
- Non-critical blockers remain documented

### NO-GO
- Execution blocked
- Critical failing tests remain
- Commands cannot run and no evidence is available
- Coverage evidence is missing for required areas

---

## OUTPUT GENERATION (MANDATORY)

Generate document:
documentation/{{TOPIC}}/AECF_<NN>_TEST_EXECUTION_REPORT.md

---

## AECF_COMPLIANCE_REPORT

Before finishing, include:

## AECF_COMPLIANCE_REPORT

- aecf_prompts/prompts/00_PLAN.md -> APLICADO
- aecf_prompts/prompts/02_AUDIT_PLAN.md -> APLICADO (GO)
- aecf_prompts/prompts/08_TEST_STRATEGY.md -> APLICADO
- aecf_prompts/prompts/09_TEST_IMPLEMENTATION.md -> APLICADO / NO APLICADO
- aecf_prompts/prompts/11_TEST_EXECUTION_REPORT.md -> APLICADO

Flow AECF: COMPLETO / PARCIAL
Commands executed: YES / NO
Coverage evidence present: YES / NO
Verdict: GO / CONDITIONAL GO / NO-GO

TEST_EXECUTION_REPORT COMPLETE

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
