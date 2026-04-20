# AECF Claude MCP Quick Start

LAST_REVIEW: 2026-04-20
OWNER SEACHAD

Esta guia rapida explica como conectar el MCP de AECF para Claude Code y Claude Desktop usando el bundle `aecf_prompts/` entregado al cliente.

En el bundle distribuido, este archivo se copia tambien como `aecf_prompts/QUICK_START_ES.md` para quedar junto a `README.md` y `README_EN.md`.

## Instalacion minima

1. Descomprime el bundle entregado por Seachad y copia la carpeta `aecf_prompts/` a la raiz de tu proyecto.
2. Desde la raiz del proyecto ejecuta `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions` para regenerar las superficies de instrucciones **y registrar automaticamente el MCP en `.mcp.json`**. El bootstrap detecta el ejecutable en `aecf_prompts/mcp/claude/` y crea o actualiza la entrada `aecf` sin borrar otros servidores que ya tengas configurados. Ademas, si Claude Desktop esta instalado en tu maquina, el bootstrap registra automaticamente el MCP en `claude_desktop_config.json` (en `%APPDATA%\Claude` en Windows o `~/Library/Application Support/Claude` en macOS) reutilizando el mismo binario.
3. Reinicia Claude Code. Claude levantara ese ejecutable automaticamente desde `.mcp.json` cuando necesite el servidor MCP; no tienes que abrir otra terminal ni lanzarlo a mano.
4. Verifica la instalacion llamando al tool `aecf_list_skills`, o usa `@aecf check_MCP` para forzar una comprobacion que solo puede resolver el MCP.

Como comprobacion funcional adicional, puedes llamar a `aecf_show_guide` con `name=START_HERE` o `language=fr` para verificar que el host sirve la guía localizada o la traducción derivada respetando `output_language`.

Si quieres que Claude priorice el MCP para comandos con tool equivalente, pídelo de forma explícita. Ejemplo: `Usa el tool MCP aecf_list_commands para resolver @aecf list commands y aecf_show_commands para resolver @aecf show commands; si no están disponibles, usa el fallback manual de aecf_prompts.`

La ejecucion manual desde terminal es solo una smoke test opcional. No forma parte de la instalacion normal porque Claude Code arranca el MCP automaticamente desde la configuracion del JSON.

Si quieres hacer esa prueba manual, ejecútalo desde la raiz del proyecto o define `AECF_WORKSPACE` antes de lanzarlo. Si lo ejecutas solo, el proceso quedara esperando entrada stdio porque actua como servidor MCP, no como CLI interactiva. Ese estado en espera es normal en una prueba manual.

## Registro en Claude Code

El bootstrap (`--sync-instructions`) genera automaticamente `.mcp.json` con la ruta absoluta correcta. Si prefieres editarlo manualmente, el formato es:

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

Sustituye ambas rutas por las reales de tu maquina. Aunque el binario puede inferir el workspace cuando se ejecuta desde el bundle dentro del proyecto, mantener `AECF_WORKSPACE` explícito en Claude Code sigue siendo la opción recomendada porque elimina ambigüedad. En versiones actuales de Claude Code, el registro compartido por proyecto vive en `.mcp.json`.

## Registro en Claude Desktop

El bootstrap registra automaticamente el MCP en Claude Desktop si detecta que la aplicacion esta instalada (el directorio `Claude/` existe en la configuracion de usuario del sistema operativo). El archivo de configuracion es:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Si prefieres editarlo manualmente:

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

Claude Desktop usa el mismo formato y el mismo binario que Claude Code. La unica diferencia es que el archivo de configuracion vive a nivel de usuario y no de proyecto.

## Variables opcionales

| Variable | Descripcion |
| --- | --- |
| `AECF_PROMPTS_USER_ID` | Fija el `user_id` usado por los artefactos prompt-only. |
| `AECF_PROMPTS_DOCUMENTATION_PATH` | Fallback legacy. Si no usas `@aecf settings set artifacts_path`, puedes usar esta variable para forzar otra ruta. Por defecto: `.aecf/documentation`. |

## Notas operativas

- El MCP no empaqueta los prompts: siempre lee `aecf_prompts/` desde el workspace activo.
- Cualquier cambio en la superficie `aecf_prompts/` queda reflejado automaticamente porque el MCP consulta esos archivos en tiempo real.
- Para skills dependientes del repo, el flujo recomendable es: `AECF_RUN_CONTEXT.json` por topic, `AECF_PROJECT_CONTEXT.md` como capa humana base y `documentation/context/*` como inteligencia estructurada reutilizable antes de la fase gobernada.
- En ese flujo, `documentation/context/*` se usa para derivar contexto filtrado y, en skills `DISCOVERY_FIRST`, para congelar un `WORKING_CONTEXT` acotado al `TOPIC`; no conviene pegar todos los JSON completos en cada prompt de fase por defecto.
- Para comandos con tool MCP equivalente, la ruta recomendada es MCP-first y fallback manual solo si el tool falla o no está disponible.
- `@aecf check_MCP` es una comprobacion MCP-only: no existe equivalente manual en `aecf_prompts/`, asi que si responde con la cabecera `AECF MCP Status` y `status: connected` sabes que el host ejecuto el tool `aecf_check_mcp`.
- En el uso normal, Claude Code arranca el MCP desde `.claude/settings.local.json`; no hace falta ejecutarlo manualmente en otra consola.
- Si arrancas el ejecutable manualmente fuera del host MCP y fuera de la raiz del proyecto, necesitas `AECF_WORKSPACE` o el proceso no podrá resolver el workspace correcto.
- La localizacion `mcp/claude/` dentro del bundle deja espacio para futuros MCP especificos de otros hosts (`mcp/codex/`, `mcp/copilot/`, etc.). Claude Desktop reutiliza el mismo binario de `mcp/claude/`.
