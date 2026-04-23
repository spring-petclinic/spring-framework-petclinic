# AECF Prompts — FIX CODE

> Versión simplificada del prompt FIX_CODE de AECF.
> Uso: Ejecutar solo si AUDIT_CODE devuelve NO-GO.

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo y ABORTAR.

1. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado para toda la ejecución.
2. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/05_<skill_name>_IMPLEMENT.md`** — implementación actual.
3. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/06_<skill_name>_AUDIT_CODE.md`** — auditoría con hallazgos.

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/07_<skill_name>_FIX_CODE.md`**

## OUTPUT LANGUAGE

1. Resolver `OUTPUT_LANGUAGE` desde `AECF_RUN_CONTEXT.json` si existe.
2. Si falta, usar `OUTPUT_LANGUAGE` de `AECF_PROJECT_CONTEXT.md`.
3. Si ambos faltan, usar ENGLISH.
4. La narrativa visible debe usar ese idioma resuelto.
5. Los elementos de control del contrato deben permanecer estables y en inglés cuando aplique.

---

## ROL

Actúa como **Senior Software Engineer** (el mismo rol que IMPLEMENT).

## TAREA

Corregir EXCLUSIVAMENTE los hallazgos señalados en AUDIT_CODE.

## PASO PREVIO: TRIAJE

Antes de corregir, clasificar cada hallazgo:

| Tipo | Significado | Acción |
|---|---|---|
| **CODE_BUG** | El código tiene un defecto | Corregir el código |
| **TEST_WRONG_ASSERTION** | El test tiene una aserción incorrecta | Corregir el test |
| **TEST_WRONG_SETUP** | El setup del test es incorrecto | Corregir el setup |
| **TEST_MISSING** | Falta un test requerido | Añadir el test |
| **AMBIGUOUS** | No está claro si es bug de código o test | Investigar primero |

## REGLAS ESTRICTAS

- **PROHIBIDO** expandir el alcance
- **PROHIBIDO** refactorizar código no relacionado con los hallazgos
- **PROHIBIDO** añadir funcionalidades no solicitadas
- Solo corregir lo que señaló el auditor
- Re-ejecutar tests después de cada corrección
- Actualizar AECF_META en funciones modificadas
- Preservar `generated_at` y `generated_by` originales; actualizar solo `last_modified_*`
	con el `Executed By ID` efectivo (o `N/A` si no existe identidad disponible)
- Actualizar también `run_time` con el timestamp UTC del run activo e incrementar `touch_count`
	exactamente en `1` en cada toque posterior de AECF
- No usar valores genéricos como `aecf`, `copilot`, `assistant`, el nombre del
	skill o el modelo en campos `*_by`
- Los comentarios y docstrings legibles por humanos deben ser suficientes para mantenimiento futuro
	y usar el idioma resuelto en `OUTPUT_LANGUAGE` / `aecf.documentationOutputLanguage`

## TEMPLATE DE SALIDA

```markdown
# AECF — FIX CODE: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Phase | FIX_CODE |
| Topic | {{TOPIC}} |
| Fix Iteration | {{1, 2, 3...}} |

## 1. Triaje de hallazgos
| # | Hallazgo | Tipo | Acción |
|---|---|---|---|
| 1 | <!-- del audit --> | CODE_BUG / TEST_WRONG_* / TEST_MISSING | <!-- qué hacer --> |

## 2. Correcciones aplicadas

### Corrección #1: {{título}}
- **Hallazgo:** <!-- del audit -->
- **Tipo:** CODE_BUG / TEST_WRONG_*
- **Archivo modificado:** <!-- ruta -->
- **Cambio:**
```python
# código corregido
```

## 3. Tests Executed (post-fix)
```
$ pytest -q tests/
X passed, Y failed
```

## 4. Verificación de no-regresión
- [ ] No se expandió el alcance
- [ ] Tests previos siguen pasando
- [ ] No se introdujeron nuevos defectos
- [ ] AECF_META actualizado en funciones modificadas
```

---

> **Siguiente fase:** AUDIT_CODE (re-evaluación)


