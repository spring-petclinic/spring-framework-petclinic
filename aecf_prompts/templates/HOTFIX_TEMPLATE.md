# HOTFIX REPORT

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Hotfix Report |
> | Phase | 00_HOTFIX |
>
> **Extension fields (append after standard fields):**
> | Incident ID | {{INCIDENT_ID}} |
> | Severity | {{P1/P2}} |
> | AECF Compliance | HOTFIX Flow |

---

## 1. Incident Identification

**Incident ID**: `[Unique identifier - e.g., INC-2026-0001]`  
**Severity**: `[P1 / P2]`  
**Detection Time**: `[YYYY-MM-DD HH:MM UTC]`  
**Detection Source**: `[Monitoring / User Report / Security Scan / Other]`  
**Impact Scope**:
- **Users Affected**: `[Number or percentage]`
- **Systems Affected**: `[List of systems/services]`
- **Business Impact**: `[Revenue loss / Data integrity / Security / Availability]`
- **SLA Breach**: `[YES / NO - specify which SLA]`

**Current Status**: `[INVESTIGATING / FIX IN PROGRESS / DEPLOYED / RESOLVED]`

---

## 2. Immediate Root Cause (Preliminary)

**Root Cause Status**: `[CONFIRMED / HYPOTHESIS]`

**Root Cause Description**:
```
[Detailed description of what caused the incident]
```

**Affected Components**:
- Component: `[component name]`
  - File(s): `[file paths]`
  - Function/Module: `[specific code locations]`
  - Version: `[version information]`

**Evidence References**:
- Log files: `[paths or links]`
- Error messages: `[specific errors]`
- Monitoring data: `[links to dashboards]`
- Related tickets: `[ticket IDs]`

**Reproduction Steps** (if applicable):
1. `[Step 1]`
2. `[Step 2]`
3. `[Expected vs Actual result]`

---

## 3. Minimal Fix Plan

**Fix Type**: `[Code / Config / Infrastructure]`

**Change Scope**:
- **Repository**: `[repository name]`
- **Branch**: `[hotfix branch name]`
- **Files Affected**: 
  - `[file path 1]`
  - `[file path 2]`
  - `[...]`
- **Lines Affected**: `[approximate line count or ranges]`

**Description of Change**:
```
[Clear, concise description of what will be changed and why]
```

**Technical Implementation**:
```
[High-level technical approach - what logic/config/infra will be modified]
```

**Alternative Solutions Considered**:
1. **Alternative 1**: `[description]`
   - **Discarded Because**: `[reason]`
2. **Alternative 2**: `[description]`
   - **Discarded Because**: `[reason]`

**Risk Assessment**:
- **Risk Level**: `[LOW / MEDIUM / HIGH]`
- **Potential Side Effects**: 
  - `[Risk 1]`
  - `[Risk 2]`
- **Mitigation Strategy**: `[how risks will be minimized]`

**Rollback Plan** (MANDATORY):
- **Rollback Method**: `[Git revert / Config rollback / Infrastructure rollback]`
- **Rollback Steps**:
  1. `[Step 1]`
  2. `[Step 2]`
- **Rollback Time Estimate**: `[minutes]`
- **Rollback Validation**: `[how to verify rollback succeeded]`

---

## 4. Emergency Audit Result

**Audit Timestamp**: `[YYYY-MM-DD HH:MM UTC]`  
**Auditor**: `[Name/Role]`

### 4.1 Functional Validation
- [ ] Fix addresses the root cause
- [ ] Fix does not introduce new critical bugs
- [ ] Minimal scope maintained (no scope creep)

**Result**: `[PASS / FAIL]`  
**Notes**: `[any concerns or observations]`

### 4.2 Security Validation
- [ ] No new vulnerabilities introduced
- [ ] No sensitive data exposed
- [ ] No authentication/authorization bypass
- [ ] No privilege escalation risks
- [ ] Dependencies secure (if changed)

**Result**: `[PASS / FAIL]`  
**Critical Findings**: `[list any critical security issues found]`

### 4.3 Side-Effect Validation
- [ ] No critical functionality broken
- [ ] No data integrity issues introduced
- [ ] Performance impact acceptable
- [ ] No breaking API changes

**Result**: `[PASS / FAIL]`  
**Impact Assessment**: `[description of any impacts]`

### 4.4 Final Decision

**Emergency Audit Score**: `[X/100 - from HOTFIX_SCORING_RULES]`  
**Verdict**: `[GO / NO-GO]`  
**Decision Rationale**: `[brief explanation]`  
**Conditions** (if any): `[special deployment conditions]`

---

## 5. Implementation Summary

**Implementation Timestamp**: `[YYYY-MM-DD HH:MM UTC]`  
**Implemented By**: `[Engineer name]`  
**Pair Review By**: `[Reviewer name - recommended for hotfixes]`

**Code References**:
- **Commit Hash**: `[full commit SHA]`
- **Commit Message**: `[commit message used]`
- **Branch**: `[branch name]`
- **Pull Request**: `[PR number or link]`
- **Tag**: `[hotfix-YYYYMMDD-description]`

**Files Changed**:
```
[List of files with brief description of changes]
- path/to/file1.py: [what changed]
- path/to/file2.js: [what changed]
```

