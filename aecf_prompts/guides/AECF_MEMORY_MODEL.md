# AECF Prompt-Only Memory Model

LAST_REVIEW: 2026-04-06
OWNER SEACHAD

---

## 1. Objetivo

Definir una memoria persistente y simple para `aecf_prompts` que enriquezca todos los skills enviados al LLM, sin depender del componente ni del engine.

Esta memoria está pensada para modo prompt-only, pero intentando mantenerse compatible con la semántica general de AECF.

---

## 2. Decisión de diseño

La memoria no debe vivir en `.aecf/runtime/`.

Debe vivir en `.aecf/memories/`.

Razón:

1. `.aecf/runtime/` se usa para artefactos de ejecución, contexto calculado y salidas runtime.
2. La memoria es persistente, curada y reutilizable entre ejecuciones.
3. El engine de AECF ya usa `.aecf/memories/project/` para `WORKSPACE_MEMORY`, así que este layout queda alineado con la dirección real del framework.

---

## 3. Layout canónico

En la versión unificada, la fuente de verdad operativa es el event store JSON y las vistas Markdown quedan materializadas de forma derivada:

```text
<workspace_root>/.aecf/memories/project/events/<YYYY>/<MM>/<DD>/*.json
<workspace_root>/.aecf/memories/project/AECF_MEMORY.md
<workspace_root>/.aecf/memories/project/AECF_MEMORY_<user_id>.md
```

Contrato:

1. `AECF_MEMORY.md` es la memoria general del proyecto.
2. `AECF_MEMORY_<user_id>.md` es la memoria específica del usuario activo.
3. La memoria general se inyecta siempre.
4. La memoria por usuario solo se inyecta cuando el `user_id` activo coincide.
5. Los `.md` son vistas derivadas para lectura humana y para hosts prompt-only; no sustituyen al event store.

---

## 4. Política de inyección

Orden de carga recomendado en prompt-only:

1. `AECF_PROJECT_CONTEXT.md`
2. `AECF_MEMORY.md`
3. `AECF_MEMORY_<user_id>.md` si existe
4. skill y prompt de fase

Regla de precedencia acordada:

1. La memoria general manda sobre la memoria por actor cuando haya conflicto.
2. La memoria por usuario sirve para añadir contexto operativo específico del usuario activo, notas de trabajo, convenciones locales o recordatorios concretos.
3. La memoria por usuario no debe contradecir restricciones globales del proyecto.

---

## 5. Cuándo debe inyectarse

En prompt-only, esta memoria debe acompañar cualquier ejecución relevante de skill, al menos en:

1. `@aecf run`
2. `@aecf continue`
3. `@aecf status`
4. `@aecf find skills`
5. cualquier invocación directa `use skill=...`

Regla práctica:

Si el LLM va a producir un artefacto AECF o a decidir la siguiente fase, debe leer primero la memoria disponible.

---

## 6. Formato recomendado de cada archivo

Usar un Markdown compacto, estable y fácil de leer por humanos y LLMs.

### 6.1 `AECF_MEMORY.md`

```markdown
# AECF_MEMORY

LAST_REVIEW: 2026-03-24
SCOPE: project

## ACTIVE_MEMORY

### mem_architecture_001 [architecture]
- status: active
- source: human
- updated_at: 2026-03-24
- applies_to: all

El módulo de facturación usa `billing_core` como frontera canónica. No crear lógica duplicada fuera de ese módulo.

### mem_testing_001 [testing]
- status: active
- source: human
- updated_at: 2026-03-24
- applies_to: all

Los tests de integración deben vivir separados de los unitarios y no deben depender de datos productivos.
```

### 6.2 `AECF_MEMORY_<user_id>.md`

```markdown
# AECF_MEMORY_<user_id>

LAST_REVIEW: 2026-04-06
SCOPE: user
USER_ID: <user_id>

## ACTIVE_MEMORY

### mem_user_pref_001 [workflow]
- status: active
- source: human
- updated_at: 2026-03-24
- applies_to: <user_id>

Cuando prepares planes para este usuario, prioriza propuestas incrementales y separa claramente cambios obligatorios de opcionales.
```

---

## 7. Operaciones equivalentes para `@aecf memory`

En modo prompt-only, `@aecf memory` puede apoyarse en las vistas Markdown, pero la semántica unificada queda así:

1. El source of truth es `.aecf/memories/project/events/*.json`.
2. `AECF_MEMORY.md` y `AECF_MEMORY_<user_id>.md` son vistas materializadas.
3. `global=True` apunta a memoria general del proyecto.
4. `global=False` apunta a memoria específica del usuario activo.

Equivalencias:

1. `@aecf memory add=... [global=True|False]` -> añadir una nueva entrada en el scope correcto.
2. `@aecf memory list` -> listar las entradas activas del archivo o combinación de archivos aplicables.
3. `@aecf memory search=...` -> buscar por texto, id o categoría.
4. `@aecf memory update id=... [global=True|False]` -> actualizar el bloque de esa entrada y, si aplica, moverla de scope.
5. `@aecf memory archive id=...` -> cambiar `status: archived`.

Selección del destino:

1. Si la memoria aplica a todo el proyecto, escribir en `AECF_MEMORY.md`.
2. Si aplica solo a un usuario concreto, escribir en `AECF_MEMORY_<user_id>.md`.

---

## 8. Regla de enriquecimiento de skills

Todo skill enviado al LLM debe enriquecerse con memoria aplicable usando esta política:

1. Cargar siempre memoria general si existe.
2. Cargar además memoria del usuario activo si existe.
3. Si hay conflicto, prevalece la memoria general.
4. Si una entrada está archivada, no se inyecta.
5. Si una entrada ya quedó obsoleta, no debe borrarse silenciosamente: debe marcarse o reescribirse explícitamente.

---

## 9. Bloque recomendado para instrucciones por defecto

```markdown
## AECF memory injection

Antes de ejecutar cualquier skill o resolver cualquier comando `@aecf` en modo prompt-only:

1. Lee `AECF_PROJECT_CONTEXT.md` si existe.
2. Lee `.aecf/memories/project/AECF_MEMORY.md` si existe.
3. Si el `user_id` activo es conocido, lee también `.aecf/memories/project/AECF_MEMORY_<user_id>.md` si existe.
4. Trata la memoria general como prioritaria sobre la memoria del usuario en caso de conflicto.
5. Usa esa memoria para enriquecer la selección de skill, el plan, la ejecución de fases y la interpretación del contexto del proyecto.
```

---

## 10. Recomendación de implantación

Orden mínimo recomendado:

1. Crear `.aecf/memories/project/` en el workspace del cliente.
2. Crear `AECF_MEMORY.md` con las restricciones o convenciones globales ya conocidas.
3. Crear `AECF_MEMORY_<user_id>.md` solo cuando realmente haya contexto específico de un usuario.
4. Cargar esta guía junto con `AECF_PROMPT_ONLY_COMMANDS.md` y `LLM_INSTRUCTIONS_SETUP.md`.

---

## 11. Límite deliberado

Este modelo es simple y usable para cualquier LLM, pero no pretende replicar todo el engine.

No incluye por sí solo:

1. event store transaccional,
2. merge automático,
3. ids generados por runtime,
4. inyección automática garantizada por código fuera del host que implemente la unificación.

Sí define un contrato claro para que la memoria enriquezca de forma consistente cualquier skill prompt-only y permanezca alineada con el runtime unificado del participante.

