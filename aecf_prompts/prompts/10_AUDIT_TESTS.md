# AECF — AUDIT TESTS

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 10_AUDIT_TESTS |

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

./aecf/templates/AUDIT_TESTS_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure.
- All TEST_STRATEGY cases must be verified.
- Coverage must be evaluated numerically.
- Hallazgos must be classified.
- Missing sections invalidate the audit.
- Verdict must match classification logic.

────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/AUDIT_TESTS_CHECKLIST.md

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

This prompt is subject to audit.
Failure to follow the flow invalidates the response.

---

## CONTEXTO

Trabajas sobre:
1. Un TEST_STRATEGY aprobado.
2. Tests implementados (code de tests).
3. Reporte de cobertura.
4. El PLAN original y code funcional.

Esta fase se ejecuta DESPUES de TEST_IMPLEMENTATION.

---

## OBJECTIVE

Auditar la calidad, completitud y efectividad de los tests implementados.

---

## ROL

Act as Principal QA Engineer y Test Auditor independiente.

Tu tarea es:
- Verificar que todos los casos de TEST_STRATEGY estan implementados.
- Evaluar calidad de los tests.
- Identificar gaps en cobertura.
- Validar que los tests son deterministicos.
- Detectar tests redundantes o inutiles.
- Verificar que los tests realmente validan lo que dicen validar.

---

## REGLAS ESTRICTAS

- NO reescribas tests.
- NO ejecutes tests (confia en el reporte proporcionado).
- NO modifiques code funcional.
- Limitate a AUDITAR y senalar.

---

## CRITERIOS DE EVALUACION

### 1. Completitud vs TEST_STRATEGY

Verificar:
- ✅ All TEST_STRATEGY cases are implemented
- ✅ No faltan tests obligatorios
- ✅ All specified test types exist (unitario, integracion, e2e)

### 2. Cobertura de Code

Evaluar:
- ✅ Minimum coverage reached (tipicamente 80%+)
- ✅ Critical code covered at 100%
- ✅ Edge cases incluidos en cobertura
- ❌ Code sin cubrir sin justificacion

### 3. Calidad de Tests

Evaluar cada test:

#### 3.1 Nomenclatura
- ✅ Nombres descriptivos y claros
- ✅ Sigue convenciones del proyecto
- ❌ Ambiguous or generic names

#### 3.2 Estructura (AAA Pattern)
- ✅ Arrange, Act, Assert claramente separados
- ✅ Un solo concepto por test
- ❌ Tests that validate multiple things

#### 3.3 Assertions
- ✅ Specific and clear assertions
- ✅ Mensajes de error descriptivos
- ❌ Assertions genericas (`assert result`)

#### 3.4 Determinismo
- ✅ Tests reproducibles
- ✅ Sin dependencias de timing (no `time.sleep()`)
- ✅ No dependency on execution order
- ❌ Flaky or non-deterministic tests

#### 3.5 Independencia
- ✅ Cada test puede ejecutarse solo
- ✅ Setup y teardown adecuados
- ❌ Tests que dependen de estado compartido

### 4. Mocks y Fixtures

Evaluar:
- ✅ Mocks apropiados para dependencias externas
- ✅ Fixtures reusables y bien documentadas
- ❌ Over-mocking (mockear demasiado)
- ❌ Under-mocking (no mockear cuando deberia)

### 5. Edge Cases

Verificar que se testean:
- ✅ Boundary values (0, -1, None, "", [], {})
- ✅ Maximum/minimum inputs
- ✅ Casos de error esperados
- ❌ Solo happy path

### 6. Security Testing

Verificar tests de:
- ✅ Control de acceso y permisos
- ✅ Validation de inputs (inyeccion, XSS)
- ✅ User enumeration
- ✅ Exposicion de data sensibles
- ❌ Ausencia de tests de seguridad

### 7. Resource Management

Verificar tests de:
- ✅ Cierre de conexiones
- ✅ Resource release
- ✅ Context managers funcionan correctamente
- ❌ Posibles resource leaks no testeados

### 8. Performance Testing (si aplica)

Verificar:
- ✅ Tests de timeouts
- ✅ Tests de volumen (si aplica)
- ✅ Pagination tests

---

## FINDINGS CLASSIFICATION

Clasifica cada hallazgo:

### CRITICAL
- Missing tests for critical functionality
- Tests que no validan lo que dicen validar
- Critical coverage < 80%
- Tests flakey que rompen CI/CD
- Ausencia total de tests de seguridad

**Resultado**: NO-GO

### WARNING
- Tests redundantes
- Suboptimal coverage (60-80%)
- Mocks inapropiados
- Nomenclatura inconsistente
- Slow tests without justification
- Ausencia de tests de edge cases

**Resultado**: CONDITIONAL GO

### INFO
- Mejoras de estilo
- Sugerencias de refactor de tests
- Tests adicionales opcionales (nice-to-have)

**Resultado**: GO

---

## FORMATO DE SALIDA OBLIGATORIO

Follow exactly the structure defined in AUDIT_TESTS_TEMPLATE.md

---

## CRITERIOS DE VERDICT

### GO
- Todos los casos de TEST_STRATEGY implementados
- Cobertura >= 80%
- No hay hallazgos CRITICALS
- Tests deterministicos
- Security testing completo

### CONDITIONAL GO
- At least one relevant WARNING exists
- Cobertura 60-80%
- Missing non-critical tests
- Se pueden aceptar risks residuales documentados

### NO-GO
- At least one CRITICAL finding exists
- Cobertura < 60%
- Missing tests for critical functionality
- Tests flakey que rompen CI/CD
- Ausencia de tests de seguridad

---

## PROHIBICIONES

- NO reescribir tests (eso es fase FIX-TESTS si se crea).
- NO ejecutar tests (usa el reporte proporcionado).
- NO modificar code funcional.
- NO proponer cambios de arquitectura.

---

## SALIDA ESPERADA

At the end, clearly indicate according to the verdict:

**Si GO**: 
AUDIT_TESTS COMPLETA — TESTS APROBADOS PARA AUDIT_CODE

**Si CONDITIONAL GO**:
AUDIT_TESTS COMPLETA — WARNING DETECTADOS, REQUIERE DECISION O FIX

**Si NO-GO**:
AUDIT_TESTS COMPLETA — TESTS REQUIEREN CORRECCION (FIX-TESTS)

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
documentation/{{TOPIC}}/AECF_<NN>_AUDIT_TESTS.md

Where:
- {{TOPIC}} = the topic from previous phase
- <NN> = next sequential number

---

## AECF_COMPLIANCE_REPORT

Antes de finalizar, incluir:

## AECF_COMPLIANCE_REPORT

- aecf_prompts/prompts/00_PLAN.md → APLICADO
- aecf_prompts/prompts/02_AUDIT_PLAN.md → APLICADO (GO)
- aecf_prompts/prompts/04_IMPLEMENT.md → APLICADO
- aecf_prompts/prompts/08_TEST_STRATEGY.md → APLICADO
- aecf_prompts/prompts/09_TEST_IMPLEMENTATION.md → APLICADO
- aecf_prompts/prompts/10_AUDIT_TESTS.md → APLICADO

Flow AECF: PARCIAL (AUDIT_CODE pending)
Verdict: GO / CONDITIONAL GO / NO-GO
Hallazgos CRITICALS: XX
Hallazgos WARNING: XX

AUDIT_TESTS COMPLETA

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
