# AECF — HOTFIX (Emergency Fix)

> **@METADATA** — Apply standard AECF metadata header from `templates/TEMPLATE_HEADERS.md`
> | Field | Value |
> |-------|-------|
> | Document Type | AECF Prompt |
> | Phase | 00_HOTFIX |

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

📌 TOPIC: Maintain {{TOPIC}} from previous phase OR infer from incident. All outputs in: documentation/{{TOPIC}}/

────────────────────────
📄 TEMPLATE ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load and strictly follow:

./aecf/templates/HOTFIX_TEMPLATE.md

Rules:
- The output MUST replicate the exact structure and headings of the template.
- You may only add content inside sections.
- You may NOT modify headings.
- You may NOT remove sections.
- Missing sections invalidate the HOTFIX.
- All phases must be documented inline.

────────────────────────
CHECKLIST ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/checklists/HOTFIX_CHECKLIST.md

Before issuing verdict:
- Validate each item.
- Declare compliance in AECF_COMPLIANCE_REPORT.
- If any item is false → automatic NO-GO.

Failure to enforce checklist invalidates the phase.

────────────────────────
SCORING ENFORCEMENT (MANDATORY)
────────────────────────

You MUST load:

./aecf/scoring/HOTFIX_SCORING_RULES.md

Rules:
- Apply simplified HOTFIX scoring model (5 categories, binary validation).
- Calculate score BEFORE issuing verdict.
- Include AECF_SCORE_REPORT in output.
- Threshold: Score >= 70 → GO / Score < 70 → NO-GO.
- Any CRITICAL security finding → Automatic NO-GO.

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
documentation/{{TOPIC}}/AECF_<NN>_HOTFIX.md

Where:
- {{TOPIC}} = incident topic (e.g., "prod_outage", "sql_injection_fix")
- <NN> = sequential number

This prompt is subject to audit.
Failure to follow the flow invalidates the response.

---

## CONTEXTO

Este prompt se usa EXCLUSIVAMENTE para:
- Critical production incidents
- Vulnerabilidades de seguridad de severidad CRITICA o ALTA
- Bugs que impactan funcionalidad core
- Data corruption activa

**NO usar para**:
- Features nuevas
- Refactors
- Mejoras de performance no criticas
- Bugs menores

---

## OBJECTIVE

Implementar una solucion minima viable que:
1. Resolve the critical problem immediately
2. Mantenga trazabilidad del flow AECF
3. Permita deployment rapido pero seguro

---

## ROL

Act as Senior Incident Response Engineer.

Tu tarea es:
- Diagnosticar rapidamente (si no hay RCA previo)
- Proponer fix minimo y seguro
- Implementar con maxima precaucion
- Documentar para analisis post-mortem
- Planificar solucion definitiva posterior

---

## FLOW HOTFIX (Simplificado pero Trazable)

El flow HOTFIX es una version ACELERADA del flow normal:

```
INCIDENT → HOTFIX_PLAN → HOTFIX_AUDIT → HOTFIX_IMPLEMENT → HOTFIX_VERIFY → DEPLOY
```

**Diferencias con flow normal**:
- Plan simplificado (no exhaustivo)
- Audit enfocada (solo en el fix)
- Tests minimos obligatorios
- Documentacion concisa pero completa
- Post-mortem obligatorio posterior

---

## CRITERIOS PARA USAR HOTFIX

### ✅ Usar HOTFIX cuando:
- Production completamente caida
- Perdida de data activa
- Vulnerabilidad CRITICA siendo explotada
- Critical SLA compromised
- Incident Severity 1 (P1)

### ❌ NO usar HOTFIX cuando:
- Hay tiempo para flow normal (> 4 horas)
- No afecta usuarios activamente
- Es un bug conocido no urgente
- Requiere cambios arquitectonicos

---

## FASE 1: HOTFIX_PLAN (Maximo 30 min)

### 1.1 Description del Incidente

**Severidad**: P1 / P2 / P3
**Impacto**: [description breve]
**Usuarios afectados**: [numero o porcentaje]
**Tiempo de inactividad**: [desde cuando]

### 1.2 Root Cause (Diagnostico Rapido)

Si ya existe RCA de fase DEBUG:
- Referencia: `AECF_XX_RCA.md`

Si NO existe RCA:
- Causa inmediata identificada: [description]
- Code/configuration afectado: [ubicacion]
- Como se reproduce: [pasos minimos]

### 1.3 Solucion Propuesta (Minima Viable)

**Tipo de fix**: Code / Config / Infrastructure

**Cambios propuestos**:
- File(s) a modificar: [lista]
- Lineas aproximadas: [rango]
- Logica del fix: [explicacion en 2-3 lineas]

**Alternativas consideradas y descartadas**:
1. [alternativa 1] - Razon de descarte: [...]
2. [alternativa 2] - Razon de descarte: [...]

### 1.4 Impacto del Fix

**Funcionalidades afectadas**:
- [lista de funcionalidades que tocara el fix]

