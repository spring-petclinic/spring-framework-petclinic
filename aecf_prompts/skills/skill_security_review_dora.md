## PHASE_DEFINITION

### AECF_SECURITY_REVIEW_DORA
output_file: AECF_01_AECF_SECURITY_REVIEW_DORA.md
gate: none
loop_to: none
requires_plan_go: false

## TAXONOMY

skill_tier: TIER1
requires_determinism: true

# AECF SKILL — SECURITY REVIEW DORA (Digital Operational Resilience Act Code Audit)

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This skill operates under the following mandatory contexts:

- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- aecf_prompts/SKILL_DISPATCHER.md (execution protocol)
- <workspace_root>/AECF_PROJECT_CONTEXT.md (if present anywhere in the active workspace)

Governance:
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

Knowledge:
- aecf_prompts/knowledge/domains/regulatory/pack.md (regulatory base layer)
- aecf_prompts/knowledge/domains/regulatory/semantic_profiles/dora.md (DORA checklist and severity mapping)
- aecf_prompts/knowledge/domains/security/pack.md (cross-cutting security layer)

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

## REGULATORY PROFILE STALENESS CHECK (MANDATORY — EXECUTE FIRST)

Before any analysis, the skill MUST:

1. Read `regulation_reference_date` and `max_staleness_months` from the DORA semantic profile frontmatter.
2. Compare against the current execution date.
3. If `current_date - regulation_reference_date > max_staleness_months`:
   - Emit `⚠️ REGULATORY PROFILE STALENESS WARNING` as the FIRST section of the report (before executive summary).
   - Include: profile name, reference date, staleness threshold, months elapsed, and recommendation to update.
   - Example:
     ```
     ## ⚠️ REGULATORY PROFILE STALENESS WARNING
     
     | Field | Value |
     |-------|-------|
     | Profile | DORA (dora.md) |
     | Reference date | 2026-03-16 |
     | Max staleness | 6 months |
     | Current date | {execution_date} |
     | Months elapsed | {N} |
     
     **Action required**: The DORA regulatory profile has not been reviewed in {N} months
     (threshold: 6 months). Regulatory references may be outdated. The responsible person
     MUST review and update the profile before relying on this report for compliance decisions.
     
     > This WARNING does not block execution but the report carries reduced regulatory confidence.
     ```
4. If within staleness window: proceed normally, no warning needed.

------------------------------------------------------------

## EXECUTION MANDATE (IMPERATIVE)

When this skill is invoked, the AI MUST:

1. **STALENESS CHECK** — execute the regulatory profile staleness check above
2. **AUTO-RESOLVE** all parameters (TOPIC, scope, numbering) per SKILL_DISPATCHER
3. **BOOTSTRAP/LOAD PROJECT SEVERITY MATRIX** at `<DOCS_ROOT>/AECF_SECURITY_REVIEW_SEVERITY_MATRIX.md`
4. **LOAD DORA CHECKLIST** from `aecf_prompts/knowledge/domains/regulatory/semantic_profiles/dora.md`
5. **SCAN** all files in scope for ICT resilience patterns exhaustively
6. **CLASSIFY** findings by DORA article and CVSS-aligned severity using dora.md severity mapping
7. **EMIT ORGANIZATIONAL WARNINGS** for compliance dimensions that cannot be verified from code
8. **CREATE FILE** at `<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_<NN>_SECURITY_REVIEW_DORA.md`

**MANDATORY POST-EXECUTION GOVERNANCE (per SKILL_DISPATCHER)**:
- **UPDATE** `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.json` for TOPIC lifecycle and **REGENERATE** `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.md` (Step 4.1)
- **APPEND** one execution entry to `<DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md` (Step 4.2)

**FORBIDDEN**:
- ❌ Responding only in chat without creating files
- ❌ Asking the user for execution mode, output path, or AECF conventions
- ❌ Requiring verbose prompts — a simple `skill: security_review_dora` MUST be sufficient
- ❌ Modifying any code (this skill is READ-ONLY, report-only)
- ❌ Claiming full DORA compliance from code audit alone
- ❌ Providing legal advice — this is a technical code audit, not a legal opinion

**DETECTION BOUNDARY (MANDATORY)**:
- This skill audits CODE-LEVEL compliance indicators only.
- Organizational, procedural, and contractual DORA requirements are beyond scope and flagged as ORGANIZATIONAL_WARNING items.
- The audit framework is deterministic (contexts, checklist, severity mapping), but concrete finding detection depends on LLM reasoning and is not a static rule engine.

