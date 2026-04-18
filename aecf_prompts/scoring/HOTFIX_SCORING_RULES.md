# HOTFIX SCORING MODEL

**Document Type**: Emergency Compliance Validation Rules  
**AECF Compliance**: HOTFIX Flow  
**Version**: 1.0  

---

## Purpose

This document defines the compliance validation model for HOTFIX deployments within the AECF framework.

Unlike standard AECF flows that use weighted scoring matrices, **HOTFIX compliance is binary** to enable fast, safe emergency deployments while maintaining traceability and governance.

---

## Scoring Philosophy

### Emergency Context

HOTFIX flow is designed for critical incidents where:
- Production is significantly impaired
- Users are actively affected
- Time-to-resolution is measured in minutes or hours
- Standard AECF flow timeframes are insufficient

### Priority Hierarchy

In emergency situations, the priority order is:

1. **Stability** — Do not make the situation worse
2. **Traceability** — Maintain full audit trail
3. **Speed** — Resolve quickly but safely
4. **Optimization** — Deferred to permanent fix phase

### Binary Approach Rationale

Complex scoring in emergencies introduces:
- Decision paralysis
- Unnecessary delays
- Cognitive overhead during high-stress incidents

Binary validation (YES/NO, PASS/FAIL) provides:
- Clear go/no-go decisions
- Faster validation
- Reduced ambiguity
- Forced focus on critical requirements

---

## HOTFIX Compliance Requirements

For a HOTFIX to be approved for production deployment, ALL of the following requirements must be satisfied:

### Requirement 1: Rollback Plan Present

**Status**: [ ] **MET** / [ ] **NOT MET**

**Criteria**:
- Documented rollback procedure exists
- Rollback can be executed in < 15 minutes
- Rollback method is tested or verified
- Responsible engineer understands rollback process

**Validation Method**:
- Review HOTFIX_TEMPLATE.md Section 3 (Rollback Plan)
- Confirm all rollback steps are actionable
- Verify rollback method is appropriate for change type

**Failure Impact**: **CRITICAL** — Cannot deploy without rollback capability.

---

### Requirement 2: Emergency Audit Result = GO

**Status**: [ ] **MET** / [ ] **NOT MET**

**Criteria**:
- Emergency audit completed
- Functional validation passed
- Security validation passed (CRITICAL)
- Side-effect validation passed
- Final verdict is GO

**Validation Method**:
- Review HOTFIX_TEMPLATE.md Section 4 (Emergency Audit Result)
- Confirm all audit subsections show PASS
- Verify any CRITICAL security finding results in automatic NO-GO

**Failure Impact**: **CRITICAL** — Emergency audit failure blocks deployment.

---

### Requirement 3: Critical Tests Passed

**Status**: [ ] **MET** / [ ] **NOT MET**

**Criteria**:
- Minimum 3 critical tests identified and executed
- All critical tests passed
- Smoke test passed
- Core functionality regression test passed
- Bug reproduction test shows issue resolved

**Validation Method**:
- Review HOTFIX_TEMPLATE.md Section 6.1 (Critical Tests)
- Verify test execution logs exist
- Confirm no test failures in critical test suite

**Failure Impact**: **HIGH** — Cannot verify fix works correctly without tests.

---

### Requirement 4: Monitoring Active

**Status**: [ ] **MET** / [ ] **NOT MET**

**Criteria**:
- Monitoring plan defined with specific metrics
- Monitoring dashboards prepared or available
- On-call engineer notified and ready
- Monitoring window duration defined (typically 30-60 minutes)
- Alert thresholds reviewed

**Validation Method**:
- Review HOTFIX_TEMPLATE.md Section 6.4 (Monitoring Preparation)
- Confirm metrics are defined
- Verify on-call engineer acknowledgment

**Failure Impact**: **HIGH** — Cannot detect deployment failures without monitoring.

---

### Requirement 5: Post-Mortem Scheduled

**Status**: [ ] **MET** / [ ] **NOT MET**

