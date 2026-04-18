# AECF — IMPLEMENT

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 04_IMPLEMENT |

------------------------------------------------------------

## MANDATORY CONTEXT LOAD

This prompt operates under the following mandatory contexts:

- aecf_prompts/AECF_SYSTEM_CONTEXT.md
- <workspace_root>/AECF_PROJECT_CONTEXT.md (if present anywhere in the active workspace)

Governance:
- aecf_prompts/_governance/AECF_EXECUTIVE_SUMMARY_GOVERNANCE.md

If any of these contexts exist, they MUST be considered active constraints.

Execution is INVALID if these contexts are not acknowledged.

------------------------------------------------------------

HARD PRECONDITION: Load and enforce context with hierarchy:
1. SYSTEM_CONTEXT: aecf_prompts/AECF_SYSTEM_CONTEXT.md
2. PROJECT_CONTEXT (workspace): <workspace_root>/AECF_PROJECT_CONTEXT.md (if exists, overrides defaults)

📌 TOPIC: Maintain {{TOPIC}} from previous phase. All outputs in: documentation/{{TOPIC}}/

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/IMPLEMENT_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure of IMPLEMENT_TEMPLATE.md.
- Code must only implement what is defined in the approved PLAN (GO).
- No new design decisions are allowed.
- No scope expansion is allowed.
- All technical obligations must be enforced.
- Missing sections invalidate the IMPLEMENT phase.

────────────────────────
🏷️ FUNCTION-LEVEL METADATA ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and apply:

./aecf/code/CODE_FUNCTION_METADATA_STANDARD.md

Rules — CREATION:
- Every new function/method/class/module MUST include a full `AECF_META` line inside its docstring
  (or equivalent language comment, per language format in the standard).
- Required fields: `skill`, `topic`, `run_time`, `generated_at`, `generated_by`,
  `last_modified_skill`, `last_modified_at`, `last_modified_by`, `touch_count`.
- On creation: `last_modified_*` and `run_time` MUST equal `generated_*` timestamps.
- Values to use:
  - `skill` → current Skill ID (e.g. `aecf_new_feature`)
  - `topic` → resolved {{TOPIC}} for this execution chain
  - `run_time` → current UTC ISO-8601 timestamp for the active AECF run
  - `generated_at` / `last_modified_at` → current UTC ISO-8601 timestamp
  - `generated_by` / `last_modified_by` → `Executed By ID` from execution context
  - `touch_count` → `1`
- Identity rule: NEVER write `aecf`, `copilot`, `assistant`, the skill id, or the model name into
  `generated_by` / `last_modified_by`; those fields MUST contain the effective `Executed By ID`
  (or `N/A` when the execution chain has no user identity).
- Human-maintenance rule: add enough comments/docstrings to explain non-obvious intent,
  invariants, fixtures, cleanup, and risk-driven choices so a human can maintain the code later.
- Human-readable comments/docstrings MUST use the resolved `OUTPUT_LANGUAGE` /
  `aecf.documentationOutputLanguage`; `AECF_META` keys stay English-only.
- Missing `AECF_META` in any produced function = **automatic IMPLEMENT checklist failure**.

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
documentation/{{TOPIC}}/AECF_<NN>_IMPLEMENT.md

Where:

OUTPUT CONTRACT FOR APPLY (MANDATORY):
- Return ONLY these two top-level blocks and nothing else:
  1) <AECF_FILE_CHANGES> ... </AECF_FILE_CHANGES>
  2) <AECF_PHASE_ARTIFACT> ... </AECF_PHASE_ARTIFACT>
- Inside <AECF_FILE_CHANGES>, include one or more file blocks in this exact format:
  <<<FILE:relative/path/from/execution_root>>>
  <full file content>
  <<<END_FILE>>>
- Do NOT use markdown code fences.
- Do NOT add narrative, explanations, confirmations, or questions outside those two blocks.
- IMPLEMENT must include at least one production code file (e.g., src/ or app/) and, when production code changes, at least one test file under tests/ or __tests__/.
- When tests are added/modified in IMPLEMENT, <AECF_PHASE_ARTIFACT> MUST include section `## Test Taxonomy Evidence` with a markdown table:
  `Taxonomy Group | Category | Status | Evidence`.
- <AECF_PHASE_ARTIFACT> MUST include section `## Static Analysis Profile` identifying only the applicable static checks for the changed scope.
- `## Static Analysis Profile` MUST contain a markdown table with columns:
  `Tool | Category | Surface | Scope | Blocking | Rationale`.
