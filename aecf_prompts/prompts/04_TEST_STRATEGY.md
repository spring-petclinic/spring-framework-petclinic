# AECF Prompts — TEST STRATEGY

> Versión simplificada del prompt TEST_STRATEGY de AECF.
> Uso: Ejecutar después de que AUDIT_PLAN devuelva GO.

---

## CARGA OBLIGATORIA DE CONTEXTO

> **INSTRUCCIÓN PARA EL LLM:** DEBES cargar y leer los siguientes archivos ANTES de generar cualquier output. Si alguno no existe, indicarlo y ABORTAR.

1. **`.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`** — contexto humano legible del proyecto.
2. **`<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md`** — si existe, cargarlo como contexto humano legible del proyecto para restricciones, stack y convenciones.
3. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/AECF_RUN_CONTEXT.json`** — si existe, usar `output_language` como idioma congelado para toda la ejecución.
4. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/01_<skill_name>_PLAN.md`** — plan aprobado (verificar que tiene veredicto GO en AUDIT_PLAN).
5. **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/02_<skill_name>_AUDIT_PLAN.md`** — verificar veredicto GO.

## OUTPUT

Guardar la salida en: **`<DOCS_ROOT>/<user_id>/{{TOPIC}}/04_<skill_name>_TEST_STRATEGY.md`**

## OUTPUT LANGUAGE

1. Resolver `OUTPUT_LANGUAGE` desde `AECF_RUN_CONTEXT.json` si existe.
2. Si falta, usar `OUTPUT_LANGUAGE` de `AECF_PROJECT_CONTEXT.md`.
3. Si ambos faltan, usar ENGLISH.
4. La narrativa visible debe usar ese idioma resuelto.
5. Los nombres de fase, metadata keys y taxonomía del contrato deben permanecer estables y en inglés cuando aplique.

---

## ROL

Actúa como **Senior Test Engineer**.

## TAREA

Diseñar la estrategia de testing para la funcionalidad planificada. **NO implementar tests, solo diseñarlos.**

1. Identificar qué componentes necesitan tests
2. Clasificar tests por tipo (unit, integration, E2E, contract)
3. Definir casos de test obligatorios para cada componente
4. Establecer criterios de cobertura

## REGLAS ESTRICTAS

- **PROHIBIDO** escribir código de tests
- **PROHIBIDO** crear fixtures o setup
- Solo diseño: QUÉ probar, no CÓMO implementar
- Cada componente debe tener al menos un test de cada categoría obligatoria

## CATEGORÍAS OBLIGATORIAS DE TEST

Cada funcionalidad DEBE tener al menos un caso de cada tipo:

| Categoría | Descripción |
|---|---|
| **Happy path** | Flujo normal exitoso |
| **Edge case** | Valores extremos, vacíos, nulos |
| **Error handling** | Comportamiento ante errores |
| **Security** | Validación de acceso, inyección, datos sensibles |
| **Non-regression** | Verificar que lo existente sigue funcionando |

## TEMPLATE DE SALIDA

```markdown
# AECF — TEST STRATEGY: {{TOPIC}}

## METADATA
| Campo | Valor |
|---|---|
| Phase | TEST_STRATEGY |
| Topic | {{TOPIC}} |
| Date | {{fecha}} |

## 1. Componentes a testear
| Componente | Tipo de test | Prioridad |
|---|---|---|
| <!-- nombre --> | Unit / Integration / E2E | Alta / Media / Baja |

## 2. Casos de test por componente

### Componente: {{nombre}}

| # | Caso | Categoría | Input | Output esperado |
|---|---|---|---|---|
| 1 | <!-- descripción --> | Happy path | <!-- --> | <!-- --> |
| 2 | <!-- descripción --> | Edge case | <!-- --> | <!-- --> |
| 3 | <!-- descripción --> | Error handling | <!-- --> | <!-- --> |
| 4 | <!-- descripción --> | Security | <!-- --> | <!-- --> |
| 5 | <!-- descripción --> | Non-regression | <!-- --> | <!-- --> |

## 3. Criterios de aceptación de testing
| Criterio | Valor objetivo |
|---|---|
| Cobertura mínima | ≥ __% |
| Tests pasando | 100% |
| Categorías obligatorias cubiertas | 5/5 por componente |

## 4. Entorno y herramientas
| Aspecto | Valor |
|---|---|
| Framework de testing | <!-- pytest, jest, etc. --> |
| Datos de test | Sintéticos / Anonimizados |

## 4A. Static Analysis Strategy
| Tool | Category | Surface | Scope | Blocking |
|---|---|---|---|---|
| <!-- herramienta --> | lint / format_check / type_check / security_static | <!-- surface --> | <!-- changed files / module / workspace --> | YES / NO |

## AECF_COMPLIANCE_REPORT
- [ ] No se generó código de tests
- [ ] Cada componente tiene las 5 categorías obligatorias
- [ ] Criterios de cobertura definidos
```

---

> **Siguiente fase:** IMPLEMENT


