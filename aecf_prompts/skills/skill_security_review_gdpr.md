## PHASE_DEFINITION

### AECF_SECURITY_REVIEW_GDPR
output_file: AECF_01_AECF_SECURITY_REVIEW_GDPR.md
gate: none
loop_to: none
requires_plan_go: false

## TAXONOMY

skill_tier: TIER1
requires_determinism: true

# AECF SKILL — SECURITY REVIEW GDPR (EU General Data Protection Regulation Code Audit)

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
- aecf_prompts/knowledge/domains/regulatory/semantic_profiles/gdpr.md (GDPR checklist and severity mapping)
- aecf_prompts/knowledge/domains/security/pack.md (cross-cutting security layer)

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

## REGULATORY PROFILE STALENESS CHECK (MANDATORY — EXECUTE FIRST)

Before any analysis, the skill MUST:

1. Read `regulation_reference_date` and `max_staleness_months` from the GDPR semantic profile frontmatter.
2. Compare against the current execution date.
3. If `current_date - regulation_reference_date > max_staleness_months`:
   - Emit `⚠️ REGULATORY PROFILE STALENESS WARNING` as the FIRST section of the report (before executive summary).
   - Include: profile name, reference date, staleness threshold, months elapsed, and recommendation to update.
   - Example:
     ```
     ## ⚠️ REGULATORY PROFILE STALENESS WARNING
     
     | Field | Value |
     |-------|-------|
     | Profile | GDPR (gdpr.md) |
     | Reference date | 2026-03-16 |
     | Max staleness | 6 months |
     | Current date | {execution_date} |
     | Months elapsed | {N} |
     
     **Action required**: The GDPR regulatory profile has not been reviewed in {N} months
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
4. **LOAD GDPR CHECKLIST** from `aecf_prompts/knowledge/domains/regulatory/semantic_profiles/gdpr.md`
5. **SCAN** all files in scope for GDPR-relevant code patterns exhaustively
6. **CLASSIFY** findings by GDPR article and CVSS-aligned severity using gdpr.md severity mapping
7. **EMIT ORGANIZATIONAL WARNINGS** for compliance dimensions that cannot be verified from code
8. **CREATE FILE** at `<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_<NN>_SECURITY_REVIEW_GDPR.md`

**MANDATORY POST-EXECUTION GOVERNANCE (per SKILL_DISPATCHER)**:
- **UPDATE** `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.json` for TOPIC lifecycle and **REGENERATE** `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.md` (Step 4.1)
- **APPEND** one execution entry to `<DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md` (Step 4.2)

**FORBIDDEN**:
- ❌ Responding only in chat without creating files
- ❌ Asking the user for execution mode, output path, or AECF conventions
- ❌ Requiring verbose prompts — a simple `skill: security_review_gdpr` MUST be sufficient
- ❌ Modifying any code (this skill is READ-ONLY, report-only)
- ❌ Claiming full GDPR compliance from code audit alone
- ❌ Providing legal advice — this is a technical code audit, not a legal opinion

**DETECTION BOUNDARY (MANDATORY)**:
- This skill audits CODE-LEVEL compliance indicators only.
- Organizational, procedural, and contractual GDPR requirements are beyond scope and flagged as ORGANIZATIONAL_WARNING items.
- The audit framework is deterministic (contexts, checklist, severity mapping), but concrete finding detection depends on LLM reasoning and is not a static rule engine.

**SCOPE LIMITATION DISCLOSURE (MANDATORY — include in every report)**:
> ⚙️ **Scope**: This audit evaluates GDPR compliance indicators observable in source code, configuration, and project artifacts. It does NOT verify organizational compliance (DPO appointment, data processing agreements, staff training, physical security, or procedural documentation that exists outside the codebase). Findings flagged as `ORGANIZATIONAL_WARNING` indicate areas where organizational verification is required but cannot be performed from code alone.

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
- `DATA_MODELS_AND_SCHEMAS` (especially models with personal data fields)
- `AUTHENTICATION_AND_AUTHORIZATION_BOUNDARIES`
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
- `Regulatory Profile Version` (from gdpr.md frontmatter `version`)
- `Regulatory Reference Date` (from gdpr.md frontmatter `regulation_reference_date`)
- `Staleness Status` (`CURRENT` or `STALE — N months overdue`)

Missing metadata or missing traceability fields => INVALID SKILL EXECUTION.

------------------------------------------------------------

## Skill ID
`aecf_security_review_gdpr`

## Description
Specialized GDPR compliance code audit. Scans source code, configuration, and project artifacts for personal data handling patterns and evaluates them against GDPR articles. Produces a deterministic, article-mapped compliance report with severity classification.

## When to Use
- Pre-deployment GDPR compliance check for systems processing EU personal data
- After `aecf_data_classification` to validate governance of discovered PII fields
- Legacy system GDPR readiness assessment
- Periodic GDPR code audit (recommended: quarterly or before major releases)
- After `aecf_security_review` when GDPR-specific depth is needed
- Due diligence for systems acquired or inherited

## When NOT to Use
- Code in PLAN phase (no implementation to audit)
- Pure organizational/procedural GDPR assessment (use external GDPR audit tools)
- Non-EU data or systems with no EU data subjects
- `aecf_security_review` already covers the needed depth (avoid double effort)

## Recommended Composition Chains

### GDPR-focused audit
```
aecf_data_classification → aecf_security_review_gdpr → aecf_release_readiness
```

### Full compliance audit
```
aecf_data_classification → aecf_security_review → aecf_security_review_gdpr → aecf_release_readiness
```

### Pre-release with regulatory gate
```
aecf_security_review_gdpr → aecf_dependency_audit → aecf_release_readiness
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
3. Use that matrix to classify severities, enhanced with GDPR-specific severity mapping from `gdpr.md`.

