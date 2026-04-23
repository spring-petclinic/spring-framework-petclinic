# AECF — FIX CODE

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 06_FIX_CODE |

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

HARD PRECONDITION: Load and enforce context with hierarchy:
1. SYSTEM_CONTEXT: aecf_prompts/AECF_SYSTEM_CONTEXT.md
2. PROJECT_CONTEXT (workspace): <workspace_root>/AECF_PROJECT_CONTEXT.md (if exists, overrides defaults)

📌 TOPIC: Maintain {{TOPIC}} from previous phase. All outputs in: documentation/{{TOPIC}}/

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/FIX_CODE_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure of FIX_CODE_TEMPLATE.md.
- Only findings explicitly flagged in AUDIT_CODE may be corrected.
- No scope expansion allowed.
- No redesign allowed.
- No new features allowed.
- All mandatory correction obligations must be addressed if present in AUDIT_CODE.
- Missing sections invalidate FIX_CODE.

────────────────────────
🏷️ FUNCTION-LEVEL METADATA UPDATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and apply:

./aecf/code/CODE_FUNCTION_METADATA_STANDARD.md

Rules — MODIFICATION:
- For every function/method/class/module whose implementation is changed in this FIX_CODE execution:
  1. Locate the existing `AECF_META` line in the function/class/module docstring or equivalent comment block.
  2. Update ONLY the latest-touch fields:
     - `last_modified_skill` → `aecf_fix_code` (or current executing skill)
     - `last_modified_at` → current UTC ISO-8601 timestamp
     - `last_modified_by` → `Executed By ID` from execution context
     - `run_time` → current UTC ISO-8601 timestamp for the active AECF run
     - `touch_count` → previous value + `1`
  3. DO NOT modify `skill`, `topic`, `generated_at`, or `generated_by`.
     These fields preserve origin provenance and MUST remain unchanged.
- If a modified function has NO `AECF_META` line (legacy / pre-standard code):
  - ADD the full line with current skill/timestamp for all creation fields.
  - Set `run_time=<current UTC timestamp>` and `touch_count=1`.
  - Append `retroactive=true` at the end to flag it as retroactively added.
- Human-maintenance rule: if the change alters non-obvious logic, fixtures, teardown, or risk
  handling, add/update enough comments/docstrings for a future human maintainer.
- Human-readable comments/docstrings MUST use the resolved `OUTPUT_LANGUAGE` /
  `aecf.documentationOutputLanguage`; `AECF_META` keys stay English-only.
- Missing metadata update on any modified function = **automatic FIX_CODE checklist failure**.

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
documentation/{{TOPIC}}/AECF_<NN>_FIX_CODE.md

Where:
- {{TOPIC}} = inherited topic
- <NN> = next sequential number

This prompt is subject to audit.
Failure to follow the flow invalidates the response.

Act as Senior Software Engineer responsable de correccion en entorno productivo.

Te proporciono:
1. Code auditado.
2. Informe de AUDIT-CODE con VERDICT NO-GO o CONDITIONAL GO.

Tu tarea es:
- Aplicar SOLO los cambios minimos necesarios para que el code
  sea apto para production.
- Corregir exclusivamente los puntos senalados en el AUDIT-CODE.
- No modificar comportamiento funcional no afectado.

REGLAS ESTRICTAS:
- NO redisenes la funcionalidad.
- NO optimices por rendimiento salvo que el AUDIT-CODE lo exija.
- NO amplies funcionalidad.
- NO introduzcas nuevas dependencias sin justificacion explicita.
- No adelantes fases.
- No omitas artefactos obligatorios.
- No incluyas razonamientos internos.
- No incluyas contenido fuera del contrato.

PHASE VIOLATION:

- Si se introducen cambios no senalados en el AUDIT-CODE,
  la respuesta se considera INVALIDA.
- Si se redisena o amplia funcionalidad,
  la respuesta se considera INVALIDA.
  
---------------------------------------------------------------------

OBLIGACIONES DE CORRECCION EN FIX-CODE  
(deben abordarse SIEMPRE que aparezcan en AUDIT-CODE):

1. Logging
   - Sustituir cualquier uso de print() por logging profesional.
   - Usar el sistema de logging del proyecto.
   - Si no existe, crear un logger minimo y estructurado.
   - Registrar eventos de error y eventos relevantes de seguridad.

2. Management de recursos
   - Garantizar cierre explicito de cualquier recurso abierto
     (DB, files, pipes, sockets, sessions, engines).
   - Usar context managers o bloques finally cuando aplique.

