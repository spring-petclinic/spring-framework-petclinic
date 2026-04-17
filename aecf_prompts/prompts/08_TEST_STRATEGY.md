# AECF — TEST STRATEGY

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 08_TEST_STRATEGY |

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
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/TEST_STRATEGY_CHECKLIST.md

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
1. Un PLAN DE IMPLEMENTACION con VERDICT GO.
2. Code implementado (si ya existe).

Esta fase se ejecuta DESPUES de PLAN (o DESPUES de IMPLEMENT si se agrega testing a code ya hecho).

---

## OBJECTIVE

Definir una estrategia de testing completa, clara y ejecutable que garantice:
- Cobertura funcional
- Casos limite (edge cases)
- Manejo de errores
- Integration entre componentes
- No-regresion

---

## ROL

Act as Senior QA Engineer y Test Architect.

Tu tarea es:
- Analizar el PLAN y el code (si existe).
- Identificar que debe testearse.
- Definir estrategia de testing (unitario, integracion, e2e).
- Especificar casos de prueba criticos.
- Establecer criterios de cobertura minima.

---

## REGLAS ESTRICTAS

- NO implementes tests (eso es fase 09_TEST_IMPLEMENTATION).
- NO generes code de tests.
- NO ejecutes tests.
- NO modifiques el code funcional.
- Limitate a DISENAR la estrategia.

---

## CLASIFICACION DE TESTS

Debes especificar para cada tipo:

### 1. Tests Unitarios
- Funciones/metodos individuales
- Sin dependencias externas (mocks/stubs)
- Cobertura objective: 80%+

### 2. Tests de Integration
- Interaccion entre componentes
- Base de data, APIs externas
- Con dependencias reales o contenedores

### 3. Tests End-to-End (E2E)
- Flows completos de usuario
- Ambiente similar a production
- Casos criticos de negocio

### 4. Tests de Contrato / API
- Validation de contratos de API
- Request/Response schemas
- Status codes esperados

---

## CASOS DE PRUEBA OBLIGATORIOS

Para cada funcionalidad debes especificar:

1. **Happy Path** (flow exitoso estandar)
2. **Edge Cases** (valores limite, casos extremos)
3. **Error Handling** (errores esperados y su manejo)
4. **Security Cases** (inyeccion, permisos, enumeracion)
5. **Performance Cases** (si aplica: timeouts, volumen)

---

## FORMATO DE SALIDA OBLIGATORIO

## 1. Summary Ejecutivo
- Alcance del testing
- Tipos de tests a implementar
- Cobertura objective

## 2. Estrategia de Testing

### 2.1 Tests Unitarios
- Componentes a testear
- Dependencias a mockear
- Cobertura minima: 80%

### 2.2 Tests de Integration
- Componentes integrados a testear
- Dependencias externas (DB, APIs, servicios)
- Fixtures y data de prueba necesarios

### 2.3 Tests End-to-End
- Flows completos a validar
- Requisitos de ambiente (containers, servicios externos)

## 3. Casos de Prueba Detallados

Para cada funcionalidad principal:

### Funcionalidad: [Nombre]

#### Test Case 1: [Nombre descriptivo]
- **Tipo**: Unitario / Integration / E2E
- **Description**: Que valida
- **Precondiciones**: Estado inicial requerido
- **Pasos**: Acciones a ejecutar
- **Resultado esperado**: Salida/comportamiento esperado
- **Criterio de exito**: Como saber que paso

#### Test Case 2: [Edge case - Nombre]
[misma estructura]

## 4. Data de Prueba (Fixtures)
- Data de entrada necesarios
- Estados de base de data
- Mocks y stubs requeridos

## 5. Dependencias de Testing
- Frameworks necesarios (pytest, unittest, etc.)
- Librerias adicionales (faker, factory_boy, etc.)
- Herramientas (coverage, pytest-cov)

## 5.1 Static Analysis Strategy
- Linters y checks estaticos aplicables segun stack, dominio y surface afectado
- Scope de ejecucion por herramienta (`changed files`, `target module`, `workspace`, etc.)
- Criterio de bloqueo por herramienta (`blocking`, `advisory`, `not_applicable`)
- Evidencia requerida en auditoria: tabla `## Static Analysis Evidence` con comando, scope, resultado y hallazgos

## 6. Criterios de Aprobacion
- Cobertura minima por tipo de test
- Todos los tests pasan
- No existen flakey tests
- Tiempo maximo de ejecucion
- Todos los checks estaticos `blocking` aplicables pasan o quedan justificados como `NOT_APPLICABLE`

## 7. Tests Excluidos (si aplica)
- Que NO se testea y por que
- Justificacion explicita

---

## CRITERIOS MINIMOS OBLIGATORIOS

1. **Logging y observabilidad**
   - Tests que validen que se llama al logger correctamente
   - Validar niveles de log

2. **Management de recursos**
   - Tests que validen cierre de conexiones
   - Tests de resource leaks

3. **Control de acceso**
   - Tests de permisos
   - Tests de autorizacion
   - Tests de roles

4. **Enumeracion**
   - Tests que validen respuestas neutras
   - Tests de information disclosure

5. **Exposicion de data**
   - Tests que validen campos devueltos
   - Tests de serializacion

6. **Paginacion**
   - Tests de limites
   - Tests de parametros de paginacion

---

## PROHIBICIONES

- NO implementar code de tests (es fase siguiente).
- NO modificar code funcional para hacerlo testeable (eso debe ir a FIX-CODE o nuevo PLAN).
- NO ejecutar tests.
- NO proponer cambios de arquitectura.

---

## SALIDA ESPERADA

Al finalizar, indica claramente:

**TEST STRATEGY COMPLETADA — Lista para IMPLEMENT o TEST_IMPLEMENTATION**

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
documentation/{{TOPIC}}/AECF_<NN>_TEST_STRATEGY.md

Where:
- {{TOPIC}} = the topic from previous phase
- <NN> = next sequential number

---

## AECF_COMPLIANCE_REPORT

Antes de finalizar, incluir:

## AECF_COMPLIANCE_REPORT

- aecf_prompts/prompts/00_PLAN.md → APLICADO / NO APLICADO
- aecf_prompts/prompts/02_AUDIT_PLAN.md → APLICADO (GO) / NO APLICADO
- aecf_prompts/prompts/08_TEST_STRATEGY.md → APLICADO

Flow AECF: COMPLETO / PARCIAL  
Decisiones fuera de plan: NO  
Estrategia basada en: PLAN aprobado

TEST_STRATEGY LISTA PARA TEST_IMPLEMENTATION

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