On subsequent executions:
1. LOAD the existing project matrix.
2. Reuse its severities to keep reports consistent.
3. If a new GDPR-specific finding appears, classify using the gdpr.md severity mapping first, then fall back to CVSS/matrix tie-breaker rules.
4. `MATRIX-PENDING` findings follow the same ADD_RULE / NO_ADD_RULE protocol as `aecf_security_review`.

### Matrix Auto-Apply Protocol (MANDATORY)

Same protocol as `aecf_security_review` — `ADD_RULE` decisions are automatically applied to the project severity matrix. See `skill_security_review.md` for the detailed auto-apply steps.

---

## GDPR Audit Execution Steps

### Step 1: Personal Data Discovery
**Input**: All files in scope
**Focus**:
- Identify data models, schemas, DTOs, and API contracts containing personal data fields
- Classify fields using GDPR categories: identifiers, contact data, financial, health, biometric, behavioral, location
- Cross-reference with `aecf_data_classification` output if available
- Map each personal data field to its processing purpose (if determinable from code)

### Step 2: GDPR Article-by-Article Code Audit
**Input**: Discovery results + GDPR checklist from `gdpr.md`
**Focus**: Evaluate each applicable GDPR article against code evidence:
- Art. 5 (Principles) → data minimization, purpose limitation evidence
- Art. 6 (Lawfulness) → legal basis implementation patterns
- Art. 7 (Consent) → consent flows, withdrawal mechanisms
- Art. 9 (Special categories) → enhanced protection for sensitive data
- Art. 13/14 (Information) → privacy notice references
- Art. 15-22 (Data subject rights) → access, rectification, erasure, portability endpoints
- Art. 25 (By design/default) → default privacy settings, pseudonymization
- Art. 32 (Security) → encryption, access control, logging
- Art. 33/34 (Breach notification) → detection and notification mechanisms
- Art. 35 (DPIA) → high-risk processing indicators
- Art. 44-49 (International transfers) → cross-border data flow indicators

### Step 3: Severity Classification
**Using**: GDPR severity mapping from `gdpr.md` + project severity matrix
- Map each finding to a GDPR article
- Apply severity from the gdpr.md mapping table
- Cross-reference with project matrix for consistency
- `MATRIX-PENDING` findings → Classification Decision Protocol

### Step 4: Organizational Warning Generation
**Output**: List of GDPR requirements that cannot be verified from code
- Art. 37-39 (DPO), Art. 28 (DPA), Art. 30 (full ROPA), Art. 35 (full DPIA), staff training, physical security
- Each warning includes: article reference, requirement description, recommended organizational action

