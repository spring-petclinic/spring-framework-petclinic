# AECF Prompts — IMPLEMENT

> Versión simplificada del prompt IMPLEMENT de AECF.
> Uso: Ejecutar después de TEST_STRATEGY.

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo y ABORTAR.

1. **`.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`** — contexto humano legible del proyecto.
2. **`<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md`** — si existe, cargarlo como contexto humano legible del proyecto para stack, estándares y restricciones técnicas.
3. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado para toda la ejecución.
4. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md`** — plan aprobado.
5. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/04_<skill_name>_TEST_STRATEGY.md`** — estrategia de tests a implementar.
5. **`aecf_prompts/checklists/IMPLEMENT_CHECKLIST.md`** — checklist de implementación.

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/05_<skill_name>_IMPLEMENT.md`**

## OUTPUT LANGUAGE

1. Resolver `OUTPUT_LANGUAGE` desde `AECF_RUN_CONTEXT.json` si existe.
2. Si falta, usar `OUTPUT_LANGUAGE` de `AECF_PROJECT_CONTEXT.md`.
3. Si ambos faltan, usar ENGLISH.
4. La narrativa visible debe usar ese idioma resuelto.
5. Fases, filenames, metadata keys, taxonomía de tests y bloques `AECF_*` deben permanecer en inglés.

---

## ROL

Actúa como **Senior Software Engineer**.

## TAREA

Implementar el código según el plan aprobado. La implementación debe:

1. Seguir exactamente las decisiones del PLAN aprobado
2. Implementar los tests diseñados en TEST_STRATEGY
3. Producir código que cumpla los estándares del proyecto
4. Incluir documentación de código (docstrings, tipos)
5. Ejecutar tests y reportar resultados

## REGLAS ESTRICTAS

- **PROHIBIDO** rediseñar la solución — seguir el PLAN
- **PROHIBIDO** expandir el alcance más allá del PLAN
- Si hay desviaciones necesarias → documentarlas explícitamente
- La implementación completa debe caber en ~8000 tokens / ~2500 líneas

## ANTI-PATTERNS PROHIBIDOS (TIER3 — obligatorio)

> El código generado NO puede contener ninguno de los siguientes anti-patterns. Los de seguridad y scope invalidan la fase automáticamente; los de mantenibilidad penalizan el score y serán detectados en AUDIT_CODE como WARNING.

### Scope (→ fallo automático de fase si presentes)
| Anti-pattern | Descripción |
|---|---|
| `SCOPE_CREEP` | No implementes features fuera del PLAN, aunque parezcan útiles |
| `DEAD_FEATURE` | No introduzcas TODOs ni código comentado que impliquen funcionalidades no autorizadas |

### Seguridad (→ fallo automático de fase si presentes)
| Anti-pattern | Descripción |
|---|---|
| `HARDCODED_SECRET` | Prohibido incluir credenciales, passwords, API keys o tokens en código fuente |
| `SQL_INJECTION` | Prohibido construir queries concatenando strings con input de usuario — usar parámetros o prepared statements |
| `COMMAND_INJECTION` | Prohibido construir shell commands con input de usuario sin sanitizar |
| `INSECURE_DESERIALIZATION` | Prohibido usar `eval()`, `pickle.loads()` o equivalentes con datos no confiables |
| `PATH_TRAVERSAL` | Prohibido construir rutas de fichero desde input de usuario sin sanitización |

### Mantenibilidad (→ penalizan score en AUDIT_CODE como WARNING)
| Anti-pattern | Descripción |
|---|---|
| `GOD_FUNCTION` | Funciones > 50 líneas o complejidad ciclomática > 10 |
| `MAGIC_NUMBER` | Usar constantes con nombre para literales numéricos o string |
| `DEEP_NESTING` | Máximo 3 niveles de anidamiento en condicionales y bucles |
| `SILENT_EXCEPTION` | Prohibido `except: pass` o bare `except` sin logging |
| `GLOBAL_MUTABLE_STATE` | Prohibido estado mutable global modificado por funciones |
| `PRINT_DEBUGGING` | Prohibido `print()` como mecanismo de logging — usar el logger del proyecto |

## OBLIGACIONES TÉCNICAS

| Obligación | Requisito |
|---|---|
| **Logging** | Usar logging estructurado (no `print()`) |
| **Recursos** | Cerrar recursos (context managers: `with`, `try/finally`) |
| **Acceso** | Validar permisos antes de ejecutar operaciones |
| **Datos sensibles** | No exponer datos sensibles en logs o respuestas |
| **Errores** | Manejar errores explícitamente (no fallos silenciosos) |
| **Tipos** | Incluir type hints / tipos en firmas de funciones |

- Todo código generado o modificado por AECF debe incluir `AECF_META` con `run_time` y `touch_count`.
- En creación: `touch_count=1`. En cada toque posterior de AECF: actualizar `last_modified_*`,
	refrescar `run_time` e incrementar `touch_count` exactamente en `1`.
- Los comentarios y docstrings legibles por humanos deben ser suficientes para mantenimiento futuro
	y usar el idioma resuelto en `OUTPUT_LANGUAGE` / `aecf.documentationOutputLanguage`.
- Las claves del bloque `AECF_META` permanecen en inglés.

## CONTRATO DE OUTPUT

La respuesta debe incluir bloques claros de cambios en archivos:

```
### AECF_FILE_CHANGES
Archivo: path/to/file.py
Acción: CREATE / MODIFY / DELETE
```

## TEMPLATE DE SALIDA

```markdown
# AECF — IMPLEMENT: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Phase | IMPLEMENT |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |
| Plan Reference | 01_<skill_name>_PLAN.md |

