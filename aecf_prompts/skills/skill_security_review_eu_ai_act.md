## PHASE_DEFINITION

### AECF_SECURITY_REVIEW_EU_AI_ACT
output_file: AECF_01_AECF_SECURITY_REVIEW_EU_AI_ACT.md
gate: none
loop_to: none
requires_plan_go: false

## TAXONOMY

skill_tier: TIER1
requires_determinism: true

# AECF SKILL — SECURITY REVIEW EU AI ACT (EU Artificial Intelligence Act Code Audit)

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
- aecf_prompts/knowledge/domains/regulatory/semantic_profiles/eu_ai_act.md (EU AI Act checklist and severity mapping)
- aecf_prompts/knowledge/domains/security/pack.md (cross-cutting security layer)

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

## REGULATORY PROFILE STALENESS CHECK (MANDATORY — EXECUTE FIRST)

Before any analysis, the skill MUST:

1. Read `regulation_reference_date` and `max_staleness_months` from the EU AI Act semantic profile frontmatter.
2. Compare against the current execution date.
3. If `current_date - regulation_reference_date > max_staleness_months`:
   - Emit `⚠️ REGULATORY PROFILE STALENESS WARNING` as the FIRST section of the report (before executive summary).
   - Include: profile name, reference date, staleness threshold, months elapsed, and recommendation to update.
   - Example:
     ```
     ## ⚠️ REGULATORY PROFILE STALENESS WARNING
     
     | Field | Value |
     |-------|-------|
     | Profile | EU AI Act (eu_ai_act.md) |
     | Reference date | 2026-03-16 |
     | Max staleness | 6 months |
     | Current date | {execution_date} |
     | Months elapsed | {N} |
     
     **Action required**: The EU AI Act regulatory profile has not been reviewed in {N} months
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
4. **LOAD EU AI ACT CHECKLIST** from `aecf_prompts/knowledge/domains/regulatory/semantic_profiles/eu_ai_act.md`
5. **SCAN** all files in scope for AI system patterns exhaustively
6. **CLASSIFY** findings by EU AI Act article and CVSS-aligned severity using eu_ai_act.md severity mapping
7. **EMIT ORGANIZATIONAL WARNINGS** for compliance dimensions that cannot be verified from code
8. **CREATE FILE** at `<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_<NN>_SECURITY_REVIEW_EU_AI_ACT.md`

**MANDATORY POST-EXECUTION GOVERNANCE (per SKILL_DISPATCHER)**:
- **UPDATE** `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.json` for TOPIC lifecycle and **REGENERATE** `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.md` (Step 4.1)
- **APPEND** one execution entry to `<DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md` (Step 4.2)

**FORBIDDEN**:
- ❌ Responding only in chat without creating files
- ❌ Asking the user for execution mode, output path, or AECF conventions
- ❌ Requiring verbose prompts — a simple `skill: security_review_eu_ai_act` MUST be sufficient
- ❌ Modifying any code (this skill is READ-ONLY, report-only)
- ❌ Claiming full EU AI Act compliance from code audit alone
- ❌ Providing legal advice — this is a technical code audit, not a legal opinion

**DETECTION BOUNDARY (MANDATORY)**:
- This skill audits CODE-LEVEL compliance indicators only.
- Organizational, procedural, and regulatory certification requirements are beyond scope and flagged as ORGANIZATIONAL_WARNING items.
- The audit framework is deterministic (contexts, checklist, severity mapping), but concrete finding detection depends on LLM reasoning and is not a static rule engine.

**SCOPE LIMITATION DISCLOSURE (MANDATORY — include in every report)**:
> ⚙️ **Scope**: This audit evaluates EU AI Act compliance indicators observable in source code, configuration, and project artifacts. It does NOT verify organizational compliance (conformity assessment, CE marking, EU database registration, staff AI literacy training, notified body interactions, or fundamental rights impact assessments that exist outside the codebase). Findings flagged as `ORGANIZATIONAL_WARNING` indicate areas where organizational verification is required but cannot be performed from code alone.

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
- `AI_MODELS_AND_PIPELINES` (model definitions, training pipelines, inference endpoints)
- `DATA_PIPELINES` (training data sources, preprocessing, bias detection)
- `DECISION_ENDPOINTS` (automated decision-making paths)
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
- `Regulatory Profile Version` (from eu_ai_act.md frontmatter `version`)
- `Regulatory Reference Date` (from eu_ai_act.md frontmatter `regulation_reference_date`)
- `Staleness Status` (`CURRENT` or `STALE — N months overdue`)

Missing metadata or missing traceability fields => INVALID SKILL EXECUTION.

------------------------------------------------------------

## Skill ID
`aecf_security_review_eu_ai_act`

## Description
Specialized EU AI Act compliance code audit. Scans source code, configuration, and project artifacts for AI system patterns and evaluates them against EU AI Act articles. Produces a deterministic, article-mapped compliance report with risk classification and severity assignment.

## When to Use
- Pre-deployment compliance check for AI systems placed on the EU market
- After `aecf_ai_risk_assessment` to validate code-level AI governance
- High-risk AI system conformity preparation
- Periodic AI compliance audit (recommended: before major releases)
- After `aecf_security_review` when AI-specific regulatory depth is needed
- Due diligence for AI systems acquired or inherited

## When NOT to Use
- Code in PLAN phase (no implementation to audit)
- Pure organizational/procedural AI Act assessment (use external compliance tools)
- Non-AI systems with no ML/AI components
- Systems not intended for EU market deployment
- `aecf_ai_risk_assessment` already covers the needed depth (avoid double effort)

## Recommended Composition Chains

### AI compliance audit
```
aecf_ai_risk_assessment → aecf_security_review_eu_ai_act → aecf_release_readiness
```

### Full AI governance + compliance
```
aecf_ai_risk_assessment → aecf_model_governance_audit → aecf_security_review_eu_ai_act → aecf_release_readiness
```

### Pre-release with AI regulatory gate
```
aecf_security_review_eu_ai_act → aecf_dependency_audit → aecf_release_readiness
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
3. Use that matrix to classify severities, enhanced with EU AI Act-specific severity mapping from `eu_ai_act.md`.

