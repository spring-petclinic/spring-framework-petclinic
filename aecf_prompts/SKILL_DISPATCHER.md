# AECF SKILL DISPATCHER — Execution Autopilot (Slim)

> ⚠️ **If you arrived here after a successful MCP dispatch (`aecf_dispatch_skill`), STOP — do not read this file.** The MCP response already contains the resolved skill, parameters, and the full EXECUTION_PROTOCOL. Reading this file after MCP dispatch wastes tokens and adds no value.

---

This file is the **prompt-only dispatch path**. It activates when MCP tools are unavailable or when `aecf_dispatch_skill` fails.

After dispatch resolution, follow **`EXECUTION_PROTOCOL.md`** for execution steps.

---

## 1. SKILL INVOCATION RECOGNITION

### Trigger Patterns (priority: D → A → C → B)

#### Pattern D: Structured triad (HIGHEST PRIORITY)
Message contains `skill` + `TOPIC` + `prompt` (any order, case-insensitive). Example:
```
use skill aecf_new_feature TOPIC:login prompt: pantalla de login
```

#### Pattern A: Explicit skill reference
```
skill: <name> | run skill: <name> | use skill <name> | ejecuta skill: <name>
```

#### Pattern C: Skill filename reference
```
skill_code_standards_audit | skill_code_standards_audit.md | aecf_code_standards_audit | code_standards_audit
```

#### Pattern B: Implicit intent (natural language → skill)
The AI recognizes natural-language phrases and maps them to skills. Each skill's `DISPATCHER GUIDE` section in its `skill_*.md` file lists its trigger phrases. See the Compact Skill List below for primary keywords.

### Compact Skill List

| Canonical | Primary triggers | File |
|-----------|-----------------|------|
| `aecf_code_standards_audit` | code_standards, audita estándares | skills/skill_code_standards_audit.md |
| `aecf_new_feature` | new_feature, implementar, implement | skills/skill_new_feature.md |
| `aecf_new_test_set` | new_test_set, tests faltantes, missing tests | skills/skill_new_test_set.md |
| `aecf_hotfix` | hotfix, emergencia, P1/P2 | skills/skill_hotfix.md |
| `aecf_document_legacy` | document_legacy, documentar código | skills/skill_document_legacy.md |
| `aecf_security_review` | security_review, auditoría seguridad | skills/skill_security_review.md |
| `aecf_explain_behavior` | explain_behavior, por qué hace, behaviour | skills/skill_explain_behaviour.md |
| `aecf_maturity_assessment` | maturity_assessment, evaluación madurez | skills/skill_maturity_assessment.md |
| `aecf_refactor` | refactor, refactorizar, clean code | skills/skill_refactor.md |
| `aecf_tech_debt_assessment` | tech_debt, deuda técnica | skills/skill_tech_debt_assessment.md |
| `aecf_release_readiness` | release_readiness, listo para release | skills/skill_release_readiness.md |
| `aecf_dependency_audit` | dependency_audit, auditar dependencias | skills/skill_dependency_audit.md |
| `aecf_data_strategy` | data_strategy, estrategia de datos, cómo ingestar | skills/skill_data_strategy.md |
| `aecf_data_governance_audit` | data_governance_audit, gobierno de datos | skills/skill_data_governance_audit.md |
| `aecf_model_governance_audit` | model_governance_audit, gobierno de modelo | skills/skill_model_governance_audit.md |
| `aecf_ai_risk_assessment` | ai_risk_assessment, riesgo IA | skills/skill_ai_risk_assessment.md |
| `aecf_define_impact_metrics` | define_impact_metrics, métricas de impacto | skills/skill_define_impact_metrics.md |
| `aecf_system_replayability_adaptive` | system_replayability, replay, deterministic replay | skills/skill_system_replayability_adaptive.md |
| `aecf_project_context_generator` | project_context, generar contexto, scan project | skills/skill_project_context_generator.md |
| `aecf_document_context_ingestion` | document_context_ingestion, ingestar documentación | skills/skill_document_context_ingestion.md |
| `aecf_executive_summary` | executive_summary, resumen ejecutivo | skills/skill_executive_summary.md |
| `aecf_data_classification` | data_classification, clasifica campos, clasifica modelos ORM | skills/skill_data_classification.md |
| `aecf_new_project` | new_project, nuevo proyecto, scaffold project | skills/skill_new_project.md |
| `aecf_codebase_intelligence` | codebase_intelligence, analizar arquitectura | skills/skill_codebase_intelligence.md |
| `aecf_application_lifecycle` | application_lifecycle, ciclo de vida | skills/skill_application_lifecycle.md |
| `aecf_coupling_assessment` | coupling_assessment, acoplamiento | skills/skill_coupling_assessment.md |
| `aecf_productivity` | productivity, productividad, cuadro de mando | skills/skill_productivity.md |
| `aecf_resolve_linting` | resolve_linting, linting, lint errors | skills/skill_resolve_linting.md |
| `aecf_set_stack` | set_stack, definir stack | skills/skill_set_stack.md |
| `aecf_surface_discovery` | surface_discovery, descubrir superficies | skills/skill_surface_discovery.md |
| `aecf_security_review_gdpr` | security_review_gdpr, gdpr, rgpd | skills/skill_security_review_gdpr.md |
| `aecf_security_review_eu_ai_act` | security_review_eu_ai_act, eu_ai_act, ley ia | skills/skill_security_review_eu_ai_act.md |
| `aecf_security_review_dora` | security_review_dora, dora | skills/skill_security_review_dora.md |

