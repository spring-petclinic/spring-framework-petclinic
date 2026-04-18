# AECF SKILL DISPATCHER — Execution Autopilot

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This dispatcher is a MANDATORY system-level component of AECF.

It MUST be loaded alongside:
- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

Extension rule (mandatory): for every process file loaded by this dispatcher, if a sibling `<name>_ext.<ext>` exists in the same folder, it MUST be loaded immediately after the base file and applied as extension/override layer.

This is the SINGLE AUTHORITATIVE document for skill invocation handling.

------------------------------------------------------------

## PURPOSE

This dispatcher eliminates the need for verbose, structured prompts when invoking AECF skills. It allows developers to use **natural, simple language** and guarantees that the full AECF execution protocol is followed automatically.

**Problem solved**: A developer should NEVER need to specify execution mode, output paths, numbering conventions, governance rules, or template enforcement. The dispatcher handles ALL of this automatically.

------------------------------------------------------------

## 1. SKILL INVOCATION RECOGNITION

### Trigger Patterns

The dispatcher activates when the user's message matches ANY of these patterns (case-insensitive, language-agnostic):

#### Pattern A: Explicit skill reference
```
skill: <skill_name>
skill <skill_name>
usar skill: <skill_name>
usar skill <skill_name>
ejecuta skill: <skill_name>
ejecutar skill: <skill_name>
run skill: <skill_name>
run skill <skill_name>
execute skill: <skill_name>
execute skill <skill_name>
use skill: <skill_name>
use skill <skill_name>
```

#### Pattern D: Structured triad invocation (MANDATORY PRIORITY)
If the message contains the three markers `skill` + `TOPIC` + `prompt` (in any order, case-insensitive),
the dispatcher MUST treat it as an explicit skill invocation, even if separators are inconsistent
(e.g., with or without `:` after `skill`).

Valid examples:
```
use skill aecf_new_feature TOPIC:login prompt: una pantalla que simule login
use skill: aecf_new_feature TOPIC: login prompt: mock de endpoint
skill aecf_hotfix TOPIC:auth_outage prompt: error 500 en login
```

Deterministic behavior for Pattern D:
1. Resolve skill from token after `skill`/`use skill`.
2. Resolve TOPIC from `TOPIC:` value.
3. Treat `prompt:` value as the task description input for the selected skill.
4. Immediately enter Section 3 (MANDATORY EXECUTION PROTOCOL).
5. Direct implementation outside skill flow is INVALID.

#### Pattern B: Implicit skill intent (AI MUST recognize these)
```
"audita los estándares del código" → skill_code_standards_audit
"revisa los estándares" → skill_code_standards_audit
"review code standards" → skill_code_standards_audit
"cómo ingestar los datos de [fuente]" → skill_data_strategy
"diseñar estrategia de datos para [fuente]" → skill_data_strategy
"¿tablas separadas o todo en una?" → skill_data_strategy
"add replay capability" → skill_system_replayability_adaptive
"make this system replayable" → skill_system_replayability_adaptive
"introduce execution traceability" → skill_system_replayability_adaptive
"deterministic replay for [module]" → skill_system_replayability_adaptive
"documenta el código legacy" → skill_document_legacy
"explica por qué [comportamiento]" → skill_explain_behaviour
"implementa [feature]" → skill_new_feature
"dime que tests faltan en [modulo]" → skill_new_test_set
"haz un barrido de tests de [modulo]" → skill_new_test_set
"propon tests para estas rutinas" → skill_new_test_set
"analiza coverage y tests pendientes" → skill_new_test_set
"generate a test set for this module" → skill_new_test_set
"implement missing tests for this code" → skill_new_test_set
"hotfix: [problema]" → skill_hotfix
"security review de [módulo]" → skill_security_review
"data governance audit de [módulo]" → skill_data_governance_audit
"model governance audit de [módulo]" → skill_model_governance_audit
"evaluar riesgo IA de [feature]" → skill_ai_risk_assessment
"define impact metrics para [feature]" → skill_define_impact_metrics
"clasifica los campos del modelo" → skill_explorator_data_classification
"clasifica los modelos ORM" → skill_explorator_data_classification
"qué campos PII tiene el proyecto" → skill_explorator_data_classification
"inventario de datos" → skill_explorator_data_classification
"descubre los modelos de datos" → skill_explorator_data_classification
"classify ORM fields" → skill_explorator_data_classification
"data classification of [scope]" → skill_explorator_data_classification
"explorar modelos" → skill_explorator_data_classification
"ingestar documentación de contexto" → skill_document_context_ingestion
"cargar pdf para contexto del proyecto" → skill_document_context_ingestion
"analiza estos documentos externos" → skill_document_context_ingestion
"build context from docs" → skill_document_context_ingestion
"ingest project documentation from pdf/md" → skill_document_context_ingestion
"crear nuevo proyecto" → skill_new_project
"crea la estructura del proyecto" → skill_new_project
"bootstrap a new project" → skill_new_project
"inicializar proyecto" → skill_new_project
"new project scaffold" → skill_new_project
"quiero empezar un proyecto nuevo" → skill_new_project
"scaffold project" → skill_new_project
"crear proyecto [tipo]" → skill_new_project
"create project skeleton" → skill_new_project
"inicializa un nuevo repositorio con estructura" → skill_new_project
"analiza la arquitectura del proyecto" → skill_codebase_intelligence
"genera el contexto de inteligencia" → skill_codebase_intelligence
"build codebase intelligence" → skill_codebase_intelligence
"analyze repository structure" → skill_codebase_intelligence
"generate architecture graph" → skill_codebase_intelligence
"crea el índice de símbolos del proyecto" → skill_codebase_intelligence
"detect entry points and hotspots" → skill_codebase_intelligence
```

#### Pattern C: Skill filename reference (any format)
```
skill_code_standards_audit
skill_code_standards_audit.md
aecf_code_standards_audit
code_standards_audit
```

### Skill Resolution Table

