# AECF Claude MCP Quick Start

LAST_REVIEW: 2026-04-20
OWNER SEACHAD

This quick-start guide explains how to connect the AECF MCP for Claude Code and Claude Desktop using the `aecf_prompts/` bundle delivered to the client.

In the distributed bundle, this file is also copied as `aecf_prompts/QUICK_START_ES.md` or `aecf_prompts/QUICK_START_EN.md` so it stays next to `README.md` and `README_EN.md`.

## Minimal installation

1. Extract the bundle delivered by Seachad and copy the `aecf_prompts/` folder to the root of your project.
2. From the project root, run `aecf_prompts\scripts\bootstrap_prompt_only_bundle.exe --sync-instructions` to regenerate the instruction surfaces **and automatically register the MCP in `.mcp.json`**. The bootstrap detects the executable under `aecf_prompts/mcp/claude/` and creates or updates the `aecf` entry without removing other servers you may have configured. Additionally, if Claude Desktop is installed on your machine, the bootstrap automatically registers the MCP in `claude_desktop_config.json` (in `%APPDATA%\Claude` on Windows or `~/Library/Application Support/Claude` on macOS) reusing the same binary.
3. Restart Claude Code. Claude will launch that executable automatically from `.mcp.json` whenever it needs the MCP server; you do not need to open another terminal or run it manually.
4. Verify the installation by calling the `aecf_list_skills` tool, or use `@aecf check_MCP` to force a check that can only be resolved by the MCP.

As an additional functional check, you can call `aecf_show_guide` with `name=START_HERE` or `language=fr` to confirm that the host serves the localized guide or the derived translation while respecting `output_language`.

If you want Claude to prioritize the MCP for commands that have an equivalent tool, ask for it explicitly. Example: `Use the MCP tool aecf_list_commands to resolve @aecf list commands and aecf_show_commands to resolve @aecf show commands; if they are unavailable, use the manual aecf_prompts fallback.`

Manual terminal execution is only an optional smoke test. It is not part of the normal installation flow because Claude Code starts the MCP automatically from the JSON configuration.

If you want that manual smoke test, launch it from the project root or set `AECF_WORKSPACE` before starting it. If you run it directly, the process will wait on stdio because it behaves as an MCP server, not as an interactive CLI. That waiting state is normal during a manual test.

## Registration in Claude Code

The bootstrap (`--sync-instructions`) automatically generates `.mcp.json` with the correct absolute path. If you prefer to edit it manually, the format is:

```json
{
  "mcpServers": {
    "aecf": {
      "type": "stdio",
      "command": "C:\\path\\to\\your\\project\\aecf_prompts\\mcp\\claude\\aecf-mcp.exe",
      "args": [],
      "env": {
        "AECF_WORKSPACE": "C:\\path\\to\\your\\project"
      }
    }
  }
}
```

Replace both paths with the real ones on your machine. Even though the binary can infer the workspace when it runs from the bundled path inside the project, keeping `AECF_WORKSPACE` explicit in Claude Code is still the recommended option because it removes ambiguity. In current Claude Code versions, shared project MCP registration lives in `.mcp.json`.

## Registration in Claude Desktop

The bootstrap automatically registers the MCP in Claude Desktop when it detects that the application is installed (the `Claude/` directory exists in the OS user configuration base). The configuration file is:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

If you prefer to edit it manually:

```json
{
  "mcpServers": {
    "aecf": {
      "type": "stdio",
      "command": "C:\\path\\to\\your\\project\\aecf_prompts\\mcp\\claude\\aecf-mcp.exe",
      "args": [],
      "env": {
        "AECF_WORKSPACE": "C:\\path\\to\\your\\project"
      }
    }
  }
}
```

Claude Desktop uses the same JSON format and the same binary as Claude Code. The only difference is that its configuration file lives at the user level instead of the project level.

## Optional variables

| Variable | Description |
| --- | --- |
| `AECF_PROMPTS_USER_ID` | Fixes the `user_id` used by prompt-only artifacts. |
| `AECF_PROMPTS_DOCUMENTATION_PATH` | If you do not want to use `.aecf/runtime/documentation`, which is the default location, you can set an absolute or relative path. |

## Operational notes

- The MCP does not package the prompts: it always reads `aecf_prompts/` from the active workspace.
- Any change in the `aecf_prompts/` surface is reflected automatically because the MCP reads those files in real time.
- For repository-dependent skills, the recommended flow is: topic-scoped `AECF_RUN_CONTEXT.json`, `AECF_PROJECT_CONTEXT.md` as the shared human base layer, and `documentation/context/*` as reusable structured intelligence before the governed phase starts.
- In that flow, `documentation/context/*` is used to derive filtered context and, for `DISCOVERY_FIRST` skills, to freeze a `WORKING_CONTEXT` scoped to the current `TOPIC`; copying the full JSON set into every phase prompt by default is not recommended.
- For commands that have an equivalent MCP tool, the recommended route is MCP-first with manual fallback only if the tool fails or is unavailable.
- `@aecf check_MCP` is an MCP-only diagnostic: there is no manual equivalent in `aecf_prompts/`, so if you see the `AECF MCP Status` header with `status: connected` you know the host actually executed the `aecf_check_mcp` tool.
- In normal usage, Claude Code starts the MCP from `.mcp.json`; there is no need to launch it manually in a separate console.
- If you start the executable manually outside the MCP host and outside the project root, you need `AECF_WORKSPACE` or the process will not be able to resolve the correct workspace.
- The `mcp/claude/` location inside the bundle leaves room for future MCP variants for other hosts (`mcp/codex/`, `mcp/copilot/`, etc.). Claude Desktop reuses the same binary from `mcp/claude/`.