**Inline Documentation**:
- [ ] Comments added explaining hotfix
- [ ] TODO markers for permanent fix (if applicable)
- [ ] Reference to incident ID in code

---

## 6. Verification Checklist

### 6.1 Critical Tests Executed

**Test Execution Timestamp**: `[YYYY-MM-DD HH:MM UTC]`

- [ ] `[Test 1 - description]` - **Result**: `[PASS / FAIL]`
- [ ] `[Test 2 - description]` - **Result**: `[PASS / FAIL]`
- [ ] `[Test 3 - description]` - **Result**: `[PASS / FAIL]`
- [ ] `[Regression test - core functionality]` - **Result**: `[PASS / FAIL]`

**Test Coverage**: `[Minimal / Adequate for hotfix]`  
**Test Logs**: `[Link to test execution logs]`

### 6.2 Manual Validation

- [ ] Bug reproduction attempt → **Cannot reproduce** (bug fixed)
- [ ] Core functionality verification → **Working as expected**
- [ ] User acceptance (if possible) → **Confirmed / Pending**

**Validation Notes**: `[observations during manual testing]`

### 6.3 Staging Environment (if applicable)

- [ ] Deployed to staging successfully
- [ ] Smoke test passed in staging
- [ ] Logs reviewed - no critical errors
- [ ] Performance metrics normal

**Staging Results**: `[summary]`

### 6.4 Monitoring Preparation

- [ ] Monitoring dashboards prepared
- [ ] Alert thresholds reviewed
- [ ] Key metrics identified for post-deploy monitoring
- [ ] On-call engineer notified

**Metrics to Monitor**:
- `[Metric 1]`
- `[Metric 2]`
- `[Metric 3]`

---

## 7. Deployment Record

**Deployment Timestamp**: `[YYYY-MM-DD HH:MM UTC]`  
**Deployment Duration**: `[minutes]`  
**Deployment Method**: `[CI/CD / Manual / Script]`

**Responsible Engineer**: `[Name]`  
**Backup Engineer**: `[Name - for immediate rollback if needed]`  
**Deployment Approver**: `[Name/Role - if required by policy]`

**Deployment Steps**:
1. `[Step 1]`
2. `[Step 2]`
3. `[Verification step]`

**Deployment Status**: `[SUCCESS / PARTIAL / FAILED / ROLLED BACK]`

**Monitoring Window**: `[Duration - typically 30-60 minutes]`  
**Monitoring Lead**: `[Name]`

**Post-Deployment Metrics** (after monitoring window):
- **Error Rate**: `[value and trend]`
- **Response Time**: `[value and trend]`
- **User Impact**: `[resolved / reduced / unchanged]`
- **System Stability**: `[stable / unstable]`

---

## 8. Post-Mortem Plan

**Post-Mortem Required**: `[YES / NO]`  
**Post-Mortem Scheduled**: `[YYYY-MM-DD HH:MM]`  
**Post-Mortem Facilitator**: `[Name]`

**Full RCA Required**: `[YES / NO]`  
**RCA Document**: `[Link to AECF_XX_RCA.md when completed]`

**Permanent Fix Required**: `[YES / NO]`  
**Hotfix Classification**: `[TEMPORARY / PERMANENT]`

**Follow-Up Actions**:
- [ ] Issue created for permanent fix: `[Issue ID]`
- [ ] Issue created for monitoring improvements: `[Issue ID]`
- [ ] Issue created for documentation updates: `[Issue ID]`
- [ ] Issue created for additional testing: `[Issue ID]`

**Lessons Learned** (preliminary):
```
[Brief notes to be expanded in post-mortem]
```

**Action Items**:
1. `[Action 1]` - Owner: `[Name]` - Due: `[Date]`
2. `[Action 2]` - Owner: `[Name]` - Due: `[Date]`

---

## Timeline Summary

| Time | Event |
|------|-------|
| `[HH:MM]` | Incident detected |
| `[HH:MM]` | Team notified |
| `[HH:MM]` | Root cause identified |
| `[HH:MM]` | Fix plan approved |
| `[HH:MM]` | Implementation completed |
| `[HH:MM]` | Tests passed |
| `[HH:MM]` | Deployed to production |
| `[HH:MM]` | Incident resolved |

**Total Incident Duration**: `[HH:MM]`  
**Time to Fix (from detection to resolution)**: `[HH:MM]`

---

## AECF Compliance Statement

**AECF Flow Applied**: `HOTFIX (Emergency Flow)`  
**Compliance Level**: `[FULL / CONDITIONAL - explain if conditional]`  
**Documentation Complete**: `[YES / NO]`  
**Traceability Maintained**: `[YES / NO]`

**Related AECF Documents**:
- HOTFIX Prompt: `aecf_prompts/prompts/00_HOTFIX.md`
- Checklist Used: `checklists/HOTFIX_CHECKLIST.md`
- Scoring Applied: `scoring/HOTFIX_SCORING_RULES.md`

---

**Document Status**: `[DRAFT / FINAL]`  
**Last Updated**: `[YYYY-MM-DD HH:MM UTC]`  
**Document Owner**: `[Name/Role]`