## 1. Implementation Summary
<!-- Resumen de lo implementado -->

## 2. Desviaciones del plan
| Desviación | Justificación |
|---|---|
| <!-- ninguna o describir --> | <!-- razón --> |

## 3. Archivos modificados

### AECF_FILE_CHANGES
| Archivo | Acción | Descripción |
|---|---|---|
| <!-- ruta --> | CREATE / MODIFY | <!-- qué hace --> |

## 4. Implementación

### Archivo: {{ruta}}
```python
# AECF_META: skill={{skill}} | topic={{TOPIC}} | run_time={{timestamp_utc}} | generated_at={{timestamp_utc}} | generated_by={{Executed By ID o N/A}} | last_modified_skill={{skill}} | last_modified_at={{timestamp_utc}} | last_modified_by={{Executed By ID o N/A}} | touch_count=1

# ... código ...
```

`generated_by` y `last_modified_by` deben usar el `Executed By ID` efectivo del flujo
(o `N/A` si no existe identidad disponible), nunca valores genéricos como `aecf`,
`copilot`, `assistant`, el nombre del skill o el modelo.

## 5. Tests implementados

### Archivo: {{ruta_tests}}
```python
# ... tests ...
```

## 6. Tests Executed
<!-- ⚠️ OBLIGATORIO: sin esta sección, AUDIT_CODE será NO-GO automático -->
```
$ pytest -q tests/
X passed, Y failed
```

| Métrica | Valor |
|---|---|
| Tests ejecutados | <!-- --> |
| Tests pasando | <!-- --> |
| Cobertura | <!-- % --> |

## 7. Test Taxonomy Evidence
| Categoría | Test | Estado |
|---|---|---|
| Happy path | test_xxx | PASS / FAIL |
| Edge case | test_xxx | PASS / FAIL |
| Error handling | test_xxx | PASS / FAIL |
| Security | test_xxx | PASS / FAIL |
| Non-regression | test_xxx | PASS / FAIL |

## 7A. Static Analysis Profile
| Tool | Category | Surface | Scope | Blocking | Rationale |
|---|---|---|---|---|---|
| <!-- herramienta --> | lint / format_check / type_check / security_static | <!-- surface --> | <!-- scope --> | YES / NO | <!-- por qué aplica --> |

## AECF_COMPLIANCE_REPORT
- [ ] Código sigue el PLAN aprobado
- [ ] No hay expansión de alcance
- [ ] Tests ejecutados y reportados
- [ ] 5 categorías obligatorias cubiertas
- [ ] Logging estructurado (no print)
- [ ] Recursos cerrados correctamente
- [ ] Type hints incluidos
- [ ] Sin datos sensibles expuestos
- [ ] Sin anti-patterns de scope (`SCOPE_CREEP`, `DEAD_FEATURE`)
- [ ] Sin anti-patterns de seguridad (`HARDCODED_SECRET`, `SQL_INJECTION`, `COMMAND_INJECTION`, `INSECURE_DESERIALIZATION`, `PATH_TRAVERSAL`)
- [ ] Anti-patterns de mantenibilidad evitados (`GOD_FUNCTION`, `MAGIC_NUMBER`, `DEEP_NESTING`, `SILENT_EXCEPTION`, `GLOBAL_MUTABLE_STATE`, `PRINT_DEBUGGING`)
```

---

> **Siguiente fase:** AUDIT_CODE


