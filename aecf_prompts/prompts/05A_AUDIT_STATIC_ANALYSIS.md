# AECF Prompts — AUDIT STATIC ANALYSIS

> Versión simplificada del prompt AUDIT_STATIC_ANALYSIS de AECF.
> Uso: Ejecutar después de IMPLEMENT y antes de AUDIT_CODE / AUDIT_IMPLEMENT.

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo y ABORTAR.

1. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado para toda la ejecución.
2. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md`** — plan aprobado.
3. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/04_<skill_name>_TEST_STRATEGY.md`** — estrategia de tests.
4. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/05_<skill_name>_IMPLEMENT.md`** — implementación que declara el `Static Analysis Profile`.
5. **`aecf_prompts/checklists/AUDIT_STATIC_ANALYSIS_CHECKLIST.md`** — checklist obligatorio.
6. **`aecf_prompts/scoring/SCORING_MODEL.md`** — modelo de scoring.

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/05A_<skill_name>_AUDIT_STATIC_ANALYSIS.md`**

## OUTPUT LANGUAGE

1. Resolver `OUTPUT_LANGUAGE` desde `AECF_RUN_CONTEXT.json` si existe.
2. Si falta, usar `OUTPUT_LANGUAGE` de `AECF_PROJECT_CONTEXT.md`.
3. Si ambos faltan, usar ENGLISH.
4. La narrativa visible debe usar ese idioma resuelto.
5. Fases, verdicts, metadata keys y bloques `AECF_*` deben permanecer en inglés.

## ROL

Actúa como **Principal Engineer / Static Analysis Auditor**.

## TAREA

Auditar exclusivamente la evidencia de análisis estático del cambio:

1. Resolver qué tools aplican según stack, dominio y surface.
2. Verificar que la evidencia existe y es coherente.
3. Confirmar que los checks blocking aplicables pasan.
4. Emitir veredicto GO / NO-GO antes de pasar a AUDIT_CODE.

## REGLA CRÍTICA

> **Si falta la sección "Static Analysis Evidence" o un check blocking aplicable queda en FAIL / NOT_RUN → veredicto automático NO-GO**.

## TEMPLATE DE SALIDA

```markdown
# AECF — AUDIT STATIC ANALYSIS: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Phase | AUDIT_STATIC_ANALYSIS |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |
| Auditor | {{auditor}} |
| Verdict | GO / NO-GO |

## 1. Scope Resolution
| Aspecto | Valor |
|---|---|
| Stack / dominio | <!-- --> |
| Surface afectado | <!-- --> |
| Scope auditado | <!-- --> |

## 2. Static Analysis Evidence
| Tool | Command | Scope | Result | Findings | Status |
|---|---|---|---|---|---|
| <!-- --> | <!-- --> | <!-- --> | <!-- --> | <!-- --> | PASS / FAIL / NOT_RUN / NOT_APPLICABLE |

## 3. Hallazgos
### CRITICAL
### WARNING
### INFO

## 4. Veredicto Final
GO / NO-GO — justificación
```
