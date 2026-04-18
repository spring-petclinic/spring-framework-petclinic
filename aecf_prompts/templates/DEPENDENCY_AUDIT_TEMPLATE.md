# AECF — DEPENDENCY AUDIT TEMPLATE

> AI Engineering Compliance Framework — Supply Chain Security & Health Report

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Dependency Audit |
> | Phase | DEPENDENCY_AUDIT |

---

## 1. Audit Overview

| Field | Value |
|-------|-------|
| Audit Date | |
| Audit Type | ☐ Full project  ☐ Module focused  ☐ Post-alert  ☐ Periodic review |
| Manifest files analyzed | |
| Languages detected | |
| Total direct dependencies | |
| Total transitive dependencies | |

---

## 2. Dependency Inventory

### Direct Dependencies

| # | Package | Version (Current) | Version (Latest) | Behind | License | CVEs | Health |
|---|---------|-------------------|-------------------|--------|---------|------|--------|
| 1 | <!-- name --> | <!-- version --> | <!-- latest --> | <!-- versions behind --> | <!-- license --> | <!-- count --> | <!-- Healthy/Warning/Critical --> |

### Transitive Dependencies (Notable)

| # | Package | Required By | Version | CVEs | License |
|---|---------|------------|---------|------|---------|
| 1 | <!-- name --> | <!-- parent --> | <!-- version --> | <!-- count --> | <!-- license --> |

---

## 3. Vulnerability Findings

### Summary

| Severity | Count | Exploitable | Fix Available |
|----------|-------|-------------|---------------|
| CRITICAL (CVSS 9.0–10.0) | | | |
| HIGH (CVSS 7.0–8.9) | | | |
| MEDIUM (CVSS 4.0–6.9) | | | |
| LOW (CVSS 0.1–3.9) | | | |

### Detailed Findings

| # | CVE | Package | Severity | CVSS | Description | Fix Version | Action |
|---|-----|---------|----------|------|-------------|-------------|--------|
| 1 | <!-- CVE-YYYY-NNNNN --> | <!-- package --> | <!-- severity --> | <!-- score --> | <!-- description --> | <!-- version --> | <!-- Upgrade/Replace/Accept --> |

---

## 4. License Compliance Matrix

### License Distribution

| License Type | Classification | Count | Packages |
|-------------|---------------|-------|----------|
| MIT | Permissive | | |
| Apache 2.0 | Permissive | | |
| BSD | Permissive | | |
| LGPL | Copyleft (weak) | | |
| GPL | Copyleft (strong) | | |
| AGPL | Copyleft (network) | | |
| Unknown | Requires review | | |
| No license | No rights granted | | |

### Compliance Issues

| # | Package | License | Risk Level | Issue | Action Required |
|---|---------|---------|-----------|-------|-----------------|
| 1 | <!-- package --> | <!-- license --> | <!-- risk --> | <!-- issue --> | <!-- action --> |

---

## 5. Maintenance Health Dashboard

| Package | Last Release | Open Issues Response | Maintainers | Community | Status |
|---------|-------------|---------------------|-------------|-----------|--------|
| <!-- name --> | <!-- date --> | <!-- days --> | <!-- count --> | <!-- Active/Declining/Inactive --> | <!-- Healthy/Warning/Critical --> |

### Health Issues

| # | Package | Issue | Risk | Recommendation |
|---|---------|-------|------|---------------|
| 1 | <!-- package --> | <!-- issue --> | <!-- risk --> | <!-- recommendation --> |

---

## 6. Version Freshness Report

| # | Package | Current | Latest | Behind | Breaking Changes | Priority |
|---|---------|---------|--------|--------|-----------------|----------|
| 1 | <!-- package --> | <!-- version --> | <!-- latest --> | <!-- N versions --> | <!-- Yes/No --> | <!-- High/Medium/Low --> |

---

## 7. Supply Chain Risk Score

### Risk Calculation

$$
\text{Risk Score} = \frac{(\text{CVE Risk} \times 3) + (\text{License Risk} \times 2) + (\text{Health Risk} \times 2) + (\text{Freshness Risk} \times 1)}{8} \times 100
$$

| Component | Score (0–100) | Weight | Weighted |
|-----------|--------------|--------|----------|
| CVE Risk | | 3 | |
| License Risk | | 2 | |
| Health Risk | | 2 | |
| Freshness Risk | | 1 | |

### **Supply Chain Risk Score: ___/100**

| Score Range | Classification | Status |
|-------------|---------------|--------|
| 0–20 | LOW — Healthy supply chain | ☐ |
| 21–40 | MODERATE — Minor improvements needed | ☐ |
| 41–60 | ELEVATED — Significant attention needed | ☐ |
| 61–80 | HIGH — Urgent remediation required | ☐ |
| 81–100 | CRITICAL — Supply chain compromised | ☐ |

---

## 8. Prioritized Remediation Plan

| Priority | Package | Action | Current → Target | Effort | Risk Mitigated | Sprint |
|----------|---------|--------|------------------|--------|---------------|--------|
| 1 | <!-- package --> | <!-- Upgrade/Replace/Remove/Pin/Accept --> | <!-- v1.0 → v2.0 --> | <!-- XS/S/M/L/XL --> | <!-- what risk --> | <!-- Immediate/Next/Backlog --> |

---

## 9. Trend Comparison

<!-- Only if previous audit exists -->

| Metric | Previous | Current | Trend |
|--------|----------|---------|-------|
| Total dependencies | | | ↑ / ↓ / → |
| Known CVEs | | | ↑ / ↓ / → |
| License issues | | | ↑ / ↓ / → |
| Health warnings | | | ↑ / ↓ / → |
| Supply Chain Risk Score | | | ↑ / ↓ / → |

---

## 10. Recommendations

1. <!-- recommendation -->

---

## AUDIT COMPLETENESS

| Aspect | Status |
|--------|--------|
| All manifests parsed | ☐ |
| CVE scan completed | ☐ |
| License audit completed | ☐ |
| Health assessment completed | ☐ |
| Freshness analysis completed | ☐ |
| Remediation plan generated | ☐ |

**Completeness: X/6**

---

*Generated by AECF — AI Engineering Compliance Framework*
