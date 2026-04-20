# AECF Run Context Contract

LAST_REVIEW: 2026-04-16
OWNER SEACHAD

---

## 1. Objetivo

Definir, solo en terminos de `aecf_prompts`, que artefactos de contexto deben existir, quien los genera y como se reutilizan despues en los flujos prompt-only.

Esta guia es exclusiva de `aecf_prompts`.

## 2. Respuesta corta

En `aecf_prompts`, los artefactos clave se reparten asi:

1. `AECF_RUN_CONTEXT.json` congela el contexto de ejecucion por `TOPIC`.
2. `aecf_project_context_generator` debe generar el contexto estructurado de bootstrap del proyecto.
3. `aecf_codebase_intelligence` debe generar los artefactos dinamicos de inteligencia del repositorio.
4. Los prompts multifase consumen directamente `AECF_RUN_CONTEXT.json` y `AECF_PROJECT_CONTEXT.md`.
5. Los skills posteriores reutilizan `STACK_JSON.json`, `AECF_CONTEXT_KEYS.json`, `AECF_SYMBOL_INDEX.json`, `AECF_ARCHITECTURE_GRAPH.json`, `AECF_CODE_HOTSPOTS.json`, `AECF_MODULE_MAP.json`, `AECF_ENTRY_POINTS.json` y `AECF_DYNAMIC_PROJECT_CONTEXT.md` para evitar redescubrir el repo entero en cada fase.
6. Esa reutilizacion debe hacerse como contexto derivado y filtrado para la ejecucion actual; no conviene pegar los JSON completos por defecto en cada prompt de fase.

## 3. Artefactos canonicos en modo prompt-only

### 3.1 Artefacto de ejecucion por topic

Ruta canonica:

- `<DOCS_ROOT>/<user_id>/<TOPIC>/AECF_RUN_CONTEXT.json`

Este archivo congela como minimo:

1. `output_language`
2. `attribution_id`
3. `attribution_kind`
4. `attribution_source`
5. `run_date`
6. `topic`

Si el repositorio usa `surfaces`, tambien debe congelar:

1. `context_mode`
2. `primary_surface`
3. `active_surfaces`
4. `selection_rationale`
5. `context_files_to_load`

### 3.2 Artefactos de bootstrap del proyecto

`aecf_project_context_generator` debe dejar materializados estos archivos:

1. `.aecf/runtime/context/AECF_PROJECT_CONTEXT_AUTO.json`
2. `.aecf/runtime/context/AECF_PROJECT_CONTEXT_HUMAN.yaml`
3. `.aecf/runtime/context/AECF_PROJECT_CONTEXT_RESOLVED.json`
4. `<DOCS_ROOT>/AECF_PROJECT_CONTEXT.md`

Artefactos de gobernanza asociados que tambien deben existir tras una ejecucion real:

1. `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.json`
2. `<DOCS_ROOT>/<user_id>/AECF_TOPICS_INVENTORY.md`
3. `<DOCS_ROOT>/<user_id>/AECF_CHANGELOG.md`

### 3.3 Artefactos dinamicos de inteligencia

`aecf_codebase_intelligence` debe dejar materializados en `documentation/context/` los 8 artefactos estructurados:

1. `STACK_JSON.json`
2. `AECF_ARCHITECTURE_GRAPH.json`
3. `AECF_SYMBOL_INDEX.json`
4. `AECF_ENTRY_POINTS.json`
5. `AECF_MODULE_MAP.json`
6. `AECF_CODE_HOTSPOTS.json`
7. `AECF_CONTEXT_KEYS.json`
8. `AECF_DYNAMIC_PROJECT_CONTEXT.md`

## 4. Quien genera cada archivo

### 4.1 `AECF_RUN_CONTEXT.json`

Lo genera el runtime prompt-only al inicializar una ejecucion real del `TOPIC`.

En el bundle prompt-only esto queda reflejado en:

1. `aecf_prompts/scripts/bootstrap_prompt_only_bundle.py`
2. los prompts de fase que leen el contrato ya congelado
3. `aecf_prompts/scripts/status.py`, que trata su ausencia como bloqueo para el estado del topic

No es un output de `aecf_project_context_generator` ni de `aecf_codebase_intelligence`.

### 4.2 `AECF_PROJECT_CONTEXT_AUTO.json`

Lo genera `aecf_project_context_generator` tras escanear e inferir el workspace.

### 4.3 `AECF_PROJECT_CONTEXT_HUMAN.yaml`

Debe existir como capa humana editable del mismo sistema de contexto. Si falta, el bootstrap debe crearla para que la fusion AUTO + HUMAN sea estable y repetible.

### 4.4 `AECF_PROJECT_CONTEXT_RESOLVED.json`

Se obtiene al resolver AUTO + HUMAN. Es la capa combinada donde lo humano prevalece sobre lo automatico.

### 4.5 `AECF_PROJECT_CONTEXT.md`

Es la version humana legible del contexto del proyecto para consumo directo por prompts y operadores del bundle.

### 4.6 Los 8 artefactos de `documentation/context/`

Los genera `aecf_codebase_intelligence` como inventario estructurado y reutilizable del repositorio.

## 5. Garantia operativa por skill

### 5.1 `aecf_project_context_generator`

Una ejecucion prompt-only correcta de este skill no debe considerarse completa si falta cualquiera de estos bloques:

1. `AECF_PROJECT_CONTEXT_AUTO.json`
2. `AECF_PROJECT_CONTEXT_HUMAN.yaml`
3. `AECF_PROJECT_CONTEXT_RESOLVED.json`
4. `AECF_PROJECT_CONTEXT.md`

Interpretacion practica:

1. `AUTO` aporta la inferencia tecnica.
2. `HUMAN` aporta curacion editable.
3. `RESOLVED` fija la fusion estable.
4. `AECF_PROJECT_CONTEXT.md` es la superficie legible que luego cargan los prompts.

### 5.2 `aecf_codebase_intelligence`

Una ejecucion prompt-only correcta de este skill no debe considerarse completa si falta cualquiera de los 8 artefactos de `documentation/context/`.

Interpretacion practica:

1. `STACK_JSON.json` fija la evidencia de stack.
2. `AECF_CONTEXT_KEYS.json` resume las claves reutilizables.
3. `AECF_SYMBOL_INDEX.json` reduce exploracion manual en implementacion.
4. `AECF_ARCHITECTURE_GRAPH.json` fija dependencias e impacto.
5. `AECF_CODE_HOTSPOTS.json` y `AECF_MODULE_MAP.json` orientan refactor y analisis.
6. `AECF_DYNAMIC_PROJECT_CONTEXT.md` es la vista humana legible del contexto dinamico.

## 6. Como usa `aecf_prompts` estos archivos una vez creados

### 6.1 Uso de `AECF_RUN_CONTEXT.json`

Los prompts multifase de `aecf_prompts` lo usan como contrato congelado de ejecucion.

Uso operativo:

1. resolver `output_language` una sola vez y reutilizarlo en todas las fases;
2. congelar la atribucion efectiva de la ejecucion;
3. mantener `run_date` como metadato estable del flujo;
4. si hay `surfaces`, congelar que contexto debe cargarse y en que orden.

En practica, el prompt-only flow debe leer `AECF_RUN_CONTEXT.json` al inicio de cada fase gobernada y no reinterpretar idioma, atribucion ni `surface` si ya estan congelados.

### 6.2 Uso de `AECF_PROJECT_CONTEXT.md`

Es el contexto humano legible que cargan los prompts de fase como base del proyecto.

Uso operativo:

1. restricciones del proyecto;
2. stack y arquitectura legibles;
3. estandares y convenciones del repo;
4. parametros de calidad o idioma definidos para el proyecto.

En prompt-only, esta es la capa que entra de forma directa y estable en PLAN, AUDIT, IMPLEMENT y fases siguientes.