| User says (any of) | Resolves to | Skill file |
|---------------------|-------------|------------|
| code_standards, standards_audit, audita estándares, revisa estándares, code standards audit | `aecf_code_standards_audit` | skills/skill_code_standards_audit.md |
| new_feature, nueva feature, implementar, implement | `aecf_new_feature` | skills/skill_new_feature.md |
| new_test_set, test_set, tests faltantes, barrido de tests, missing tests, test coverage hardening, generate test set, implement missing tests | `aecf_new_test_set` | skills/skill_new_test_set.md |
| hotfix, emergencia, producción caída, P1, P2 | `aecf_hotfix` | skills/skill_hotfix.md |
| document_legacy, documentar legacy, documentar código | `aecf_document_legacy` | skills/skill_document_legacy.md |
| security_review, security audit, auditoría seguridad | `aecf_security_review` | skills/skill_security_review.md |
| explain_behavior, explicar comportamiento, por qué hace | `aecf_explain_behavior` | skills/skill_explain_behaviour.md |
| maturity_assessment, evaluación madurez, maturity, nivel madurez, baseline maturity | `aecf_maturity_assessment` | skills/skill_maturity_assessment.md |
| refactor, refactorizar, reestructurar, limpiar código, clean code | `aecf_refactor` | skills/skill_refactor.md |
| tech_debt, deuda técnica, technical debt, evaluar deuda, debt assessment | `aecf_tech_debt_assessment` | skills/skill_tech_debt_assessment.md |
| release_readiness, release ready, listo para release, pre-release, ready to deploy | `aecf_release_readiness` | skills/skill_release_readiness.md |
| dependency_audit, auditar dependencias, dependency check, supply chain, vulnerabilidades deps | `aecf_dependency_audit` | skills/skill_dependency_audit.md |
| data_strategy, estrategia de datos, diseñar ingestión, data ingestion, pipeline de datos, cómo ingestar, tablas separadas, deduplicación, ETL strategy, ELT strategy | `aecf_data_strategy` | skills/skill_data_strategy.md |
| data_governance_audit, data governance, gobierno de datos, clasificación de datos, data lineage, retención de datos | `aecf_data_governance_audit` | skills/skill_data_governance_audit.md |
| model_governance_audit, model governance, gobierno de modelo, inferencia auditable, model impact | `aecf_model_governance_audit` | skills/skill_model_governance_audit.md |
| ai_risk_assessment, riesgo IA, AI risk, risk assessment IA, evaluación riesgo IA | `aecf_ai_risk_assessment` | skills/skill_ai_risk_assessment.md |
| define_impact_metrics, impact metrics, métricas de impacto, baseline y target, KPI governance | `aecf_define_impact_metrics` | skills/skill_define_impact_metrics.md |
| system_replayability, replayability, replay, reproducibility, replay trace, replayable, traceability adaptive, deterministic replay, execution trace, replay capability | `aecf_system_replayability_adaptive` | skills/skill_system_replayability_adaptive.md |
| project_context, generar contexto, generate context, bootstrap context, analizar proyecto, scan project, workspace context, AECF_PROJECT_CONTEXT | `aecf_project_context_generator` | skills/skill_project_context_generator.md |
| document_context_ingestion, ingestar documentación, contexto desde pdf, contexto desde md, external docs context, ingest documents | `aecf_document_context_ingestion` | skills/skill_document_context_ingestion.md |
| executive_summary, resumen ejecutivo, generar resumen ejecutivo, consolidated summary | `aecf_executive_summary` | skills/skill_executive_summary.md |
| explorator_data_classification, explorator data classification, clasifica campos, clasifica modelos ORM, clasifica los modelos, qué campos PII, inventario de datos, descubre modelos de datos, classify ORM fields, data classification, explorar modelos, clasificación de campos | `aecf_explorator_data_classification` | skills/skill_explorator_data_classification.md |
| new_project, nuevo proyecto, scaffold project, crear proyecto, project bootstrap, inicializar proyecto, project skeleton, create project, bootstrap project, nueva app, nueva api, nuevo servicio | `aecf_new_project` | skills/skill_new_project.md |
| codebase_intelligence, codebase intelligence, inteligencia de código, analyze architecture, architecture graph, symbol index, analizar arquitectura, entry points, hotspots, grafo de dependencias, intelligence context | `aecf_codebase_intelligence` | skills/skill_codebase_intelligence.md |

---

## 2. AUTOMATIC PARAMETER RESOLUTION

When a skill is triggered, the dispatcher MUST automatically resolve ALL required parameters. The user should NOT be asked unless truly ambiguous.

### 2.1 TOPIC Resolution

Priority order:
1. **User explicitly provides TOPIC**: Use it directly
   - `TOPIC: STANDARDS` → use "STANDARDS"
   - `TOPIC: auth_module` → use "auth_module"
2. **Infer from user's description**: If user describes scope or intent
   - "revisa los estándares del backend" → TOPIC: "backend_standards"  
   - "audita el módulo de pagos" → TOPIC: "payment_standards"
3. **Infer from scope**: If scope is provided but not TOPIC
   - scope: `sentinel-multichat/backend` → TOPIC: "sentinel_backend"
4. **Use chat context**: Use conversation title or subject
5. **ONLY IF ALL ABOVE FAIL**: Ask the user (ONE question, not multiple)

Normalization rules:
- Max 20 characters
- snake_case
- lowercase
- No spaces

### 2.2 Scope Resolution

Priority order:
1. **User explicitly provides scope**: Use it
2. **Infer from user's description**: "revisa el código generado" → look for recently changed/generated code in workspace
3. **Infer from workspace structure**:
   - If workspace has clear project directories, use them
   - If `AECF_PROJECT_CONTEXT.md` exists, extract scope from it
4. **Default**: Use workspace root (`./ `)
5. **ONLY IF genuinely ambiguous**: Ask user ONCE: "¿Qué directorio(s) debo auditar?"

### 2.3 TOPIC Directory

Once TOPIC is resolved, ALL outputs go to:
```
documentation/{{TOPIC}}/
```

### 2.4 Sequential Numbering

ALWAYS:
1. Check existing files in `documentation/{{TOPIC}}/`
2. Find the highest `AECF_<NN>_` number
3. Use `<NN+1>` as next number
4. If directory is empty or new, start at `01`

Format: Two-digit zero-padded: `01`, `02`, `03`, ... `10`, `11`...

---

## 3. MANDATORY EXECUTION PROTOCOL

When a skill invocation is recognized, execute these steps IN ORDER. No step may be skipped.

### Step 1: ACKNOWLEDGE
```
✅ Skill recognized: <skill_name>
📌 TOPIC: <resolved_topic>
📂 Scope: <resolved_scope>
🔢 Next number: <NN>
📄 Output: documentation/<TOPIC>/AECF_<NN>_<DOCUMENT_NAME>.md
```

Display this to the user BEFORE starting execution. This provides transparency and allows correction if something was misresolved.

### Step 2: LOAD CONTEXTS (Mandatory, Silent)
Load in order:
1. `aecf_prompts/AECF_SYSTEM_CONTEXT.md`
2. `<workspace_root>/AECF_PROJECT_CONTEXT.md` (if exists)
3. `aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md`
4. **`aecf_prompts/templates/TEMPLATE_HEADERS.md`** (universal metadata standard)
5. The specific skill file from `skills/`
6. Any referenced template from `templates/` (read its `@METADATA` directive)
7. Any referenced checklist from `checklists/`
8. Any referenced phase prompt from `prompts/` (**must include `@METADATA` header**)

### Step 2.1: APPLY `_ext` LAYERS (Mandatory, Deterministic)
For EACH file loaded in Step 2 (and any additional process file loaded later during execution):

1. Check for sibling extension file in the same directory:
   - Base: `<name>.<ext>`
   - Extension: `<name>_ext.<ext>`
2. If extension exists, load it immediately after the base.
3. Apply extension precedence:
   - `_ext` may add, modify, or cancel sections from the base.
   - On conflict, `_ext` content wins.
4. Continue execution using the merged effective document.

This rule applies to contexts, dispatcher-referenced files, skills, prompts, templates, scoring files, checklists, governance specs, and equivalent runtime process artifacts.

### Step 2.2: PROMPT METADATA GATE (Mandatory)
For EACH prompt file loaded from `aecf_prompts/prompts/`:

1. Validate that the prompt contains an `@METADATA` header at the top section.
2. Validate at minimum these rows inside the prompt metadata directive:
   - `Document Type`
   - `Phase`
3. If missing/incomplete, treat execution as INVALID and stop before phase execution.
4. Resolve metadata using `templates/TEMPLATE_HEADERS.md` as canonical schema.

### Step 3: EXECUTE SKILL
Execute the skill's defined workflow completely.
- Follow the skill's execution flow
- Apply all AECF rules from SYSTEM_CONTEXT (including `_ext` overlays)
- Apply governance from EXECUTIVE_SUMMARY_GOVERNANCE
- Use templates as specified
- Use prompt-level `@METADATA` from each phase prompt as mandatory execution contract
- **Apply metadata from TEMPLATE_HEADERS.md to ALL generated documents**

### Step 3.2: PHASE-BY-PHASE MATERIALIZATION GATE (MANDATORY)

For any skill with a multi-phase flow, execution MUST be strictly sequential and stateful:

1. Execute the current phase prompt.
2. Create/update the phase output document(s) for that phase immediately.
3. Validate that the phase artifact(s) exist and include mandatory metadata.
4. Only then continue to the next phase.

Deferred/batch creation at the end of the flow is INVALID.

If a phase is defined in the skill flow as document-producing, skipping file materialization for that phase blocks progression (NO-GO for next phase).

### Step 3.1: EXPLAINABILITY GATE (Conditional, Mandatory)
Read `AI_USED` from the invoked skill file (`skills/skill_*.md`).

- If `AI_USED` is missing:
   - Default to `AI_USED = FALSE` (backward compatibility)
   - `## AI_EXPLAINABILITY_VALIDATION` is not required

