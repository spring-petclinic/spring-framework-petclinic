# Configuración de instrucciones por defecto para hosts y LLMs

LAST_REVIEW: 2026-04-07
OWNER SEACHAD

---

> Cómo configurar las instrucciones de AECF como contexto por defecto en cada host o proveedor compatible para que todas las ejecuciones sigan automáticamente la metodología.

---

## 1. Concepto

`aecf_prompts/` contiene prompts, skills, templates, checklists y scoring diseñados para ejecución manual con cualquier LLM. Si se configura el host para cargar las instrucciones de AECF como contexto por defecto, **cada conversación nueva arranca con la metodología activa** sin necesidad de pegar instrucciones manualmente.

Las instrucciones de este bundle deben mantenerse **agnósticas al modelo**:

- No fijar un model ID concreto salvo que el operador lo haga fuera del bundle.
- Si la herramienta expone el modelo activo o un perfil de capacidades, adaptar el comportamiento a esa señal inferida.
- `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md` y `.codex/instructions.md` son superficies de carga, no contratos ligados a un modelo concreto.

Si además quieres emular una experiencia parecida a `@aecf` sin instalar el componente, añade también `aecf_prompts/guides/AECF_PROMPT_ONLY_COMMANDS.md` al contexto por defecto. Esa guía convierte entradas tipo `@aecf run ...` o `@aecf list skills` en resoluciones manuales basadas en `aecf_prompts/`.

Para hosts tipo CLI, esa guía no debe cargarse solo como documentación pasiva: las entradas con gramática explícita `@aecf <command>` deben resolverse primero contra su contrato prompt-only antes de iniciar búsquedas amplias por el repo. Esto es especialmente importante para comandos como `@aecf memory list`, que deben inspeccionar primero `.aecf/memories/project/` y devolver un estado determinista si el store aún no existe.

Si además quieres que exista memoria persistente que enriquezca todos los skills enviados al LLM, añade también `aecf_prompts/guides/AECF_MEMORY_MODEL.md`. Esa guía define una memoria general del proyecto y una memoria específica por `user_id` bajo `.aecf/memories/project/`.

Si ejecutas `aecf_project_context_generator` desde la raíz del bundle `aecf_prompts`, el generador puede crear o refrescar automáticamente `aecf_forced_instructions.md` con el bloque canónico de `aecf_prompts/guides/AECF_PROMPT_ONLY_INSTRUCTIONS_BLOCK.md` y dejar `.github/copilot-instructions.md`, `copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md` y `.codex/instructions.md` como superficies mínimas que solo lo cargan.

Si trabajas sin ese generador, puedes conseguir el mismo resultado ejecutando `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions` desde la raíz del bundle entregado al cliente. En modo fuente, el fallback sigue siendo `python aecf_prompts/scripts/bootstrap_prompt_only_bundle.py --sync-instructions`.

---

## 2. GitHub Copilot (VS Code)

### 2.1 Copilot Instructions (`.github/copilot-instructions.md`)

Copilot carga automáticamente `.github/copilot-instructions.md` en cada chat. Para inyectar las instrucciones de AECF:

1. Crear o editar `.github/copilot-instructions.md` en la raíz del proyecto.
2. Añadir una única línea de carga:

```markdown
Before responding, load and follow the instructions in `aecf_forced_instructions.md`.
```

### 2.2 Prompt files (`.github/copilot-instructions.md` + `.prompt.md`)

Para skills específicos, también se puede crear un `.prompt.md` por tarea:

```markdown
---
mode: agent
description: "Ejecutar skill AECF new_feature"
---

Ejecuta el skill `new_feature` siguiendo la metodología AECF.
Lee `aecf_prompts/skills/skill_new_feature.md` para el flujo de fases.
Aplica cada prompt de `aecf_prompts/prompts/` en orden.
```

---

## 3. Claude (Anthropic)

### 3.1 CLAUDE.md (contexto por defecto)

Claude Code y Claude en terminal cargan automáticamente `CLAUDE.md` desde la raíz del proyecto. Crear o editar `CLAUDE.md`:

```markdown
Before responding, load and follow the instructions in `aecf_forced_instructions.md`.
```

### 3.2 Claude Projects (system prompt)

En Claude Projects (interfaz web), pegar el contenido de `aecf_prompts/AECF_METHODOLOGY.md` como **system prompt** del proyecto.

Opcionalmente, subir como archivos de conocimiento:
- `aecf_prompts/AECF_METHODOLOGY.md`
- `aecf_prompts/scoring/SCORING_MODEL.md`
- El skill que más use el equipo (por ejemplo `aecf_prompts/skills/skill_new_feature.md`)

### 3.3 Claude API (system message)

Para integraciones con la API de Claude, inyectar la metodología como `system` message:

```python
response = client.messages.create(
    model="<configured-model>",
    system="Lee y aplica la metodología AECF. " + methodology_content,
    messages=[{"role": "user", "content": prompt_content}]
)
```

---

## 4. OpenAI Codex / ChatGPT

### 4.1 AGENTS.md (Codex CLI)