### 6.3 Uso de `AECF_PROJECT_CONTEXT_AUTO.json`, `HUMAN.yaml` y `RESOLVED.json`

En terminos de `aecf_prompts`, estos archivos sirven como sistema de bootstrap y mantenimiento del contexto, no como sustituto de `AECF_PROJECT_CONTEXT.md` dentro del prompt de fase.

Uso operativo:

1. `AUTO` permite recalcular contexto tecnico sin rehacer todo a mano;
2. `HUMAN` permite fijar overrides del equipo o del dominio;
3. `RESOLVED` deja una fuente de verdad combinada para regenerar o contrastar el `AECF_PROJECT_CONTEXT.md` legible.

Regla practica:

si hay desalineacion entre lo tecnico inferido y lo humano curado, el ajuste se hace en `HUMAN.yaml`, se vuelve a resolver y despues se refresca `AECF_PROJECT_CONTEXT.md`.

### 6.4 Uso de `STACK_JSON.json`

Es la evidencia por defecto del stack detectado.

Uso operativo:

1. skills stack-aware la heredan sin pedir `stack=` otra vez;
2. knowledge packs y semantic profiles pueden adaptarse a esa evidencia;
3. si luego se pasa `stack=` explicitamente, ese override solo afecta a esa ejecucion concreta.

### 6.5 Uso de `AECF_CONTEXT_KEYS.json`

Sirve para reducir el tamaño del contexto en fases de planificacion y analisis.

Uso operativo:

1. identificar modulos nucleares;
2. identificar clases, funciones y entry points relevantes;
3. evitar un escaneo completo del repo cuando ya existe un resumen estructurado.

### 6.6 Uso de `AECF_SYMBOL_INDEX.json`

Sirve como indice reutilizable de simbolos para implementacion y navegacion tecnica.

Uso operativo:

1. localizar simbolos por nombre;
2. reducir ambiguedad entre clases y funciones homonimas;
3. orientar cambios en IMPLEMENT y en fases de pruebas.

### 6.7 Uso de `AECF_ARCHITECTURE_GRAPH.json`

Sirve para razonamiento estructural sobre dependencias.

Uso operativo:

1. entender cadenas de impacto;
2. detectar acoplamiento;
3. soportar auditorias, arquitectura y refactor.

### 6.8 Uso de `AECF_CODE_HOTSPOTS.json` y `AECF_MODULE_MAP.json`

Sirven para priorizacion tecnica.

Uso operativo:

1. localizar zonas de riesgo;
2. delimitar modulos y agrupaciones logicas;
3. orientar `aecf_refactor`, `aecf_new_test_set` y auditorias.

### 6.9 Uso de `AECF_DYNAMIC_PROJECT_CONTEXT.md`

Es la vista humana legible de la inteligencia del repositorio.

Uso operativo:

1. documentar estructura, entry points y hotspots;
2. servir de contexto reutilizable para documentacion y razonamiento de arquitectura;
3. complementar `AECF_PROJECT_CONTEXT.md` con una capa mas dinamica y tecnica.

### 6.10 Uso de `documentation/context/*` en la construccion del prompt efectivo

En `aecf_prompts`, los artefactos de `documentation/context/` deben entrar como capa reutilizable de inteligencia estructurada para skills dependientes del repositorio.

Uso operativo:

1. antes de reexplorar el repo entero, revisar si ya existen artefactos estructurados relevantes en `documentation/context/`;
2. derivar desde esos artefactos un bloque compacto y filtrado para la ejecucion actual;
3. filtrar por `TOPIC`, `surface`, skill y fase cuando aplique;
4. priorizar evidencia resumida y reutilizable frente a pegar JSON completos;
5. solo inyectar JSON completos cuando el contrato del skill o de la fase lo exija de forma explicita.

Regla practica:

`documentation/context/*` no sustituye al prompt del skill ni a `AECF_PROJECT_CONTEXT.md`; actua como capa estructurada de apoyo para construir mejor el prompt efectivo.

### 6.11 Uso de `WORKING_CONTEXT`