- If `AI_USED = TRUE`:
   - The skill output MUST include `## AI_EXPLAINABILITY_VALIDATION`
   - The block MUST include all fields:
      - Explainability level defined? YES/NO
      - User-facing explanation provided? YES/NO
      - Model version logged? YES/NO
      - Decision trace stored? YES/NO
   - Missing block or missing fields → **SKILL EXECUTION INVALID**

- If `AI_USED = FALSE`:
   - `## AI_EXPLAINABILITY_VALIDATION` is not required

### Step 4: GENERATE OUTPUT FILE (MANDATORY PER PHASE — NOT OPTIONAL)
**CRITICAL**: The skill execution is INVALID if the current phase output file is not created before continuing.

For each document-producing phase, the output MUST be created at:
```
documentation/{{TOPIC}}/AECF_<NN>_<DOCUMENT_NAME>.md
```

**METADATA ENFORCEMENT**: The output file MUST include the standard `## METADATA` block
as defined in `templates/TEMPLATE_HEADERS.md`, filled with:
- `Document Type` and `Phase` from the template's `@METADATA` directive
- `TOPIC`, `Scope`, `Date`, `Timestamp (UTC)`, `Executed By`, `Executed By ID`,
  `Execution Identity Source`, `Repository`, `Branch`, `Root Prompt`, `Skill Executed`,
  `Sequence Position`, `Total Prompts Executed` auto-resolved
- Any document-type specific extension fields from the directive

Missing or incomplete metadata → **DOCUMENT INVALID**.

The AI MUST use the file creation tool to create the phase file.
Chat-only responses are NOT valid skill executions.

### Step 4.1: UPDATE TOPICS_INVENTORY (MANDATORY — EVERY SKILL EXECUTION)

**CRITICAL**: After creating the output file, the AI MUST update the project's lifecycle inventory.
This step is NON-OPTIONAL and applies to EVERY skill execution, including `aecf_executive_summary`.

The inventory lives in the **target project's workspace**, NOT in the AECF_Prompts repo.
It MUST be user-scoped to avoid concurrent overwrite/merge collisions across different operators:
```
documentation/AECF_TOPICS_INVENTORY_<user_id>.json
documentation/AECF_TOPICS_INVENTORY_<user_id>.md
```

`<user_id>` MUST be resolved from execution identity (`Executed By ID`) and sanitized to
`[a-z0-9_-]` (replace any other character with `_`).
If identity is unavailable, use fallback `anonymous`.

#### 4.1.1 Initialization

If `documentation/` does not exist in the target project workspace → **CREATE** it first.

If `documentation/AECF_TOPICS_INVENTORY_<user_id>.json` does not exist:
- **CREATE** `documentation/AECF_TOPICS_INVENTORY_<user_id>.json` with the data model below.
- **CREATE** `documentation/AECF_TOPICS_INVENTORY_<user_id>.md` immediately after JSON creation (bootstrap markdown view from the same data).

If `documentation/AECF_TOPICS_INVENTORY_<user_id>.json` exists:
- **LOAD** it, update, and overwrite.
- **REGENERATE** `documentation/AECF_TOPICS_INVENTORY_<user_id>.md` from the updated JSON.

Creation of TOPICS_INVENTORY files is **MANDATORY on first skill execution**. Skipping creation is an invalid Step 4.1 behavior.

#### 4.1.2 Status Logic (deterministic, no ambiguity)

| Condition | Status |
|-----------|--------|
| First artifact created in `documentation/{{TOPIC}}/` (no prior entry) | **OPEN** |
| Multiple artifacts exist, no EXECUTIVE_SUMMARY | **ACTIVE** |
| EXECUTIVE_SUMMARY exists AND no artifact created after it | **CLOSED** |
| Any skill creates an artifact AFTER a CLOSED status | **REOPENED** (then transitions to ACTIVE) |

#### 4.1.3 Update Rules

For the current `{{TOPIC}}`:

1. **If TOPIC not in inventory** → Add new entry:
   - `status`: OPEN
   - `opened_at`: current UTC timestamp
   - `opening_skill`: current skill ID
   - `lifecycle_history`: append `{"event": "OPENED", "timestamp": "<now>", "trigger_skill": "<skill_id>"}`

2. **If TOPIC exists and status is OPEN** → Update to ACTIVE:
   - `status`: ACTIVE
   - Append current skill to `executed_skills`
   - Update `artifact_count`, `last_updated`

3. **If current skill is `aecf_executive_summary`** → Mark CLOSED:
   - `status`: CLOSED
   - `closed_at`: current UTC timestamp
   - `closing_skill`: `aecf_executive_summary`
   - `has_executive_summary`: true
   - `lifecycle_history`: append `{"event": "CLOSED", "timestamp": "<now>", "trigger_skill": "aecf_executive_summary"}`

4. **If TOPIC exists and status is CLOSED** (skill executes after closure) → REOPEN:
   - `status`: ACTIVE
   - Clear `closed_at`
   - `lifecycle_history`: append `{"event": "REOPENED", "timestamp": "<now>", "trigger_skill": "<skill_id>"}`
   - Then apply normal ACTIVE update (append skill, update counts)

5. **Always** recalculate `summary` totals (total_topics, open, active, closed, reopened, compliance_average).

#### 4.1.4 JSON Data Model (per topic)

```json
{
  "topic_name": "",
  "status": "OPEN | ACTIVE | CLOSED | REOPENED",
  "opened_at": "",
  "closed_at": "",
  "last_updated": "",
  "opening_skill": "",
  "closing_skill": "",
  "executed_skills": [],
  "artifact_count": 0,
  "has_executive_summary": false,
  "compliance_score": 0,
  "lifecycle_history": [
    {
      "event": "OPENED | CLOSED | REOPENED",
      "timestamp": "",
      "trigger_skill": ""
    }
  ]
}
```

#### 4.1.5 TOPICS_INVENTORY.md Regeneration

After updating the JSON, regenerate `documentation/AECF_TOPICS_INVENTORY_<user_id>.md` with:
- Global Summary (totals, compliance average)
- Per-topic section: Status, Opened, Closed, Last Updated, Skills, Artifacts, Compliance, Timeline

#### 4.1.6 Constraints

- **Idempotent**: Running the same skill twice produces the same inventory state.
- **Deterministic**: No ambiguity in status transitions.
- **Non-destructive**: Never deletes topics or modifies artifact files.
- **Project-scoped**: The inventory belongs to the project running the skills, not to AECF_Prompts.
- **No silent skip**: If TOPICS_INVENTORY files are missing, the dispatcher MUST create them in Step 4.1 before completion.

If inventory update fails → **LOG WARNING** but do NOT block skill execution.

### Step 4.2: UPDATE PROJECT CHANGELOG (MANDATORY — EVERY SKILL EXECUTION)

**CRITICAL**: Every skill execution MUST append an entry to the target project's changelog.
This step is NON-OPTIONAL and applies to ALL skills, including `aecf_executive_summary`.

The changelog lives in the **target project's workspace**:
```
documentation/AECF_CHANGELOG_<user_id>.md
```

`<user_id>` MUST be the same value resolved in Step 4.1 from execution identity
(`Executed By ID`), sanitized to `[a-z0-9_-]`, with fallback `anonymous`.

#### 4.2.1 Initialization

If `documentation/` does not exist in the target project workspace → **CREATE** it first.

If `documentation/AECF_CHANGELOG_<user_id>.md` does not exist:
- **CREATE** `documentation/AECF_CHANGELOG_<user_id>.md` with a project changelog header and entry template.

If `documentation/AECF_CHANGELOG_<user_id>.md` exists:
- **LOAD** it and append a new entry at the top of the entries section.

#### 4.2.2 Mandatory Entry Content

Each appended entry MUST include at least:
- Date and UTC timestamp
- `TOPIC`
- Executed skill ID
- Generated artifact path (`documentation/{{TOPIC}}/AECF_<NN>_<DOCUMENT_NAME>.md`)
- Short summary of what was generated/updated

#### 4.2.3 Constraints