- Categories allowed in `## Static Analysis Profile`: `lint`, `format_check`, `type_check`, `security_static`.
- When a category is not applicable, explain it explicitly instead of inventing a tool.
- IMPLEMENT defines applicability only; execution evidence for blocking static checks is audited in `AUDIT_STATIC_ANALYSIS`, not in IMPLEMENT.
- Required Category rows in `## Test Taxonomy Evidence`:
  - Test types: `unit`, `integration`, `e2e` (at least one must be `COVERED`; others can be `MISSING`/`NOT_APPLICABLE`).
  - Mandatory case categories: `happy_path`, `edge_case`, `error_handling` (MUST be `COVERED`).
  - Conditional categories: `security`, `performance` (`COVERED` when applicable, otherwise `NOT_APPLICABLE` with reason).
- Evidence column rules (MANDATORY):
  - The `Evidence` cell MUST list ONLY the specific test names/files that directly cover that particular category. Do NOT copy the full test list into every row.
  - For rows with Status `MISSING` or `NOT_APPLICABLE`, the `Evidence` cell MUST be empty or contain `none`. Listing tests as evidence on a `MISSING` row is a contract violation.
  - For rows with Status `COVERED`, list only the tests that target that specific taxonomy category (e.g., `error_handling` evidence should only cite tests that validate error/exception paths).
- If this contract is not followed exactly, APPLY is invalid.

────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/IMPLEMENT_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.

────────────────────────
SCORING ENFORCEMENT (MANDATORY)
────────────────────────

You MUST:

1. Score each checklist item (0,1,2).
2. Apply category weights.
3. Compute normalized score.
4. Declare maturity level.
5. Apply automatic verdict rules.

If scoring is not included → Phase invalid.

Include in AECF_COMPLIANCE_REPORT:

## AECF_SCORE_REPORT

- Raw Score:
- Normalized Score:
- Maturity Level:
- Automatic Verdict:
- Critical Findings Present: YES / NO

────────────────────────

Act as Senior Software Engineer.

This prompt is subject to audit.
Failure to follow the flow invalidates the response.

Trabaja sobre el plan generado o regenerado:
1. Un PLAN DE IMPLEMENTACION con VERDICT GO.
2. (Opcionalmente) restricciones tecnicas adicionales.

Tu tarea es IMPLEMENTAR el plan de forma literal.

Debes:
- Seguir el plan paso a paso.
- No introducir nuevas decisiones de diseno.
- Respetar el alcance definido.
- Implementar code claro, mantenible y documentado.

────────────────────────
⚠️ OUTPUT SIZE CONSTRAINT (MANDATORY)
────────────────────────

Your ENTIRE response (all file blocks + AECF_PHASE_ARTIFACT + AECF_COMPLIANCE_REPORT)
MUST fit within approximately 8,000 output tokens (~2,500 lines).

If the PLAN scope exceeds this budget:
1. Implement the MINIMUM VIABLE subset that demonstrates the pattern.
2. Clearly state in AECF_PHASE_ARTIFACT what was deferred and why (output budget constraint).
3. DO NOT attempt to generate exhaustive content that will be truncated.
4. Prefer concise, well-structured code over verbose boilerplate.
5. Use inline comments sparingly — only where logic is non-obvious.
6. Do NOT include example usage blocks or extensive docstrings when the function signature
7. Prefer stack-native static analysis tools already present in the repo; do not invent or install new linters automatically.
   is self-explanatory.

PRIORITY ORDER when output budget is tight:
1. Production code files (required)
2. Test files (required — at least one)
3. AECF_PHASE_ARTIFACT (required)
4. AECF_COMPLIANCE_REPORT (required, keep minimal)

A truncated response is WORSE than a scoped-down but complete response.

REGLAS ESTRICTAS:
- NO redisenes.
- NO cuestiones el plan.
- NO anadas funcionalidades no descritas.
- AECF NO puede instalar librerías automáticamente en el entorno del cliente.
- Si necesitas dependencias externas nuevas para completar la implementación o ejecutar tests, debes pedir aprobación explícita del usuario y esperar a que la instalación la haga el usuario manualmente fuera de AECF.
- No simules que una dependencia está instalada ni inventes ejecuciones satisfactorias si el entorno no la tiene disponible.
- Si necesitas esa aprobación, emite una solicitud de aprobación estructurada usando `Type: approval_request` con una pregunta concreta y opciones para continuar o cancelar.
- Si algo no esta claro, detente y dilo explicitamente.
- No adelantes fases
- No omitas artefactos obligatorios
- No incluyas razonamientos internos
- No incluyas contenido fuera del contrato

