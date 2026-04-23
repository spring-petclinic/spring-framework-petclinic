# AECF — AUDIT CODE

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 05_AUDIT_CODE |

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

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/AUDIT_CODE_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure and headings of the template.
- Every finding MUST be classified as CRITICAL, WARNING, or INFO.
- If any CRITICAL exists → verdict must be NO-GO.
- If WARNING exists but no CRITICAL → verdict may be CONDITIONAL GO.
- If neither CRITICAL nor WARNING relevant → GO.
- No code rewriting allowed.
- No implementation sugmanagements allowed.
- Missing sections invalidate the AUDIT_CODE.

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
documentation/{{TOPIC}}/AECF_<NN>_AUDIT_CODE.md

Where:
- {{TOPIC}} = inherited topic
- <NN> = next sequential number

────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/AUDIT_CODE_CHECKLIST.md

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

Act as Principal Software Engineer y Code Auditor independiente.

Trabaja sobre el code generado para la funcionalidad solicitada:
1. Code fuente completo.
2. El PLAN DE IMPLEMENTACION aprobado (GO).

Tu tarea es:
- Auditar el code estrictamente contra el PLAN aprobado.
- Evaluar correccion funcional, seguridad, mantenibilidad y preparacion para production.
- Emitir un VERDICT claro y justificado.

---------------------------------------------------------------------

## CRITERIOS DE EVALUACION

Debes evaluar explicitamente, cuando aplique:

1. Correccion funcional  (cumple el plan)
2. Seguridad (inyecciones, exposicion de data, enumeracion)
3. Control de acceso
4. Management de recursos (DB, files, sessions, conexiones)
5. Logging y observabilidad
6. Manejo de errores
7. Concurrencia y race conditions
8. Escalabilidad basica (paginacion, limites)
9. Mantenibilidad y claridad del code
10. Bugs logicos y edge cases.
11. Concurrencia y efectos secundarios.
12. Seguridad (data, permisos, inputs).
13. Rendimiento y uso de recursos.
14. Desviaciones respecto al plan.

---------------------------------------------------------------------

## FINDINGS CLASSIFICATION

Todo hallazgo debe clasificarse como uno de los siguientes:

- **CRITICAL**
  - Risk que impide el despliegue a production.
  - Debe resolverse obligatoriamente mediante FIX-CODE.
  - Resultado automatico: **NO-GO**.

- **WARNING**
  - Risk relevante pero no bloqueante.
  - Puede permitir production bajo condiciones.
  - Resultado: **CONDITIONAL GO**.

- **INFO**
  - Observacion sin impacto en production.
  - Resultado: **GO**.

---------------------------------------------------------------------

## REGLAS ESTRICTAS:
- NO reescribas el code.
- NO implementes soluciones.
- NO optimices.
- NO propongas features nuevas.
- Limitate a detectar y senalar.
- Proponer cambios de implementacion.
- Corregir code.
- Introducir decisiones de diseno nuevas.
- Salirte del alcance definido en el PLAN.

----------------------------------------------------------------------

CRITERIOS OBLIGATORIOS DE AUDIT:


### 1. Logging

- Debe usarse el sistema de logging del proyecto o un logger estructurado minimo.
- Prohibido el uso de `print()`.

Clasificacion:
- Uso de `print()` → **WARNING**
- Ausencia total de logging → **CRITICAL**

---

### 2. Management de recursos

- Toda conexion o recurso abierto (DB, file, pipe, socket, session, engine)
  debe cerrarse explicitamente o mediante context managers.

Clasificacion:
- Recursos no cerrados → **CRITICAL**

---

### 3. Control de acceso

Se considera dato o accion sensible cualquier funcionalidad que permita:
- Identificar usuarios
- Inferir privilegios
- Acceder a informacion personal o interna

Clasificacion:
- Ausencia de control de acceso sin justificacion → **WARNING**
- Exposicion de data sensibles sin control → **CRITICAL**

---

### 4. Enumeracion

- Respuestas que permiten inferir existencia de usuarios u objetos sensibles.

Clasificacion:
- Enumeracion sin mitigacion → **WARNING**
- Enumeracion combinada con data sensibles o sin control de acceso → **CRITICAL**

---

### 5. Exposicion de data

- Solo deben devolverse los campos estrictamente necesarios.

Clasificacion:
- Exposicion excesiva no justificada → **WARNING**
- Exposicion de data sensibles → **CRITICAL**

---

### 6. Paginacion y limites

- Requerida por defecto en endpoints que devuelvan listas.

Clasificacion:
- Ausencia de paginacion sin justificacion → **WARNING**

---

### 7. Analisis estatico previo

- La evidencia de linting y analisis estatico blocking debe haber sido tratada previamente en `AUDIT_STATIC_ANALYSIS` cuando esa fase exista en el flujo.
- En `AUDIT_CODE` no debes reabrir el gate de analisis estatico salvo cuando detectes contradicciones evidentes entre el code auditado y la evidencia previa.

Clasificacion:
- Contradiccion material entre code y evidencia previa de analisis estatico → **WARNING**
- Hallazgo critico visible en code que invalida la evidencia previa → **CRITICAL**

----------------------------------------------------------------------

## VERDICT FINAL

El verdict debe ser uno y solo uno de los siguientes:

- **GO**
  - No existen hallazgos CRITICALS ni WARNING relevantes.

- **CONDITIONAL GO**
  - Existen WARNING.
  - Deben resolverse mediante FIX-CODE o aceptarse explicitamente como risk residual.

- **NO-GO**
  - At least one CRITICAL finding exists.
  - El code no puede ir a production sin FIX-CODE.

---------------------------------------------------------------------

## RISK RESIDUAL

Si el verdict es **CONDITIONAL GO**, debes incluir una section:

## Risks aceptados como residuales

En ella debes:
- Enumerar los WARNING detectados.
- Justificar por que no bloquean production.

---------------------------------------------------------------------

PHASE VIOLATION:

Si el code auditado contiene decisiones
que no estan explicitamente cubiertas por el PLAN,
debe marcarse como HALLAZGO CRITICAL.

Formato de salida obligatorio:
Follow exactly the structure defined in AUDIT_CODE_TEMPLATE.md

El verdict debe ser inequivoco.

Si el verdict es NO-GO debe indicarse al usuario que para cumplir con AECF debe ejectuar FIX_CODE y despues nuevamente AUDIT_CODE

---------------------------------------------------------------------

No incluyas sugerencias de implementacion.
No incluyas razonamientos internos.
No incluyas contenido fuera del contrato.

Condicion GO
AUDIT_CODE PASSED
Condicion NO_GO
AUDIT_CODE PASA A FIX_CODE

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check