- **One execution = one changelog entry**
- **Project-scoped**: This changelog belongs to the project using AECF, not to AECF_Prompts
- **Location fixed**: `documentation/AECF_CHANGELOG_<user_id>.md` is mandatory
- **No silent skip**: Missing changelog file/directories MUST be created before completion
- **Legacy override**: Any skill-local legacy mention of `documentation/CHANGELOG.md` MUST be interpreted as `documentation/AECF_CHANGELOG_<user_id>.md`

### Step 5: CONFIRM COMPLETION
```
✅ Skill execution complete
📄 File created: documentation/<TOPIC>/AECF_<NN>_<DOCUMENT_NAME>.md
📊 TOPICS_INVENTORY updated/created: <TOPIC> → <STATUS>
📝 CHANGELOG updated/created: documentation/AECF_CHANGELOG_<user_id>.md
```

Executive summaries are generated on-demand only.
To generate one, invoke:
`skill: executive_summary TOPIC: <topic_name>`

---

## 4. SKILL-SPECIFIC EXECUTION GUIDES

### 4.1 aecf_code_standards_audit

**Minimal valid invocations** (any of these MUST work):
```
"skill: code_standards_audit"
"Auditar estándares del código"
"Revisa el código y dime qué cosas debería cambiar según los estándares"
"skill: skill_code_standards_audit.md. TOPIC: STANDARDS"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "STANDARDS"
- Scope: from user or workspace root
- Output: `documentation/{{TOPIC}}/AECF_<NN>_CODE_STANDARDS_AUDIT.md`

**Execution**:
1. Load skill: `skills/skill_code_standards_audit.md`
2. Ensure project-local severity matrix exists at `documentation/AECF_CODE_STANDARDS_AUDIT_SEVERITY_MATRIX.md`
   - If missing, create from `templates/CODE_STANDARDS_AUDIT_SEVERITY_MATRIX_TEMPLATE.md`
3. Load template: `templates/AUDIT_CODE_TEMPLATE.md` (if applicable)
4. Scan files in scope
5. Analyze against all standards (SYSTEM_CONTEXT + PROJECT_CONTEXT)
6. Classify findings using project matrix (CRITICAL / WARNING / INFO / MATRIX-PENDING)
   - For MATRIX-PENDING, decide `ADD_RULE` or `NO_ADD_RULE` with rationale
7. **CREATE FILE** with findings using the skill's output format
8. **MATRIX AUTO-APPLY**: If any `ADD_RULE` decisions exist → auto-insert new rules into matrix, bump version, update changelog (per Matrix Auto-Apply Protocol in skill definition)
9. Complete report generation (executive summary is optional via `skill_executive_summary`)

### 4.2 aecf_new_feature

**Minimal valid invocations**:
```
"Implementar [descripción]. skill: new_feature TOPIC: [nombre]"
"skill: new_feature — [descripción]"
"Necesito implementar [descripción]"
```

**Execution**: PLAN → AUDIT_PLAN → [loop FIX_PLAN if NO-GO] → IMPLEMENT → AUDIT_IMPLEMENT (AUDIT_CODE) → [loop FIX_CODE if NO-GO] → VERSION

**Mandatory phase gates (no skip allowed)**:
1. Do NOT implement any production code before generating `PLAN` and obtaining `AUDIT_PLAN = GO`.
2. If `AUDIT_PLAN = NO-GO`, execute `FIX_PLAN` and re-run `AUDIT_PLAN` until `GO`.
3. After `IMPLEMENT`, run `AUDIT_IMPLEMENT` (using the `AUDIT_CODE` phase) before declaring completion.
4. If `AUDIT_IMPLEMENT = NO-GO`, execute `FIX_CODE` and re-run `AUDIT_IMPLEMENT` until `GO`.
5. Any behavior that creates code first and documentation later is INVALID for this skill.

### 4.3 aecf_hotfix

**Minimal valid invocations**:
```
"🚨 P1: [descripción]. skill: hotfix TOPIC: [nombre]"
"Hotfix: [descripción]"
"Producción caída: [descripción]"
```

**Execution**: DEBUG → HOTFIX_PLAN → HOTFIX_AUDIT → HOTFIX_IMPL → HOTFIX_VERIFY → DEPLOY → POST-MORTEM

### 4.4 aecf_document_legacy

**Minimal valid invocations**:
```
"Documentar [módulo]. skill: document_legacy TOPIC: [nombre]"
"skill: document_legacy — [módulo]"
"Necesito documentar el código de [módulo]"
```

**Execution**: DOCUMENT_EXISTING → [Optional: DISCOVERY → PLAN...]

### 4.5 aecf_security_review

**Minimal valid invocations**:
```
"Security review de [módulo]. skill: security_review TOPIC: [nombre]"
"Auditoría de seguridad de [código]"
```

**Execution**: 
1. Load skill: `skills/skill_security_review.md`
2. Ensure project-local severity matrix exists at `documentation/AECF_SECURITY_REVIEW_SEVERITY_MATRIX.md`
   - If missing, create from `templates/SECURITY_REVIEW_SEVERITY_MATRIX_TEMPLATE.md`
3. SECURITY_AUDIT → FIX_CRITICAL → FIX_HIGH → DOCUMENT_RESIDUAL_RISKS
4. Classify findings using project matrix (CRITICAL/HIGH/MEDIUM/LOW/MATRIX-PENDING)
   - For MATRIX-PENDING, decide `ADD_RULE` or `NO_ADD_RULE` with rationale
5. **MATRIX AUTO-APPLY**: If any `ADD_RULE` decisions exist → auto-insert new rules into matrix, bump version, update changelog
6. Complete report generation (executive summary is optional via `skill_executive_summary`)

### 4.6 aecf_explain_behavior

**Minimal valid invocations**:
```
"Explicar por qué [comportamiento]. skill: explain_behavior TOPIC: [nombre]"
"¿Por qué el sistema [comportamiento]?"
```

**Execution**: EXPLAIN_BEHAVIOR (single phase)

### 4.7 aecf_maturity_assessment

**Minimal valid invocations**:
```
"skill: maturity_assessment. TOPIC: maturity_baseline"
"Evaluar madurez AECF del proyecto"
"¿Qué nivel de madurez tenemos?"
"Maturity assessment trimestral"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "maturity_assessment"
- Scope: from user, workspace root, or organization level
- Output: `documentation/{{TOPIC}}/AECF_<NN>_MATURITY_ASSESSMENT.md`

**Execution**:
1. Load skill: `skills/skill_maturity_assessment.md`
2. Load maturity model: `maturity/AECF_MATURITY_MODEL.md`
3. Load scoring rubric: `maturity/AECF_MATURITY_SCORING.md`
4. Load template: `maturity/AECF_MATURITY_ASSESSMENT_TEMPLATE.md`
5. Scan documentation/ and workspace for evidence per dimension
6. Score 10 dimensions (0–5) with evidence
7. Calculate maturity level
8. Generate gap analysis and improvement roadmap
9. **CREATE FILE** with assessment report
10. Complete assessment report generation

### 4.8 aecf_refactor

**Minimal valid invocations**:
```
"skill: refactor. TOPIC: refactor_auth"
"Refactorizar [módulo/código]"
"Limpiar el código de [scope]"
"Reestructurar [módulo] siguiendo estándares"
```

**Auto-resolution**:
- TOPIC: from user or infer from scope
- Scope: from user or workspace context
- Output: `documentation/{{TOPIC}}/AECF_<NN>_<PHASE>.md`

**Execution**: DOCUMENT_EXISTING → REFACTOR_PLAN → AUDIT_PLAN → [loop FIX_PLAN if NO-GO] → TEST_STRATEGY → TEST_IMPLEMENTATION (pre-refactor baseline) → VERIFY_PRE → REFACTORING → VERIFY_POST → AUDIT_CODE → [loop FIX_CODE if NO-GO] → VERSION

### 4.9 aecf_tech_debt_assessment