TECHNICAL OBLIGATIONS OBLIGATORIAS:

0. Dependency governance
  - Si introduces una dependencia Python nueva, declárala en `requirements.txt` dentro de `AECF_FILE_CHANGES`.
  - La instalación la realiza exclusivamente el usuario, nunca AECF.
  - Si la continuación depende de esa instalación manual, solicita aprobación explícita con este formato mínimo:
    - `Approval required`
    - `Type: approval_request`
    - `Question: ¿Apruebas instalar manualmente las dependencias requeridas para continuar IMPLEMENT?`
    - `Options:`
     - `1. Sí, las instalaré y continuaré`
     - `2. No, cancelar la ejecución`
  - No conviertas esta situación en un `UNKNOWN`: en IMPLEMENT debe resolverse mediante aprobación del usuario o cancelación explícita.

1. Logging
   - Todo code debe usar el sistema de logging del proyecto.
   - Si no existe, debe crearse un logger estructurado minimo.
   - Prohibido usar print().
   - El logger minimo debe:
     - Tener nombre de module o funcionalidad
     - Usar niveles (info, warning, error)
     - Incluir contexto relevante (request_id, usuario si aplica)
   - Los eventos de error y seguridad deben registrarse explicitamente.

2. Management de recursos
   - Toda conexion o recurso abierto directa o indirectamente
     (incluidos helpers o servicios llamados)
     debe cerrarse explicitamente o mediante context managers.
   - No deben quedar recursos abiertos tras la ejecucion.

3. Control de acceso
   - Se considera “dato sensible” cualquier informacion que permita:
     - Identificar usuarios
     - Inferir privilegios
     - Acceder a informacion personal o interna
   - Si la funcionalidad expone este tipo de data:
     - Debe implementarse control de acceso, o
     - Justificarse explicitamente por que no aplica

4. User enumeration
   - Los mensajes de error no deben permitir inferir
     la existencia de usuarios u objetos sensibles.

5. Exposicion de data:
  - Solo devolver campos estrictamente necesarios
  - Cualquier campo sensible debe justificarse     

6. Paginacion
   - Requerida por defecto en endpoints que devuelvan listas.
   - Puede omitirse solo si:
     - El volumen es acotado y documentado, o
     - El PLAN lo justifica explicitamente.

7. Function-level AECF Metadata
   - Every function/method created MUST include an `AECF_META` line in its docstring.
   - See `aecf_prompts/code/CODE_FUNCTION_METADATA_STANDARD.md` for canonical format per language.
   - Mandatory fields: skill, topic, generated_at, generated_by,
     last_modified_skill, last_modified_at, last_modified_by.
   - On creation last_modified_* MUST mirror generated_*.
   - Omitting this line from any function is an automatic checklist failure.

El code debe incluir:
- Docstrings claras
- Tipado cuando aplique
- Ejemplos de uso si procede

Al finalizar, indica claramente:
IMPLEMENTACION COMPLETADA

-------------------------------------------------------------------------

OBLIGATORIO — Verificacion de cumplimiento AECF

Antes de finalizar, debes incluir una section titulada exactamente:

## AECF_COMPLIANCE_REPORT

En esa section debes:

1. Enumerar que files de `aecf_prompts/` has seguido,
   indicando para cada uno:
   - Nombre exacto del file
   - Fase que representa
   - Estado (APLICADO / NO APLICADO)

2. Indicar si el flow AECF se ha seguido de forma completa o parcial.

3. Declarar explicitamente:
   - Si se ha generado code sin una fase previa (PLAN o AUDIT)
   - Si se ha tomado alguna decision no contenida en el PLAN aprobado

FORMATO OBLIGATORIO (ejemplo):

## AECF_COMPLIANCE_REPORT

- aecf_prompts/prompts/00_PLAN.md → APLICADO
- aecf_prompts/prompts/02_AUDIT_PLAN.md → APLICADO (GO)
- aecf_prompts/prompts/04_IMPLEMENT.md → APLICADO
- aecf_prompts/prompts/05_AUDIT_CODE.md → NO APLICADO (pendiente)

Flow AECF: COMPLETO / PARCIAL  
Decisiones fuera de plan: NO  
Code generado sin audit previa: NO

No expliques razonamientos internos.
No incluyas pensamiento paso a paso.
Limitate a declarar cumplimiento del proceso.

IMPLEMENT LISTO PARA AUDIT_CODE

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check

