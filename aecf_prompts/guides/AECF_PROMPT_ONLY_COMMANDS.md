# AECF Prompt-Only Command Equivalents

LAST_REVIEW: 2026-04-16
OWNER SEACHAD

---

## 1. Objetivo

Esta guía permite emular, en la medida de lo posible, la UX de `@aecf` usando `aecf_prompts/` y, cuando exista, el MCP incluido para el host. Si el MCP no está disponible, el fallback sigue siendo solo `aecf_prompts/`, sin componente, sin engine y sin tocar `embedded/`.

La idea no es ejecutar comandos reales, sino dar al LLM un contrato estable para resolver una entrada tipo `@aecf ...` hacia los assets manuales de `aecf_prompts/`.

Esto la hace válida para cualquier LLM que pueda:

1. Leer archivos del workspace, o
2. Recibir pegados los archivos relevantes en el chat.

---

## 2. Principio de resolución

Sin componente, `@aecf` deja de ser un comando ejecutable y pasa a ser una intención textual. Si el host dispone del MCP AECF y existe un tool equivalente para ese comando, la resolución preferida pasa a ser MCP-first con fallback manual.

El LLM debe interpretarlo así:

1. Normalizar la intención del usuario.
2. Resolver qué skill, prompt, guía o artefacto de `aecf_prompts/` corresponde.
3. Devolver la respuesta o el siguiente paso manual exacto.
4. Declarar explícitamente cuando algo no puede emularse sin runtime, memoria persistente, GitHub API o ejecución de código.

---

## 3. Contrato base para cualquier LLM

Si quieres conservar sintaxis tipo `@aecf`, carga esta guía como contexto por defecto y aplica estas reglas:

1. Si el usuario escribe `@aecf ...`, no digas que el comando no existe: si hay tool MCP equivalente, úsalo primero; si no, resuélvelo contra `aecf_prompts/`.
2. Usa `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md` si existe.
3. Si existen `AECF_SURFACES_INDEX.md` o `AECF_SURFACES_INDEX.json`, úsalos para resolver qué `surface` o `surfaces` deben cargarse para el trabajo actual.
4. Usa `aecf_prompts/skills/` como fuente para flujos y skill selection.
5. Usa `aecf_prompts/prompts/` como fuente de fases ejecutables.
6. Usa `aecf_prompts/templates/`, `checklists/` y `scoring/` cuando la respuesta implique una fase AECF.
7. Si existe `.aecf/memories/project/AECF_MEMORY.md`, cárgalo siempre antes de resolver skills o comandos.
8. Si existe `.aecf/memories/project/AECF_MEMORY_<user_id>.md` para el usuario activo, cárgalo además del general.
9. La atribución activa debe resolverse con esta prioridad: `AECF_PROMPTS_USER_ID`, `AECF_PROMPTS_MODEL_ID` o `MODEL_ID`, y finalmente `AECF_PROMPTS_AGENT_ID` o `AGENT_ID`.
10. Si faltan archivos previos o artefactos, pídelo explícitamente o indica el siguiente artefacto a crear.
11. Si el comando original dependía de runtime, VS Code, GitHub o estado persistente, responde con una variante manual equivalente y marca la limitación.
12. Si la entrada coincide con una gramática explícita `@aecf <command>`, aplica primero el router del comando y, si existe tool MCP equivalente, úsalo antes de leer archivos adicionales estrictamente necesarios para la ruta manual.
13. Evita empezar por búsquedas recursivas amplias o por documentación no canónica cuando el comando ya define rutas de verdad operativas.
14. Para `@aecf memory list`, la resolución mínima empieza por `.aecf/memories/project/AECF_MEMORY.md`, `.aecf/memories/project/AECF_MEMORY_<user_id>.md` y `.aecf/memories/project/events/`; si esas rutas no existen, la respuesta correcta es "0 entradas" o "store no inicializado".

### 3.1 MCP-first when available

Si el host ha registrado el MCP de AECF y expone tools nativos, usa esta prioridad:

1. Intentar el tool MCP equivalente.
2. Si el tool no existe, no está conectado o falla, declarar ese fallo y caer al flujo manual descrito en esta guía.
3. No resolver `aecf_list_commands` ni `aecf_show_commands` como búsquedas de archivo: son nombres de tools MCP y deben ejecutarse como tales cuando estén disponibles.

Mapeo MCP preferido:

| Intento del usuario | Tool MCP preferido | Fallback manual |
| --- | --- | --- |
| `@aecf list commands` | `aecf_list_commands` | Tabla de esta guía |
| `@aecf show commands` | `aecf_show_commands` | Tabla de esta guía |
| `@aecf list skills` | `aecf_list_skills` | Leer `aecf_prompts/skills/` |
| `@aecf list prompts` | `aecf_list_prompts` | Leer `aecf_prompts/prompts/` |
| `@aecf list topics` | `aecf_list_topics` | Inventario prompt-only |
| `@aecf show prompt=<name>` | `aecf_show_prompt` | Cargar el prompt manualmente |
| `@aecf show guide=<name>` | `aecf_show_guide` | Cargar la guía localizada o devolver traducción derivada |
| `@aecf context` / `@aecf context examine` | `aecf_context_examine` | Leer `AECF_PROJECT_CONTEXT.md` y surfaces |
| `@aecf find skills prompt=...` | `aecf_find_skills` | Resolver skills por intención |
| `@aecf status [topic=...]` | `aecf_status` | `status.py` o inferencia manual |
| `@aecf memory list` | `aecf_memory_list` | Leer memoria prompt-only |
| `@aecf memory add ...` | `aecf_memory_add` | Escritura manual asistida |

---

## 4. Equivalencias canónicas