**Minimal valid invocations**:
```
"skill: tech_debt_assessment. TOPIC: tech_debt_q1"
"Evaluar deuda técnica del proyecto"
"¿Cuánta deuda técnica tenemos?"
"Technical debt assessment"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "tech_debt"
- Scope: from user or workspace root
- Output: `documentation/{{TOPIC}}/AECF_<NN>_TECH_DEBT_ASSESSMENT.md`

**Execution**:
1. Load skill: `skills/skill_tech_debt_assessment.md`
2. Ensure project-local severity matrix exists at `documentation/AECF_TECH_DEBT_ASSESSMENT_SEVERITY_MATRIX.md`
   - If missing, create from `templates/TECH_DEBT_ASSESSMENT_SEVERITY_MATRIX_TEMPLATE.md`
3. Scan codebase for debt indicators across 6 categories
4. Classify by severity using project matrix and business impact
   - For MATRIX-PENDING, decide `ADD_RULE` or `NO_ADD_RULE` with rationale
5. Quantify remediation effort per finding using matrix effort calibration
6. Prioritize with risk × impact matrix
7. Generate remediation backlog
8. **CREATE FILE** with assessment report
9. **MATRIX AUTO-APPLY**: If any `ADD_RULE` decisions exist → auto-insert new rules into matrix, bump version, update changelog
10. Complete report generation (executive summary is optional via `skill_executive_summary`)

### 4.10 aecf_release_readiness

**Minimal valid invocations**:
```
"skill: release_readiness. TOPIC: release_v1_5_0"
"¿Está listo para release?"
"Verificar readiness del sprint"
"Pre-release check"
```

**Auto-resolution**:
- TOPIC: from user or infer from version/sprint
- Scope: from user or all pending changes
- Output: `documentation/{{TOPIC}}/AECF_<NN>_RELEASE_READINESS.md`

**Execution**:
1. Load skill: `skills/skill_release_readiness.md`
2. Determine release scope
3. Verify AECF phase completion
4. Validate audit results (all GO)
5. Check version management
6. Verify documentation completeness
7. Verify security clearance
8. Verify testing completeness
9. Assess operational readiness
10. Calculate Release Readiness Score
11. Issue GO/NO-GO verdict
12. **CREATE FILE** with release readiness report
13. Complete release readiness report generation

### 4.11 aecf_dependency_audit

**Minimal valid invocations**:
```
"skill: dependency_audit. TOPIC: dep_audit_q1"
"Auditar dependencias del proyecto"
"Dependency check"
"¿Tenemos vulnerabilidades en las dependencias?"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "dependency_audit"
- Scope: from user or workspace root (locate manifest files)
- Output: `documentation/{{TOPIC}}/AECF_<NN>_DEPENDENCY_AUDIT.md`

**Execution**:
1. Load skill: `skills/skill_dependency_audit.md`
2. Ensure project-local severity matrix exists at `documentation/AECF_DEPENDENCY_AUDIT_SEVERITY_MATRIX.md`
   - If missing, create from `templates/DEPENDENCY_AUDIT_SEVERITY_MATRIX_TEMPLATE.md`
3. Discover all dependency manifest files
4. Build dependency inventory (direct + transitive)
5. Vulnerability scan (CVE databases)
6. License compliance check
7. Maintenance health assessment
8. Version freshness analysis
9. Supply chain risk scoring
10. Classify findings using project matrix (CRITICAL/HIGH/MEDIUM/LOW/MATRIX-PENDING)
    - For MATRIX-PENDING, decide `ADD_RULE` or `NO_ADD_RULE` with rationale
11. Generate remediation plan
12. **CREATE FILE** with audit report
13. **MATRIX AUTO-APPLY**: If any `ADD_RULE` decisions exist → auto-insert new rules into matrix, bump version, update changelog
14. Complete report generation (executive summary is optional via `skill_executive_summary`)

### 4.12 aecf_data_strategy

**Minimal valid invocations**:
```
"skill: data_strategy. TOPIC: azure_cost_data"
"¿Cómo ingestar los datos de Azure Cost Connector?"
"Diseñar estrategia de datos para [fuente]"
"¿Es mejor tablas separadas o todo en una tabla?"
"Data ingestion strategy para [fuente de alto volumen]"
```

**Auto-resolution**:
- TOPIC: from user or infer from data source name → default: "data_strategy"
- Scope: from user or workspace root (locate existing data/pipeline code)
- Output: `documentation/{{TOPIC}}/AECF_<NN>_DATA_STRATEGY.md`

**Execution**:
1. Load skill: `skills/skill_data_strategy.md`
2. Load template: `templates/DATA_STRATEGY_TEMPLATE.md`
3. Load checklist: `checklists/DATA_STRATEGY_CHECKLIST.md`
4. Characterize data source (4 Vs + operational)
5. Identify constraints & requirements
6. Enumerate viable strategies (min 3)
7. Trade-off analysis per strategy
8. Score with decision matrix (7 dimensions)
9. Issue recommendation with justification
10. Design schema & storage at high level
11. Generate downstream handoff sections
12. **CREATE FILE** with data strategy report
13. Complete data strategy report generation

### 4.13 aecf_system_replayability_adaptive

**Minimal valid invocations**:
```
"skill: system_replayability_adaptive. TOPIC: replay_backend"
"Add replay capability to the project"
"Make this system replayable"
"Introduce execution traceability"
"Deterministic replay for [module]"
"generar contexto del proyecto" → skill_project_context_generator
"scan the workspace" → skill_project_context_generator
"bootstrap project context" → skill_project_context_generator
"analizar el proyecto" → skill_project_context_generator
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "replay"
- Scope: from user or workspace root
- Output: `documentation/{{TOPIC}}/AECF_<NN>_ARCHITECTURE_DISCOVERY.md` (first phase)

**Execution**:
1. Load skill: `skills/skill_system_replayability_adaptive.md`
2. Phase 1: Architecture Discovery (language, framework, entry points, persistence, concurrency)
3. Phase 2: Replay Strategy Selection (Case A–F based on architecture)
4. Phase 3: Replayability Design (technology-agnostic, clean architecture)
5. Phase 4: Minimal Injection (generate decorators, store, runner, config)
6. Phase 5: Validation Block (12-criterion safety check, ALL must PASS)
7. Maturity Classification (L1–L5 with upgrade path)
8. **CREATE FILES** for each phase
9. Complete replayability artifacts generation

### 4.15 aecf_executive_summary

**Minimal valid invocations**:
```
"skill: executive_summary. TOPIC: backend_auth"
"Generar resumen ejecutivo TOPIC: release_v32"
```

**Auto-resolution**:
- TOPIC: mandatory. Cannot be inferred.
- Scope: `documentation/{{TOPIC}}/`
- Output: `documentation/{{TOPIC}}/AECF_<NN>_EXECUTIVE_SUMMARY.md`

**Execution**:
1. Load skill: `skills/skill_executive_summary.md`
2. Validate TOPIC was provided
3. Validate `documentation/{{TOPIC}}/` exists and contains AECF docs
4. Scan and analyze all documents in TOPIC
5. Generate summary using `templates/EXECUTIVE_SUMMARY_TEMPLATE.md`
6. **CREATE FILE** with next sequential number
7. **CLOSE TOPIC** in `documentation/AECF_TOPICS_INVENTORY_<user_id>.json` (Step 4.1.3 rule 3)
8. **APPEND PROJECT CHANGELOG ENTRY** in `documentation/AECF_CHANGELOG_<user_id>.md` (Step 4.2)

**IMPORTANT**: This is the ONLY skill that transitions a TOPIC to CLOSED status.
If any other skill runs on this TOPIC after closure, the TOPIC is automatically REOPENED (Step 4.1.3 rule 4).

### 4.16 aecf_project_context_generator

**Minimal valid invocations**:
```
"skill: project_context_generator"
"Generar contexto del proyecto"
"Analizar el proyecto y generar PROJECT_CONTEXT"
"Scan the workspace"
"Bootstrap project context"
```

**Auto-resolution**:
- TOPIC: N/A (este skill no usa TOPIC — genera `AECF_PROJECT_CONTEXT.md` en la raíz)
- Scope: workspace root (siempre escanea todo el workspace)
- Output: `<workspace_root>/AECF_PROJECT_CONTEXT.md`

**Execution**:
1. Load skill: `skills/skill_project_context_generator.md`
2. Check if `AECF_PROJECT_CONTEXT.md` already exists → warn if so
3. Phase 1: Workspace Scan (directory tree, configs, source files, docs)
4. Phase 2: Deep Analysis (tech stack, frameworks, patterns, conventions)
5. Phase 3: Architecture Inference (entry points, deployment, integrations, critical patterns)
6. Phase 4: Context Composition (generate structured `AECF_PROJECT_CONTEXT.md`)
7. Phase 5: User Review (present with confidence levels, iterate on feedback)
8. **CREATE FILE** `AECF_PROJECT_CONTEXT.md` at workspace root
9. No executive summary (this is a **config file**, not an AECF analysis document)

**Special behavior**:
- Output goes to workspace root, NOT to `documentation/{{TOPIC}}/`
- Does NOT generate executive summaries (it IS the context, not a report)
- Does NOT overwrite existing `AECF_PROJECT_CONTEXT.md` without user confirmation
- Interactive: presents results for user review before finalizing

### 4.17 aecf_data_governance_audit

**Minimal valid invocations**:
```
"skill: data_governance_audit. TOPIC: data_gov_q1"
"Audita gobierno de datos del módulo de anomalías"
"Data governance audit for Azure anomaly detection"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "data_governance"
- Scope: from user or workspace root
- Output: `documentation/{{TOPIC}}/AECF_<NN>_DATA_GOVERNANCE_AUDIT.md`