> Full keyword tables and detailed trigger phrases live in each skill's `DISPATCHER GUIDE` section and in `SKILL_CATALOG.md`.

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

Reserved TOPIC names (MUST be rejected with an error message):
- `context` — reserved for codebase intelligence artifacts (`documentation/context/`)

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
<DOCS_ROOT>/<user_id>/{{TOPIC}}/
```

`<DOCS_ROOT>` resolves as: `artifacts_path` setting from `.aecf/user_settings.json` (as `.aecf/<artifacts_path>`) → `AECF_PROMPTS_DOCUMENTATION_PATH` env var → `AECF_PROMPTS_DIRECTORY_PATH` (legacy alias) → `<workspace>/.aecf/documentation` (default).

### 2.4 Sequential Numbering

ALWAYS:
1. Check existing files in `<DOCS_ROOT>/<user_id>/{{TOPIC}}/`
2. Find the highest `AECF_<NN>_` number
3. Use `<NN+1>` as next number
4. If directory is empty or new, start at `01`

Format: Two-digit zero-padded: `01`, `02`, `03`, ... `10`, `11`...

### 2.5 Attribution Resolution (Mandatory)

`<user_id>` is resolved ONCE at skill invocation and reused for all governance paths.

Resolution chain (first available wins):
1. `AECF_PROMPTS_USER_ID` environment variable
2. `AECF_PROMPTS_MODEL_ID` or `MODEL_ID` environment variable
3. `AECF_PROMPTS_AGENT_ID` or `AGENT_ID` environment variable
4. Output of `aecf_prompts/scripts/bootstrap_prompt_only_bundle.exe --diagnose-env` if available
5. **Fallback**: generate a random 8-character lowercase alphanumeric identifier (e.g. `user_k7m2p9xa`). Prefix it with `user_` to make it recognizable as auto-generated.

The resolved value is sanitized to `[a-z0-9_-]` (replace any non-matching character with `_`).

Forbidden:
- ❌ Silently falling back to OS username, hostname, or machine-specific identifier
- ❌ Asking the user for attribution — resolution must be autonomous
- ❌ Using `anonymous` as fallback — always generate a unique random identifier

### 2.6 Output Language Resolution (Mandatory)

`output_language` is resolved ONCE at skill invocation and applied to all generated narrative text.

Resolution chain (first available wins):
1. **MCP dispatch result** → `output_language` field (when dispatched via `aecf_dispatch_skill`)
2. **User settings** → `output_language` in `.aecf/user_settings_<user_id>.json` or `.aecf/user_settings.json`
3. **`AECF_RUN_CONTEXT.json`** → `output_language` field (if present)
4. **`auto`** → detect language from the user's prompt

Scope of application:
- **Narrative text** (descriptions, findings, summaries, recommendations) → uses the resolved language
- **Machine keys** (phase names, metadata fields, header names, enum values, file names) → always English

When `output_language` resolves to `auto`, the AI MUST detect the user's prompt language and use that for narrative text. If detection is ambiguous, default to Spanish (`es`).

---

## 3. EXECUTION

→ After resolving skill + parameters above, follow **EXECUTION_PROTOCOL.md** for the universal execution contract (Steps 1–5: Acknowledge → Load Contexts → Execute Skill → Generate Output → Confirm).

Each skill_*.md file is **self-contained**: it includes phase definitions, exit gates, required context files, and its own DISPATCHER GUIDE section with minimal valid invocations and auto-resolution defaults.

### Pre-execution self-check

Before executing, verify:
- [ ] Skill correctly identified?
- [ ] TOPIC resolved (explicit or inferred)?
- [ ] Scope resolved?
- [ ] Next sequential number determined?
- [ ] Output path: <DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_<NN>_<NAME>.md?
- [ ] If skill + TOPIC + prompt present → Pattern D triad enforcement applied?

If ANY item is unresolvable, ask the user ONCE with a specific question.

---

**END OF SKILL_DISPATCHER.md (Slim)**
