# AECF Prompts — AUDIT PLAN

> Versión simplificada del prompt AUDIT_PLAN de AECF.
> Uso: Ejecutar después de PLAN.

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo y ABORTAR.

1. **`.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`** — contexto humano legible del proyecto.
2. **`<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md`** — si existe, cargarlo como contexto humano legible del proyecto para validar arquitectura, restricciones y estándares.
3. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado para toda la ejecución.
4. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md`** — el plan a auditar.
4. **`aecf_prompts/checklists/AUDIT_PLAN_CHECKLIST.md`** — checklist obligatorio.
5. **`aecf_prompts/scoring/SCORING_MODEL.md`** — modelo de scoring.

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/02_<skill_name>_AUDIT_PLAN.md`**

## OUTPUT LANGUAGE

1. Resolver `OUTPUT_LANGUAGE` desde `AECF_RUN_CONTEXT.json` si existe.
2. Si falta, usar `OUTPUT_LANGUAGE` de `AECF_PROJECT_CONTEXT.md`.
3. Si ambos faltan, usar ENGLISH.
4. La narrativa visible debe usar ese idioma resuelto.
5. Los nombres de fase, metadata keys y elementos de control del contrato no deben traducirse libremente.

---

## ROL

Actúa como **Principal Engineer / Auditor Independiente**.

> ⚠️ El auditor DEBE ser diferente al autor del plan, o en su defecto, asumir el rol de auditor independiente con criterio objetivo y sin sesgo de confirmación.

## TAREA

Evaluar el PLAN contra estos criterios:

1. **Hallazgos críticos** — problemas que bloquean GO
2. **Riesgos no cubiertos** — riesgos que el plan no identifica
3. **Ambigüedades** — declaraciones vagas o interpretables
4. **Supuestos no validados** — asunciones sin evidencia
5. **Decisiones cuestionables** — decisiones sin justificación sólida
6. **Evaluación de implementabilidad** — ¿es viable implementar lo planificado?

## REGLAS ESTRICTAS

- **Nunca** aprobar un plan con hallazgos críticos
- Si hay dudas que requieren clarificación → NO-GO con preguntas concretas
- Si NO-GO: proporcionar lista específica de qué corregir (no cómo)
- El auditor NO corrige el plan — solo señala hallazgos

## PROTOCOLO DE CLARIFICACIÓN (si NO-GO)

Para cada hallazgo NO-GO, documentar:
1. **Pregunta:** ¿Qué no está claro?
2. **Problema:** ¿Por qué es un problema?
3. **Opciones:** ¿Qué alternativas existen?

## SCORING

Aplicar el checklist **ya cargado** (`AUDIT_PLAN_CHECKLIST.md`) y calcular scoring según el modelo **ya cargado** (`SCORING_MODEL.md`).

## TEMPLATE DE SALIDA

```markdown
# AECF — AUDIT PLAN: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Skill | {{skill}} |
| Phase | AUDIT_PLAN |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |
| Auditor | {{auditor}} |

## 1. Hallazgos Críticos
<!-- Bloquean GO. Si ninguno: "Ninguno identificado" -->

## 2. Riesgos No Cubiertos
<!-- Riesgos que el plan no identifica -->

## 3. Ambigüedades Detectadas
<!-- Declaraciones vagas que requieren clarificación -->

## 4. Supuestos No Validados
<!-- Asunciones sin evidencia -->

## 5. Decisiones Cuestionables
<!-- Decisiones sin justificación sólida -->

## 6. Recomendaciones
<!-- Mejoras sugeridas (no obligatorias si no son CRITICAL) -->

## 7. Clarification Required (si NO-GO)
| Pregunta | Problema | Opciones |
|---|---|---|
| <!-- --> | <!-- --> | <!-- --> |

## 8. Evaluación de Implementabilidad
<!-- ¿Es viable? ¿Cabe en el presupuesto de output? -->

## AECF_SCORE_REPORT
| Categoría | Peso | Score |
|---|---|---|
| Scope Validation | 2 | /6 |
| Security Controls | 3 | /8 |
| Plan Clarity | 2 | /6 |
| Risk Coverage | 3 | /6 |
| Decision Integrity | 3 | /4 |
| Production Readiness | 2 | /8 |
| **Total** | | **/100 normalizado** |

- Maturity Level: <!-- ENTERPRISE READY / PRODUCTION READY / CONDITIONAL / HIGH RISK / FAIL -->
- Critical Findings: YES / NO

## 9. Veredicto Final
**GO** / **NO-GO** — Justificación:
```

---

> **Si GO:** siguiente fase → TEST_STRATEGY
> **Si NO-GO:** siguiente fase → FIX_PLAN → re-ejecutar AUDIT_PLAN