En `aecf_prompts`, `WORKING_CONTEXT` debe entenderse como un artefacto de evidencia de ejecucion, no como el cache global del repositorio.

Uso operativo:

1. se construye para una ejecucion concreta y para un `TOPIC` concreto;
2. puede derivarse de `AECF_RUN_CONTEXT.json`, de los artefactos relevantes de `documentation/context/` y de evidencia nueva descubierta durante esa ejecucion;
3. debe congelar solo el recorte de evidencia necesario para la siguiente fase gobernada o para la fase final del skill;
4. no debe reemplazar ni duplicar toda la inteligencia global de `documentation/context/`.

Consecuencia practica:

si dos `TOPIC` distintos trabajan sobre el mismo repo, ambos pueden compartir `documentation/context/*` como base global, pero cada uno debe poder tener un `WORKING_CONTEXT` distinto segun su alcance.

### 6.12 Secuencia recomendada para construir el prompt efectivo downstream

Para skills prompt-only dependientes del repositorio, la secuencia recomendada es esta:

1. cargar `AECF_RUN_CONTEXT.json` si existe para congelar idioma, atribucion y `surface`;
2. cargar `AECF_PROJECT_CONTEXT.md` como capa humana base del proyecto;
3. inspeccionar `documentation/context/*` para reutilizar inteligencia estructurada ya generada;
4. derivar un bloque compacto de contexto filtrado para la ejecucion actual;
5. si el skill es `DISCOVERY_FIRST`, congelar despues un `WORKING_CONTEXT` de esa ejecucion antes de la fase final;
6. solo entonces completar el resto del prompt de skill o de fase.

## 7. Que no debes mezclar

En prompt-only conviene separar cuatro capas:

1. `AECF_RUN_CONTEXT.json` = contrato congelado por `TOPIC`.
2. `AECF_PROJECT_CONTEXT.*` = bootstrap y fuente de verdad del contexto del proyecto.
3. `documentation/context/*` = inteligencia dinamica reutilizable del repositorio.
4. `WORKING_CONTEXT` = artefacto de evidencia acotado a una ejecucion/topic.

No son equivalentes y no deben sustituirse entre si.

## 8. Secuencia recomendada en `aecf_prompts`

Para dejar el sistema estable antes de ejecutar skills multifase:

1. inicializar o refrescar `AECF_RUN_CONTEXT.json` para el `TOPIC` real;
2. ejecutar `aecf_project_context_generator` para fijar `AUTO`, `HUMAN`, `RESOLVED` y `AECF_PROJECT_CONTEXT.md`;
3. ejecutar `aecf_codebase_intelligence` para fijar los 8 artefactos dinamicos en `documentation/context/`;
4. derivar desde `documentation/context/*` el contexto filtrado que haga falta para la ejecucion actual;
5. si el skill es `DISCOVERY_FIRST`, congelar un `WORKING_CONTEXT` acotado al `TOPIC` antes de la fase final;
6. ejecutar despues `aecf_new_feature`, `aecf_refactor`, `aecf_hotfix`, `aecf_new_test_set`, auditorias o documentacion reutilizando esos artefactos.

## 9. Conclusion operativa

Si quieres controlar al 100% el contexto en `aecf_prompts`, la lectura correcta es esta:

1. `AECF_RUN_CONTEXT.json` fija el contrato de ejecucion del `TOPIC`.
2. `aecf_project_context_generator` fija el bootstrap estructurado del proyecto.
3. `aecf_codebase_intelligence` fija la inteligencia dinamica reutilizable del repo.
4. Los prompts de fase consumen `AECF_RUN_CONTEXT.json` y `AECF_PROJECT_CONTEXT.md` como entrada directa.
5. Los skills posteriores reutilizan los artefactos de `documentation/context/` para derivar contexto estructurado acotado a la ejecucion actual.
6. `WORKING_CONTEXT` queda reservado para el handoff de evidencia por ejecucion y por `TOPIC`, no para almacenar la inteligencia global del repo.