| Comando `@aecf` | Equivalente prompt-only | Estado | Resolución esperada |
| --- | --- | --- | --- |
| `@aecf` | `@aecf list commands` | Soportado | Mostrar esta tabla de equivalencias y cómo usar `aecf_prompts/` |
| `@aecf help` | Ayuda general | Soportado | Explicar sintaxis prompt-only, skills disponibles y comandos equivalentes |
| `@aecf <command> help` | Ayuda por comando | Soportado | Mostrar gramática emulada, límites y ejemplos manuales |
| `@aecf run skill=<skill> TOPIC=<topic> prompt=...` | `use skill=<skill> TOPIC=<topic> prompt=...` | Soportado | Cargar el skill, listar flujo y decir qué prompt de fase ejecutar a continuación |
| `@aecf list commands` | Índice prompt-only | Soportado | Mostrar comandos emulados, parciales y no soportados |
| `@aecf list skills` | Leer `aecf_prompts/skills/` | Soportado | Listar skills publicados y su uso recomendado |
| `@aecf list prompts` | Leer `aecf_prompts/prompts/` | Soportado | Listar prompts de fase disponibles |
| `@aecf show prompt=<name>` | Mostrar/sintetizar prompt | Soportado | Cargar el prompt indicado y explicarlo o reproducirlo |
| `@aecf show guide=<name>` | Mostrar guía localizada | Soportado | Preferir `aecf_show_guide`; si no existe, leer `aecf_prompts/guides/` y aplicar localización/traducción derivada |
| `@aecf show commands` | Alias de `list commands` | Soportado | Igual que `list commands` |
| `@aecf show workspace_statistics` | Estadísticas del workspace por helper o inspección manual | Soportado | Preferir `python aecf_prompts/scripts/workspace_statistics.py`; si el host no ejecuta herramientas, reproducir el contrato leyendo el workspace y las exclusiones CI |
| `@aecf find skills prompt=...` | Resolver skill por intención | Soportado | Recomendar uno o varios skills con justificación breve |
| `@aecf context` / `@aecf context examine` | Examinar `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md` y, si existen, `AECF_SURFACES_INDEX.*` | Soportado | Resumir contexto, huecos, surfaces activables y riesgos de contexto incompleto |
| `@aecf continue [topic=...]` | Reanudar desde artefactos existentes | Parcial | Detectar la última fase completada y proponer la siguiente fase manual |
| `@aecf status [topic=...]` | Inspección de artefactos existentes | Soportado | Preferir `python aecf_prompts/scripts/status.py --topic <topic>`; si no puede ejecutarse, inferir estado desde `AECF_RUN_CONTEXT.json` y artefactos del topic |
| `@aecf show settings` | Estado efectivo prompt-only | Soportado | Preferir `python aecf_prompts/scripts/show_settings.py`; si no puede ejecutarse, reproducir los valores efectivos de bundle, atribución, `DOCS_ROOT` y user settings |
| `@aecf settings show` | Alias de `show settings` | Soportado | Igual que `@aecf show settings` |
| `@aecf settings set <key>=<value>` | Cambiar un setting de usuario | Soportado | Preferir `python aecf_prompts/scripts/settings.py set <key>=<value>`; si el valor no pertenece al conjunto cerrado, mostrar opciones y pedir al usuario que elija |
| `@aecf list topics` | Inventario de topics | Soportado | Leer `.aecf/runtime/documentation/<user_id>/AECF_TOPICS_INVENTORY.json` o `.md`; si falta, bootstrap desde artefactos existentes |
| `@aecf resolve_issue ...` | Resolver issue pegando su contenido | Parcial | Pedir el body del issue o URL accesible; luego recomendar skill y plan manual |
| `@aecf implement_feature ...` | Implementar feature pegando su contenido | Parcial | Pedir el texto de la feature; luego resolver a `new_feature` u otro skill |
| `@aecf init` | Preparación manual | Parcial | Explicar bootstrap de `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md`; usar la atribución resuelta por entorno si ya existe y solo pedirla si no puede resolverse |
| `@aecf send issue` / `@aecf send feature` | Publicar tickets GitHub desde prompt-only | Soportado | Si el host puede ejecutar herramientas, generar un payload JSON y llamar a `python aecf_prompts/scripts/publish_github_ticket.py create --payload-file <file>`; si falla la API, usar la `compose_url` devuelta |
| `@aecf create ...` | Proponer scaffold manual | Parcial | Puede generar el contenido sugerido, pero no materializarlo automáticamente |
| `@aecf prueba ...` | Demo de UI | No soportado | Depende de webview/chat participante del componente |
| `@aecf test skills ...` | Revisión documental de skills | Parcial | Puede revisar coherencia del skill, pero no ejecutar la suite del engine |
| `@aecf memory ...` | Memoria general y por usuario | Parcial | Puede operar sobre `.aecf/memories/project/AECF_MEMORY.md` y `AECF_MEMORY_<user_id>.md` si existen |
| `@aecf command ...` | Ejecutar CLIs | No soportado | Requiere runtime/herramientas del componente |

---

## 5. Gramática recomendada en prompt-only

Puedes mantener la sintaxis literal de `@aecf`, o usar una forma neutra para LLMs genéricos:

```text
use command=<command> [args...]
```

Equivalencias recomendadas:

```text
@aecf run skill=new_feature TOPIC=billing prompt="Add rate limiter"
use skill=new_feature TOPIC=billing prompt="Add rate limiter"

@aecf list skills
use command=list skills

@aecf show prompt=00_PLAN
use command=show prompt=00_PLAN
```

Si el LLM ya tiene cargada esta guía, ambas formas deben resolverse igual.

---

## 6. Reglas específicas por comando

### 6.1 `run`

Resolución mínima:

1. Cargar `aecf_prompts/skills/skill_<skill>.md`.
2. Si existen `AECF_SURFACES_INDEX.*`, resolver primero la `surface` primaria del trabajo y las `related_surfaces` necesarias.
3. Identificar la primera fase del skill.
4. Indicar qué prompt de `aecf_prompts/prompts/` corresponde.
5. Resolver `DOCS_ROOT`: usar `AECF_PROMPTS_DOCUMENTATION_PATH`; si tampoco existe, aceptar `AECF_PROMPTS_DIRECTORY_PATH` como alias legado; y si no, usar `<workspace>/.aecf/runtime/documentation`.
6. Recordar la ruta de salida canónica en `<DOCS_ROOT>/<user_id>/<TOPIC>/`.
7. Recordar la prioridad de atribución: `AECF_PROMPTS_USER_ID`, después `AECF_PROMPTS_MODEL_ID`/`MODEL_ID`, y finalmente `AECF_PROMPTS_AGENT_ID`/`AGENT_ID`.

