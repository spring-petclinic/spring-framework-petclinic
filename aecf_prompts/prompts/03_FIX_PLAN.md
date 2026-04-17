# AECF Prompts — FIX PLAN

> Versión simplificada del prompt FIX_PLAN de AECF.
> Uso: Ejecutar solo si AUDIT_PLAN devuelve NO-GO.

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo y ABORTAR.

1. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado para toda la ejecución.
2. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md`** — plan original.
3. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/02_<skill_name>_AUDIT_PLAN.md`** — auditoría con hallazgos.

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/03_<skill_name>_FIX_PLAN.md`**

## OUTPUT LANGUAGE

1. Resolver `OUTPUT_LANGUAGE` desde `AECF_RUN_CONTEXT.json` si existe.
2. Si falta, usar `OUTPUT_LANGUAGE` de `AECF_PROJECT_CONTEXT.md`.
3. Si ambos faltan, usar ENGLISH.
4. La narrativa visible debe usar ese idioma resuelto.
5. Los elementos de control del contrato deben permanecer estables y en inglés cuando aplique.

---

## ROL

Actúa como **Senior Software Architect** (el mismo rol que PLAN).

## TAREA

Corregir EXCLUSIVAMENTE los puntos señalados como hallazgos en AUDIT_PLAN.

## REGLAS ESTRICTAS

- **PROHIBIDO** expandir el alcance del plan original
- **PROHIBIDO** añadir funcionalidades no solicitadas
- **PROHIBIDO** rediseñar la solución completa
- **PROHIBIDO** generar código
- Solo corregir los hallazgos señalados por el auditor
- Mantener la estructura original del plan

## TEMPLATE DE SALIDA

```markdown
# AECF — FIX PLAN: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Phase | FIX_PLAN |
| Topic | {{TOPIC}} |
| Fix Iteration | {{1, 2, 3...}} |

## Hallazgos corregidos

| # | Hallazgo original | Corrección aplicada |
|---|---|---|
| 1 | <!-- del audit --> | <!-- qué se cambió --> |

## Plan corregido
<!-- Incluir el plan completo con las correcciones aplicadas, siguiendo el mismo template que 00_PLAN -->
```

---

> **Siguiente fase:** AUDIT_PLAN (re-evaluación)