**Execution**:
1. Load skill: `skills/skill_data_governance_audit.md`
2. Inventory data assets in scope
3. Validate data classification and handling controls
4. Validate lineage and retention policies
5. Score governance gaps and define remediation actions
6. **CREATE FILE** with data governance audit report

### 4.18 aecf_model_governance_audit

**Minimal valid invocations**:
```
"skill: model_governance_audit. TOPIC: model_gov_q1"
"Audita el gobierno de modelo de detección de anomalías"
"Model governance audit for inference pipeline"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "model_governance"
- Scope: from user or workspace root
- Output: `documentation/{{TOPIC}}/AECF_<NN>_MODEL_GOVERNANCE_AUDIT.md`

**Execution**:
1. Load skill: `skills/skill_model_governance_audit.md`
2. Identify model-impacting changes
3. Validate inference-path determinism and auditability
4. Declare model impact (YES/NO) with rationale
5. Define controls and governance recommendations
6. **CREATE FILE** with model governance audit report

### 4.19 aecf_ai_risk_assessment

**Minimal valid invocations**:
```
"skill: ai_risk_assessment. TOPIC: ai_risk_q1"
"Evalúa riesgos de IA para Azure anomaly detection"
"AI risk assessment for anomaly pipeline"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "ai_risk"
- Scope: from user or workspace root
- Output: `documentation/{{TOPIC}}/AECF_<NN>_AI_RISK_ASSESSMENT.md`

**Execution**:
1. Load skill: `skills/skill_ai_risk_assessment.md`
2. Identify risks by category (operational, security, compliance, reliability)
3. Score each risk with rationale (LOW/MEDIUM/HIGH)
4. Define mitigations and residual risk stance
5. Build prioritized risk register
6. **CREATE FILE** with AI risk assessment report

### 4.20 aecf_define_impact_metrics

