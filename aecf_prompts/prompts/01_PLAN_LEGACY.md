> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 01_PLAN_LEGACY |

MODO: LEGACY

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This prompt operates under the following mandatory contexts:

- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- <workspace_root>/AECF_PROJECT_CONTEXT.md (if present anywhere in the active workspace)
- **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — if present, use `output_language` as the frozen language for the entire execution.

Governance:
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

## OUTPUT LANGUAGE

1. Resolve `OUTPUT_LANGUAGE` from `AECF_RUN_CONTEXT.json` if it exists.
2. If missing, use `OUTPUT_LANGUAGE` from `AECF_PROJECT_CONTEXT.md`.
3. If both are missing, use ENGLISH.
4. Visible narrative must use the resolved language.
5. Control-plane contract elements must remain stable and in English where applicable.

------------------------------------------------------------

HARD PRECONDITION: Load and enforce context with hierarchy:
1. SYSTEM_CONTEXT: aecf_prompts/AECF_SYSTEM_CONTEXT.md
2. PROJECT_CONTEXT (workspace): <workspace_root>/AECF_PROJECT_CONTEXT.md (if exists, overrides defaults)

📌 TOPIC: Maintain {{TOPIC}} from previous phase. All outputs in: documentation/{{TOPIC}}/

FASE: PLAN_LEGACY

Contexto:
La funcionalidad esta implementada
en los files que acabamos de obtener

Objective:
Comprender y contextualizar la funcionalidad existente
para permitir su planificacion o audit posterior.
NO emitir verdicts de seguridad ni calidad.

REGLAS:
- NO generes code
- NO refactorices

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/PLAN_LEGACY_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure and headings of the template.
- You may only add content inside sections.
- You may NOT modify headings.
- You may NOT remove sections.
- Missing sections invalidate the PLAN_LEGACY output.
- No design, no refactor, no quality judgment allowed.

Formato de salida obligatorio:
Follow exactly the structure defined in PLAN_LEGACY_TEMPLATE.md

────────────────────────
INPUT / OUTPUT CONTRACT (MANDATORY)
────────────────────────

Expected input artifact from previous phase:
- documentation/{{TOPIC}}/AECF_<NN_prev>_DISCOVERY.md

This phase MUST generate:
- documentation/{{TOPIC}}/AECF_<NN>_PLAN_LEGACY.md

Traceability rule:
- The output MUST reference the discovery artifact used as input.
- It MUST keep a clear sequence of decisions inherited from discovery.

------------------------------------------------------------

## CONTEXT VALIDATION

Confirm:

[ ] AECF_SYSTEM_CONTEXT.md loaded
[ ] Workspace AECF_PROJECT_CONTEXT.md checked (if present)
[ ] Governance rules applied

If confirmation cannot be provided → STOP execution.

------------------------------------------------------------

───────────────────────────────
📁 OUTPUT GENERATION (MANDATORY)
───────────────────────────────

Generate document:
documentation/{{TOPIC}}/AECF_<NN>_PLAN_LEGACY.md

Where:
- {{TOPIC}} = topic maintained from previous phase
- <NN> = next sequential number (01, 02, 03...)

Finaliza con EXACTAMENTE:
PLAN LEGACY COMPLETADO PARA AECF

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