Respuesta esperada:

- skill resuelto,
- `surface` primaria y `surfaces` relacionadas si aplican,
- flujo de fases,
- siguiente fase exacta,
- archivos que debe leer,
- artefacto que debe producir.

### 6.2 `continue`

Resolución manual:

1. Leer el skill del topic si está claro.
2. Inspeccionar los artefactos ya existentes del topic.
3. Detectar la última fase válida completada.
4. Proponer solo la siguiente fase gobernada.

Si no puede inferirse la fase anterior con seguridad, el LLM debe decirlo y pedir el último artefacto generado.

### 6.3 `status`

Sin runtime, el estado solo puede inferirse desde documentación ya escrita.

Si el host puede ejecutar herramientas locales, preferir:

```text
python aecf_prompts/scripts/status.py --topic billing
python aecf_prompts/scripts/status.py --topic billing --user-id ana.garcia@empresa.com
```

La respuesta debe incluir:

1. fases completadas,
2. fase pendiente,
3. último veredicto GO/NO-GO si existe,
4. bloqueos por artefactos ausentes.

Resolución mínima del helper:

1. Resolver `DOCS_ROOT` con la misma prioridad del bundle prompt-only.
2. Resolver `user_id` activo desde la atribución efectiva o `--user-id`.
3. Leer `<DOCS_ROOT>/<user_id>/<TOPIC>/AECF_RUN_CONTEXT.json` si existe.
4. Leer los artefactos `*.md` del topic y mapear fases conocidas desde el sufijo del fichero.
5. Detectar el último veredicto explícito `GO`, `NO-GO` o `UNKNOWN` desde artefactos de auditoría.
6. Inferir la siguiente fase gobernada y los bloqueos.

### 6.4 `list topics`

En prompt-only, este comando sí puede resolverse de forma bastante fiable porque `aecf_prompts` ya contempla un inventario persistido de topics.

Orden de resolución:

1. Leer `.aecf/runtime/documentation/<user_id>/AECF_TOPICS_INVENTORY.json`.
2. Si no existe, leer `.aecf/runtime/documentation/<user_id>/AECF_TOPICS_INVENTORY.md`.
3. Si tampoco existe, inferir topics desde `<DOCS_ROOT>/<user_id>/<TOPIC>/`.
4. Si se infiere desde artefactos, recomendar regenerar el inventario canónico.

Por eso `list topics` no depende realmente del componente, sino de que el workspace conserve esos artefactos.

### 6.5 `init`

Resolución manual:

1. Si el host permite ejecutar herramientas y existe `aecf_prompts/scripts/bootstrap_prompt_only_bundle.exe`, ejecutar primero `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env` y usar su salida como fuente canónica para `DOCS_ROOT` y atribución.
2. Cuando el `.exe --diagnose-env` esté disponible, NO intentes inspeccionar variables de entorno con `pwsh`, `cmd`, `set`, `echo %VAR%`, `$env:`, ni herramientas equivalentes del sistema.
3. Solo si el `.exe` no puede ejecutarse, resolver `DOCS_ROOT` con esta prioridad: `AECF_PROMPTS_DOCUMENTATION_PATH`, después `AECF_PROMPTS_DIRECTORY_PATH`, y si ninguno existe usar `<workspace>/.aecf/runtime/documentation`.
4. Si `AECF_PROJECT_CONTEXT.md` no existe, indicar que debe generarse con `skill_project_context_generator`.
5. Resolver la atribución activa con prioridad `AECF_PROMPTS_USER_ID`, `AECF_PROMPTS_MODEL_ID`/`MODEL_ID`, y `AECF_PROMPTS_AGENT_ID`/`AGENT_ID`.
6. Si la atribución ya se ha resuelto desde `--diagnose-env`, desde entorno o desde `AECF_RUN_CONTEXT.json`, no preguntar al usuario otra vez; declarar qué valor se ha resuelto y continuar.
7. Solo pedir confirmación manual de `user_id` cuando no exista ninguna fuente de atribución resoluble y tampoco se haya podido ejecutar `--diagnose-env`.
8. Si `DOCS_ROOT` no existe, indicar que debe crearse automáticamente como parte del bootstrap o del skill generador.
9. Si el host no puede inspeccionar el entorno de forma fiable, usar la salida de `bootstrap_prompt_only_bundle.exe --diagnose-env` como evidencia canónica de las variables visibles para el bundle.