Codex CLI carga `AGENTS.md` o `.codex/instructions.md` como contexto por defecto. Crear en la raíz del proyecto:

```markdown
Before responding, load and follow the instructions in `aecf_forced_instructions.md`.
```

### 4.2 Custom GPTs (system instructions)

Para Custom GPTs de OpenAI, subir como archivos de conocimiento:
- `aecf_prompts/AECF_METHODOLOGY.md`
- `aecf_prompts/scoring/SCORING_MODEL.md`
- `aecf_prompts/skills/` (los skills que use el equipo)

Y definir las instrucciones del sistema con las reglas de AECF.

### 4.3 OpenAI API (system message)

```python
response = openai.chat.completions.create(
    model="<configured-model>",
    messages=[
        {"role": "system", "content": "Aplica la metodología AECF. " + methodology_content},
        {"role": "user", "content": prompt_content}
    ]
)
```

---

## 5. Otros LLMs (Gemini, Mistral, Llama, etc.)

### Patrón genérico

1. **Si el LLM soporta instrucciones de sistema**: inyectar `aecf_prompts/AECF_METHODOLOGY.md` como system prompt.
2. **Si el LLM soporta carga de archivos**: subir la carpeta `aecf_prompts/` o los archivos clave como contexto.
3. **Si el LLM es solo chat**: pegar el contenido del skill y prompt de fase manualmente al inicio de cada conversación (ver `guides/QUICK_START.md`).
4. **Si la herramienta expone el modelo activo**: usar esa información solo para ajustar estilo, límites o capacidades; nunca para hacer depender el contrato AECF de un model ID fijo.

---

## 6. Resumen de archivos de instrucciones por LLM

| LLM / Herramienta | Archivo de instrucciones | Ubicación |
|---|---|---|
| GitHub Copilot (VS Code) | `.github/copilot-instructions.md` | Raíz del proyecto |
| Claude Code / Terminal | `CLAUDE.md` | Raíz del proyecto |
| Claude Projects | System prompt (web UI) | Configuración del proyecto |
| OpenAI Codex CLI | `AGENTS.md` o `.codex/instructions.md` | Raíz del proyecto |
| Custom GPTs | System instructions + knowledge files | Configuración del GPT |
| API (cualquiera) | System message | En el código de integración |

---

## 7. Instalación de CLIs de agente

Antes de configurar las instrucciones de AECF para un host CLI, es necesario tener instalada la herramienta correspondiente. A continuación se listan los comandos de instalación estándar vía npm (requieren Node.js 18+).

### 7.1 Claude Code (Anthropic)

```bash
npm install -g @anthropic-ai/claude-code
```

Tras la instalación, ejecutar `claude` en la raíz del proyecto para iniciar una sesión interactiva.

### 7.2 Codex CLI (OpenAI)

```bash
npm install -g @openai/codex
```

Alternativa en macOS: `brew install --cask codex`. Tras la instalación, ejecutar `codex` en la raíz del proyecto.

### 7.3 GitHub Copilot CLI

Copilot CLI se instala como extensión de GitHub CLI (`gh`):

```bash
# 1. Instalar GitHub CLI (si no está instalado)
# Windows (winget):
winget install --id GitHub.cli
# macOS (brew):
brew install gh

# 2. Instalar la extensión Copilot
gh extension install github/gh-copilot
```

Tras la instalación, usar `gh copilot` para interactuar con Copilot desde la terminal.

> **Nota**: Los tres CLIs requieren autenticación con sus respectivos proveedores antes del primer uso. Consultar la documentación oficial de cada herramienta para completar el flujo de autenticación.

---

## 7. Contenido mínimo recomendado

Independientemente del LLM, la configuración por defecto debe incluir:

1. **Archivo canónico**: `aecf_forced_instructions.md`
2. **Una sola línea de carga** en `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md` o `.codex/instructions.md`
3. **Referencia a la metodología** dentro del archivo canónico: `aecf_prompts/AECF_METHODOLOGY.md`
4. **Flujo obligatorio** dentro del archivo canónico: PLAN → AUDIT → TEST → IMPLEMENT → AUDIT → VERSION
5. **Templates, checklists y scoring** dentro del archivo canónico: `aecf_prompts/templates/`, `aecf_prompts/checklists/`, `aecf_prompts/scoring/SCORING_MODEL.md`
6. **Output** dentro del archivo canónico: `<DOCS_ROOT>/<user_id>/{{TOPIC}}/`
7. **Contexto del proyecto** dentro del archivo canónico: `AECF_PROJECT_CONTEXT.md`
8. **Skills** dentro del archivo canónico: `aecf_prompts/skills/`
9. **Router prompt-only opcional** dentro del archivo canónico: `aecf_prompts/guides/AECF_PROMPT_ONLY_COMMANDS.md`
10. **Memoria prompt-only opcional** dentro del archivo canónico: `aecf_prompts/guides/AECF_MEMORY_MODEL.md`

---

## Autoría

> **Autor de la metodología:** Fernando García Varela (youngluke)
> **Framework:** AECF (AI Engineering Compliance Framework)

