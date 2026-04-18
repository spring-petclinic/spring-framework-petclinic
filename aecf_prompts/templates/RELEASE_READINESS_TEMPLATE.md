# AECF — RELEASE READINESS TEMPLATE

> AI Engineering Compliance Framework — Pre-Release Governance Validation Report

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Release Readiness Report |
> | Phase | RELEASE_READINESS |
> | Release Version | {{VERSION}} |

---

## 1. Release Overview

| Field | Value |
|-------|-------|
| Target Version | |
| Release Type | ☐ Major  ☐ Minor  ☐ Patch  ☐ Hotfix |
| Deployment Target | ☐ Staging  ☐ Production |
| Features Included | |
| Fixes Included | |

---

## 2. AECF Phase Completion Matrix

### Phase Verification (Weight: 3)

| Phase | Required | Document Reference | Status |
|-------|----------|-------------------|--------|
| PLAN | ✅ | `AECF_<NN>_PLAN.md` | ☐ Present ☐ Missing |
| AUDIT_PLAN | ✅ | `AECF_<NN>_AUDIT_PLAN.md` | ☐ GO ☐ NO-GO ☐ Missing |
| IMPLEMENT | ✅ | `AECF_<NN>_IMPLEMENTATION.md` | ☐ Present ☐ Missing |
| AUDIT_CODE | ✅ | `AECF_<NN>_AUDIT_CODE.md` | ☐ GO ☐ NO-GO ☐ Missing |
| FIX_CODE (if NO-GO) | conditional | `AECF_<NN>_FIX_CODE.md` | ☐ Applied ☐ N/A |
| VERSION_MANAGEMENT | ✅ | `AECF_<NN>_VERSION.md` | ☐ Present ☐ Missing |

**Section Score**: ___/100

---

## 3. Testing Completeness (Weight: 3)

| Check | Required | Evidence | Status |
|-------|----------|----------|--------|
| TEST_STRATEGY documented | ✅ | `AECF_<NN>_TEST_STRATEGY.md` | ☐ |
| TEST_IMPLEMENTATION completed | ✅ | `AECF_<NN>_TEST_IMPLEMENTATION.md` | ☐ |
| AUDIT_TESTS completed with GO | ✅ | `AECF_<NN>_AUDIT_TESTS.md` | ☐ |
| Test coverage ≥ 80% | ✅ | Coverage report | ☐ Coverage: ___% |
| All tests passing | ✅ | Test execution | ☐ |
| Regression tests included | ✅ | Test suite | ☐ |

**Section Score**: ___/100

---

## 4. Security Clearance (Weight: 3)

| Check | Required | Evidence | Status |
|-------|----------|----------|--------|
| SECURITY_AUDIT executed | conditional | `AECF_<NN>_SECURITY_AUDIT.md` | ☐ Done ☐ N/A |
| No CRITICAL vulnerabilities | ✅ | Security report | ☐ |
| No unmitigated HIGH vulnerabilities | ✅ | Security report | ☐ |
| Residual risks documented | conditional | Residual risks doc | ☐ Done ☐ N/A |
| Dependencies scanned for CVEs | recommended | Dependency audit | ☐ Done ☐ N/A |

**Section Score**: ___/100

---

## 5. Version Management (Weight: 2)

| Check | Required | Evidence | Status |
|-------|----------|----------|--------|
| SemVer correctly applied | ✅ | Version files | ☐ |
| CHANGELOG.md updated | ✅ | CHANGELOG.md | ☐ |
| Git tag prepared/created | ✅ | Git | ☐ |
| Version bumped in relevant files | ✅ | Source files | ☐ |

**Section Score**: ___/100

---

## 6. Documentation Completeness (Weight: 2)

| Check | Required | Evidence | Status |
|-------|----------|----------|--------|
| All AECF phase documents exist | ✅ | documentation/ | ☐ |
| Executive summary generated | ✅ | AECF_[NN]_EXECUTIVE_SUMMARY.md | ☐ |
| README updated (if applicable) | conditional | README.md | ☐ N/A |
| API documentation updated | conditional | API docs | ☐ N/A |
| Migration guide (if breaking) | conditional | Migration doc | ☐ N/A |

**Section Score**: ___/100

---

## 7. Operational Readiness (Weight: 2)

| Check | Required | Evidence | Status |
|-------|----------|----------|--------|
| Rollback plan documented | ✅ | | ☐ |
| Monitoring/alerting configured | recommended | | ☐ N/A |
| Feature flags (if applicable) | conditional | | ☐ N/A |
| DB migrations tested | conditional | | ☐ N/A |
| Config changes documented | conditional | | ☐ N/A |

**Section Score**: ___/100

---

## 8. Release Readiness Score

### Section Scores

| Section | Weight | Score | Weighted Score |
|---------|--------|-------|---------------|
| AECF Phase Completion | 3 | ___/100 | ___ |
| Testing Completeness | 3 | ___/100 | ___ |
| Security Clearance | 3 | ___/100 | ___ |
| Version Management | 2 | ___/100 | ___ |
| Documentation Completeness | 2 | ___/100 | ___ |
| Operational Readiness | 2 | ___/100 | ___ |

### Final Score

$$
\text{Release Readiness Score} = \frac{\sum (\text{Weight}_i \times \text{Score}_i)}{\sum \text{Weight}_i} = \text{\_\_\_/100}
$$

---

## 9. VERDICT

| Score Range | Verdict | Status |
|-------------|---------|--------|
| ≥ 90 | **GO** — Release approved | ☐ |
| 75–89 | **GO CONDICIONAL** — Release with documented exceptions | ☐ |
| 60–74 | **NO-GO REMEDIABLE** — Address gaps, re-evaluate | ☐ |
| < 60 | **NO-GO CRITICAL** — Significant governance gaps | ☐ |

### Override Rules Applied
- [ ] Unresolved AUDIT NO-GO → Automatic NO-GO
- [ ] Open CRITICAL security vulnerability → Automatic NO-GO
- [ ] Missing phase documentation → NO-GO

### **FINAL VERDICT**: ___

---

## 10. Blocking Items (if NO-GO)

| # | Blocking Item | Section | Required Action | Owner |
|---|--------------|---------|----------------|-------|
| 1 | <!-- item --> | <!-- section --> | <!-- action --> | <!-- owner --> |

---

## 11. Conditional Items (if GO CONDICIONAL)

| # | Condition | Accepted By | Deadline | Tracking |
|---|-----------|------------|----------|----------|
| 1 | <!-- condition --> | <!-- name --> | <!-- date --> | <!-- ticket/issue --> |

---

## 12. Approval Chain

| Role | Name | Decision | Date |
|------|------|----------|------|
| Assessor | | | |
| Tech Lead | | | |
| Release Manager | | | |

---

*Generated by AECF — AI Engineering Compliance Framework*