### 6.6 `find skills`

Debe usar `aecf_prompts/skills/README_SKILLS.md` y los `skill_*.md` publicados para recomendar el skill más adecuado.

### 6.7 `show` y `settings show`

Gramática recomendada en prompt-only:

- `@aecf show commands`
- `@aecf show prompt=<name>`
- `@aecf show guide=<name>`
- `@aecf show settings`
- `@aecf settings show`
- `@aecf show workspace_statistics`

`@aecf settings show` es un alias de `@aecf show settings`; ambas formas deben resolverse igual.

Para `@aecf show guide=<name>`, resolución mínima:

1. Preferir el tool MCP `aecf_show_guide` cuando exista.
2. Resolver el idioma efectivo con `output_language` o con el override explícito pedido por el usuario.
3. Si existe copia humana localizada, devolverla tal cual.
4. Si no existe, usar la guía canónica como fuente y pedir al host LLM una traducción derivada preservando nombres de archivo, rutas, comandos, variables de entorno, claves estructurales y bloques de código.

Para `@aecf show workspace_statistics`, resolución mínima:

1. Resolver `aecf_prompts/` como bundle root activo.
2. Resolver el workspace raíz como la carpeta contenedora del bundle, salvo que el host proporcione un root explícito.
3. Cargar `aecf_prompts/ci_exclusions.json` y, si existe, `.aecf/custom/ci_exclusions.json` del workspace.
4. Recorrer el workspace sin seguir symlinks.
5. Excluir directorios, sufijos, prefijos, nombres exactos y patrones de fichero definidos por CI.
6. Contar directorios, ficheros incluidos, ficheros excluidos por CI, bytes totales, texto, binarios, errores de lectura, symlinks omitidos y LOC no vacío por extensión.
7. Devolver exactamente el bloque Markdown `## AECF · Workspace Statistics` con las tablas de extensiones y LOC.

Si el host puede ejecutar herramientas locales, preferir:

```text
python aecf_prompts/scripts/workspace_statistics.py
python aecf_prompts/scripts/workspace_statistics.py --workspace-root .
```

Si el host no puede ejecutar herramientas, el LLM debe emular la misma salida y declarar que es una resolución manual prompt-only.

Para `@aecf show settings` y `@aecf settings show`, resolución mínima:

1. Resolver `aecf_prompts/` como bundle root activo.
2. Resolver `workspace_root` como la carpeta contenedora del bundle.
3. Resolver la atribución efectiva con prioridad `AECF_PROMPTS_USER_ID`, `AECF_PROMPTS_MODEL_ID`/`MODEL_ID`, `AECF_PROMPTS_AGENT_ID`/`AGENT_ID`.
4. Resolver `DOCS_ROOT` con la prioridad documentada del bundle.
5. Leer `<workspace>/.aecf/user_settings.json` si existe; si `user_id` está resuelto, leer también `<workspace>/.aecf/user_settings_<user_id>.json` y calcular los valores efectivos con prioridad usuario -> global -> default.
6. Mostrar el origen de la atribución, el origen de `DOCS_ROOT`, el estado de `aecf_forced_instructions.md`, los helpers disponibles y los user settings, atribuyendo la fuente efectiva de cada valor (`usuario`, `global` o `default`).

Si el host puede ejecutar herramientas locales, preferir:

```text
python aecf_prompts/scripts/show_settings.py
```

### 6.10 `settings set`

#### Scoping: global vs. usuario

Los settings tienen dos capas de persistencia:

| Archivo | Ámbito | Prioridad |
| --- | --- | --- |
| `<workspace>/.aecf/user_settings.json` | Global (todos los usuarios) | Base |
| `<workspace>/.aecf/user_settings_<user_id>.json` | Usuario concreto | Sobreescribe global |

El valor efectivo se resuelve así: usuario si existe → global si existe → default del schema.

#### Gramática:

```text
@aecf settings set <key>=<value>           # escribe en el archivo del usuario activo
@aecf settings set <key>=<value> --global  # escribe en el archivo global (todos los usuarios)
@aecf settings set output_language=es
@aecf settings set language=en
@aecf settings set idiom=fr --global
```

#### Settings disponibles:

| Setting | Aliases | Descripción | Impacta en |
| --- | --- | --- | --- |
| `output_language` | `language`, `idiom`, `idioma`, `lang` | Idioma de los outputs de AECF | `AECF_RUN_CONTEXT.json → output_language`, todos los artefactos de fase |

Valores permitidos para `output_language`:

| Valor | Descripción |
| --- | --- |
| `auto` | Detectar automáticamente del prompt del usuario (valor por defecto) |
| `es` | Español |
| `en` | English |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `it` | Italiano |

#### Resolución mínima cuando el LLM resuelve `@aecf settings set`:

1. Parsear `<key>=<value>` y el flag `--global` desde la entrada del usuario.
2. Normalizar la clave resolviendo aliases (p.ej. `language` → `output_language`, `idiom` → `output_language`).
3. Si la clave no existe, devolver error con la lista de settings disponibles.
4. Si el setting tiene valores cerrados y el valor no pertenece al conjunto permitido **o no se ha proporcionado**, mostrar la tabla de valores y pedir al usuario que elija uno explícitamente. No asumir un valor por defecto sin confirmación.
5. Determinar el archivo de destino:
   - Con `--global`: `<workspace>/.aecf/user_settings.json`
   - Sin `--global`: `<workspace>/.aecf/user_settings_<user_id>.json` donde `user_id` es la atribución efectiva.
6. Leer el archivo de destino (crearlo si no existe), actualizar la clave y guardar.
7. Confirmar el cambio mostrando el setting, el valor, el scope (usuario/global) y la ruta del archivo.

Si el host puede ejecutar herramientas locales, preferir:

```text
python aecf_prompts/scripts/settings.py set output_language=es
python aecf_prompts/scripts/settings.py set output_language=es --global
python aecf_prompts/scripts/settings.py set language=en
```

Si el host no puede ejecutar herramientas, el LLM debe seguir la resolución mínima editando directamente el archivo JSON apropiado (`user_settings.json` para global o `user_settings_<user_id>.json` para usuario).

---

### 6.8 `memory`

`@aecf memory` no puede emular exactamente el store/event log del componente, pero sí puede tener una versión útil en modo prompt-only si se apoya en archivos del workspace.

Resolución recomendada:

1. Usar memoria persistida bajo `.aecf/memories/project/`, no bajo `.aecf/runtime/`.
2. Mantener una memoria general en `.aecf/memories/project/AECF_MEMORY.md`.
3. Mantener memoria por usuario en `.aecf/memories/project/AECF_MEMORY_<user_id>.md`.
4. Mantener una sección o índice compacto de memorias activas con `id`, `category`, `status`, `text` y `source`.
5. Hacer que el LLM lea esa memoria antes de ejecutar cualquier skill relevante.
6. Referenciar esa memoria desde el contexto estático sintetizado o desde el prompt actual si aplica.

Orden mínimo de lectura para `@aecf memory list`:

1. Resolver `user_id` activo con la prioridad definida en esta guía.
2. Intentar leer directamente `.aecf/memories/project/AECF_MEMORY.md`.
3. Si el `user_id` está resuelto, intentar leer `.aecf/memories/project/AECF_MEMORY_<user_id>.md`.
4. Si existe `.aecf/memories/project/events/`, usarlo como apoyo para confirmar materialización o trazabilidad.
5. Solo si las rutas canónicas no existen, responder que el store no está inicializado; no empezar por `AECF_STATIC_PROJECT_CONTEXT.md` ni por búsquedas glob amplias.

