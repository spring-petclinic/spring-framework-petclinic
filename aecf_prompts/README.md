# AECF Prompts

LAST_REVIEW: 2026-04-16
OWNER SEACHAD

---

`aecf_prompts/` es la version prompt-only de AECF para trabajar dentro del repositorio del cliente sin instalar el componente automatizado. El bundle aporta metodologia, skills, prompts, templates, checklists y scoring para ejecutar flujos manuales con el LLM que el equipo ya use.

En este repositorio, `aecf_prompts/` es tambien la superficie fuente completa para prompts, skills y activos prompt-only. El bundle cliente no tiene por qué incluir todo: el task de empaquetado filtra los skills distribuibles segun `aecf_prompts/skills/SKILL_RELEASE.json`, la politica del cliente en `aecf_prompts_release_data/<client>.json` y el `bundle-mode` seleccionado. En `release` solo se entregan los skills `released` autorizados para ese cliente y solo los knowledge domains permitidos; en `god` se entrega toda la superficie publicada del bundle.

Este README debe leerse como una guia de implantacion rapida para usuario final: que copiar, que preparar en el repo y como arrancar el primer flujo.

La version inglesa equivalente esta en `README_EN.md`.

Si quieres extender un skill base con criterios o conocimiento especifico del proyecto sin meter nada en AECF base, usa la guia [guides/AECF_EXTERNAL_SKILLS.md](guides/AECF_EXTERNAL_SKILLS.md).

Para consulta rapida, abre [../index.html](../index.html). Esa portada publica en la raiz del repo enlaza a [../guias/SKILL_CATALOG.html](../guias/SKILL_CATALOG.html) para skills, [../guias/AECF_COMMANDS.html](../guias/AECF_COMMANDS.html) para comandos prompt-only y [../guias/GUIDE_VIEWER.html?doc=START_HERE.md](../guias/GUIDE_VIEWER.html?doc=START_HERE.md) para el resto de guias markdown sin exponer enlaces descargables del repo. Las dos guias interactivas siguen leyendo sus `.md` canonicos desde `aecf_prompts/guides/`, asi que cualquier cambio en esos markdown queda reflejado automaticamente sin reconstruir el HTML publicado.

En workspace destino con MCP prompt-only, el tool `aecf_show_guide` puede servir guias en el `output_language` efectivo. Si no existe copia humana localizada para ese idioma, el host LLM debe renderizar una traduccion derivada preservando rutas, comandos, ids AECF y bloques de codigo.

La misma portada y el catálogo de skills exponen ahora los stamps de versionado generados desde [guides/AECF_ASSET_VERSIONS.md](guides/AECF_ASSET_VERSIONS.md) y `AECF_ASSET_VERSIONS.json`. Cada stamp se deriva del contenido del markdown canónico, por lo que cualquier modificación en un skill o prompt cambia el valor mostrado en documentación y HTML en el siguiente sync.

## Que es

Con `aecf_prompts/` el trabajo se organiza en fases predefinidas. El LLM no decide el proceso sobre la marcha: cada skill marca que pasos seguir y cada prompt de fase indica que contexto leer, que salida generar y en que ubicacion guardarla.

En los flujos de generacion de codigo, el analisis estatico blocking puede gatearse en una fase dedicada `AUDIT_STATIC_ANALYSIS` antes de pasar al audit de code/tests.

Casos tipicos:

1. Diseñar e implementar una nueva feature.
2. Auditar seguridad o estandares de codigo.
3. Documentar un sistema ya existente o explicar como funciona codigo que el equipo no conoce bien.
4. Trabajar de forma manual con Claude, Copilot, Codex u otro host compatible.

## Que necesitas antes de empezar

Necesitas estas tres piezas:

1. Un repositorio del cliente donde copiar `aecf_prompts/`.
2. Un host LLM ya instalado y autenticado.

Hosts habituales:

1. GitHub Copilot en VS Code.
2. GitHub Copilot CLI.
3. Claude Code / Claude CLI.
4. Codex CLI.
5. Un chat web con carga de archivos o, si no la hay, pegando manualmente los archivos requeridos.

## Instalacion del host que va a usar el equipo

Elige uno de estos caminos antes de arrancar con `aecf_prompts`.

### GitHub Copilot en VS Code

Si el equipo va a trabajar dentro de VS Code, este es el camino mas directo.

