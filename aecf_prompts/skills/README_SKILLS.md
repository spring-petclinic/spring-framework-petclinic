# AECF Skills - Quick Reference Guide

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Available Skills](#available-skills)
3. [Search-First Matrix](#search-first-matrix)
4. [AECF Skill Taxonomy](#aecf-skill-taxonomy)
5. [Scoring, Checklists & Maturity](#scoring-checklists--maturity)
6. [Complete Usage Examples](#complete-usage-examples)
7. [GO / NO-GO Flow Examples](#go--no-go-flow-examples)
8. [Choosing the Right Skill](#choosing-the-right-skill)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

**AECF Skills** are automated sequences of AECF prompts designed to execute complete workflows while maintaining traceability and auditing.

> `aecf_prompts/skills/` is now the full prompt-only source surface. It keeps released, beta, hidden, and deprecated skills together with the canonical `SKILL_RELEASE.json` and `SKILL_CATALOG.md`.

> Client delivery is filtered later by the bundle builder. `--bundle-mode release` stages only `released` skills, while `--bundle-mode god` stages `released + beta`. `hidden` and `deprecated` skills stay out of distributed bundles.

> Edit `aecf_prompts/skills/` directly as the source of truth. `node aecf_test_participant/embed-prompts.js` propagates that surface into the component runtime copies and the embedded assets used by the VS Code component.

### Why Skills?

✅ **Automation**: Execute entire sequences without intervention
✅ **Consistency**: Ensures that everyone follows the same process
✅ **Speed**: Quick summon without copy/paste prompts
✅ **Composition**: Combinable skills for complex cases
✅ **Traceability**: Complete documentation generated automatically

### How It Works

```
User invokes skill (simple prompt or natural language)
  → SKILL_DISPATCHER recognizes intent and auto-resolves parameters
  → AI executes sequence of prompts
  → Handles GO/NO-GO loops
  → Generates documentation files (MANDATORY)
  → Executive summary is optional on-demand via dedicated skill
```

Generate executive summary explicitly with:
`@aecf run skill=executive_summary topic=<topic_name> prompt="Close topic with executive summary"`

### Surface-Aware Scope

If the client workspace uses `surfaces`, the published prompt-only bundle now distinguishes four roles:

1. `aecf_project_context_generator` decides whether `surfaces` exist and requires human confirmation.
2. `aecf_codebase_intelligence` and `aecf_set_stack` assist with evidence.
3. Common repo-dependent skills consume the frozen `primary_surface` and `active_surfaces`.
4. `aecf_new_project` stays global-only.

Shared contract for consumer skills:

- `aecf_prompts/guides/AECF_SKILL_SURFACE_CONTRACT.md`

> **IMPORTANTE**: El **SKILL_DISPATCHER** (`aecf/SKILL_DISPATCHER.md`) permite invocar skills
> with simple prompts. It is not necessary to specify execution mode, AECF conventions,
> exit routes or numbering. Everything is resolved automatically.

---

## Available Skills

### 1. 🆕 `aecf_new_feature`
**Purpose**: Implement new functionality complete with testing
**Time**: 1.5 - 4 horas  
**Phases**: PLAN → AUDIT_PLAN → TEST_STRATEGY → IMPLEMENT → TEST_IMPL → AUDIT_TESTS → AUDIT_CODE → VERSION  
**Use when**: Developing new feature from scratch
[📖 Full Documentation](skills/skill_new_feature.md)

---

### 18. 🧪 `aecf_new_test_set`
**Purpose**: Discover missing tests for existing code, propose them first, and optionally pre-approve implementation and execution with `execute=True` for an extensive report
**Layer**: Execution - test hardening of existing modules or routines
**Time**: 1 - 3.5 horas
**Phases**: DISCOVERY SWEEP -> PLAN -> AUDIT_PLAN -> TEST_STRATEGY -> APPROVAL -> TEST_IMPLEMENTATION -> TEST_EXECUTION_REPORT
**Use when**: Existing code needs stronger coverage, security tests, SQL injection checks, forced-error tests, permission tests, performance checks, or an explicit missing-test sweep before release or refactor
**Modifies code**: YES - but only test files, and only after explicit user approval or `execute=True`
**Output**: `<DOCS_ROOT>/<user_id>/{{TOPIC}}/<NN>_<skill_name>_PLAN.md` -> `..._AUDIT_PLAN.md` -> `..._TEST_STRATEGY.md` and, if approved, `..._TEST_IMPLEMENTATION.md` + `..._TEST_EXECUTION_REPORT.md`
[📖 Full Documentation](skills/skill_new_test_set.md)

---

### 19. 🔬 `aecf_codebase_intelligence`
**Purpose**: Analyze the entire workspace and generate 8 structured intelligence artifacts (stack json, architecture graph, symbol index, entry points, module map, code hotspots, context keys, dynamic project context)
**Layer**: Bootstrap — Phase 0 context generation
**Time**: 1 – 5 min
**Phases**: EXECUTE (single pass)
**Use when**: Before any PLAN or IMPLEMENT step; when downstream skills need structured architectural context instead of raw code scanning
**Modifies code**: NO — strictly read-only repository inspection
**Output**: `.aecf/context/STACK_JSON.json`, `AECF_DYNAMIC_PROJECT_CONTEXT.md`, `AECF_ARCHITECTURE_GRAPH.json`, `AECF_SYMBOL_INDEX.json`, `AECF_ENTRY_POINTS.json`, `AECF_MODULE_MAP.json`, `AECF_CODE_HOTSPOTS.json`, `AECF_CONTEXT_KEYS.json`
[📖 Full Documentation](skills/skill_codebase_intelligence.md)

---

### 2. 🚨 `aecf_hotfix`
**Purpose**: Resolve critical production incidents
**Time**: 1 - 3 horas  
**Phases**: DEBUG → HOTFIX_PLAN → HOTFIX_AUDIT → HOTFIX_IMPL → HOTFIX_VERIFY → DEPLOY → POST-MORTEM  
**Use when**: Production down (P1) or critical vulnerability (P1/P2)
[📖 Full Documentation](skills/skill_hotfix.md)

---

### 3. 📚 `aecf_document_legacy`
**Purpose**: Document legacy code before modifying it
**Time**: 30 min - 2 horas  
**Phases**: `INTAKE -> AECF_DOCUMENT_LEGACY` by default; `document_code=True` reroutes through `PLAN -> AUDIT_PLAN -> IMPLEMENT -> AUDIT_CODE -> VERSION -> AECF_DOCUMENT_LEGACY` for documentation-only edits  
**Use when**: You need to document undocumented code, or update docstrings/comments/README text without changing logic
**Modifies code**: Default NO; with `document_code=True`, YES but only documentation surfaces and never executable behavior
[📖 Full Documentation](skills/skill_document_legacy.md)

---

### 4. 🔒 `aecf_security_review`
**Purpose**: Specialized security audit
**Time**: 45 min - 6 horas  
**Phases**: SECURITY_AUDIT → FIX_CRITICAL → FIX_HIGH → DOCUMENT_RESIDUAL_RISKS  
**Use when**: Pre-deployment security check or sensitive code
**🔧 Includes Matrix Auto-Apply Protocol** — auto-evolves `AECF_SECURITY_REVIEW_SEVERITY_MATRIX.md`  
[📖 Full Documentation](skills/skill_security_review.md)

---

### 5. 🔍 `aecf_explain_behavior`
**Purpose**: Analyze and explain current system behavior
**Time**: 15 - 60 min  
**Phases**: EXPLAIN_BEHAVIOR (single phase)  
**Use when**: Understand why the system acts in a certain way, pre-debugging, analysis of unexpected behavior
[📖 Full Documentation](skills/skill_explain_behaviour.md)

---

### 6. 📊 `aecf_code_standards_audit`
**Purpose**: Audit code standards compliance against GLOBAL_CONTEXT and PROJECT_CONTEXT
**Time**: 30 min - 4 hours (depends on scope)
**Phases**: Analyze existing code against all standards (single comprehensive phase)  
**Use when**: Audit legacy code, pre-refactoring, identify technical debt, validate organizational compliance
**Output**: Detailed report of violations classified by severity
**🔧 Includes Matrix Auto-Apply Protocol** — auto-evolves `AECF_CODE_STANDARDS_AUDIT_SEVERITY_MATRIX.md`  
[📖 Full Documentation](skills/skill_code_standards_audit.md)

---

### 7. 🏗️ `aecf_maturity_assessment`
**Purpose**: Formal AECF maturity assessment of the project, team or organization
**Time**: 30 min - 3 horas  
**Phases**: LOAD_FRAMEWORK → COLLECT_EVIDENCE → SCORE_DIMENSIONS → GAP_ANALYSIS → ROADMAP  
**Use when**: Initial baseline, quarterly review, post-incident, pre-certification
**Output**: Assessment con scoring 10 dimensiones (0–5), nivel L1–L5, gap analysis y roadmap  
[📖 Full Documentation](skills/skill_maturity_assessment.md)

---

### 8. ♻️ `aecf_refactor`
**Purpose**: Governed refactoring with prior documentation and regression checking
**Time**: 1.5 - 8 horas  
**Phases**: DOCUMENT_EXISTING → REFACTOR_PLAN → AUDIT_PLAN → TEST_STRATEGY → TEST_IMPL_PRE → REFACTORING → VERIFY_POST → AUDIT_CODE → VERSION  
**Use when**: Post document_legacy, post code_standards_audit, post tech_debt_assessment, complex code
**Output**: Refactored code with verified regression and complete documentation
[📖 Full Documentation](skills/skill_refactor.md)

---

### 9. 💳 `aecf_tech_debt_assessment`
**Purpose**: Comprehensive technical debt assessment with prioritized backlog
**Time**: 30 min - 4 horas  
**Phases**: SCAN → CLASSIFY (6 categories) → QUANTIFY → PRIORITIZE → BACKLOG
**Use when**: Sprint planning, pre-refactoring, technical due diligence, pre-migration
**Output**: Report with classified, quantified findings and prioritized backlog
**🔧 Includes Matrix Auto-Apply Protocol** — auto-evolves `AECF_TECH_DEBT_ASSESSMENT_SEVERITY_MATRIX.md`  
[📖 Full Documentation](skills/skill_tech_debt_assessment.md)

---

### 10. 🚀 `aecf_release_readiness`
**Purpose**: Comprehensive AECF governance pre-release validation complete
**Time**: 15 min - 3 horas  
**Phases**: PHASE_CHECK → AUDIT_CHECK → VERSION_CHECK → DOC_CHECK → SECURITY_CHECK → TEST_CHECK → OPS_CHECK → VERDICT  
**Use when**: Pre-release to production, post new_feature, sprint end, compliance checkpoint
**Output**: Reporte release readiness con GO/NO-GO verdict y score  
[📖 Full Documentation](skills/skill_release_readiness.md)

---

### 11. 🔗 `aecf_dependency_audit`
**Purpose**: Supply chain audit: CVEs, licenses, health and freshness of dependencies
**Time**: 20 min - 3 horas  
**Phases**: DISCOVER → VULN_SCAN → LICENSE_AUDIT → HEALTH_CHECK → FRESHNESS → SUPPLY_CHAIN_RISK  
**Use when**: Pre-release, periodic review, post-alert Dependabot/Snyk, due diligence
**Output**: Report with Supply Chain Risk Score (0–100) and remediation plan
**🔧 Includes Matrix Auto-Apply Protocol** — auto-evolves `AECF_DEPENDENCY_AUDIT_SEVERITY_MATRIX.md`  
[📖 Full Documentation](skills/skill_dependency_audit.md)

---

### 12. 📊 `aecf_data_strategy`
**Purpose**: Design optimal high-volume data ingestion, storage and management strategy
**Layer**: Explorators (Knowledge Extraction)  
**Time**: 20 min - 3 horas  
**Phases**: CHARACTERIZE → CONSTRAINTS → ENUMERATE_STRATEGIES → TRADE-OFF → DECISION_MATRIX → RECOMMEND → SCHEMA_DESIGN → HANDOFF  
**Use when**: Integrate massive data sources (Azure Cost, APIs), decide tables/schema, choose between incremental loading vs. full-load, design deduplication, pre-input for new_feature/plan
**Output**: Report with decision matrix, justified recommendation, schema design and handoff for downstream skills
[📖 Full Documentation](skills/skill_data_strategy.md)

---

### 13. 🔄 `aecf_system_replayability_adaptive`
**Purpose**: Introduce architecture-adaptive replayable trace capability into ANY project, regardless of framework or tech stack  
**Time**: 1.5 - 6 hours  
**Phases**: ARCHITECTURE_DISCOVERY → REPLAY_STRATEGY_SELECTION → REPLAYABILITY_DESIGN → MINIMAL_INJECTION → VALIDATION_BLOCK  
**Use when**: Adding reproducibility/replay to a project, enabling deterministic trace capture for debugging/auditing, compliance traceability, post-document_legacy, post-security_review, pre-release_readiness  
**Output**: Architecture assessment, replay strategy, design docs, generated code (decorators, store, runner), validation report, risk analysis, rollback plan, maturity classification (L1–L5)  
[📖 Full Documentation](skills/skill_system_replayability_adaptive.md)

---

### 14. 📑 `aecf_executive_summary`
**Purpose**: Generate consolidated executive summary for a specific TOPIC
**Time**: 5 - 30 min  
**Phases**: VALIDATE_TOPIC → SCAN_DOCS → ANALYZE → CONSOLIDATE → GENERATE_SUMMARY  
**Use when**: You need a global executive summary of all TOPIC documents
**Requirement**: Mandatory explicit TOPIC
[📖 Full Documentation](skills/skill_executive_summary.md)

---

### 15. 🔬 `aecf_data_classification`
**Purpose**: Discover, extract, and classify all data models, schemas, migrations, and DTOs using deterministic heuristics  
**Layer**: Explorators (Knowledge Extraction)  
**Time**: 15 min - 2 hours  
**Phases**: DISCOVERY → EXTRACTION → CLASSIFICATION → RELATIONSHIP_GRAPH → GOVERNANCE_PROPOSAL → YAML_OUTPUT  
**Use when**: Pre-data governance audit, GDPR/CCPA compliance check, onboarding a project with unknown data landscape, pre-release with PII fields, feeding `aecf_data_governance_audit` with a structured inventory  
**Modifies code**: NO — strictly read-only  
**Output**: `<DOCS_ROOT>/<user_id>/{{TOPIC}}/<NN>_<skill_name>_DATA_CLASSIFICATION.md` with full field inventory, YAML classification output, relationship graph, and governance proposal  
[📖 Full Documentation](skills/skill_data_classification.md)

---

### 16. 🧾 `aecf_document_context_ingestion`
**Purpose**: Ingest and normalize project context from PDF/MD/text/URL documentation sources (including outside workspace folders)
**Layer**: Bootstrap + Knowledge Extraction
**Time**: 15 min - 2 hours
**Phases**: SOURCE_DISCOVERY → EXTRACTION → QUALITY_CHECK → NORMALIZATION → HANDOFF_MAPPING → REPORT
**Use when**: Critical project context lives in external documents (contracts, specs, governance docs), before `aecf_project_context_generator`, onboarding projects with sparse in-repo docs
**Modifies code**: NO — strictly read-only
**Output**: `<DOCS_ROOT>/<user_id>/{{TOPIC}}/<NN>_<skill_name>_DOCUMENT_CONTEXT_INGESTION.md` with source inventory, normalized context blocks, confidence/conflict analysis, and downstream handoff matrix
[📖 Full Documentation](skills/skill_document_context_ingestion.md)
[⚡ Quick Ops](skills/README_DOCUMENT_CONTEXT_INGESTION.md)

---

### 17. 🏗️ `aecf_new_project`
**Purpose**: Bootstrap a complete production-ready project skeleton from scratch with concrete type/framework/db catalog and mandatory intake gate
**Layer**: Bootstrap — Greenfield initialization
**Time**: 15 – 30 min
**Phases**: INTAKE → SCAFFOLD → GENERATE_README → GENERATE_CONTEXT
**Use when**: Starting a brand-new project; team needs consistent structure; onboarding a new service or library; scaffolding standardized skeleton for a known type/stack
**Modifies code**: YES — creates new project files (folders, configs, stubs, README, CI/CD)
**Supported project types**: `web_api_rest` · `web_full_stack` · `cli_tool` · `data_pipeline` · `ml_model_service` · `microservice` · `library_package` · `iac` · `scheduled_job` · `mobile_app`
**Intake gate**: BLOCKS if project_name / project_type / language_framework / database are not confirmed — generates intake doc with specific questions and stops
**Output**: Full project skeleton at `<project_name>/` including `README.md`, `AECF_PROJECT_CONTEXT.md`, `.gitignore`, `.env.example`, CI/CD workflow, and stack-specific source structure
[📖 Full Documentation](skills/skill_new_project.md)

---

## AECF Skill Taxonomy

- **TIER1 — ENTERPRISE_DETERMINISTIC**: formal audits with scoring/severity/decision outputs for compliance and contractual evidence; deterministic pipeline required.
- **TIER2 — STRUCTURED_ANALYSIS**: structured analysis and comparable reporting without contractual scoring requirements; deterministic scoring engine not required.
- **TIER3 — GENERATIVE**: implementation-oriented skills that generate or modify code/artifacts; formal scoring is not required.

| Skill | Tier | Deterministic |
|-------|------|---------------|
| aecf_ai_risk_assessment | TIER1 | true |
| aecf_code_standards_audit | TIER1 | true |
| aecf_data_classification | TIER1 | true |
| aecf_data_governance_audit | TIER1 | true |
| aecf_data_strategy | TIER2 | false |
| aecf_define_impact_metrics | TIER2 | false |
| aecf_dependency_audit | TIER1 | true |
| aecf_document_context_ingestion | TIER2 | false |
| aecf_document_legacy | TIER2 | false |
| aecf_executive_summary | TIER2 | false |
| aecf_explain_behaviour | TIER1 | true |
| aecf_hotfix | TIER3 | false |
| aecf_maturity_assessment | TIER1 | true |
| aecf_model_governance_audit | TIER1 | true |
| aecf_new_feature | TIER3 | false |
| aecf_new_project | TIER3 | false |
| aecf_project_context_generator | TIER2 | false |
| aecf_refactor | TIER3 | false |
| aecf_release_readiness | TIER1 | true |
| aecf_security_review | TIER1 | true |
| aecf_system_replayability_adaptive | TIER3 | false |
| aecf_tech_debt_assessment | TIER1 | true |

---

## Search-First Matrix

This matrix indicates whether the skill must execute explicit repository discovery/search before its first analysis/audit action.

| Skill | Search-First Required | Notes |
|------|------------------------|-------|
| `aecf_explain_behavior` | YES | Mandatory PHASE 0 repository context discovery gate (`WORKING_CONTEXT`) |
| `aecf_code_standards_audit` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_security_review` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_tech_debt_assessment` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_dependency_audit` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_data_classification` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_document_context_ingestion` | YES | Mandatory workspace + external source discovery gate |
| `aecf_project_context_generator` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_system_replayability_adaptive` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_executive_summary` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_maturity_assessment` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_data_governance_audit` | YES | Mandatory `SEARCH-FIRST` discovery gate |
| `aecf_new_feature` | NO | Starts with implementation planning workflow |
| `aecf_new_test_set` | YES | Mandatory discovery of modules or routines, existing tests, coverage tooling, and runnable test commands |
| `aecf_hotfix` | NO | Starts with incident debug workflow |
| `aecf_document_legacy` | NO (conditional) | Discovery appears as optional/conditional path |
| `aecf_refactor` | NO | Starts from documentation/planning baseline |
| `aecf_release_readiness` | NO | Starts with release evidence/check validation |
| `aecf_ai_risk_assessment` | NO | Risk evaluation workflow, no mandatory repo scan gate |
| `aecf_data_strategy` | NO | Strategy design workflow |
| `aecf_define_impact_metrics` | NO | Metrics definition workflow |

---

## Scoring, Checklists & Maturity

Starting with AECF v1.0, **three transversal systems** are integrated into each phase and skill to ensure quantifiable governance, traceability and continuous improvement.

### 📋 Checklists — Enforcement por Fase

Each AECF phase loads a mandatory checklist that must be validated **before** issuing a verdict.

**Location**: `./aecf/checklists/`

| Phase | Checklist | Specialized Section |
|------|-----------|----------------------|
| PLAN | `PLAN_CHECKLIST.md` | Plan Clarity |
| AUDIT_PLAN | `AUDIT_PLAN_CHECKLIST.md` | Audit Integrity |
| IMPLEMENT | `IMPLEMENT_CHECKLIST.md` | Implementation Integrity |
| AUDIT_CODE | `AUDIT_CODE_CHECKLIST.md` | Code Audit Integrity |
| SECURITY_AUDIT | `SECURITY_AUDIT_CHECKLIST.md` | OWASP Coverage |
| TEST_STRATEGY | `TEST_STRATEGY_CHECKLIST.md` | Testing Coverage Design |
| TEST_IMPLEMENTATION | `TEST_IMPLEMENTATION_CHECKLIST.md` | Test Implementation Integrity |
| TEST_EXECUTION_REPORT | `TEST_EXECUTION_REPORT_CHECKLIST.md` | Test Run Evidence |
| AUDIT_TESTS | `AUDIT_TESTS_CHECKLIST.md` | Test Audit Integrity |
| HOTFIX | `HOTFIX_CHECKLIST.md` | Hotfix Validation |

**Common sections** (all phases):
1. Scope Validation
2. Security Controls
3. Resource Management
4. Logging & Observability
5. Compliance with Previous Phase
6. Production Readiness
7. Decision Integrity
8. [Phase Specific Section]

**Enforcement rule**:
```
If ANY checklist item = FALSE → automatic NO-GO
```

📖 Integration Guide: [ENFORCEMENT_INTEGRATION_GUIDE.md](../checklists/ENFORCEMENT_INTEGRATION_GUIDE.md)

---

### 📊 Scoring — Quantitative Evaluation by Phase

Cada fase produce un **AECF_SCORE_REPORT** como parte del `AECF_COMPLIANCE_REPORT`.

**Location**: `./aecf/scoring/`

**Proceso de scoring**:
1. Evaluate each item on the checklist → score (0 = does not comply, 1 = partial, 2 = complies)
2. Apply weights by category
3. Calcular score normalizado (0–100)
4. Determine maturity level
5. Apply automatic verdict rules

**Weights by category**:

| Category | Weight |
|-----------|------|
| Scope Validation | 2 |
| Security Controls | 3 |
| Resource Management | 2 |
| Logging & Observability | 2 |
| Compliance with Previous Phase | 3 |
| Production Readiness | 2 |
| Decision Integrity | 3 |
| Phase-specific sections | 2 |

**Maturity levels (per phase)**:

| Score | Nivel |
|-------|-------|
| 90–100 | ENTERPRISE READY |
| 75–89 | PRODUCTION READY |
| 60–74 | CONDITIONAL |
| 40–59 | HIGH RISK |
| 0–39 | FAIL |

**Verdict rules**:
- Score ≥ 75 → **GO**
- Score 60–74 → **CONDITIONAL GO** (requires user decision)
- Score < 60 → **NO-GO**
- CRITICAL finding → **Score = 0, automatic NO-GO**

**Output en cada fase**:
```markdown
## AECF_SCORE_REPORT

- Raw Score: X/Y
- Normalized Score: Z/100
- Maturity Level: [LEVEL]
- Automatic Verdict: GO / NO-GO / CONDITIONAL
- Critical Findings Present: YES / NO
```

📖 Modelo completo: [AECF_SCORING_MODEL.md](../scoring/AECF_SCORING_MODEL.md)  
📖 Reglas de aplicabilidad: [SCORING_APPLICABILITY.md](../scoring/SCORING_APPLICABILITY.md)

---

### 🏛️ Maturity — Organizational Assessment

The maturity model assesses **how deeply** an organization has adopted AECF governance across 10 dimensions.

**Location**: `./aecf/maturity/`

**10 dimensions of evaluation**:

| # | Dimension | Related AECF phases |
|---|-----------|------------------------|
| 1 | Discovery discipline | `00_DISCOVERY_LEGACY`, `00_DOCUMENT_EXISTING_FUNCTIONALITY` |
| 2 | Plan quality | `00_PLAN`, `02_AUDIT_PLAN`, `03_FIX_PLAN` |
| 3 | Audit enforcement | `02_AUDIT_PLAN`, `05_AUDIT_CODE`, `10_AUDIT_TESTS` |
| 4 | Code governance | `04_IMPLEMENT`, `05_AUDIT_CODE`, `06_FIX_CODE` |
| 5 | Security audit rigor | `17_SECURITY_AUDIT`, `skill_security_review` |
| 6 | Testing maturity | `08_TEST_STRATEGY`, `09_TEST_IMPLEMENTATION`, `10_AUDIT_TESTS` |
| 7 | Incident governance | `00_HOTFIX`, `00_DEBUG`, `skill_hotfix` |
| 8 | Version control discipline | `07_VERSION_MANAGEMENT` |
| 9 | Documentation traceability | Todos los prompts |
| 10 | AI compliance reporting | Audit artifacts + reports |

**Scoring scale (per dimension, 0–5)**:

| Score | Classification |
|-------|---------------|
| 0 | No evidence |
| 1 | Informal (ad-hoc) |
| 2 | Enforcement parcial |
| 3 | Structured |
| 4 | Enforced (automatic gates) |
| 5 | Governed and measurable |

**Organizational maturity levels**:

| Average | Level | Classification |
|----------|-------|---------------|
| 0.0–1.4 | Level 1 | Ad-hoc AI Usage |
| 1.5–2.4 | Level 2 | Structured Prompt Usage |
| 2.5–3.4 | Level 3 | Governed Development Flow |
| 3.5–4.4 | Level 4 | Auditable AI SDLC |
| 4.5–5.0 | Level 5 | Enterprise AI Governance |

**When to evaluate**:

| Trigger | Action |
|---------|--------|
| Initial adoption of AECF | Establish baseline |
| Quarterly review | Re-evaluate and track trends |
| Complete AECF cycle | Validate governance coverage |
| Post-incident | Assess governance gaps |
| Pre-certification | Produce report with evidence |

**Impact of each skill on maturity**:

| Skill | Impacted Dimensions |
|-------|------------------------|
| `skill_new_feature` | 2, 3, 4, 6, 8, 9 |
| `skill_hotfix` | 3, 4, 7, 8 |
| `skill_security_review` | 5, 9, 10 |
| `skill_document_legacy` | 1, 9 |
| `skill_explain_behaviour` | 1, 9 |
| `skill_code_standards_audit` | 4, 9, 10 |
| `skill_maturity_assessment` | ALL (1–10) — evaluates all dimensions |
| `skill_refactor` | 3, 4, 6, 8, 9 |
| `skill_tech_debt_assessment` | 4, 9, 10 |
| `skill_release_readiness` | 3, 6, 8, 9, 10 |
| `skill_dependency_audit` | 5, 9, 10 |

📖 Modelo: [AECF_MATURITY_MODEL.md](../maturity/AECF_MATURITY_MODEL.md)  
📖 Scoring: [AECF_MATURITY_SCORING.md](../maturity/AECF_MATURITY_SCORING.md)  
📖 Template: [AECF_MATURITY_ASSESSMENT_TEMPLATE.md](../maturity/AECF_MATURITY_ASSESSMENT_TEMPLATE.md)

---

### 🔗 Flujo Integrado: Skill → Checklist → Scoring → Maturity

```
┌──────────────────────────────────────────────────────────────┐
│                    SKILL EXECUTION                          │
│                                                              │
│  ┌────────┐    ┌────────────┐    ┌──────────────┐           │
│  │ Phase  │───►│ CHECKLIST  │───►│ SCORING      │           │
│  │ Prompt │    │ Validation │    │ Calculation  │           │
│  └────────┘    └─────┬──────┘    └──────┬───────┘           │
│                      │                  │                    │
│                      ▼                  ▼                    │
│              ┌──────────────┐   ┌──────────────┐            │
│              │ COMPLIANCE   │   │ SCORE        │            │
│              │ REPORT       │   │ REPORT       │            │
│              └──────┬───────┘   └──────┬───────┘            │
│                     │                  │                     │
│                     ▼                  ▼                     │
│              ┌──────────────────────────────┐               │
│              │    GO / NO-GO / CONDITIONAL   │               │
│              └──────────────┬───────────────┘               │
└─────────────────────────────┼───────────────────────────────┘
                              │
                              ▼
              ┌──────────────────────────────┐
              │ MATURITY ASSESSMENT          │
              │ (Aggregated across phases    │
              │  and projects — quarterly)   │
              └──────────────────────────────┘
```

**In summary**:
- **Checklists** → binary enforcement by phase (does it comply or not?)
- **Scoring** → quantitative evaluation by phase (how well does it comply?)
- **Maturity** → periodic organizational evaluation (how governed is the process?)

---

## Complete Usage Examples

### Example 1: New Functionality (GO/NO-GO Flow)

#### Scenario:
Implement endpoint export of reports in PDF and CSV.

#### Invocation:
```
User: "I need to implement an endpoint /api/reports/export that allows
Export reports in PDF and CSV format with filters by date and user.
Must include permissions and pagination control. @aecf run skill=new_feature topic=report_export prompt=\"Implement endpoint /api/reports/export for PDF/CSV report export with date/user filters, permissions, and pagination\""
```

#### Execution Flow:

**Phase 1: PLAN → GO**
```
[AI executes 00_PLAN.md]

Output: documentation/report_export/AECF_01_PLAN.md

## Range
- Endpoint: GET /api/reports/export?format={pdf|csv}&start_date=...&end_date=...&user_id=...
- Supported formats: PDF, CSV
- Filters: date (mandatory), user (optional for admins)
- Authentication: JWT required
- Authorization: User sees their reports, admin sees all

## Design decisions
- Use WeasyPrint to PDF
- CSV con pandas
- Pagination: max 1000 records per request
- Rate limiting: 10 exports/user/hora

## Implementation plan
1. Crear endpoint en app/api/reports.py
2. Implement export service
3. Permission validation
4. Rate limiting middleware
5. Unit tests and integration
6. API documentation

[Output completo...]
```

**Phase 2: AUDIT_PLAN → NO-GO**
```
[AI executes 02_AUDIT_PLAN.md]

Output: documentation/report_export/AECF_02_AUDIT_PLAN.md

## Critical findings
[None]

## Ambiguities detected
1. It is missing to specify which fields are included in the export
2. There is no mention of handling large reports (> 10K records)
3. Rate limiting does not cover per IP (only per authenticated user)

## Questionable decisions
- Pagination of 1000 records may be insufficient for large exports
- Falta estrategia de async processing para exports pesados

## Final Verdict: NO-GO

Reason: Ambiguities about exported fields and handling of large volumes.
```

**Phase 2b: FIX_PLAN → Fix**
```
[AI executes 03_FIX_PLAN.md]

Output: documentation/report_export/AECF_03_FIX_PLAN.md

## Changes made:
1. Added "Export Fields" section with complete list
2. Limit of 5K records per export
3. For exports > 5K: async processing with notification email
4. Rate limiting por usuario + rate limiting global por IP

[corrected PLAN complete...]

CORRECTED PLAN READY FOR AUDIT
```

**Phase 2 retry: AUDIT_PLAN → GO**
```
[AI executes 02_AUDIT_PLAN.md on corrected PLAN]

Output: documentation/report_export/AECF_04_AUDIT_PLAN.md

## Critical findings
[None]

## Risks not covered
[All covered]

## Final verdict: GO ✅

AUDIT_PLAN READY FOR IMPLEMENT
```

**Phase 3: TEST_STRATEGY**
```
[AI executes 08_TEST_STRATEGY.md]

Output: documentation/report_export/AECF_05_TEST_STRATEGY.md

## Testing Strategy

### Tests Unitarios (80% coverage target):
- test_export_service_pdf_generation
- test_export_service_csv_generation
- test_permission_validation_user
- test_permission_validation_admin
- test_rate_limiting_enforced

### Integration Tests:
- test_export_endpoint_pdf_success
- test_export_endpoint_csv_success
- test_export_endpoint_unauthorized
- test_export_large_dataset_async

### Tests E2E:
- test_full_export_flow_user
- test_full_export_flow_admin

[Complete output with detailed cases...]

TEST_STRATEGY COMPLETADA
```

**Phase 4-7: IMPLEMENT → TEST_IMPL → AUDIT_TESTS → AUDIT_CODE → GO**
```
[AI executes 04_IMPLEMENT.md]
→ Implemented code in app/api/reports.py, app/services/export_service.py
→ Output: documentation/report_export/AECF_06_IMPLEMENT.md

[AI executes 09_TEST_IMPLEMENTATION.md]
→ Implemented tests in tests/test_reports_export.py
→ Coverage: 89%
→ Output: documentation/report_export/AECF_07_TEST_IMPLEMENTATION.md

[AI executes 10_AUDIT_TESTS.md]
→ Verdict: GO ✅
→ Output: documentation/report_export/AECF_08_AUDIT_TESTS.md

[AI executes 05_AUDIT_CODE.md]
→ Verdict: GO ✅ (no critical findings)
→ Output: documentation/report_export/AECF_09_AUDIT_CODE.md
```

**Phase 8: VERSION**
```
[AI executes 07_VERSION_MANAGEMENT.md]

Version: 1.4.2 → 1.5.0 (MINOR - new functionality)
CHANGELOG updated
Output: documentation/report_export/AECF_10_VERSION.md

✅ FEATURE COMPLETE AND READY FOR DEPLOY
```

**Total time**: ~2.5 hours (1 FIX_PLAN iteration)

---

### Example 2: Critical Hotfix (P1 Incident)

#### Scenario:
Authentication API returns 500, users cannot log in.

#### Invocation:
```
User: "🚨 INCIDENT P1: API /auth/login returns 500. Users cannot
log in. Error in logs: 'Connection pool exhausted'. @aecf run skill=hotfix topic=prod_auth_500 prompt=\"INCIDENT P1: API /auth/login returns 500 with connection pool exhausted\""
```

#### Execution Flow:

**[10:15] Detection**
```
[AI executes triage]
Severity: P1 ✅
Impact: Critical - All users
Incident response activated
```

**[10:17] Phase 1: DEBUG → RCA**
```
[AI executes 00_DEBUG.md - RUNTIME mode]

Log analysis:
- DB connection pool: size=10
- Active connections: 10/10
- Peak traffic: 500 requests/second
- Pool exhausted → requests en espera → timeout → 500 error

ROOT CAUSE: Pool size=10 insufficient for peak traffic

Output: documentation/prod_auth_500/AECF_01_RCA.md
```

**[10:25] Phase 2: HOTFIX_PLAN**
```
[AI executes 00_HOTFIX.md - PLAN phase]

PROPOSED FIX:
Archivo: config/database.py
Cambio: pool_size=10 → pool_size=50

Alternativas descartadas:
- Restart service: Does not resolve root cause
- Scale horizontally: Takes > 30 min

Rollback plan: Revertir pool_size a 10

Critical Tests:
1. test_database_connection_pool_size
2. test_concurrent_logins_100_users

Output: documentation/prod_auth_500/AECF_01_HOTFIX.md (PLAN section)
```

**[10:35] Phase 3: HOTFIX_AUDIT → GO**
```
[AI executes 00_HOTFIX.md - AUDIT phase]

✅ Fix solves the problem
✅ Does not introduce vulnerabilities
✅ Does not break functionality
✅ Rollback viable
⚠️ WARNING: pool_size=50 may impact DB, monitor

VERDICT: GO ✅
```

**[10:40] Phase 4: HOTFIX_IMPLEMENT**
```
[AI executes 00_HOTFIX.md - IMPLEMENT phase]

Code:
# HOTFIX: PROD-AUTH-500 2026-02-10
# ROOT CAUSE: DB pool exhausted
# SOLUTION: Increase pool to 50
# ROLLBACK: Revert to 10
pool_size = 50  # was: 10

Tests implementados:
✅ test_database_connection_pool_size PASSED
✅ test_concurrent_logins_100_users PASSED

Output: documentation/prod_auth_500/AECF_01_HOTFIX.md (IMPLEMENT section)
```

**[10:55] Phase 5: HOTFIX_VERIFY**
```
[AI executes 00_HOTFIX.md - VERIFY phase]

✅ Tests pasan
✅ Smoke test en staging OK
✅ Bug reproduced → SOLVED
✅ Rollback plan verificado

Ready for deploy
```

**[11:00] Phase 6: DEPLOY**
```
[AI executes 00_HOTFIX.md - DEPLOY phase]

Tag: hotfix-20260210-1100-auth-pool-fix
Deploy to production: STARTED
Active monitoring: ON
```

**[11:05] Deploy completed**

**[11:05-11:35] Phase 7: MONITORING**
```
✅ API /auth/login: 200 OK
✅ Latency: 150ms (normal)
✅ Error rate: 0%
✅ DB connections: 15/50 (healthy)

[11:35] ✅ INCIDENT RESOLVED
```

**[Next day] Phase 8: POST-MORTEM**
```
[AI executes 00_HOTFIX.md - POST-MORTEM]

Timeline: 10:15 detection → 11:35 resolved (1h 20min)

Definitive solution?: NO (temporary)
Reason: Fixed pool size not scaling

ACTION ITEMS:
- [ ] Implementar dynamic pool scaling (next sprint)
- [ ] Add pool usage alerts
- [ ] Load testing regular

Output: documentation/prod_auth_500/AECF_01_HOTFIX.md (POST-MORTEM section)
```

**Total time:** 1h 20min (detection → resolution)  
**Downtime:** 1h 20min

---

### Example 3: Document Legacy Functionality

#### Scenario:
I need to modify the legacy authentication module to add MFA.

#### Invocation:
```
User: "I need to document authentication module in app/auth/ before
agregar MFA. @aecf run skill=document_legacy topic=user_auth_mfa prompt=\"I need to document authentication module in app/auth/ before adding MFA\""
```

#### Execution Flow:

**Phase 1: DOCUMENT_EXISTING**
```
[AI executes 00_DOCUMENT_EXISTING_FUNCTIONALITY.md]

Analysis:
Entry points:
- app/auth/login.py: login_user()
- app/auth/session.py: create_session()
- app/auth/middleware.py: @auth_required

Flow:
1. POST /auth/login
2. login_user() valida con DB
3. create_session() genera JWT
4. Token en Redis
5. @auth_required verifica token

Dependencies:
- Internal: app/models/user.py, app/database/
- External: PyJWT, Redis, bcrypt

Side effects:
- Write to Redis
- Logs en app.log
- Session cookie

Observed risks:
- Sin rate limiting
- JWT without rotation
- Session timeout hardcoded (24h)

Unknowns:
- How are sessions invalidated in logout?
- Cleanup of expired sessions?

Output:
- documentation/user_auth_mfa/AECF_01_DOCUMENTATION.md
- documentation/user_auth_mfa/AECF_01_FLOW_HIGHLEVEL.mmd
- documentation/user_auth_mfa/AECF_01_FLOW_TECHNICAL.mmd
```

**Phase 2: User Reviews**
```
User: "Documentation correct. I will modify to add MFA."
```

**Phase 3: DISCOVERY_LEGACY**
```
[AI executes 00_DISCOVERY_LEGACY.md]

Modification scope:
- Files: app/auth/login.py, app/auth/mfa.py (new)
- Limits: DO NOT touch session.py or middleware.py

Output: documentation/user_auth_mfa/AECF_02_DISCOVERY.md

DELIMITED FUNCTIONALITY FOR AECF ✅
```

**Phase 4: Continue to PLAN**
```
User: "Now run PLAN to add MFA"

[AI continues with normal AECF flow]
[Executes 00_PLAN.md using DISCOVERY as context]
[Then continues with aecf_new_feature flow...]
```

**Total time:** ~45 min (documentation + discovery)

---

### Example 4: Security Review with Vulnerabilities

#### Scenario:
Security review of new payment endpoint before deploying.

#### Invocation:
```
User: "Security review for endpoint /api/payments/ before deploy.
@aecf run skill=security_review topic=payment_api_security prompt=\"Security review for endpoint /api/payments/ before deploy\""
```

#### Execution Flow:

**Phase 1: SECURITY_AUDIT**
```
[AI executes 17_SECURITY_AUDIT.md]

EXECUTIVE SUMMARY:
Total vulnerabilities: 5
REVIEWS: 1
ALTAS: 2
MEDIAS: 1
LOSSES: 1

VULNERABILIDADES:

[CRIT-001] SQL Injection en payment history
CVSS: 9.8
Location: app/api/payments.py:145
Code: query = f"SELECT * FROM payments WHERE user_id = {user_id}"
Impacto: Full DB access

[HIGH-001] Missing authentication en /api/payments/stats
CVSS: 7.5
Problema: Sin @auth_required
Impact: Anyone sees global stats

[HIGH-002] Payment amount without server-side validation
CVSS: 7.2
Problem: Unvalidated request amount
Impact: User can modify price

[MED-001] Falta rate limiting
CVSS: 5.3

[LOW-001] API version exposed
CVSS: 2.1

VERDICT: NO-GO (CRITICAL vulnerability)

Output: documentation/payment_api_security/AECF_01_SECURITY_AUDIT.md
```

**Phase 2: FIX_CRITICAL**
```
[AI executes 06_FIX_CODE.md for CRIT-001]

CORRECTED CODE:
# BEFORE (VULNERABLE):
query = f"SELECT * FROM payments WHERE user_id = {user_id}"

# AFTER (SAFE):
query = "SELECT * FROM payments WHERE user_id = ?"
cursor.execute(query, (user_id,))

✅ CRIT-001 CORREGIDA

Output: documentation/payment_api_security/AECF_02_FIX_SECURITY_CRITICAL.md
```

**Phase 3: FIX_HIGH**
```
[AI executes 06_FIX_CODE.md for HIGH-001, HIGH-002]

FIX HIGH-001:
@app.route('/api/payments/stats')
@admin_required # ← ADDED
def get_payment_stats():
    ...

FIX HIGH-002:
# Validar amount server-side contra DB
expected_amount = Cart.query.get(cart_id).calculate_total()
if provided_amount != expected_amount:
    return error(400, 'Amount mismatch')

✅ HIGH-001 CORREGIDA
✅ HIGH-002 CORREGIDA

Output: documentation/payment_api_security/AECF_03_FIX_SECURITY_HIGH.md
```

**Phase 4: Risk Decision**
```
User: "MED-001 (rate limiting): postpone a next sprint.
LOW-001 (version header): accept risk."
```

**Phase 5: RESIDUAL_RISKS**
```
[AI generates residual risks document]

## Accepted Vulnerabilities

### [MED-001] Falta rate limiting
Severity: MEDIUM
Justification: Urgent deployment, compensatory monitoring
Compensatory measures:
- Alerts for > 10 attempts/user/hour
- Dashboard de monitoring
Plan: Implement in sprint 2026-Q1-S3
Approved by: John Doe (Lead Engineer), 2026-02-10

### [LOW-001] API version exposed
Severity: LOW
Rationale: Minor information disclosure, useful for debugging
No mitigation required
Approved by: Jane Smith (Security Lead), 2026-02-10

Output: documentation/payment_api_security/AECF_04_RESIDUAL_RISKS.md
```

**Phase 6: CLEARANCE**
```
✅ No CRITICAL vulnerabilities
✅ HIGH vulnerabilities fixed
✅ MEDIUM/LOW vulnerabilities documented and approved

SECURITY CLEARANCE GRANTED ✅
APPROVED CODE FOR DEPLOY
```

**Total time:** ~3 hours (with corrections)

---

## GO / NO-GO Flow Examples

### Flow 1: Clean Pass (All GO)

```
PLAN → AUDIT_PLAN (GO) → IMPLEMENT → AUDIT_CODE (GO) → PRODUCTION
```

**Time:** Minimum (no iterations)
**When:** Well-defined plan, correct implementation

---

### Flow 2: Plan Issues (NO-GO en AUDIT_PLAN)

```
PLAN → AUDIT_PLAN (NO-GO) → FIX_PLAN → AUDIT_PLAN (GO) → IMPLEMENT → ...
```

**Time:** +20-40 min per iteration
**When:** Plan ambiguo o incompleto

---

### Flow 3: Code Issues (NO-GO en AUDIT_CODE)

```
... → IMPLEMENT → AUDIT_CODE (NO-GO) → FIX_CODE → AUDIT_CODE (GO) → PRODUCTION
```

**Time:** +30-60 min per iteration
**When:** Bugs, security issues, missing features

---

### Flow 4: Multiple Iterations

```
PLAN → AUDIT_PLAN (NO-GO) → FIX_PLAN → 
AUDIT_PLAN (NO-GO) → FIX_PLAN → 
AUDIT_PLAN (GO) → IMPLEMENT → 
AUDIT_CODE (NO-GO) → FIX_CODE → 
AUDIT_CODE (GO CONDICIONAL) → [Decision] → PRODUCTION
```

**Time:** Can be extended significantly
**When:** Complex problem, unclear requirements

---

### Flow 5: GO CONDICIONAL

```
... → AUDIT_CODE (GO CONDICIONAL) → [User Decision]
├─→ Accept risk → PRODUCTION (with documented residual risks)
└─→ Mitigate → FIX_CODE → AUDIT_CODE (GO) → PRODUCTION
```

**Time:** Depends on decision
**When:** WARNING but not blocking findings

---

## Choosing the Right Skill

### Decision Tree:

```
What do you need to do?
│
├─ Implement new functionality
│  └─→ aecf_new_feature
│
├─ Discover or implement missing tests for existing code
│  └─→ aecf_new_test_set
│
├─ Down production or critical vulnerability
│  └─→ aecf_hotfix
│
├─ Modify legacy code without documentation
│ ├─ Documentation only → aecf_document_legacy (stop)
│  └─ Documentar + modificar → aecf_document_legacy + aecf_new_feature
│
├─ Audit code security
│  └─→ aecf_security_review
│
└─ Case not covered
└─→ Run individual prompts manually
```

---

## Troubleshooting

### Issue: Skill takes too long
**Causes:**
- Multiple NO-GOs (ill-defined plan)
- Complex code
- Many vulnerabilities in security review

**Solutions:**
- Clarify requirements BEFORE executing skill
- Split feature into multiple smaller TOPICs
- For security: fix critical vulnerabilities first, then medium/low ones

---

### Issue: Skill stops unexpectedly
**Causes:**
- Lack of context (files not found)
- User decision required (CONDITIONAL GO)

**Solutions:**
- Verify that all necessary files exist
- For GO CONDITIONAL: make an explicit decision to accept or mitigate

---

### Issue: Incorrect generated documentation
**Causes:**
- Insufficient context provided
- Very complex code

**Solutions:**
- Provide more context when invoking skill
- Manually review and correct documentation
- Re-run specific phase with corrections

---

### Issue: Repeated NO-GO Verdicts
**Causes:**
- Unclear requirements
- Fundamental architectural problem

**Solutions:**
- Stop and clarify requirements with stakeholders
- Consider if the approach is correct
- May require rethinking the solution

---

## Best Practices

### ✅ Do:
- Provide clear context when invoking skill
- Review outputs from each phase before continuing
- Make explicit decisions in GO CONDITIONAL
- Formally document residual risks
- Use short, descriptive TOPICs (< 20 chars)

### ❌ Don't:
- Skip skill phases manually
- Ignore undocumented WARNING findings
- Use hotfix for non-critical bugs
- Modify code without documentation in legacy systems
- Deploy with CRITICAL vulnerabilities

---

## Support & Feedback

To report issues or suggest improvements to skills:
- Documentar el problema en `documentation/skills_feedback/`
- Include: skill used, phase that failed, full context

---

**SKILLS REFERENCE GUIDE v1.1**  
**Last updated:** 2026-02-12

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check