Equivalencias prácticas:

- `@aecf memory add=... global=True|False` -> añadir una entrada nueva a la memoria general o a la memoria del usuario activo.
- `@aecf memory list` -> listar entradas activas de la memoria general y, si aplica, de la memoria del usuario.
- `@aecf memory search=...` -> buscar por texto, id o categoría en ambas capas de memoria.
- `@aecf memory update id=...` -> reescribir la entrada manteniendo trazabilidad simple.
- `@aecf memory archive id=...` -> mover la entrada a estado archivado.

Límite importante:

- Sin componente no hay store transaccional, ids garantizados por runtime ni inyección automática por código.
- Sí puede existir memoria útil si el LLM trata esos archivos como fuente de contexto obligatoria.

### 6.9 `send issue` y `send feature`

En prompt-only estos comandos pueden ejecutarse de forma automática sin depender del componente si el host puede lanzar herramientas locales.

Contrato recomendado:

1. resolver el comando a un payload JSON canónico,
2. preferir `python aecf_prompts/scripts/publish_github_ticket.py create-from-args --kind <issue|feature> --title "..." --body-file -` cuando el host pueda pasar stdin;
3. usar `python aecf_prompts/scripts/publish_github_ticket.py create --payload-file <file>` si el host trabaja mejor con JSON estructurado,
4. leer el JSON de salida,
5. si `status=created`, devolver el número y la URL del issue,
6. si `status=manual_publish_required`, devolver la `compose_url` para apertura manual.

Payload mínimo para `send issue`:

```json
{
	"kind": "issue",
	"title": "Bug: @aecf continue pierde el estado",
	"body": "Describe el problema, impacto, topic y skill asociados.",
	"labels": ["Bug"]
}
```

Payload mínimo para `send feature`:

```json
{
	"kind": "feature",
	"title": "Feature: exportación CSV en reporting",
	"body": "Describe la feature, alcance esperado y restricciones.",
	"labels": ["feature"]
}
```

Variables de entorno recomendadas:

1. token: `GITHUB_TOKEN` o `GH_TOKEN`.
2. target opcional: `AECF_PROMPTS_GITHUB_ISSUES_OWNER` y `AECF_PROMPTS_GITHUB_ISSUES_REPOSITORY`.
3. fallback: si `gh` está instalado, el helper puede usar `gh auth token`.

Ejemplos:

```text
@aecf send issue prompt="@aecf continue pierde el estado tras PLAN"
@aecf send feature prompt="Añadir exportación CSV a reporting"
```

Cuando el host no puede ejecutar herramientas, el LLM debe al menos generar el payload JSON y devolver la instrucción exacta para ejecutar el helper.

Para recetas multi-CLI exactas, ver `guides/AECF_PROMPT_ONLY_TICKET_PUBLISHER.md`.

---

### 6.9 `resolve_issue` e `implement_feature`

Sin integración con GitHub, estos comandos se resuelven así:

1. pedir el texto del issue/feature si no se aporta,
2. resumirlo,
3. mapearlo a un skill AECF,
4. proponer la invocación manual equivalente.

Ejemplo:

```text
@aecf implement_feature feature_text="Export reports to PDF with RBAC and pagination"
```

Se resuelve a algo como:

```text
use skill=new_feature TOPIC=report_export prompt="Export reports to PDF with RBAC and pagination"
```

---

## 7. Respuesta estándar para comandos no emulables

Cuando el usuario pida algo que dependía del componente, el LLM debe usar esta pauta:

1. Decir que en modo prompt-only no existe ejecución real del comando.
2. Explicar la limitación concreta: runtime, persistencia, GitHub, terminal, webview o tests del engine.
3. Ofrecer el equivalente manual más cercano dentro de `aecf_prompts/`.

Ejemplo:

```text
`@aecf command ...` no puede ejecutarse en modo prompt-only si el host no permite lanzar herramientas locales.
Equivalente prompt-only: te indico el comando exacto o el script local que debes ejecutar.
```

---

## 8. Bloque recomendado para instrucciones por defecto