- Instalacion: GitHub indica que en VS Code la extension necesaria se instala automaticamente durante el setup inicial.
- Referencia oficial: [Installing the GitHub Copilot extension in your environment](https://docs.github.com/en/copilot/how-tos/set-up/installing-the-github-copilot-extension-in-your-environment)
- Guia de VS Code: [Set up Copilot in VS Code](https://code.visualstudio.com/docs/copilot/setup)

### GitHub Copilot CLI

Si el equipo quiere trabajar en terminal con Copilot, la documentacion oficial recomienda estas opciones:

```powershell
npm install -g @github/copilot
```

En Windows tambien existe via WinGet:

```powershell
winget install GitHub.Copilot
```

Despues, arranca con:

```powershell
copilot
```

Y autentica con `/login` cuando lo pida.

- Instalacion oficial: [Installing GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli)
- Uso y configuracion: [Using GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)

### Claude Code / Claude CLI

Se instala así:

```powershell
npm install -g @anthropic-ai/claude-code
```

Despues, arranca con:

```powershell
claude
```

Y sigue el login en navegador cuando lo solicite.

- Setup oficial: [Claude Code setup](https://code.claude.com/docs/en/setup)
- Quickstart oficial: [Claude Code quickstart](https://code.claude.com/docs/en/quickstart)
- Autenticacion: [Claude Code authentication](https://code.claude.com/docs/en/authentication)

Nota para Windows: Claude Code requiere Git for Windows o WSL. Anthropic lo documenta en la misma guia de setup.

### Codex CLI

Para Codex CLI, OpenAI publica este arranque rapido:

```powershell
npm install -g @openai/codex
```

Despues, arranca con:

```powershell
codex
```

Puedes autenticar con tu cuenta de ChatGPT al iniciar o configurar acceso por API key segun la documentacion oficial.

- Repositorio y quickstart oficial: [openai/codex](https://github.com/openai/codex)
- Documentacion oficial: [Codex documentation](https://developers.openai.com/codex)
- Autenticacion: [Codex auth](https://developers.openai.com/codex/auth)

## Implantacion minima en el repo del cliente

### 1. Copia el bundle al proyecto

Estructura minima esperada:

```text
mi-proyecto/
├── aecf_prompts/
├── src/
└── ...
```

### 2. Indica quien realiza el trabajo

Antes de empezar un flujo real, define el identificador que AECF usara para saber quien esta ejecutando ese topic.

Prioridad canonica:

1. `AECF_PROMPTS_USER_ID`
2. `AECF_PROMPTS_MODEL_ID` o `MODEL_ID`
3. `AECF_PROMPTS_AGENT_ID` o `AGENT_ID`

Ejemplo en Windows PowerShell:

```powershell
setx AECF_PROMPTS_USER_ID "ana.garcia@empresa.com"
```

Despues, abre una consola nueva.

Si quieres comprobar exactamente qué ve el bundle sin depender del host de chat, ejecuta:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --diagnose-env
```

Para `@aecf init` en hosts con herramientas, esta es tambien la ruta recomendada: el host debe usar la salida de `--diagnose-env` en lugar de intentar leer variables con comandos de shell del sistema.

### 3. Genera o refresca las instrucciones por defecto

Desde la raiz del repo cliente:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions
```

Si estas trabajando sobre una copia fuente y no sobre el bundle entregado al cliente, puedes usar el `.py` equivalente.

Ese comando crea o actualiza:

En la raiz del repo cliente, no dentro de `aecf_prompts/`:

1. `aecf_forced_instructions.md`
2. `.github/copilot-instructions.md`
3. `copilot-instructions.md`
4. `CLAUDE.md`
5. `AGENTS.md`
6. `.codex/instructions.md`

Si alguna de esas carpetas o archivos no existe todavia, el bootstrap los crea automaticamente.

La linea de carga no se inserta como texto suelto: AECF la deja dentro de un bloque gestionado y visible de AECF para que sea facil identificar que parte del archivo controla el bootstrap.

La idea es simple: el host carga una sola linea de entrada y desde ahi AECF inyecta su bloque canonico de instrucciones.

### 3.b Instala el MCP incluido para el host empaquetado

El bundle entregado al cliente incluye un MCP especifico para un host a la vez. Por defecto el builder empaqueta `claude`, pero tambien puede empaquetar `copilot` o `codex`.

La ruta depende del host elegido al construir el bundle:

```text
aecf_prompts/mcp/claude/aecf-mcp.exe
aecf_prompts/mcp/copilot/aecf-mcp.exe
aecf_prompts/mcp/codex/aecf-mcp.exe
```

Tambien incluye una guia local en:

```text
aecf_prompts/QUICK_START_ES.md
aecf_prompts/QUICK_START_EN.md
```

Esas guias se entregan en la raiz del bundle, junto a `README.md` y `README_EN.md`, para que queden visibles sin entrar en la carpeta `mcp/<host>/` elegida.

El registro exacto depende del host empaquetado:

- `claude`: usa la guia `QUICK_START_ES.md` para registrar `aecf_prompts\mcp\claude\aecf-mcp.exe` en `.mcp.json`.
- `copilot`: usa la misma guia para registrar `aecf_prompts\mcp\copilot\aecf-mcp.exe` en `.vscode/mcp.json`.
- `codex`: usa la misma guia para registrar `aecf_prompts\mcp\codex\aecf-mcp.exe` en la configuracion MCP de Codex.

Ejemplo minimo para Claude en `.mcp.json`:

```json
{
	"mcpServers": {
		"aecf": {
			"type": "stdio",
			"command": "C:\\ruta\\a\\tu\\proyecto\\aecf_prompts\\mcp\\claude\\aecf-mcp.exe",
			"args": [],
			"env": {
				"AECF_WORKSPACE": "C:\\ruta\\a\\tu\\proyecto"
			}
		}
	}
}
```

La ruta del ejecutable esta dentro del bundle para que la instalacion del MCP quede desacoplada del host y el builder pueda elegir que variante publicar.

En el flujo normal no debes ejecutar manualmente el `aecf-mcp.exe` empaquetado en otra terminal. El host MCP elegido debe levantarlo por si mismo desde su configuracion.

Cuando el host tenga este MCP registrado, los comandos `@aecf` con tool equivalente deben resolverse por MCP primero y solo caer al router manual de `aecf_prompts` si el tool no existe, no esta conectado o falla. Ejemplos: `@aecf list commands` debe entrar por `aecf_list_commands` y `@aecf show commands` por `aecf_show_commands`, no por una busqueda textual en el repo.

### 4. Prepara el contexto minimo del proyecto

Debes tener este archivo:

```text
.aecf/runtime/documentation/AECF_PROJECT_CONTEXT.md
```

Si aun no existe, crea una primera version minima o sigue la guia [guides/AECF_PROJECT_CONTEXT_BOOTSTRAP.md](guides/AECF_PROJECT_CONTEXT_BOOTSTRAP.md).

### 5. Inicializa cada topic real antes de la primera fase

Cuando vayas a ejecutar un trabajo real, congela el contexto de ejecucion del topic:

```powershell
aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --topic user_auth --prompt-text "Implementar autenticacion JWT con refresh tokens"
```

Si estas trabajando sobre una copia fuente y no sobre el bundle entregado al cliente, puedes usar el `.py` equivalente.

Ese paso crea el contexto de corrida del topic y fija:

1. `user_id`
2. `RUN_DATE`
3. `output_language`
4. La ruta efectiva donde iran los artefactos

Si el trabajo va a depender del repositorio, conviene asegurar antes dos capas adicionales:

1. `aecf_project_context_generator` para refrescar `AECF_PROJECT_CONTEXT.md`;
2. `aecf_codebase_intelligence` para materializar `.aecf/context/*`.

En el bundle prompt-only, esos artefactos de `.aecf/context/*` no deben copiarse completos en cada fase por defecto. Se reutilizan para derivar contexto filtrado por `TOPIC` y, en skills search-first, para congelar un `WORKING_CONTEXT` acotado a esa ejecucion.

Por defecto, las salidas viven en:

```text
<workspace>/.aecf/runtime/documentation
```

Patron canónico completo de artefactos por fase:

```text
.aecf/runtime/documentation/<user_id>/<TOPIC>/<NN>_<skill_name>_<ARTEFACT_NAME>.md
```

Si necesitas otra ubicacion, usa `AECF_PROMPTS_DOCUMENTATION_PATH`. Si en un entorno heredado ya existe `AECF_PROMPTS_DIRECTORY_PATH`, el bundle tambien lo acepta como alias legado.

## Como trabaja el bundle

El uso normal es este:

1. Eliges un skill en `aecf_prompts/skills/`.
2. Lees su flujo de fases.
3. Pegas en el host la invocacion del skill.
4. Pegas a continuacion el prompt de la fase correspondiente de `aecf_prompts/prompts/`.
5. Guardas la salida en la ruta indicada.
6. Avanzas o entras en fix loop segun el veredicto GO o NO-GO.

Invocacion base:

```text
use skill=<skill_name> TOPIC=<topic> prompt=<descripcion del trabajo>
```

Ejemplo:

```text
use skill=new_feature TOPIC=user_auth prompt=Implementar autenticacion JWT con refresh tokens
```

## Primer flujo recomendado

Si es la primera vez que el equipo usa el bundle, el orden practico es este:

1. Lee [guides/QUICK_START.md](guides/QUICK_START.md).
2. Elige un skill inicial, normalmente `new_feature`, `refactor` o `hotfix`.
3. Abre `skills/skill_<skill>.md` para ver el flujo.
4. Ejecuta la primera fase con `prompts/00_PLAN.md`.
5. Sigue el resto del flujo fase a fase hasta cerrar VERSION.

## Que host usar y donde mirar

### Uso con GitHub Copilot en VS Code

Usa el repo cliente en VS Code y ejecuta `--sync-instructions` para dejar preparada la carga por `.github/copilot-instructions.md`.

Si el bundle fue generado con `--mcp-host copilot`, registra ademas `aecf_prompts/mcp/copilot/aecf-mcp.exe` en `.vscode/mcp.json` siguiendo `QUICK_START_ES.md`.

Referencia: [guides/LLM_INSTRUCTIONS_SETUP.md](guides/LLM_INSTRUCTIONS_SETUP.md)

### Uso con Claude Code / Claude CLI

Trabaja desde la raiz del repo cliente con `CLAUDE.md` como superficie de carga.

Si quieres tools MCP nativos dentro de Claude Code, usa ademas el ejecutable incluido en `aecf_prompts/mcp/claude/aecf-mcp.exe` y registra el server con `AECF_WORKSPACE` apuntando a la raiz del proyecto.

Si el ejecutable se lanza desde el bundle dentro de la raiz del proyecto, tambien puede inferir el workspace por si mismo, pero `AECF_WORKSPACE` sigue siendo la configuracion recomendada para Claude Code.

Referencia: [guides/AECF_PROMPTS_CLAUDE_CLI.md](guides/AECF_PROMPTS_CLAUDE_CLI.md)

### Uso con Codex CLI

Trabaja desde la raiz del repo cliente con `AGENTS.md` o `.codex/instructions.md`.

Si el bundle fue generado con `--mcp-host codex`, registra ademas `aecf_prompts/mcp/codex/aecf-mcp.exe` en la configuracion MCP de Codex siguiendo `QUICK_START_ES.md`.

Referencia: [guides/AECF_PROMPTS_CODEX_CLI.md](guides/AECF_PROMPTS_CODEX_CLI.md)

### Chat web sin integracion local

Tambien puedes usar el bundle en modo manual: pega el skill, el prompt de fase y, si el host no puede leer archivos del repo, pega tambien los archivos requeridos.

Referencia: [guides/QUICK_START.md](guides/QUICK_START.md)

## Archivos clave del bundle

1. `AECF_METHODOLOGY.md` / `AECF_METHODOLOGY_EN.md`: reglas globales de la metodologia en español e inglés.
2. `skills/`: skills disponibles y su flujo.
3. `prompts/`: prompts de fase.
4. `templates/`: estructura de salida esperada.
5. `checklists/`: criterios de revision por fase.
6. `scoring/SCORING_MODEL.md`: umbrales y scoring.
7. `knowledge/`: knowledge packs y semantic profiles cuando el flujo los necesite.
8. `documentation/`: salida generada por cada ejecucion.
9. `QUICK_START_ES.md` / `QUICK_START_EN.md`: arranque rapido del MCP del host empaquetado, copiado en la raiz del bundle junto a `README.md` y `README_EN.md`.

## Ruta recomendada de lectura

1. [guides/START_HERE.md](guides/START_HERE.md)
2. [guides/AECF_GUIDES_MASTER.md](guides/AECF_GUIDES_MASTER.md)
3. [guides/QUICK_START.md](guides/QUICK_START.md)
4. [guides/AECF_PROJECT_CONTEXT_BOOTSTRAP.md](guides/AECF_PROJECT_CONTEXT_BOOTSTRAP.md)
5. [skills/README_SKILLS.md](skills/README_SKILLS.md)
6. [guides/AECF_APPLICATION_LIFECYCLE_GUIDE.md](guides/AECF_APPLICATION_LIFECYCLE_GUIDE.md)
7. [AECF_METHODOLOGY.md](AECF_METHODOLOGY.md)
8. [AECF_METHODOLOGY_EN.md](AECF_METHODOLOGY_EN.md)
9. [guides/AECF_EXTERNAL_SKILLS.md](guides/AECF_EXTERNAL_SKILLS.md)

## Autoría

> **Autor de la metodología:** Fernando García Varela (youngluke)
> **Framework:** AECF (AI Engineering Compliance Framework)

