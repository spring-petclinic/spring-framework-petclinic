# AECF CHECKLIST SYSTEM — INDEX

## DIRECTORY STRUCTURE

```
./aecf/checklists/
├── PLAN_CHECKLIST.md
├── AUDIT_PLAN_CHECKLIST.md
├── IMPLEMENT_CHECKLIST.md
├── AUDIT_CODE_CHECKLIST.md
├── SECURITY_AUDIT_CHECKLIST.md
├── TEST_STRATEGY_CHECKLIST.md
├── TEST_IMPLEMENTATION_CHECKLIST.md
├── AUDIT_TESTS_CHECKLIST.md
├── ENFORCEMENT_INTEGRATION_GUIDE.md
└── README.md (this file)
```

## CHECKLIST FILES

| Phase | Checklist File | Specialized Section |
|-------|---------------|---------------------|
| PLAN | `PLAN_CHECKLIST.md` | Plan Clarity |
| AUDIT_PLAN | `AUDIT_PLAN_CHECKLIST.md` | Audit Integrity |
| IMPLEMENT | `IMPLEMENT_CHECKLIST.md` | Implementation Integrity |
| AUDIT_CODE | `AUDIT_CODE_CHECKLIST.md` | Code Audit Integrity |
| SECURITY_AUDIT | `SECURITY_AUDIT_CHECKLIST.md` | OWASP Coverage |
| TEST_STRATEGY | `TEST_STRATEGY_CHECKLIST.md` | Testing Coverage Design |
| TEST_IMPLEMENTATION | `TEST_IMPLEMENTATION_CHECKLIST.md` | Test Implementation Integrity |
| AUDIT_TESTS | `AUDIT_TESTS_CHECKLIST.md` | Test Audit Integrity |

## COMMON CHECKLIST SECTIONS (ALL PHASES)

1. Scope Validation
2. Security Controls
3. Resource Management
4. Logging & Observability
5. Compliance with Previous Phase
6. Production Readiness
7. Decision Integrity
8. [Phase-Specific Section]

## USAGE

### For Prompt Engineers
1. Read `ENFORCEMENT_INTEGRATION_GUIDE.md`
2. Add enforcement block to existing phase prompts
3. Do not modify existing logic — only add enforcement layer

### For AECF Agents
1. Load appropriate checklist before verdict
2. Validate ALL items
3. Report compliance in `AECF_COMPLIANCE_REPORT`
4. If any item fails → NO-GO

### For Auditors
1. Verify checklist enforcement in agent outputs
2. Check `AECF_COMPLIANCE_REPORT` presence
3. Validate NO-GO issued when items fail

## ENFORCEMENT RULE

```
If ANY checklist item = FALSE → automatic NO-GO
```

No exceptions.
No explanations.
Only compliance.

## NEXT STEPS

1. Integrate enforcement blocks into existing phase prompts
2. Update agent templates to include `AECF_COMPLIANCE_REPORT`
3. Train agents on checklist validation
4. Audit existing workflows for compliance

## VALIDATION STATUS

- [x] Directory created
- [x] 8 checklist files created
- [x] Phase-specific sections added
- [x] Enforcement guide created
- [x] Index created
- [x] Enforcement blocks integrated into AECF prompts (8/8)
- [ ] Enforcement blocks integrated into AECF_AGENTS prompts (pending)
- [ ] Agent training completed
- [ ] Compliance audits passed

## INTEGRATED PROMPTS (AECF SYSTEM)

**Location:** `aecf_prompts/prompts/`

1. [00_PLAN.md](aecf_prompts/prompts/00_PLAN.md) → PLAN_CHECKLIST.md
2. [02_AUDIT_PLAN.md](aecf_prompts/prompts/02_AUDIT_PLAN.md) → AUDIT_PLAN_CHECKLIST.md
3. [04_IMPLEMENT.md](aecf_prompts/prompts/04_IMPLEMENT.md) → IMPLEMENT_CHECKLIST.md
4. [05_AUDIT_CODE.md](aecf_prompts/prompts/05_AUDIT_CODE.md) → AUDIT_CODE_CHECKLIST.md
5. [17_SECURITY_AUDIT.md](aecf_prompts/prompts/17_SECURITY_AUDIT.md) → SECURITY_AUDIT_CHECKLIST.md
6. [08_TEST_STRATEGY.md](aecf_prompts/prompts/08_TEST_STRATEGY.md) → TEST_STRATEGY_CHECKLIST.md
7. [09_TEST_IMPLEMENTATION.md](aecf_prompts/prompts/09_TEST_IMPLEMENTATION.md) → TEST_IMPLEMENTATION_CHECKLIST.md
8. [10_AUDIT_TESTS.md](aecf_prompts/prompts/10_AUDIT_TESTS.md) → AUDIT_TESTS_CHECKLIST.md

**Status:** ✅ COMPLETE (8/8)

**Next Phase:** AECF_AGENTS system integration (`aecf_prompts_agents/prompts/`)

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
