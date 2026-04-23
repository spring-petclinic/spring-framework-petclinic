# AECF Prompts — Start Here

LAST_REVIEW: 2026-04-20
OWNER SEACHAD

---

## Paso 1 — Configura tu identidad de usuario

Define la variable de entorno `AECF_PROMPTS_USER_ID` con tu email o identificador. AECF la usa para atribuir cada topic y artefacto.

```powershell
# Windows (persistente para el usuario)
setx AECF_PROMPTS_USER_ID "tu.email@empresa.com"
# Abre un terminal nuevo para que surta efecto.
```

```bash
# Linux / macOS
echo 'export AECF_PROMPTS_USER_ID="tu.email@empresa.com"' >> ~/.bashrc
source ~/.bashrc
```

> Si no defines ninguna variable, el sistema genera un ID aleatorio con prefijo `user_` que no podrás rastrear. Para comprobar qué ve el bundle: `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env`

---

## Paso 2 — Verifica que tu LLM está operativo

AECF es model-agnostic: funciona con cualquier LLM que pueda leer archivos del workspace (Copilot Chat, Claude, Codex, ChatGPT…).

Comprueba antes de continuar:

- **VS Code + Copilot Chat / GitHub Copilot**: abre el panel de chat y confirma que responde.
- **Claude CLI**: ejecuta `claude --version` y verifica que tienes sesión activa.
- **Codex CLI**: ejecuta `codex --version`.
- **ChatGPT web**: abre una conversación y confirma acceso.

Si tu host no puede leer archivos del workspace directamente, tendrás que pegar manualmente el contenido de los prompts.

---

## Paso 3 — Copia el bundle y sincroniza instrucciones

1. Copia la carpeta `aecf_prompts/` a la raíz de tu proyecto destino.
2. Ejecuta el bootstrap para crear los archivos de instrucciones que tu LLM necesita:

```powershell
# Desde la raíz del proyecto destino
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions
```

Esto genera `aecf_forced_instructions.md` y las instrucciones específicas por host (`.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`, `.codex/instructions.md`).

---

## Paso 4 — Genera el contexto del proyecto

Pide al LLM que ejecute el skill de contexto. No necesitas redactarlo a mano:

```
@aecf run skill=project_context_generator topic=static_context
```

En este caso no es necesario poner topic, lo elegiría la tool, pero es conveniente acostumbrarse a hacerlo porque es una unidad de control de tareas ejecutadas.

El skill analiza el workspace y genera `AECF_PROJECT_CONTEXT.md` con la estructura, stack, estándares y equipo del proyecto.

A continuación, si el repo es mediano o grande, ejecuta también:

```
@aecf run skill=codebase_intelligence
```

Este skill produce 8 artefactos de análisis en `documentation/context/` (incluyendo `STACK_JSON.json`) que enriquecen todos los skills posteriores.

> **Camino rápido**: si prefieres crear el contexto a mano, basta con escribir `.aecf/documentation/AECF_PROJECT_CONTEXT.md` con las secciones Project, Team, Standards y Scoring Thresholds.

---

## Paso 5 — Lanza tu primer skill

Ya estás listo. Ejecuta tu primer flujo real, normalmente con `new_feature`, `refactor` o `hotfix`:

```
@aecf run skill=new_feature TOPIC=mi_primera_feature prompt="Descripción de lo que quiero implementar"
```

Consulta [QUICK_START.md](QUICK_START.md) para el detalle de las fases y cómo iterar sobre ellas.

---

## Guías complementarias

| Necesidad | Guía |
|---|---|
| Flujo completo paso a paso | [QUICK_START.md](QUICK_START.md) |
| Sintaxis `@aecf` sin componente | [AECF_PROMPT_ONLY_COMMANDS.md](AECF_PROMPT_ONLY_COMMANDS.md) |
| Memoria de proyecto entre sesiones | [AECF_MEMORY_MODEL.md](AECF_MEMORY_MODEL.md) |
| Repos grandes o multi-equipo (surfaces) | [AECF_SURFACE_CONTEXT_MODEL.md](AECF_SURFACE_CONTEXT_MODEL.md) |
| Extender un skill con reglas locales | [AECF_EXTERNAL_SKILLS.md](AECF_EXTERNAL_SKILLS.md) |
| Ahorro de tokens por sesión | [AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md](AECF_STATIC_CONTEXT_SYNTHESIS_PROMPT.md) |
| Catálogo de skills | [../skills/README_SKILLS.md](../skills/README_SKILLS.md) |
| Metodología completa | [../AECF_METHODOLOGY.md](../AECF_METHODOLOGY.md) |
| Mapeo con metodologías de gestión | [AECF_APPLICATION_LIFECYCLE_GUIDE.md](AECF_APPLICATION_LIFECYCLE_GUIDE.md) |
| Índice general de guías | [AECF_GUIDES_MASTER.md](AECF_GUIDES_MASTER.md) |

### Guía específica por host LLM

| Host | Guía |
|---|---|
| ChatGPT / Copilot Chat web | [QUICK_START.md](QUICK_START.md) |
| Claude CLI | [AECF_PROMPTS_CLAUDE_CLI.md](AECF_PROMPTS_CLAUDE_CLI.md) |
| Codex CLI | [AECF_PROMPTS_CODEX_CLI.md](AECF_PROMPTS_CODEX_CLI.md) |

---

## Knowledge packs

Los knowledge packs y semantic profiles están en `aecf_prompts/knowledge/domains/<domain>/pack.md` y `.../semantic_profiles/<profile>.md`. Se cargan automáticamente cuando usas `stack=` en la invocación del skill.

---

> `START_HERE.md` orienta. [QUICK_START.md](QUICK_START.md) manda. Si dudas, empieza siempre por QUICK_START.