Este bloque puede añadirse al system prompt, `AGENTS.md`, `CLAUDE.md` o `.github/copilot-instructions.md` del proyecto cliente:

```markdown
## AECF prompt-only command router

Si el usuario escribe `@aecf ...`, interprétalo como una intención textual resuelta contra `aecf_prompts/`, no como un comando ejecutable del componente.

Aplica estas reglas:

1. Usa `.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md` si existe.
2. Si existen `AECF_SURFACES_INDEX.md` o `AECF_SURFACES_INDEX.json`, úsalos para resolver la `surface` primaria y las `surfaces` relacionadas del trabajo actual.
3. Si existe `AECF_RUN_CONTEXT.json`, úsalo como contrato congelado de idioma y de selección de `surface` para el `TOPIC` actual.
4. Usa `.aecf/memories/project/AECF_MEMORY.md` si existe.
5. Resuelve la atribución activa con prioridad `AECF_PROMPTS_USER_ID`, `AECF_PROMPTS_MODEL_ID`/`MODEL_ID`, y `AECF_PROMPTS_AGENT_ID`/`AGENT_ID`.
6. Si el usuario activo es conocido, usa también `.aecf/memories/project/AECF_MEMORY_<user_id>.md` si existe.
7. La memoria general prevalece sobre la memoria del usuario si hay conflicto.
8. Usa `aecf_prompts/skills/` para resolver skills y flujos.
9. Usa `aecf_prompts/prompts/` para resolver fases ejecutables.
10. Si el comando depende de runtime, GitHub, memoria persistente o terminal, dilo claramente y ofrece el equivalente manual más cercano.
11. Para `@aecf run`, resuelve al equivalente `use skill=<skill> TOPIC=<topic> prompt=<texto>`.
12. Para `@aecf continue` y `@aecf status`, infiere el estado solo desde artefactos existentes en `.aecf/runtime/documentation/`.
13. Para `@aecf list commands`, usa la guía `aecf_prompts/guides/AECF_PROMPT_ONLY_COMMANDS.md` como referencia exhaustiva.
14. Para cualquier entrada con gramática explícita `@aecf <command>`, no la conviertas primero en una tarea de investigación abierta: aplica el contrato del comando y lee únicamente las rutas canónicas que ese contrato exige.
15. Para `@aecf memory list`, comprueba primero `.aecf/memories/project/` y, si falta, devuelve un estado determinista de store vacío o no inicializado.
```

---

## 9. Ejemplos de uso

### 9.1 Ayuda general

```text
@aecf
```

Resultado esperado: índice de equivalencias prompt-only.

### 9.2 Ejecutar un skill

```text
@aecf run skill=new_feature TOPIC=billing prompt="Add rate limiter"
```

### 9.3 Estadísticas del workspace

```text
@aecf show workspace_statistics
```

Resultado esperado: bloque `AECF · Workspace Statistics` usando el helper prompt-only o, si no puede ejecutarse, una emulación manual con el mismo contrato de campos.

### 9.4 Mostrar settings efectivos

```text
@aecf show settings
```

Resultado esperado: bloque `AECF · Prompt-Only Settings` con bundle root, workspace root, atribución efectiva, `DOCS_ROOT` y helpers disponibles.

### 9.5 Consultar estado de un topic

```text
@aecf status topic=billing
```

Resultado esperado: bloque `AECF · Topic Status` con fases completadas, fase pendiente, último veredicto y bloqueos.

Resultado esperado: el LLM carga `skill_new_feature.md`, identifica la fase inicial y te dice que ejecutes `aecf_prompts/prompts/00_PLAN.md`.

### 9.3 Listar skills

```text
@aecf list skills
```

Resultado esperado: skills publicados en `aecf_prompts/skills/` con recomendación de uso.

### 9.4 Reanudar un topic

```text
@aecf continue topic=billing
```

Resultado esperado: el LLM revisa artefactos existentes y propone la siguiente fase manual.

### 9.5 Resolver una feature sin componente

```text
@aecf implement_feature feature_text="Export reports to PDF with RBAC and pagination"
```

Resultado esperado: el LLM la reescribe como ejecución manual de `new_feature`.
