# HOTFIX CHECKLIST

**Purpose**: Fast emergency validation before production deployment  
**Usage**: Binary validation - all items must PASS  
**AECF Compliance**: HOTFIX Flow  

---

## Pre-Deployment Validation

Complete this checklist before deploying any HOTFIX to production.

**Incident ID**: `_______________`  
**Date**: `_______________`  
**Validator**: `_______________`

---

## SECTION 1: Incident Qualification

This section validates that HOTFIX flow is appropriate.

- [ ] **PASS** / [ ] **FAIL** — Incident severity is confirmed P1 or P2
- [ ] **PASS** / [ ] **FAIL** — Production users are actively affected
- [ ] **PASS** / [ ] **FAIL** — Normal AECF flow timeframe is insufficient (> 4 hours unacceptable)
- [ ] **PASS** / [ ] **FAIL** — Business/security impact justifies emergency process
- [ ] **PASS** / [ ] **FAIL** — Incident documented in HOTFIX_TEMPLATE.md

**Section Result**: [ ] **ALL PASS** / [ ] **ANY FAIL**

**If ANY FAIL**: Do not proceed with HOTFIX flow. Use standard AECF PLAN → AUDIT → IMPLEMENT.

---

## SECTION 2: Risk Containment

This section validates that emergency controls are in place.

- [ ] **PASS** / [ ] **FAIL** — Rollback plan is documented and tested
- [ ] **PASS** / [ ] **FAIL** — Rollback can be executed in < 15 minutes
- [ ] **PASS** / [ ] **FAIL** — Monitoring plan is active with defined metrics
- [ ] **PASS** / [ ] **FAIL** — On-call engineer is notified and available
- [ ] **PASS** / [ ] **FAIL** — Change scope is minimal (no refactoring, no feature additions)
- [ ] **PASS** / [ ] **FAIL** — Backup engineer available for immediate rollback execution

**Section Result**: [ ] **ALL PASS** / [ ] **ANY FAIL**

**If ANY FAIL**: Address deficiency before proceeding.

---

## SECTION 3: Technical Validation

This section validates the fix quality and safety.

### 3.1 Functional Correctness
- [ ] **PASS** / [ ] **FAIL** — Fix directly addresses identified root cause
- [ ] **PASS** / [ ] **FAIL** — Critical functionality validated and working
- [ ] **PASS** / [ ] **FAIL** — Bug can no longer be reproduced after fix

### 3.2 Security Controls
- [ ] **PASS** / [ ] **FAIL** — No new vulnerabilities introduced (verified)
- [ ] **PASS** / [ ] **FAIL** — No sensitive data exposed by changes
- [ ] **PASS** / [ ] **FAIL** — No authentication/authorization bypass introduced
- [ ] **PASS** / [ ] **FAIL** — No privilege escalation risks created
- [ ] **PASS** / [ ] **FAIL** — Dependencies (if changed) are secure and approved

### 3.3 Side Effects
- [ ] **PASS** / [ ] **FAIL** — Core functionality not broken by changes
- [ ] **PASS** / [ ] **FAIL** — No data integrity issues introduced
- [ ] **PASS** / [ ] **FAIL** — Performance degradation acceptable or none
- [ ] **PASS** / [ ] **FAIL** — No breaking changes to APIs or interfaces

**Section Result**: [ ] **ALL PASS** / [ ] **ANY FAIL**

**If ANY FAIL in Security**: Automatic NO-GO. Fix must be reworked.  
**If ANY FAIL in Functional/Side Effects**: Review and justify or rework.

---

## SECTION 4: Testing

This section validates that critical tests have been executed.

- [ ] **PASS** / [ ] **FAIL** — Critical test suite executed (minimum 3 tests)
- [ ] **PASS** / [ ] **FAIL** — All critical tests passed
- [ ] **PASS** / [ ] **FAIL** — Smoke test passed (basic functionality works)
- [ ] **PASS** / [ ] **FAIL** — Regression test passed (existing features still work)
- [ ] **PASS** / [ ] **FAIL** — Manual validation completed successfully
- [ ] **PASS** / [ ] **FAIL** — Staging environment validation completed (if staging exists)

**Section Result**: [ ] **ALL PASS** / [ ] **ANY FAIL**