**Minimal valid invocations**:
```
"skill: define_impact_metrics. TOPIC: metrics_q1"
"Define métricas de impacto para Azure anomaly detection"
"Define impact metrics for this feature"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "impact_metrics"
- Scope: from user or workspace root
- Output: `documentation/{{TOPIC}}/AECF_<NN>_IMPACT_METRICS.md`

**Execution**:
1. Load skill: `skills/skill_define_impact_metrics.md`
2. Define outcomes and measurable metrics
3. Establish baseline and post-change targets
4. Assign ownership, cadence, and measurement method
5. Validate governance readiness of metric definitions
6. **CREATE FILE** with impact metrics specification

### 4.21 aecf_explorator_data_classification

**Minimal valid invocations**:
```
"skill: explorator_data_classification. TOPIC: data_classification"
"use skill aecf_explorator_data_classification TOPIC: explorator_data_classification"
"Clasifica los campos de los modelos ORM"
"¿Qué campos PII/SENSITIVE tiene el proyecto?"
"Inventario de datos del módulo [scope]"
"Explorar y clasificar los modelos de datos"
```

**Auto-resolution**:
- TOPIC: from user or infer from scope → default: "data_classification"
- Scope: from user description or workspace root (locate ORM models, migrations, DTOs)
- Output: `documentation/{{TOPIC}}/AECF_<NN>_EXPLORATOR_DATA_CLASSIFICATION.md`

**Execution**:
1. Load skill: `skills/skill_explorator_data_classification.md`
2. Load schema reference: `aecf_prompts/_governance/DATA_GOVERNANCE_SPEC_SCHEMA.md` (if exists)
3. **Step 1 — Discovery**: Scan scope for ORM models, migrations, DTOs, API schemas, fixtures
4. **Step 2 — Extraction**: For each artifact, extract table name, fields, types, nullability, PKs, FKs, constraints, comments
5. **Step 3 — Classification**: Apply deterministic heuristics in priority order (annotation → name pattern → FK inference → default PUBLIC). Assign confidence per field
6. **Step 4 — Relationship Graph**: Map FK relationships and cardinality; propagate classification impact
7. **Step 5 — Governance Proposal**: Summarize risk, flag missing annotations, identify retention gaps, access control recommendations, data minimization candidates
8. **Step 6 — YAML Output**: Generate schema-compliant `data_classification.yaml` block embedded in the document
9. **Validation Block**: Confirm all fields classified, YAML valid, no code modified, all relationships mapped
10. **CREATE FILE** `documentation/{{TOPIC}}/AECF_<NN>_EXPLORATOR_DATA_CLASSIFICATION.md`

**Special behavior**:
- STRICTLY read-only — NEVER modifies source files, models, or migrations
- If user requests inline documentation (e.g., "add a line of explanation per field"), include it as `governance_note` in the YAML and as a column in the report table — do NOT write to source code
- Classification is deterministic; governance recommendations section may include AI-generated suggestions (marked as such)
- If `DATA_GOVERNANCE_SPEC_SCHEMA.md` does not exist → create it at `aecf_prompts/_governance/DATA_GOVERNANCE_SPEC_SCHEMA.md`

### 4.22 aecf_document_context_ingestion

**Minimal valid invocations**:
```
"skill: document_context_ingestion. TOPIC: external_context"
"Ingesta contexto desde PDF y Markdown para este proyecto"
"build context from docs in C:/contracts and external URLs"
```

**Auto-resolution**:
- TOPIC: from user or infer → default: "doc_context"
- Scope: workspace docs + user-provided external sources
- Output: `documentation/{{TOPIC}}/AECF_<NN>_DOCUMENT_CONTEXT_INGESTION.md`

**Execution**:
1. Load skill: `skills/skill_document_context_ingestion.md`
2. Discover sources in workspace docs (`documentation/`, `docs/`, `README*`, `CHANGELOG*`) and optional external paths/URLs
3. Build source inventory with type and accessibility status
4. Extract deterministic constraints, assumptions, and key sections from each source
5. Evaluate confidence/freshness and detect cross-source conflicts
6. Normalize context into reusable blocks for downstream skills
7. Build handoff matrix to `aecf_project_context_generator`, `aecf_new_feature`, `aecf_security_review`, `aecf_data_governance_audit`, and `aecf_release_readiness`
8. **CREATE FILE** `documentation/{{TOPIC}}/AECF_<NN>_DOCUMENT_CONTEXT_INGESTION.md`

**Special behavior**:
- STRICTLY read-only: this skill never modifies source code or source documents
- Supports documents outside workspace when user provides absolute paths/URLs
- Every critical claim in output MUST include source reference and confidence

---

### 4.23 aecf_new_project

**Minimal valid invocations**:
```
"skill: new_project. project_name: my_api project_type: web_api_rest language_framework: python_fastapi database: postgresql"
"Crear nuevo proyecto REST API con FastAPI y PostgreSQL"
"Bootstrap un proyecto CLI en Python con Click, sin base de datos"
"skill: new_project — quiero una app de datos con Airflow y MySQL"
```

**Auto-resolution**:
- TOPIC: `new_project_<project_name>` (inferred from project_name)
- Scope: new project root `<workspace_root>/<project_name>/`
- Output: `<project_name>/AECF_PROJECT_CONTEXT.md` + full scaffold files

**INTAKE BLOCKING RULES** (mandatory — no scaffold until all are resolved):
1. `project_name` — cannot be inferred, must be explicit
2. `project_type` — must match catalog in skill file (10 supported types)
3. `language_framework` — must match sub-catalog for the resolved type
4. `database` — must be explicit: `none` or a specific engine from catalog

If ANY of the above is missing or ambiguous → generate `documentation/new_project/AECF_01_NEW_PROJECT_INTAKE.md` and STOP.

**Execution**:
1. Load skill: `skills/skill_new_project.md`
2. **PHASE INTAKE**: Parse all 4 required parameters from the prompt
   - Validate against supported catalogs in the skill file
   - If ANY missing or ambiguous → CREATE `00_NEW_PROJECT_INTAKE.md` with specific questions → STOP
3. **PHASE SCAFFOLD**: Create full directory structure and all config/stub files
   - Use stack-specific blueprint from skill file
   - Add database integration files if database ≠ none
   - Generate `.gitignore`, `.env.example`, CI/CD workflow
4. **PHASE GENERATE_README**: Create professional `README.md` at project root
5. **PHASE GENERATE_CONTEXT**: Create `AECF_PROJECT_CONTEXT.md` bootstrapped with all known info
6. **PHASE IMPLEMENT**: Materialize the scaffold physically in the client workspace via `<AECF_FILE_CHANGES>`
7. **PHASE AUDIT_IMPLEMENT**: Audit the real scaffold under `<workspace_root>/<project_name>/` and require `GO` before completion
8. If `AUDIT_IMPLEMENT = NO-GO`, execute `FIX_CODE` and re-run `AUDIT_IMPLEMENT` until `GO`
9. Output scaffolding summary block only after the audit loop is satisfied

**Special behavior**:
- This skill creates files in a NEW directory, not in `documentation/TOPIC/`
- Files are created relative to `output_path` (default: `<workspace_root>/<project_name>/`)
- The `AECF_PROJECT_CONTEXT.md` created here should later be enriched with `aecf_project_context_generator`
- Recommended natural next skill: `aecf_new_feature` for the first feature
- NEVER scaffold before all 4 required parameters are confirmed — this is a hard gate

---

### 4.24 aecf_new_test_set

**Minimal valid invocations**:
```
"skill: new_test_set. TOPIC: auth_testset prompt: revisa auth/service.py y dime que tests faltan"
"Haz un barrido de tests del modulo payments y propon los que faltan"
"Generate a test set for this module and execute it after approval"
```

**Auto-resolution**:
- TOPIC: from user or infer from scope -> default: `test_set`
- Scope: from user description or recently modified module(s)
- Output (first phase): `documentation/{{TOPIC}}/AECF_<NN>_PLAN.md`

**Execution**:
1. Load skill: `skills/skill_new_test_set.md`
2. Perform mandatory repository sweep:
   - discover modules or routines in scope
   - discover existing tests
   - discover coverage tooling and runnable test commands
3. Execute `00_PLAN.md` using discovery evidence to define the test hardening scope
4. Execute `02_AUDIT_PLAN.md`; if `NO-GO`, run `03_FIX_PLAN.md` and loop until `GO`
5. Execute `08_TEST_STRATEGY.md` to list missing tests by routine and risk category
6. If the user has not already approved implementation and the run does not carry `execute=True`, ask exactly one question:
   - `Do I implement and execute the proposed tests?`
7. If user declines, stop after `TEST_STRATEGY`
8. If user approves, execute `09_TEST_IMPLEMENTATION.md`
9. Execute `11_TEST_EXECUTION_REPORT.md`
10. CREATE FILES for every document-producing phase

**Special behavior**:
- This skill is search-first and test-focused
- It MUST NOT invoke `10_AUDIT_TESTS.md` recursively
- It MUST NOT create tests for the generated tests
- If execution cannot run because of environment or dependencies, the final report MUST document the real blocker and verdict

---

### 4.25 aecf_codebase_intelligence

**Minimal valid invocations**:
```
"skill: codebase_intelligence"
"analiza la arquitectura del proyecto y genera el contexto de inteligencia"
"build codebase intelligence for this workspace"
```

**Auto-resolution**:
- TOPIC: not required (`requires_topic: false`)
- Scope: entire workspace
- Output: `.aecf/context/` (8 structured artifacts, including `STACK_JSON.json`)

**Execution**:
1. Load skill: `skills/skill_codebase_intelligence.md`
2. Analyze project structure (directory tree, exclude standard dirs)
3. Detect languages by file extension and compute distribution
4. Inspect dependency files for stack detection
5. Search for entry point patterns and `__main__` blocks
6. Extract all symbols (classes, functions, methods) via AST or pattern matching
7. Build import/dependency graph between modules
8. Identify core components (most referenced classes, functions, modules)
9. Detect hotspots (large files, high coupling, many references)
10. Detect configuration and testing structures
11. Generate all 7 output artifacts in `.aecf/context/`

**Special behavior**:
- This skill is strictly READ-ONLY — no source code modification
- Must run in Phase 0 before other skills
- Language-independent analysis
- Output artifacts serve as context keys for downstream skills

---

## 5. ERROR PREVENTION RULES

### 5.1 NEVER ask the user for execution mode
The execution mode is ALWAYS "AECF STRICT". There is no other mode.

### 5.2 NEVER respond only in chat
If a skill is invoked, the AI MUST create a file. A chat-only response is an INVALID execution.

### 5.3 NEVER ask if the user wants AECF conventions
If a skill is invoked, AECF conventions are MANDATORY. Not optional. Not negotiable.

### 5.4 NEVER ask for template confirmation
Templates are loaded automatically. The user does not need to know which template is used.

### 5.5 NEVER require verbose prompts
The following prompt MUST be sufficient to trigger full execution:
```
skill: code_standards_audit. TOPIC: STANDARDS
```

If the AI cannot execute with this level of simplicity, the dispatcher implementation is broken.

### 5.6 ALWAYS create the output file
Even if the analysis is incomplete, create the file with whatever has been analyzed. An incomplete file is better than no file.

### 5.7 ALWAYS use AECF naming conventions
All output files MUST follow: `AECF_<NN>_<DOCUMENT_NAME>.md`

### 5.8 Numbering across the TOPIC
The `<NN>` number is sequential WITHIN the TOPIC directory. Check existing files before assigning the next number.

### 5.9 Triad Enforcement (skill + TOPIC + prompt)
If a user message includes `skill` + `TOPIC` + `prompt`, the AI MUST:
- Treat the message as an enforced skill invocation (no fallback to free-form coding).
- Execute the selected skill workflow from Step 1 ACK through file generation.
- Reject/directly avoid any behavior that jumps straight to code implementation.

Skipping skill flow under this condition is a dispatcher violation.

### 5.10 Triad Parse Failure Handling
If `skill` + `TOPIC` + `prompt` are present but the skill token is malformed/unknown:
- Ask ONE corrective question only about the skill identifier.
- Do NOT implement code until a valid skill is resolved.

### 5.11 `aecf_new_feature` Sequential Gate (Mandatory)
When resolved skill is `aecf_new_feature`, the AI MUST enforce this order:
1. `PLAN`
2. `AUDIT_PLAN`
3. `FIX_PLAN` loop (if `AUDIT_PLAN = NO-GO`)
4. `IMPLEMENT`
5. `AUDIT_IMPLEMENT` (`AUDIT_CODE`)
6. `FIX_IMPLEMENT` loop (`FIX_CODE`) if `AUDIT_IMPLEMENT = NO-GO`

Implementation before steps 1-3 are completed with `AUDIT_PLAN = GO` is a dispatcher violation.

### 5.12 `aecf_new_test_set` Approval Gate (Mandatory)
When resolved skill is `aecf_new_test_set`, the AI MUST enforce this order:
1. Repository sweep
2. `PLAN`
3. `AUDIT_PLAN`
4. `FIX_PLAN` loop if needed
5. `TEST_STRATEGY`
6. Explicit user approval or `execute=True`
7. `TEST_IMPLEMENTATION`
8. `TEST_EXECUTION_REPORT`

Test implementation or execution before explicit user approval or `execute=True` is a dispatcher violation.
Recursive invocation of `AUDIT_TESTS` inside this skill is also a dispatcher violation.

---

## 6. INVOCATION EXAMPLES (EXPECTED BEHAVIOR)

### Example 1: Minimal invocation
```
User: "skill: code_standards_audit. TOPIC: STANDARDS"