**SCOPE LIMITATION DISCLOSURE (MANDATORY — include in every report)**:
> ⚙️ **Scope**: This audit evaluates DORA compliance indicators observable in source code, configuration, and project artifacts. It does NOT verify organizational compliance (ICT risk management governance, board-level responsibility, crisis communication plans, contractual arrangements with ICT third-party providers, regulatory reporting to EBA/EIOPA/ESMA, or staff ICT security training that exists outside the codebase). Findings flagged as `ORGANIZATIONAL_WARNING` indicate areas where organizational verification is required but cannot be performed from code alone.

------------------------------------------------------------

## MANDATORY REPOSITORY DISCOVERY (SEARCH-FIRST)

This skill requires explicit repository discovery before executing its first audit/analysis step.

Execution rules:
1. Execute an initial repository search pass within scope using IDE capabilities.
2. Build an execution-scoped `WORKING_CONTEXT` before starting the first skill step.
3. If discovery evidence is incomplete, set discovery status to NO-GO and STOP.

Minimum `WORKING_CONTEXT` for search-first execution:
- `TARGET_SCOPE`
- `ENTRY_POINTS_OR_ARTIFACTS`
- `DISCOVERED_PATHS`
- `CONFIG_AND_DEPENDENCIES`
- `ICT_INFRASTRUCTURE` (deployment configs, container orchestration, cloud resources)
- `MONITORING_AND_ALERTING` (monitoring configs, dashboards, alert rules)
- `BACKUP_AND_RECOVERY` (backup configs, DR plans, failover mechanisms)
- `THIRD_PARTY_DEPENDENCIES` (cloud providers, SaaS integrations, API gateways)
- `UNCERTAINTIES_AND_ASSUMPTIONS`
- `SOURCE_REFERENCES` (concrete file paths and line-level references)

Forbidden:
- Skipping discovery and jumping directly to analysis.
- Assuming repository structure without verification.
- Reusing shared static discovery files across executions.

## TRACEABILITY METADATA ENFORCEMENT (MANDATORY)

Every document generated by this skill MUST include `## METADATA` following
`aecf_prompts/templates/TEMPLATE_HEADERS.md`.

The metadata block is INVALID unless it includes, at minimum:
- `Timestamp (UTC)`
- `Executed By`
- `Executed By ID`
- `Execution Identity Source`
- `Repository`
- `Branch`
- `Root Prompt`
- `Skill Executed`
- `Sequence Position`
- `Total Prompts Executed`
- `Regulatory Profile Version` (from dora.md frontmatter `version`)
- `Regulatory Reference Date` (from dora.md frontmatter `regulation_reference_date`)
- `Staleness Status` (`CURRENT` or `STALE — N months overdue`)

Missing metadata or missing traceability fields => INVALID SKILL EXECUTION.

------------------------------------------------------------

## Skill ID
`aecf_security_review_dora`

## Description
Specialized DORA compliance code audit for financial entities. Scans source code, configuration, and project artifacts for ICT operational resilience patterns and evaluates them against DORA articles. Produces a deterministic, article-mapped compliance report with severity classification.

## When to Use
- Pre-deployment DORA compliance check for financial sector ICT systems
- After `aecf_security_review` to validate ICT operational resilience depth
- Third-party ICT provider risk assessment (from code/configuration perspective)
- Periodic DORA compliance audit (recommended: quarterly or before major releases)
- Due diligence for financial sector systems acquired or inherited
- Post-incident resilience posture validation

## When NOT to Use
- Code in PLAN phase (no implementation to audit)
- Pure organizational/procedural DORA assessment (use external compliance tools)
- Non-financial-sector systems not subject to DORA
- `aecf_security_review` already covers the needed depth (avoid double effort)

## Recommended Composition Chains

### DORA compliance audit
```
aecf_security_review → aecf_security_review_dora → aecf_release_readiness
```

### Full financial sector compliance
```
aecf_security_review → aecf_security_review_dora → aecf_dependency_audit → aecf_release_readiness
```

### Pre-release with DORA regulatory gate
```
aecf_security_review_dora → aecf_dependency_audit → aecf_release_readiness
```

### DORA + GDPR combined (financial entities processing personal data)
```
aecf_security_review → aecf_security_review_gdpr → aecf_security_review_dora → aecf_release_readiness
```

---

## Project Severity Matrix Bootstrap (MANDATORY)

To avoid cross-run severity drift, this skill MUST use a **project-local severity matrix**:

- **Path**: `<DOCS_ROOT>/AECF_SECURITY_REVIEW_SEVERITY_MATRIX.md`
- **Scope**: Applies only to the current project/workspace

### Bootstrap rule

On the first execution in a project:
1. If the matrix file does NOT exist, CREATE it from template:
   - `aecf_prompts/templates/SECURITY_REVIEW_SEVERITY_MATRIX_TEMPLATE.md`