**If ANY FAIL**: Do not deploy until tests pass.

---

## SECTION 5: Governance

This section validates AECF compliance and traceability.

- [ ] **PASS** / [ ] **FAIL** — HOTFIX_TEMPLATE.md completed with all required sections
- [ ] **PASS** / [ ] **FAIL** — Root cause documented (confirmed or hypothesis)
- [ ] **PASS** / [ ] **FAIL** — Emergency audit completed with GO verdict
- [ ] **PASS** / [ ] **FAIL** — Code changes have inline documentation referencing incident
- [ ] **PASS** / [ ] **FAIL** — Commit properly tagged (`hotfix-YYYYMMDD-description`)
- [ ] **PASS** / [ ] **FAIL** — Post-mortem scheduled (next business day)
- [ ] **PASS** / [ ] **FAIL** — Follow-up ticket created (if permanent fix needed)

**Section Result**: [ ] **ALL PASS** / [ ] **ANY FAIL**

**If ANY FAIL**: Complete governance requirements before deployment.

---

## FINAL VALIDATION

**All Sections Status**:
- Section 1 (Incident Qualification): [ ] **ALL PASS** / [ ] **ANY FAIL**
- Section 2 (Risk Containment): [ ] **ALL PASS** / [ ] **ANY FAIL**
- Section 3 (Technical Validation): [ ] **ALL PASS** / [ ] **ANY FAIL**
- Section 4 (Testing): [ ] **ALL PASS** / [ ] **ANY FAIL**
- Section 5 (Governance): [ ] **ALL PASS** / [ ] **ANY FAIL**

---

## DEPLOYMENT DECISION

### HOTFIX VALIDATED: [ ] **YES** / [ ] **NO**

**Decision Rule**: ALL sections must show "ALL PASS" for YES.

**If NO**: 
- List failures: `_________________________________`
- Required actions: `_________________________________`
- Re-validation required: [ ] **YES**

**If YES**:
- Deployment approved by: `_________________` (Name/Role)
- Deployment window: `_________________` (Timestamp)
- Monitoring lead: `_________________` (Name)

---

## POST-DEPLOYMENT CHECKLIST

Execute immediately after deployment and during monitoring window.

- [ ] **PASS** / [ ] **FAIL** — Deployment completed successfully
- [ ] **PASS** / [ ] **FAIL** — Monitoring active and showing expected behavior
- [ ] **PASS** / [ ] **FAIL** — Error rates normal or improved
- [ ] **PASS** / [ ] **FAIL** — Response times normal or improved
- [ ] **PASS** / [ ] **FAIL** — No new critical errors in logs
- [ ] **PASS** / [ ] **FAIL** — User reports confirm issue resolution
- [ ] **PASS** / [ ] **FAIL** — System stable after monitoring window (30-60 min)

**Post-Deployment Status**: [ ] **STABLE** / [ ] **ROLLBACK REQUIRED**

**If ROLLBACK REQUIRED**:
- Rollback executed at: `_________________`
- Rollback completed at: `_________________`
- System restored: [ ] **YES** / [ ] **NO**

---

## CHECKLIST METADATA

**Checklist Version**: 1.0  
**AECF Compliance**: HOTFIX Flow  
**Related Documents**:
- Template: `templates/HOTFIX_TEMPLATE.md`
- Scoring: `scoring/HOTFIX_SCORING_RULES.md`
- Prompt: `aecf_prompts/prompts/00_HOTFIX.md`

**Completed By**: `_________________` (Name)  
**Completion Date**: `_________________` (YYYY-MM-DD)  
**Signature**: `_________________` (if required by organization)

---

## AUDIT TRAIL

| Action | Timestamp | Engineer | Result |
|--------|-----------|----------|--------|
| Checklist Started | | | |
| Section 1 Validated | | | PASS / FAIL |
| Section 2 Validated | | | PASS / FAIL |
| Section 3 Validated | | | PASS / FAIL |
| Section 4 Validated | | | PASS / FAIL |
| Section 5 Validated | | | PASS / FAIL |
| Final Decision | | | GO / NO-GO |
| Deployment Started | | | |
| Deployment Completed | | | SUCCESS / FAIL |
| Monitoring Completed | | | STABLE / ROLLBACK |

---

**END OF CHECKLIST**

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