AI:
✅ Skill recognized: aecf_code_standards_audit
📌 TOPIC: STANDARDS  
📂 Scope: [workspace root or inferred]
🔢 Next number: 01
📄 Output: documentation/STANDARDS/AECF_01_CODE_STANDARDS_AUDIT.md

[Executes full audit...]
[Creates file...]

✅ Skill execution complete
📄 File created: documentation/STANDARDS/AECF_01_CODE_STANDARDS_AUDIT.md
```

### Example 2: Natural language (Spanish)
```
User: "quiero que revises el código generado y me digas qué cosas debería cambiar"

AI:
✅ Skill recognized: aecf_code_standards_audit (inferred from intent)
📌 TOPIC: code_review (inferred)
📂 Scope: [workspace root]
🔢 Next number: 01
📄 Output: documentation/code_review/AECF_01_CODE_STANDARDS_AUDIT.md

[Executes full audit...]
[Creates file...]
```

### Example 3: With explicit scope
```
User: "skill: code_standards_audit. revisa sentinel-multichat/backend"

AI:
✅ Skill recognized: aecf_code_standards_audit
📌 TOPIC: sentinel_backend (inferred from scope)
📂 Scope: sentinel-multichat/backend
🔢 Next number: 01
📄 Output: documentation/sentinel_backend/AECF_01_CODE_STANDARDS_AUDIT.md

[Executes full audit...]
```

### Example 4: Simple feature request
```
User: "Implementar endpoint de exportación PDF. Usar skill: new_feature TOPIC: pdf_export"

AI:
✅ Skill recognized: aecf_new_feature
📌 TOPIC: pdf_export
📂 Scope: [inferred from workspace]
🔢 Starting at: 01
📄 First output: documentation/pdf_export/AECF_01_PLAN.md

[Executes full skill sequence...]
```

---

## 7. TROUBLESHOOTING SELF-CHECK

Before executing any skill, the AI MUST verify:

- [ ] Skill correctly identified?
- [ ] TOPIC resolved (explicit or inferred)?
- [ ] Scope resolved (explicit, inferred, or workspace root)?
- [ ] Next sequential number determined?
- [ ] Output path confirmed: `documentation/{{TOPIC}}/AECF_<NN>_<NAME>.md`?
- [ ] All mandatory contexts loaded?
- [ ] TOPICS_INVENTORY files present for current `user_id` (`AECF_TOPICS_INVENTORY_<user_id>.json` + `.md`) or created now if missing?
- [ ] Current TOPIC lifecycle status checked (OPEN/ACTIVE/CLOSED/REOPENED)?
- [ ] If `skill` + `TOPIC` + `prompt` present, was Pattern D triad enforcement applied?

If ANY item is unresolvable, ask the user ONCE with a specific question.
Do NOT ask multiple questions. Do NOT ask for information that can be inferred.

## 8. NEW SKILL REGISTRATION PROTOCOL

This section is the AUTHORITATIVE GATE for registering any new AECF skill.
It applies to ALL skill creation activities — whether triggered by a meta-prompt,
a direct user request, or an AI-generated skill. No skill is operational until
ALL steps in this protocol are completed.

### 8.1 When this protocol activates

This protocol MUST be executed whenever:
- A new `skills/skill_<name>.md` file is created
- A meta-prompt of type `CREATE_SKILL_*` is executed
- The user requests "add a new skill" or equivalent
- Any AI generates a new skill file as part of any task

### 8.2 Mandatory Registration Steps

Execute ALL steps in order. Each step is REQUIRED. None may be skipped.

#### Step R1 — Pattern B: Implicit Trigger Phrases
Location: This file (§1. SKILL INVOCATION RECOGNITION, Pattern B)

Add ≥5 natural-language phrases (mix of English and Spanish) that a user might say
when they mean this skill, prefixed with the skill ID:
```
"<phrase>" → skill_<id>
```

#### Step R2 — Skill Resolution Table
Location: This file (§1. SKILL INVOCATION RECOGNITION, Skill Resolution Table)

Add a new row:
```
| <keyword1, keyword2, natural phrase, alias, ...> | `aecf_<id>` | skills/skill_<id>.md |
```
Keywords must cover: skill filename variants, common natural-language aliases, and multilingual triggers.

#### Step R3 — Section 4.XX Execution Guide
Location: This file (§4. SKILL-SPECIFIC EXECUTION GUIDES)

Add `### 4.XX aecf_<id>` with:
- **Minimal valid invocations** (at least 3 copy-pasteable examples)
- **Auto-resolution rules**: TOPIC default, Scope default, Output path (MUST include `documentation/{{TOPIC}}/AECF_<NN>_<DOCUMENT_NAME>.md`)
- **Numbered execution steps** (what the AI must do in sequence)
- **Special behaviour** notes (anything diverging from standard execution protocol)

#### Step R4 — SKILL_CATALOG.md
Location: `aecf_prompts/skills/SKILL_CATALOG.md`

- Add node to Mermaid diagram (with styling)
- Add row to category summary table
- Add entry in the correct category section
- Add row to Matriz de Skills Completa (with Modifica Código, Genera Docs, Tiempo Estimado, Modo)
- Add to composition chains if applicable

#### Step R5 — README_SKILLS.md
Location: `aecf_prompts/skills/README_SKILLS.md`

Add numbered section `### N. <emoji> \`aecf_<id>\`` containing:
`Purpose` / `Layer` / `Time` / `Phases` / `Use when` / `Modifies code` / `Output` / `[Full Documentation]` link

#### Step R6 — Course / Executive Documentation (conditional)
If skill relates to data governance, model governance, AI risk, or impact metrics:
- Add **Related AECF Skills** row in the relevant `documentation/courses/0X_*.md`

### 8.3 SKILL_CREATION_VALIDATION BLOCK

Before declaring the skill creation task complete, the AI MUST confirm:

| # | Check | Required | Status |
|---|-------|----------|--------|
| R1 | Pattern B trigger phrases added to SKILL_DISPATCHER | ≥5 phrases | |
| R2 | Skill Resolution Table row added to SKILL_DISPATCHER | 1 row, full keyword list | |
| R3 | Section 4.XX execution guide added to SKILL_DISPATCHER | Full guide with output path | |
| R4 | SKILL_CATALOG.md updated | Mermaid, table, section, matrix | |
| R5 | README_SKILLS.md entry added | Numbered section, all fields | |
| R6 | Course documentation updated (if applicable) | Row in relevant course module | |

**If ANY row is empty → STOP. Complete missing steps. Do NOT declare the task done.**

### 8.4 Enforcement Rule

A skill file that exists in `skills/` but is NOT registered in all locations above
is INVISIBLE to the SKILL_DISPATCHER and WILL NOT execute with AECF conventions.
The naming convention, output path, and numbering protocol will NOT apply.
The skill is INOPERABLE until all registration steps are complete.

---

## CONTEXT VALIDATION

Confirm:

[ ] SKILL_DISPATCHER.md loaded
[ ] AECF_SYSTEM_CONTEXT.md loaded
[ ] Governance rules applied
[ ] Skill file loaded
[ ] Output path computed
[ ] File will be created (not chat-only)

If not confirmed → STOP execution.

------------------------------------------------------------

**END OF SKILL_DISPATCHER.md**

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check

