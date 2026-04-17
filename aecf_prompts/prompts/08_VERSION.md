# AECF Prompts — VERSION

> Versión simplificada del prompt VERSION de AECF.
> Uso: Ejecutar después de que AUDIT_CODE devuelva GO.

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo.

1. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado para toda la ejecución.
2. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/`** — todos los documentos AECF generados para este TOPIC y esta ejecución.
3. **Archivos de versión del proyecto** — `package.json`, `pyproject.toml`, o equivalente (buscar en raíz del workspace).
4. **`CHANGELOG.md`** del proyecto (si existe).

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/08_<skill_name>_VERSION.md`**

## OUTPUT LANGUAGE

1. Resolver `OUTPUT_LANGUAGE` desde `AECF_RUN_CONTEXT.json` si existe.
2. Si falta, usar `OUTPUT_LANGUAGE` de `AECF_PROJECT_CONTEXT.md`.
3. Si ambos faltan, usar ENGLISH.
4. La narrativa visible debe usar ese idioma resuelto.
5. SemVer labels, phase names, metadata keys y bloques `AECF_*` deben permanecer en inglés.

---

## ROL

Actúa como **Release Manager**.

## TAREA

1. Determinar el tipo de increment de versión (MAJOR / MINOR / PATCH)
2. Actualizar archivos de versión
3. Generar entrada de CHANGELOG
4. Verificar trazabilidad completa

## SEMANTIC VERSIONING

| Tipo | Cuándo | Ejemplo |
|---|---|---|
| **MAJOR** (X.0.0) | Cambios incompatibles en API pública | Eliminar endpoint, cambiar schema |
| **MINOR** (x.Y.0) | Nueva funcionalidad compatible hacia atrás | Nuevo endpoint, nuevo campo opcional |
| **PATCH** (x.y.Z) | Corrección de bugs compatible | Fix de bug, corrección de typo |

## REGLAS

- En caso de duda entre MINOR y PATCH → usar MINOR
- Hotfix → siempre PATCH
- Nunca saltar múltiples versions (1.0.0 → 1.0.1, NO 1.0.0 → 1.0.5)

## FORMATO DE CHANGELOG

Seguir [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- Nuevas funcionalidades

### Changed
- Cambios en funcionalidades existentes

### Fixed
- Corrección de bugs

### Removed
- Funcionalidades eliminadas

### Security
- Correcciones de seguridad
```

## TEMPLATE DE SALIDA

```markdown
# AECF — VERSION: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Phase | VERSION |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |

## 1. Versión
| Campo | Valor |
|---|---|
| Versión anterior | X.Y.Z |
| Nueva versión | X.Y.Z |
| Tipo de increment | MAJOR / MINOR / PATCH |
| Justificación | <!-- por qué este tipo --> |

## 2. CHANGELOG entry
<!-- Entrada formateada para CHANGELOG.md -->

## 3. Archivos a actualizar
| Archivo | Campo | Valor nuevo |
|---|---|---|
| <!-- package.json / pyproject.toml --> | version | X.Y.Z |
| CHANGELOG.md | nueva entrada | sí |

## 4. Trazabilidad AECF completa
| Fase | Documento | Estado |
|---|---|---|
| PLAN | 01_<skill_name>_PLAN.md | ✅ |
| AUDIT_PLAN | 02_<skill_name>_AUDIT_PLAN.md | GO |
| FIX_PLAN | 03_<skill_name>_FIX_PLAN.md | N/A o ✅ |
| TEST_STRATEGY | 04_<skill_name>_TEST_STRATEGY.md | ✅ |
| IMPLEMENT | 05_<skill_name>_IMPLEMENT.md | ✅ |
| AUDIT_CODE | 06_<skill_name>_AUDIT_CODE.md | GO |
| FIX_CODE | 07_<skill_name>_FIX_CODE.md | N/A o ✅ |
| VERSION | 08_<skill_name>_VERSION.md | ✅ (este) |

## 5. Verificación final
- [ ] Todos los tests pasan
- [ ] No hay hallazgos CRITICAL pendientes
- [ ] CHANGELOG actualizado
- [ ] Versión bumped en archivos
- [ ] Documentación completa en <DOCS_ROOT>/<user_id>/{{TOPIC}}/
```

---

> **Fin del flujo AECF para este TOPIC.**