**Criteria**:
- Post-mortem meeting scheduled (typically next business day)
- Post-mortem facilitator assigned
- Follow-up action items identified (if permanent fix needed)
- RCA requirement determined

**Validation Method**:
- Review HOTFIX_TEMPLATE.md Section 8 (Post-Mortem Plan)
- Confirm calendar invite exists or equivalent commitment
- Verify permanent fix tracking if HOTFIX is temporary

**Failure Impact**: **MEDIUM** — Required for continuous improvement but does not block emergency deployment.

---

## Compliance Decision Matrix

### Decision Logic

```
IF Requirement 1 = MET
AND Requirement 2 = MET
AND Requirement 3 = MET
AND Requirement 4 = MET
AND Requirement 5 = MET
THEN HOTFIX_COMPLIANCE = APPROVED
ELSE HOTFIX_COMPLIANCE = FAILED
```

### Automatic NO-GO Conditions

Certain conditions trigger automatic NO-GO regardless of other requirements:

1. **Critical Security Finding** — Any security vulnerability introduced by the fix
2. **No Rollback Plan** — Cannot deploy without ability to revert
3. **Tests Not Executed** — Fix not validated
4. **Severity Misclassification** — Not a true P1/P2 incident

---

## Compliance Validation Process

### Step 1: Complete HOTFIX_TEMPLATE.md

Ensure all required sections are filled:
- Incident Identification
- Root Cause
- Fix Plan with Rollback
- Emergency Audit
- Testing Results
- Post-Mortem Plan

### Step 2: Execute HOTFIX_CHECKLIST.md

Complete the binary checklist:
- All sections must show "ALL PASS"
- Any "ANY FAIL" blocks deployment
- Address failures before proceeding

### Step 3: Apply Scoring Rules

Evaluate each of the 5 requirements:
- Mark each as MET or NOT MET
- If ALL MET → APPROVED
- If ANY NOT MET → FAILED

### Step 4: Document Decision

Record compliance decision in HOTFIX_TEMPLATE.md:
- HOTFIX_COMPLIANCE: APPROVED / FAILED
- List any NOT MET requirements
- Document justification if deployment proceeds with conditions

---

## Scoring Report Format

Use this format in all HOTFIX documentation:

```
## HOTFIX_COMPLIANCE_REPORT

**Evaluation Date**: [YYYY-MM-DD HH:MM UTC]
**Evaluator**: [Name/Role]

**Requirements Status**:
1. Rollback Plan Present: [MET / NOT MET]
2. Emergency Audit = GO: [MET / NOT MET]
3. Critical Tests Passed: [MET / NOT MET]
4. Monitoring Active: [MET / NOT MET]
5. Post-Mortem Scheduled: [MET / NOT MET]

**Automatic NO-GO Conditions**:
- Critical Security Finding: [YES / NO]
- No Rollback Plan: [YES / NO]
- Tests Not Executed: [YES / NO]
- Severity Misclassification: [YES / NO]

**Final Compliance Decision**: [APPROVED / FAILED]

**Deployment Authorization**: [GO / NO-GO]

**Conditions** (if any): [List any special conditions]

**Approver**: [Name/Role]
**Approval Timestamp**: [YYYY-MM-DD HH:MM UTC]
```

---

## Compliance Levels

### APPROVED (Compliant)

**Status**: ✅ All requirements MET, ready for deployment

**Characteristics**:
- All 5 requirements satisfied
- No automatic NO-GO conditions present
- HOTFIX_TEMPLATE complete
- HOTFIX_CHECKLIST shows all PASS
- Deployment can proceed

**Next Steps**:
- Proceed to deployment
- Activate monitoring
- Execute post-deployment checklist

---

### FAILED (Non-Compliant)

**Status**: ❌ One or more requirements NOT MET, deployment blocked

**Characteristics**:
- At least one requirement not satisfied
- OR automatic NO-GO condition present
- Deployment must not proceed