On subsequent executions:
1. LOAD the existing project matrix.
2. Reuse its severities to keep reports consistent.
3. If a new AI Act-specific finding appears, classify using the eu_ai_act.md severity mapping first, then fall back to CVSS/matrix tie-breaker rules.
4. `MATRIX-PENDING` findings follow the same ADD_RULE / NO_ADD_RULE protocol as `aecf_security_review`.

### Matrix Auto-Apply Protocol (MANDATORY)

Same protocol as `aecf_security_review` — `ADD_RULE` decisions are automatically applied to the project severity matrix. See `skill_security_review.md` for the detailed auto-apply steps.

---

## EU AI Act Audit Execution Steps

### Step 1: AI System Discovery
**Input**: All files in scope
**Focus**:
- Identify AI/ML models, training pipelines, inference endpoints
- Classify system risk level against Annex III categories
- Map AI components to their intended use and affected persons
- Cross-reference with `aecf_ai_risk_assessment` output if available
- Identify GPAI model usage (foundation models, LLM integrations)

### Step 2: EU AI Act Article-by-Article Code Audit
**Input**: Discovery results + EU AI Act checklist from `eu_ai_act.md`
**Focus**: Evaluate each applicable article against code evidence:
- Art. 5 (Prohibited practices) → social scoring, manipulative AI, real-time biometrics
- Art. 6 (Risk classification) → Annex III high-risk indicators
- Art. 9 (Risk management) → risk artifacts, mitigations
- Art. 10 (Data governance) → bias detection, data quality, versioning
- Art. 12 (Record-keeping) → decision logging, audit trails
- Art. 13 (Transparency) → AI disclosure, explainability
- Art. 14 (Human oversight) → human-in-the-loop, override mechanisms
- Art. 15 (Accuracy/robustness) → monitoring, drift detection, adversarial defenses
- Art. 50 (Transparency for generative AI) → content labelling, provenance
- Art. 52 (GPAI) → documentation, copyright compliance

### Step 3: Severity Classification
**Using**: EU AI Act severity mapping from `eu_ai_act.md` + project severity matrix
- Map each finding to an EU AI Act article
- Apply severity from the eu_ai_act.md mapping table
- Cross-reference with project matrix for consistency
- `MATRIX-PENDING` findings → Classification Decision Protocol

### Step 4: Organizational Warning Generation
**Output**: List of EU AI Act requirements that cannot be verified from code
- Conformity assessment, CE marking, EU database registration, notified body interactions, staff AI literacy training
- Each warning includes: article reference, requirement description, recommended organizational action

### Step 5: Report Generation
**Output**: `<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_<NN>_SECURITY_REVIEW_EU_AI_ACT.md`

**Report structure (MANDATORY)**:

```
## ⚠️ REGULATORY PROFILE STALENESS WARNING (if applicable)
## METADATA
## ⚙️ Scope Limitation Disclosure
## 📊 Executive Summary
  - Total findings by severity (CRITICAL / HIGH / MEDIUM / LOW)
  - EU AI Act risk classification (Unacceptable / High-Risk / Limited / Minimal)
  - AI components discovered
  - Organizational warnings count
  - Staleness status
  - VERDICT: GO / CONDITIONAL_GO / NO-GO
## 🗂️ Sections Analyzed — Navigation Index
  | # | EU AI Act Article | Findings | Severity | Link |
## 📋 AI System Inventory
  - AI components discovered, risk classification, intended use
## 🔍 EU AI Act Article Findings (one section per applicable article)
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