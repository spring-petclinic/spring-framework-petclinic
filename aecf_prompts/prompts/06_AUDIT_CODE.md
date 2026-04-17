# AECF Prompts — AUDIT CODE

LAST_REVIEW: 2026-04-17

> Versión simplificada del prompt AUDIT_CODE de AECF.
> Uso: Ejecutar después de IMPLEMENT.

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo y ABORTAR.

1. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado para toda la ejecución.
2. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md`** — plan aprobado.
3. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/04_<skill_name>_TEST_STRATEGY.md`** — estrategia de tests.
4. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/05_<skill_name>_IMPLEMENT.md`** — implementación a auditar.
5. **`aecf_prompts/checklists/AUDIT_CODE_CHECKLIST.md`** — checklist obligatorio.
6. **`aecf_prompts/scoring/SCORING_MODEL.md`** — modelo de scoring.

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/06_<skill_name>_AUDIT_CODE.md`**

## OUTPUT LANGUAGE

1. Resolver `OUTPUT_LANGUAGE` desde `AECF_RUN_CONTEXT.json` si existe.
2. Si falta, usar `OUTPUT_LANGUAGE` de `AECF_PROJECT_CONTEXT.md`.
3. Si ambos faltan, usar ENGLISH.
4. La narrativa visible debe usar ese idioma resuelto.
5. Fases, verdicts, metadata keys, scoring labels y bloques `AECF_*` deben permanecer en inglés.

---

## ROL

Actúa como **Principal Engineer / Code Auditor Independiente**.

> ⚠️ El auditor DEBE ser diferente al desarrollador que implementó, o asumir rol independiente sin sesgo.

## TAREA

Auditar el código implementado contra:

1. Adherencia al PLAN aprobado
2. Calidad de código y estándares
3. Seguridad básica y decisión de escalado a `aecf_security_review`
4. Cobertura y calidad de tests
5. Logging y observabilidad
6. Gestión de recursos
7. Manejo de errores

## POLÍTICA DE ESCALADO A `security_review`

`AUDIT_CODE` sigue siendo el gate general de calidad y release. No sustituye la revisión OWASP completa ni debe intentar ejecutarla implícitamente dentro de esta fase.

`AUDIT_CODE` DEBE exigir un `aecf_security_review` explícito antes de pasar a `VERSION` cuando se cumpla cualquiera de estas condiciones:

1. `skill_name` es `new_feature`, `new_test_set` o `hotfix`.
2. El cambio toca superficies sensibles como autenticación, autorización, secretos, criptografía, validación de inputs externos, uploads, consultas dinámicas, deserialización, llamadas salientes HTTP/webhooks, SSRF, operaciones privilegiadas, endpoints públicos, integraciones externas o datos personales/sensibles.

Evidencia aceptable:

- Existe `<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_01_SECURITY_AUDIT.md` para el mismo `{{TOPIC}}`.
- O existe un artefacto posterior `AECF_<NN>_SECURITY_AUDIT.md` para el mismo `{{TOPIC}}` y alcance.

Si el `security_review` es obligatorio y no existe evidencia válida, el veredicto de `AUDIT_CODE` DEBE ser `NO-GO` aunque el resto de criterios sean aceptables. En ese caso, la siguiente acción obligatoria es ejecutar `aecf_security_review` y re-evaluar el gate.

Si el `security_review` no es obligatorio, `AUDIT_CODE` mantiene la revisión básica de seguridad y puede seguir con su veredicto normal.

## CRITERIOS DE EVALUACIÓN

| # | Criterio | Peso |
|---|---|---|
| 1 | Código implementa lo definido en el PLAN | Alto |
| 2 | No hay expansión de alcance no autorizada | Alto |
| 3 | Tests cubren las 5 categorías obligatorias | Alto |
| 4 | **Evidencia de tests ejecutados** (sección "Tests Executed") | **CRÍTICO** |
| 5 | Naming conventions correctas | Medio |
| 6 | Logging estructurado (no print) | Medio |
| 7 | Recursos cerrados correctamente | Alto |
| 8 | Sin datos sensibles expuestos | Alto |
| 9 | Validación de entrada presente | Alto |
| 10 | Error handling completo (sin fallos silenciosos) | Alto |
| 11 | Type hints / tipos incluidos | Medio |
| 12 | Documentación de código (docstrings) | Medio |
| 13 | Complejidad controlada | Medio |
| 14 | Sin código duplicado innecesario | Bajo |
| 15 | **Anti-patterns de scope** ausentes (`SCOPE_CREEP`, `DEAD_FEATURE`) | **CRÍTICO** |
| 16 | **Anti-patterns de seguridad** ausentes (`HARDCODED_SECRET`, `SQL_INJECTION`, `COMMAND_INJECTION`, `INSECURE_DESERIALIZATION`, `PATH_TRAVERSAL`) | **CRÍTICO** |
| 17 | Anti-patterns de mantenibilidad controlados (`GOD_FUNCTION`, `MAGIC_NUMBER`, `DEEP_NESTING`, `SILENT_EXCEPTION`, `GLOBAL_MUTABLE_STATE`, `PRINT_DEBUGGING`) | Medio |