**Risks del fix**:
- [lista de posibles efectos secundarios]

**Rollback plan**:
- [como revertir si el fix falla]

### 1.5 Testing Minimo Obligatorio

**Tests que DEBEN pasar antes de deploy**:
1. [critical test 1]
2. [critical test 2]
3. [test de regresion minimo]

No se requiere suite completa, solo critical tests.

---

## FASE 2: HOTFIX_AUDIT (Maximo 15 min)

Audit rapida enfocada en:

### 2.1 Correccion Funcional
- ✅ Fix resuelve el problema
- ✅ Fix does not introduce new critical bugs

### 2.2 Seguridad (CRITICAL)
- ✅ No introduce vulnerabilidades
- ✅ No expone data sensibles
- ✅ No bypasea autenticacion/autorizacion

### 2.3 Efectos Secundarios
- ✅ No rompe funcionalidad critica existente
- ✅ Rollback es posible

### 2.4 Code
- ✅ Cambios minimos y focalizados
- ✅ Sin refactors innecesarios
- ✅ Comentado adecuadamente

### 2.5 HOTFIX SCORING (Simplified)

| Categoria | Peso | Items | Score (0/1/2) |
|-----------|------|-------|---------------|
| Root Cause Validated | 3 | 2 |  |
| Fix is Minimal | 2 | 1 |  |
| Security Controls | 3 | 3 |  |
| Rollback Plan Exists | 3 | 2 |  |
| Production Readiness | 2 | 3 |  |

**Score Calculation**:
- Raw Score = Σ (item_value × category_weight)
- Max Possible = (2×3) + (1×2) + (3×3) + (2×3) + (3×2) = 29
- Normalized Score = (Raw Score / 29) × 100

**Thresholds**:
- Score >= 70 → GO
- Score < 70 → NO-GO
- Any CRITICAL security finding → Automatic NO-GO

**HOTFIX Score**: [X/100]
**Maturity**: [PRODUCTION READY / CONDITIONAL / FAIL]

**Verdict**: GO / NO-GO

Si NO-GO:
- Razon: [...]
- Volver a HOTFIX_PLAN

---

## FASE 3: HOTFIX_IMPLEMENT

Implementar el fix con:

### 3.1 Cambios de Code

```python
# HOTFIX: [ID-INCIDENT] [Fecha] - [Description breve]
# ROOT CAUSE: [causa identificada]
# SOLUTION: [que hace este fix]
# ROLLBACK: [como revertir si falla]

[code del fix]
```

Todo código generado o modificado en HOTFIX_IMPLEMENT debe seguir `./aecf/code/CODE_FUNCTION_METADATA_STANDARD.md`.

Reglas mínimas:
- Cada función, método, clase o módulo tocado por AECF debe llevar un `AECF_META` completo en docstring o comentario equivalente.
- El bloque debe incluir `skill`, `topic`, `run_time`, `generated_at`, `generated_by`, `last_modified_skill`, `last_modified_at`, `last_modified_by` y `touch_count`.
- En creación: `touch_count=1`. En modificación posterior: preservar `generated_*`, actualizar `last_modified_*`, refrescar `run_time` e incrementar `touch_count` exactamente en `1`.
- Los comentarios/docstrings legibles por humanos deben ser suficientes para mantenimiento futuro y usar el idioma resuelto en `OUTPUT_LANGUAGE` / `aecf.documentationOutputLanguage`.
- Las claves máquina de `AECF_META` permanecen en inglés.

### 3.2 Critical Tests

Implementar SOLO tests minimos especificados en HOTFIX_PLAN.

Todo test creado en esta fase debe incluir docstring de trazabilidad con, como minimo:
- `Generated by AECF framework`
- `TOPIC: {{TOPIC}}`
- el bloque completo `AECF_META` como última línea del docstring/comentario

Formato minimo recomendado:
`"""Generated by AECF framework. TOPIC: {{TOPIC}}."""`

### 3.3 Documentacion Inline

Agregar comentarios explicando:
- Por que este code es necesario
- Que problema especifico resuelve
- Referencia al issue/ticket
- Mantener los comentarios en el idioma resuelto de salida del run

---

## FASE 4: HOTFIX_VERIFY

### 4.1 Tests Ejecutados

```
✅ test_critical_functionality_works
✅ test_hotfix_resolves_issue
✅ test_no_regression_on_core_feature
```

### 4.2 Verificacion Manual

- [ ] Reproducir el bug original → Esta resuelto? YES / NO
- [ ] Verificar funcionalidad core → Funciona? YES / NO
- [ ] Verificar rollback plan → Es viable? YES / NO

### 4.3 Smoke Test en Staging (si existe)

- [ ] Deploy en staging exitoso
- [ ] Funcionalidad basica verificada
- [ ] Logs without critical errors

---

## FASE 5: DEPLOY

### 5.1 Checklist Pre-Deploy