### Step 5: Report Generation
**Output**: `<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_<NN>_SECURITY_REVIEW_GDPR.md`

**Report structure (MANDATORY)**:

```
## ⚠️ REGULATORY PROFILE STALENESS WARNING (if applicable)
## METADATA
## ⚙️ Scope Limitation Disclosure
## 📊 Executive Summary
  - Total findings by severity (CRITICAL / HIGH / MEDIUM / LOW)
  - GDPR articles covered vs. not applicable
  - Personal data fields discovered
  - Organizational warnings count
  - Staleness status
  - VERDICT: GO / CONDITIONAL_GO / NO-GO
## 🗂️ Sections Analyzed — Navigation Index
  | # | GDPR Article | Findings | Severity | Link |
## 📋 Personal Data Inventory
  - Fields discovered, classification, processing purpose
## 🔍 GDPR Article Findings (one section per applicable article)
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

### GDPR-Specific Badge

In addition to severity badges, use a GDPR article badge for each finding:

- **Article reference**: `<span style="background:#6f42c1;color:#fff;padding:2px 8px;border-radius:4px;font-size:0.85em">Art. NN</span>`

### Remediation Skill Mapping

| GDPR Finding Type | Recommended Skill | Example |
|-------------------|-------------------|---------|
| Missing encryption | `aecf_refactor` | `@aecf run skill=aecf_refactor topic={{TOPIC}} prompt="Add encryption for PII field in models.py:45"` |
| Missing consent flow | `aecf_new_feature` | `@aecf run skill=aecf_new_feature topic={{TOPIC}} prompt="Implement consent acquisition flow for user registration"` |
| Personal data in logs | `aecf_refactor` | `@aecf run skill=aecf_refactor topic={{TOPIC}} prompt="Remove PII from log output in handler.py:120"` |
| Missing data deletion | `aecf_new_feature` | `@aecf run skill=aecf_new_feature topic={{TOPIC}} prompt="Implement account deletion endpoint for GDPR Art. 17"` |
| Missing data export | `aecf_new_feature` | `@aecf run skill=aecf_new_feature topic={{TOPIC}} prompt="Implement data portability export for GDPR Art. 20"` |
| Vulnerable dependency with PII | `aecf_dependency_audit` | `@aecf run skill=aecf_dependency_audit topic={{TOPIC}} prompt="Audit dependencies handling personal data"` |
| Default-on data collection | `aecf_refactor` | `@aecf run skill=aecf_refactor topic={{TOPIC}} prompt="Change default settings to minimize data collection per Art. 25"` |
| Cross-border transfer | `aecf_security_review` | `@aecf run skill=aecf_security_review topic={{TOPIC}} prompt="Review cross-border data transfer safeguards"` |

---

## VERDICT Criteria

| Verdict | Condition |
|---------|-----------|
| **GO** | Zero CRITICAL, zero HIGH findings. All applicable articles evaluated. |
| **CONDITIONAL_GO** | Zero CRITICAL. HIGH findings have documented mitigation plan with timeline. |
| **NO-GO** | Any CRITICAL finding, OR multiple HIGH findings without mitigation plan. |

---

## AI_USAGE_DECLARATION

AI_USED = TRUE

## AI_EXPLAINABILITY_VALIDATION

- Explainability level defined? YES/NO
- User-facing explanation provided? YES/NO
- Model version logged? YES/NO
- Decision trace stored? YES/NO

## Governance Validation Block

- **Data governance**: ✅ evaluated personal data classification, lineage, retention
- **Model governance**: ✅ impact on training/inference data identified (YES/NO)
- **AI risk management**: ✅ defined risk level and mitigations
- **Impact metrics**: ✅ GDPR compliance coverage metrics
- **Compliance check**: ✅ GDPR article-level verification performed (code scope only)
- **Regulatory profile staleness**: ✅ checked / ⚠️ stale

---

## Example Usage

```
skill: security_review_gdpr
```

```
@aecf run skill=security_review_gdpr topic=user_service
```

```
@aecf run skill=security_review_gdpr scope=src/auth/
```

------------------------------------------------------------

**END OF skill_security_review_gdpr.md**