## REGLA CRÍTICA

> **Si NO existe la sección "Tests Executed" con evidencia REAL de ejecución → veredicto es automáticamente NO-GO**, independientemente de la calidad del código.
> **Si la política de escalado exige `aecf_security_review` y no hay evidencia del artefacto `SECURITY_AUDIT` → veredicto es automáticamente NO-GO**, independientemente del score restante.
> **Si se detecta cualquier anti-pattern de seguridad o scope (`HARDCODED_SECRET`, `SQL_INJECTION`, `COMMAND_INJECTION`, `INSECURE_DESERIALIZATION`, `PATH_TRAVERSAL`, `SCOPE_CREEP`, `DEAD_FEATURE`) → veredicto es automáticamente NO-GO**, clasificar como CRITICAL.

## CLASIFICACIÓN DE HALLAZGOS

| Severidad | Significado | Impacto en veredicto |
|---|---|---|
| **CRITICAL** | Bloquea release, riesgo de seguridad o datos | → NO-GO automático |
| **WARNING** | Afecta calidad pero no bloquea | → Reduce score |
| **INFO** | Observación, mejora futura | → No afecta veredicto |

## SCORING

Aplicar el checklist **ya cargado** (`AUDIT_CODE_CHECKLIST.md`) y calcular según el modelo **ya cargado** (`SCORING_MODEL.md`).

La tabla `AECF_SCORE_REPORT` DEBE reflejar exactamente las categorías puntuadas en `AUDIT_CODE_CHECKLIST.md`.

- Si `Dependency Outage Resilience` no aplica porque el cambio no toca dependencias externas, marcar `N/A` y excluir esa categoría del máximo ponderado final.
- No sustituir `Compliance with Previous Phase` por variantes abreviadas o semánticamente distintas.
- La fila `Anti-patterns` es obligatoria y debe incluir el total agregado de los 13 checks definidos en el checklist.

## TEMPLATE DE SALIDA

```markdown
# AECF — AUDIT CODE: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Phase | AUDIT_CODE |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |
| Auditor | {{auditor}} |
| Verdict | GO / NO-GO |

## 1. Hallazgos

### CRITICAL
| # | Hallazgo | Archivo | Línea | Impacto |
|---|---|---|---|---|
| <!-- si ninguno: "Ningún hallazgo crítico" --> | | | | |

### WARNING
| # | Hallazgo | Archivo | Impacto |
|---|---|---|---|

### INFO
| # | Hallazgo | Recomendación |
|---|---|---|

## 2. Evaluación de adherencia al PLAN
<!-- ¿El código implementa lo planificado? ¿Hay desviaciones? -->

## 3. Evaluación de testing
- Fuente de evidencia: `05_<skill_name>_IMPLEMENT.md` -> sección `## 6. Tests Executed`
- Evidencia de tests ejecutados: SÍ / NO
- Comandos observados: <!-- listar -->
- Resultados observados: <!-- resumir salida -->
- Categorías cubiertas: __/5
- Tests pasando: __/__


## 4. Evaluación de seguridad
<!-- Revisar seguridad básica y decidir si la política obliga a ejecutar aecf_security_review -->

## 5. Evaluación de calidad
<!-- Naming, logging, recursos, errores, tipos, docs -->

## AECF_SCORE_REPORT
| Categoría | Peso | Raw Score | Max Raw | Weighted | Max Weighted |
|---|---|---|---|---|---|
| Scope Validation | 2 | __ | 6 | __ | 12 |
| Security Controls | 3 | __ | 8 | __ | 24 |
| Resource Management | 2 | __ | 4 | __ | 8 |
| Dep. Outage Resilience | 3 | __ / N/A | 10 | __ / N/A | 30 / N/A |
| Logging & Observability | 2 | __ | 6 | __ | 12 |
| Compliance with Previous Phase | 3 | __ | 6 | __ | 18 |
| Production Readiness | 2 | __ | 8 | __ | 16 |
| Decision Integrity | 3 | __ | 4 | __ | 12 |
| Code Audit Integrity | 2 | __ | 6 | __ | 12 |
| Testing Evidence | 3 | __ | 6 | __ | 18 |
| Anti-patterns | 3 | __ | 26 | __ | 78 |
| **Total** | | **__** | **__** | **__** | **__** |

- Raw Score: <!-- weighted score obtained / weighted max -->
- Normalized Score: <!-- 0-100 -->
- Maturity Level: <!-- ENTERPRISE READY / PRODUCTION READY / CONDITIONAL / HIGH RISK / FAIL -->
- Critical Findings: YES / NO
- Test Evidence Present: YES / NO

## 6. Veredicto Final
**GO** / **NO-GO** — Justificación:
```

---

> **Si GO:** siguiente fase → VERSION
> **Si NO-GO por hallazgos de código:** siguiente fase → FIX_CODE → re-ejecutar AUDIT_CODE
> **Si NO-GO por política de seguridad:** siguiente fase → `aecf_security_review` → re-ejecutar AUDIT_CODE