3. Control de acceso
   - Si el AUDIT-CODE detecta ausencia de control de acceso:
     - Implementar el control minimo requerido, o
     - Justificar explicitamente por que no aplica en esta funcionalidad.

4. Enumeracion y exposicion de data
   - Neutralizar mensajes o respuestas que permitan inferir
     existencia de usuarios u objetos sensibles.
   - Reducir la exposicion de data a los campos estrictamente necesarios.

5. CONDITIONAL GO
   - Si el AUDIT-CODE indica CONDITIONAL GO:
     - Resolver todos los WARNING obligatorios.
     - Documentar explicitamente los WARNING aceptados como risk residual.

6. Function-level AECF Metadata Update
   - For every function modified in this fix: update the `last_modified_*` trio
     in the `AECF_META` line (skill, timestamp, user).
   - Preserved fields: skill, topic, generated_at, generated_by.
   - For functions without a prior `AECF_META` line: add the full line retroactively
     with `retroactive=true` appended.
   - See `aecf_prompts/code/CODE_FUNCTION_METADATA_STANDARD.md` for canonical format.

---------------------------------------------------------------------

NO SE PERMITE:
- Introducir cambios no senalados en el AUDIT-CODE.
- Resolver WARNING no exigidos alterando el diseno original.
- Convertir FIX-CODE en una reimplementacion encubierta.

---------------------------------------------------------------------

EXTENDED FIX SCOPE — AUDIT_IMPLEMENT TEST FAILURES (MANDATORY)

When the NO-GO originates from `AUDIT_IMPLEMENT` (automated test execution via pytest)
rather than from a manual `AUDIT_CODE` code-quality review, the fix scope EXPANDS as follows:

You MUST apply this triage before writing any fix:

### TRIAGE STEP (MANDATORY)

For each failing test, classify the failure as ONE of:

| Type | Description | Allowed Fix |
|---|---|---|
| `CODE_BUG` | Functional code is wrong or missing (e.g., function not implemented) | Fix the source code |
| `TEST_WRONG_IMPORT` | Test imports a symbol that doesn't exist in the module | Fix the test import to match the real module/symbol |
| `TEST_WRONG_ASSERTION` | Test assertion is semantically incorrect (e.g., comparing JSON string to YAML string) | Fix the assertion to be structurally correct |
| `TEST_WRONG_PATH` | Test references a file path or module path that doesn't match actual structure | Fix the path in the test |
| `AMBIGUOUS` | Cannot determine from test evidence alone | Read the actual implementation file first, then reclassify |

### FIX RULES

- `CODE_BUG` → Fix the production code. Do NOT modify the test unless the test itself is also wrong.
- `TEST_WRONG_*` → Fix the test. Do NOT modify production code for a test error.
- If BOTH code and test are wrong → Fix both, documenting each fix under its own hallazgo entry.
- `AMBIGUOUS` → MANDATORY: read the actual implementation file content before deciding.

### GROUNDING CHECK (WHEN FIXING TEST_WRONG_*)

Before writing a corrected test:
1. Read the actual implementation file.
2. Confirm the real symbol name and module path.
3. For assertion corrections: deserialize structured outputs to native structures before comparing. Never compare raw serialized strings of different formats.

This extended scope does NOT authorize:
- Adding new test cases beyond what was already failing.
- Changing the tested behavior described in TEST_STRATEGY.
- Altering production code behavior to make a wrong test pass.

---------------------------------------------------------------------

Al finalizar, indica exactamente:
CODE CORREGIDO LISTO PARA AUDIT

---------------------------------------------------------------------

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
   - Si existian WARNING aceptados como risk residual

FORMATO OBLIGATORIO (ejemplo):

## AECF_COMPLIANCE_REPORT

- aecf_prompts/prompts/00_PLAN.md → APLICADO
- aecf_prompts/prompts/02_AUDIT_PLAN.md → APLICADO (GO)
- aecf_prompts/prompts/04_IMPLEMENT.md → APLICADO
- aecf_prompts/prompts/05_AUDIT_CODE.md → APLICADO (CONDITIONAL GO)
- aecf_prompts/prompts/06_FIX_CODE.md → APLICADO

Flow AECF: COMPLETO  
Decisiones fuera de plan: NO  
Code generado sin audit previa: NO  
WARNING aceptados: YES / NO (detallar si aplica)

No expliques razonamientos internos.
No incluyas pensamiento paso a paso.
Limitate a declarar cumplimiento del proceso.

FIX_CODE LISTO PARA AUDIT_CODE

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
