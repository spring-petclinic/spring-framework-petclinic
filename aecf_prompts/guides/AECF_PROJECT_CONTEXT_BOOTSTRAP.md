# AECF Project Context Bootstrap

LAST_REVIEW: 2026-04-16
OWNER SEACHAD

---

## Objetivo

Tener el contexto minimo util para ejecutar el resto de skills de `aecf_prompts` sin escribir `AECF_PROJECT_CONTEXT.md` completamente a mano y reduciendo tokens por sesion.

## Skill correcto

El skill que debes usar en `aecf_prompts` es:

- `aecf_project_context_generator`

## Que genera

`aecf_project_context_generator` genera contexto estructurado en:

- `.aecf/runtime/context/AECF_PROJECT_CONTEXT_AUTO.json`
- `.aecf/runtime/context/AECF_PROJECT_CONTEXT_HUMAN.yaml`
- `.aecf/runtime/context/AECF_PROJECT_CONTEXT_RESOLVED.json`

En `aecf_prompts` conviene usarlo como bootstrap de una sola vez y, a partir de ese resultado, consolidar o refrescar `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md` para consumo manual por los prompts.

Si ejecutas el generador desde la raiz del bundle `aecf_prompts`, tambien debe crear o refrescar `aecf_forced_instructions.md` con el bloque canonico en ingles y dejar estas superficies con una sola linea que obligue a cargarlo si aun no existe:

- `aecf_forced_instructions.md`
- `.github/copilot-instructions.md`
- `copilot-instructions.md`
- `CLAUDE.md`
- `AGENTS.md`
- `.codex/instructions.md`

Para cada ejecucion real de un `TOPIC`, el bundle prompt-only tambien debe crear `<DOCS_ROOT>/<user_id>/<TOPIC>/AECF_RUN_CONTEXT.json` con el `output_language` congelado para todas las fases del flujo. `DOCS_ROOT` usa `AECF_PROMPTS_DOCUMENTATION_PATH` si existe; si no, cae por defecto en `<workspace>/.aecf/runtime/documentation` y debe crearse si todavia no existe.

## Flujo recomendado

1. Ejecutar `aecf_project_context_generator` una vez.
2. Ejecutar `aecf_codebase_intelligence`.
3. Si el stack detectado no es fiable, usar `aecf_set_stack` en lugar de `aecf_codebase_intelligence`.
4. Generar una version sintetica del contexto para sesiones repetidas.

## Artefactos utiles despues del bootstrap

### Contexto de proyecto

- `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`
- `.aecf/runtime/context/AECF_PROJECT_CONTEXT_AUTO.json`
- `.aecf/runtime/context/AECF_PROJECT_CONTEXT_HUMAN.yaml`
- `.aecf/runtime/context/AECF_PROJECT_CONTEXT_RESOLVED.json`
- `.aecf/runtime/documentation/<user_id>/AECF_TOPICS_INVENTORY.json`
- `.aecf/runtime/documentation/<user_id>/AECF_TOPICS_INVENTORY.md`
- `.aecf/runtime/documentation/<user_id>/AECF_CHANGELOG.md`

Si durante una ejecucion prompt-only aparece otro `AECF_PROJECT_CONTEXT` fuera de `.aecf/runtime/documentation/`, o si `AECF_CHANGELOG` / `AECF_TOPICS_INVENTORY` aparecen fuera de `.aecf/runtime/documentation/<user_id>/`, la salida no sigue el contrato del bundle.

### Contexto tecnico dinamico

`aecf_codebase_intelligence` o `aecf_set_stack` generan en `.aecf/context/`:

- `STACK_JSON.json`
- `AECF_ARCHITECTURE_GRAPH.json`
- `AECF_SYMBOL_INDEX.json`
- `AECF_ENTRY_POINTS.json`
- `AECF_MODULE_MAP.json`
- `AECF_CODE_HOTSPOTS.json`
- `AECF_CONTEXT_KEYS.json`
- `AECF_DYNAMIC_PROJECT_CONTEXT.md`

## Regla de consumo downstream

Para el resto de skills prompt-only dependientes del repositorio:

1. `.aecf/context/*` debe reutilizarse como capa estructurada global del repo;
2. no conviene pegar todos esos JSON completos en cada prompt de fase;
3. lo correcto es derivar un bloque compacto y filtrado segun `TOPIC`, `surface`, skill y fase;
4. en skills `DISCOVERY_FIRST`, ese recorte debe congelarse despues como `WORKING_CONTEXT` acotado a la ejecucion actual.

Regla practica:

`.aecf/context/*` = inteligencia global reutilizable.

`WORKING_CONTEXT` = evidencia de ejecucion por `TOPIC`, derivada en parte de esa inteligencia global y en parte de la discovery puntual de la ejecucion.

## Donde usar el sintetizador de contexto

El mayor ahorro aparece en los flujos multifase que reutilizan `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md` en varias sesiones.

Prioridad alta:

- `aecf_new_feature`
- `aecf_refactor`
- `aecf_hotfix`
- `aecf_new_test_set`

Prioridad media:

- `aecf_code_standards_audit`
- `aecf_release_readiness`
- `aecf_document_legacy`
- `aecf_explain_behaviour`
- `aecf_executive_summary`

No es donde mas compensa:

- `aecf_project_context_generator`
- `aecf_codebase_intelligence`
- `aecf_set_stack`

Estos tres hacen discovery o generacion de contexto; el coste fuerte esta en el analisis del repo, no en inyectar un contexto largo.

## Regla practica

Para sesiones repetidas:

1. Mantener `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md` como fuente humana legible.
2. Mantener `AECF_CHANGELOG.md` y `AECF_TOPICS_INVENTORY.{json,md}` en `.aecf/runtime/documentation/<user_id>/`.
3. No duplicar `AECF_PROJECT_CONTEXT` dentro de `<user_id>/<TOPIC>/`.
4. Crear una version sintetica para pegarla en prompts recurrentes.
5. Reservar el contexto completo solo para:
   - bootstrap inicial
   - cambios grandes de arquitectura
   - auditorias profundas
6. Mantener sincronizados los archivos de instrucciones prompt-only para que cualquier referencia `@aecf` o `aecf_*` se resuelva primero contra `aecf_prompts/`.

## Conclusion corta

Si quieres evitar redactar todo el contexto a mano, usa `aecf_project_context_generator` una vez.

Si quieres bajar tokens por sesion, pasa el contexto sintetico sobre todo a `new_feature`, `refactor`, `hotfix` y `new_test_set`.
