**Next Steps**:
- Address NOT MET requirements
- Rework fix if necessary
- Re-evaluate after corrections
- Consider escalation to peer review

**Escalation Criteria**:
- If 2+ re-evaluations fail
- If automatic NO-GO cannot be resolved
- If incident severity increases during fix attempt

---

## Conditional Deployment

In rare, extreme circumstances (e.g., data loss actively occurring, security breach in progress), deployment MAY proceed with documented risk acceptance.

### Conditions for Conditional Deployment

- [ ] Company/Team Executive approval obtained (CTO/VP Engineering or equivalent)
- [ ] Risk explicitly accepted in writing
- [ ] NOT MET requirements documented with mitigation plan
- [ ] Monitoring increased to continuous observation
- [ ] Rollback engineer on standby with rollback plan ready for immediate execution

### Documentation Requirements

Conditional deployments must include:

```
## CONDITIONAL DEPLOYMENT AUTHORIZATION

**Risk Acceptance**: [Executive Name/Title]
**Timestamp**: [YYYY-MM-DD HH:MM UTC]

**NOT MET Requirements**:
1. [Requirement] - Mitigation: [how risk is mitigated]

**Justification**: [why conditional deployment is necessary]

**Enhanced Monitoring**: [describe increased monitoring]

**Rollback Standby**: [engineer name on immediate rollback duty]

**Business Impact if NOT Deployed**: [describe consequences of delay]
```

**Note**: Conditional deployments are EXCEPTIONAL and should be rare (< 1% of all HOTFIXes).

---

## Quality Metrics

Track HOTFIX quality over time using these metrics:

### Process Metrics
- **Time to Resolution** (incident detection → deployed fix)
- **HOTFIX Compliance Rate** (% of HOTFIXes that achieve APPROVED status)
- **Rollback Rate** (% of HOTFIXes requiring rollback)
- **Permanent Fix Rate** (% of HOTFIXes requiring follow-up permanent fix)

### Target Thresholds
- Compliance Rate: > 95%
- Rollback Rate: < 5%
- Permanent Fix Rate: < 30% (prefer permanent fixes in HOTFIX flow)

### Red Flags
- Compliance Rate < 80%: Process gaps
- Rollback Rate > 10%: Quality issues
- Permanent Fix Rate > 50%: Band-aid culture

---

## Continuous Improvement

### Post-Mortem Analysis

During post-mortem, evaluate:
1. Was HOTFIX flow appropriate for this incident?
2. Were compliance requirements sufficient?
3. Did binary validation provide clear direction?
4. Were there delays due to compliance requirements?

### Feedback Loop

Update this document based on:
- Recurring compliance failures
- New risk patterns
- Technology changes
- Regulatory requirements
- Team feedback

### Version Control

- Major changes: Version increment (1.0 → 2.0)
- Minor updates: Patch increment (1.0 → 1.1)
- All changes documented in version history

---

## Related Documents

**AECF Framework**:
- HOTFIX Prompt: `aecf_prompts/prompts/00_HOTFIX.md`
- HOTFIX Template: `templates/HOTFIX_TEMPLATE.md`
- HOTFIX Checklist: `checklists/HOTFIX_CHECKLIST.md`

**Standard AECF Flows**:
- For non-emergency work: Use standard PLAN → AUDIT → IMPLEMENT flow
- For debugging: Use 00_DEBUG.md flow
- For architecture: Use 00_ARCH.md flow

---

## Summary

**HOTFIX Scoring Philosophy**:
> Hotfix flow prioritizes stability and traceability over optimization. Binary validation ensures fast, clear decisions during high-pressure incidents while maintaining governance and enabling continuous improvement through systematic post-mortem analysis.

**Key Principle**:
> In emergencies, simple binary controls prevent worse outcomes better than complex scoring systems that delay action.

**Compliance Mission**:
> Enable rapid response while preserving audit trails, learning opportunities, and team accountability.

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-12  
**Document Owner**: AECF Governance  
**Review Cycle**: Quarterly or after major incidents