- [ ] HOTFIX_AUDIT with GO verdict
- [ ] Tests criticos pasan
- [ ] Smoke test OK (si aplica)
- [ ] Rollback plan documentado
- [ ] Equipo de guardia notificado

### 5.2 Deploy Execution

- [ ] Crear tag: `hotfix-YYYYMMDD-<description>`
- [ ] Deploy a production
- [ ] Monitoreo activo durante 30 min

### 5.3 Post-Deploy Verification

- [ ] Incidente resuelto (verificado por usuarios)
- [ ] Logs sin errores nuevos
- [ ] Metricas estables
- [ ] Performance sin degradacion

---

## POST-MORTEM OBLIGATORIO

Despues de estabilizar production, DEBE ejecutarse:

### Analisis Completo (siguiente dia habil):
1. RCA completo (si no existe): usar `00_DEBUG.md`
2. Evaluar si el hotfix es solucion definitiva o temporal
3. Si es temporal: crear PLAN para solucion definitiva

### Documento de Post-Mortem:

#### 1. Timeline del Incidente
- [HH:MM] Incidente detectado
- [HH:MM] Equipo notificado
- [HH:MM] Root cause identificado
- [HH:MM] Hotfix implementado
- [HH:MM] Deploy a production
- [HH:MM] Incidente resuelto

#### 2. Root Cause Analysis
- [RCA detallado o referencia a AECF_XX_RCA.md]

#### 3. Evaluacion del Hotfix
- Es solucion definitiva? YES / NO
- Si NO: [que falta para solucion definitiva]

#### 4. Lecciones Aprendidas
- Que funciono bien
- Que mejorar

#### 5. Action Items
- [ ] Solucion definitiva (si hotfix es temporal)
- [ ] Mejoras de monitoreo
- [ ] Documentacion actualizada
- [ ] Tests adicionales

---

## REGLAS ESTRICTAS DEL HOTFIX

### ✅ PERMITIDO:
- Cambios minimos y focalizados
- Comentarios inline explicativos
- Tests criticos minimos
- Documentacion concisa

### ❌ PROHIBIDO:
- Refactors "de paso"
- Optimizaciones no relacionadas
- Features nuevas "aprovechando"
- Cambios arquitectonicos
- Reformateo de code no afectado

---

## CLASIFICACION DE SEVERIDAD

### P1 (CRITICAL) - Hotfix inmediato
- Production completamente caida
- Perdida de data
- Vulnerabilidad siendo explotada
- **Tiempo de respuesta**: < 1 hora

### P2 (HIGH) - Hotfix urgente
- Funcionalidad core degradada
- Afecta a muchos usuarios
- Workaround complicado
- **Tiempo de respuesta**: < 4 horas

### P3 (MEDIO) - NO usar hotfix
- Bug severo pero con workaround
- Afecta funcionalidad secundaria
- **Usar flow normal**: PLAN → AUDIT → IMPLEMENT

---

## FORMATO DE SALIDA OBLIGATORIO

## HOTFIX SUMMARY

**Incident ID**: [ID]
**Severity**: P1 / P2
**Status**: RESOLVED / DEPLOYED / MONITORING
**Total Time**: [desde deteccion hasta deploy]

## HOTFIX_PLAN
[contenido de fase 1]

## HOTFIX_AUDIT
[contenido de fase 2]

## HOTFIX_IMPLEMENTATION
[contenido de fase 3]

## HOTFIX_VERIFICATION
[contenido de fase 4]

## DEPLOYMENT
[contenido de fase 5]

## POST-MORTEM
[contenido obligatorio]

---

## SALIDA ESPERADA

Al finalizar, indica claramente:

**HOTFIX DEPLOYED — Monitoreo activo, Post-mortem pendiente**

───────────────────────────────
📁 OUTPUT GENERATION (MANDATORY)
───────────────────────────────

Generate document:
documentation/{{TOPIC}}/AECF_<NN>_HOTFIX.md

Where:
- {{TOPIC}} = incident topic (ej: "prod_outage", "sql_injection_fix")
- <NN> = sequential number

---

## AECF_COMPLIANCE_REPORT

Antes de finalizar, incluir:

## AECF_COMPLIANCE_REPORT

- aecf_prompts/prompts/00_HOTFIX.md → APLICADO

Flow AECF: HOTFIX (EMERGENCY FLOW)
Severidad incidente: P1 / P2
Tiempo total: [HH:MM desde deteccion hasta deploy]
Solucion: DEFINITIVA / TEMPORAL
Post-mortem: PENDIENTE / COMPLETADO

## AECF_SCORE_REPORT (HOTFIX Simplified)

- Raw Score: [X/29]
- Normalized Score: [Y/100]
- Maturity Level: [PRODUCTION READY / CONDITIONAL / FAIL]
- Automatic Verdict: [GO / NO-GO]
- Critical Findings Present: YES / NO

HOTFIX COMPLETO — Production estabilizada

## GOVERNANCE VALIDATION BLOCK

- Data lineage impact
- Model impact (YES/NO)
- Risk impact
- Compliance check