2. Mark it as baseline (`v1`) for the project.
3. Use that matrix to classify severities, enhanced with DORA-specific severity mapping from `dora.md`.

On subsequent executions:
1. LOAD the existing project matrix.
2. Reuse its severities to keep reports consistent.
3. If a new DORA-specific finding appears, classify using the dora.md severity mapping first, then fall back to CVSS/matrix tie-breaker rules.
4. `MATRIX-PENDING` findings follow the same ADD_RULE / NO_ADD_RULE protocol as `aecf_security_review`.

### Matrix Auto-Apply Protocol (MANDATORY)

Same protocol as `aecf_security_review` — `ADD_RULE` decisions are automatically applied to the project severity matrix. See `skill_security_review.md` for the detailed auto-apply steps.

---

## DORA Audit Execution Steps

### Step 1: ICT Infrastructure Discovery
**Input**: All files in scope
**Focus**:
- Identify ICT infrastructure components (deployment configs, Dockerfiles, Kubernetes manifests, Terraform/IaC)
- Map third-party ICT dependencies (cloud providers, SaaS, external APIs)
- Identify monitoring, alerting, and incident management integrations
- Identify backup and disaster recovery configurations
- Cross-reference with `aecf_dependency_audit` output if available

### Step 2: DORA Article-by-Article Code Audit
**Input**: Discovery results + DORA checklist from `dora.md`
**Focus**: Evaluate each applicable DORA article against code evidence:
- Art. 7 (ICT systems security) → hardening, segregation, capacity
- Art. 8 (ICT risk identification) → asset classification, dependency mapping, SPOF analysis
- Art. 9 (Protection/prevention) → encryption, access control, patching, DLP
- Art. 10 (Detection) → monitoring, SIEM, anomaly detection, alerting
- Art. 11 (Response/recovery) → incident automation, DR, failover, RTO/RPO
- Art. 12 (Backup) → schedules, encryption, integrity, geo-separation
- Art. 15-16 (Incident management) → classification, lifecycle, SLA
- Art. 17 (Incident reporting) → severity classification, reporting hooks
- Art. 23-24 (Resilience testing) → load/stress tests, chaos engineering
- Art. 25-27 (TLPT) → penetration testing evidence
- Art. 28-30 (Third-party risk) → vendor assessment, concentration, exit strategy

### Step 3: Severity Classification
**Using**: DORA severity mapping from `dora.md` + project severity matrix
- Map each finding to a DORA article
- Apply severity from the dora.md mapping table
- Cross-reference with project matrix for consistency
- `MATRIX-PENDING` findings → Classification Decision Protocol

### Step 4: Organizational Warning Generation
**Output**: List of DORA requirements that cannot be verified from code
- ICT risk governance (board-level), crisis communication, contractual arrangements, regulatory reporting
- Each warning includes: article reference, requirement description, recommended organizational action

### Step 5: Report Generation
**Output**: `<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_<NN>_SECURITY_REVIEW_DORA.md`

**Report structure (MANDATORY)**:

```
## ⚠️ REGULATORY PROFILE STALENESS WARNING (if applicable)
## METADATA
## ⚙️ Scope Limitation Disclosure
## 📊 Executive Summary
  - Total findings by severity (CRITICAL / HIGH / MEDIUM / LOW)
  - DORA pillars covered (ICT Risk Mgmt / Incident Mgmt / Resilience Testing / Third-Party Risk / Information Sharing)
  - ICT components discovered
  - Third-party dependencies identified
  - Organizational warnings count
  - Staleness status
  - VERDICT: GO / CONDITIONAL_GO / NO-GO
## 🗂️ Sections Analyzed — Navigation Index
  | # | DORA Article | Findings | Severity | Link |
## 📋 ICT Infrastructure Inventory
  - Components discovered, classification, third-party dependencies
## 🔍 DORA Article Findings (one section per applicable article)
  - Article reference and requirement
  - Code evidence (file:line links)
  - Severity badge
  - Remediation recommendation with copyable @aecf command
## ⚠️ Organizational Warnings (CANNOT be verified from code)
  - Article reference
  - What needs organizational verification
  - Recommended action
## 📈 Classification Decision Log
  - MATRIX-PENDING findings with ADD_RULE / NO_ADD_RULE decisions
## 🎯 Prioritized Remediation Plan
  - Grouped by severity, each with @aecf command
## GOVERNANCE VALIDATION BLOCK
```

---

## Visual Format Specification (MANDATORY)

Same visual format as `aecf_security_review`:
- Severity badges (HTML colored spans)
- Clickable file locations (Markdown links with line numbers)
- Copyable `@aecf` remediation commands for CRITICAL and HIGH findings